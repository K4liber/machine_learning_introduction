import os
from typing import List, Tuple

import face_recognition
from matplotlib import pyplot, patches
from PIL import Image
import numpy as np

from ..access.ftp import upload_file
from ..configs.credential.ftp import FTPCredential
from ..scheme.logger import logger
from ..scheme.job_rest_client import JobRestClient
from ..scheme.pin import PinMetaData, MissingPin
from ..scheme.processing import ProcessingInterface
from ..scheme.status import ComputationStatus
from ..scheme.utils import camel_to_snake, snake_to_camel, get_random_output_folder

from ftplib import FTP
# Hacking the FTP library
_old_makepasv = FTP.makepasv


def _new_makepasv(self):
    host, port = _old_makepasv(self)
    host = self.sock.getpeername()[0]
    return host, port


FTP.makepasv = _new_makepasv
# Hacking the FTP library


class Processing(ProcessingInterface):
    def process(self, rest_client: JobRestClient, msg_uid: str,
                input_pin: PinMetaData, input_token_values: dict, output_pins: List[PinMetaData]):
        ###################################################################
        # PUT YOUR CODE HERE                                              #
        ###################################################################
        # 1) Use input_pin and input_access_details variable to read data #
        # 2) Preform operation on data                                    #
        # 3) Send output data to given output,                            #
        #    use output_pins variable to get credentials to output source #
        ###################################################################
        logger.info('starting processing for input pin="' + str(input_pin) + '"')
        logger.info('input token values="' + str(input_token_values) + '"')
        input_access_credential = input_pin.access_credential
        input_token_values = {camel_to_snake(key): value for key, value in input_token_values.items()}
        # TODO refactor this function, make unit tests
        # START # Establish input credentials and folder # START #
        if input_access_credential is None:
            logger.info('missing "access_credential" in input pin, trying to use input token values instead')
            input_access_credential = input_token_values
        else:
            input_access_credential = {camel_to_snake(key): value for key, value in input_access_credential.items()}
            logger.info('using input access credential from pin: ' + str(input_access_credential))

        input_ftp_credential = FTPCredential(**input_access_credential)

        if input_pin.access_path is None:
            logger.info('input pin access path is None, using input token values')

        if 'resource_path' not in input_token_values:
            logger.info('missing "resource_path" in input token values, cannot establish input folder')
        else:
            input_folder = input_token_values['resource_path']
        # STOP # Establish input credentials and folder # STOP #
        # START # Establish output credentials and folder # START #
        output_pin_name_to_pin = {output_pin.pin_name: output_pin for output_pin in output_pins}
        output_pin_name: str = 'Output'

        if output_pin_name not in output_pin_name_to_pin:
            error_msg = 'missing pin with name="' + output_pin_name + '" in output pins config'
            logger.error(error_msg)
            self._module_status = ComputationStatus.Failed
            rest_client.send_ack_token(is_final=True, is_failed=True, note=error_msg)
            raise MissingPin(output_pins, error_msg)

        output_pin = output_pin_name_to_pin[output_pin_name]
        logger.info('loading output pin=' + str(output_pin))
        output_access_credential = output_pin.access_credential

        if output_access_credential is None:
            logger.info('output pin access credentials is None, using input access credentials')
            output_access_credential = input_access_credential
            output_ftp_credential = input_ftp_credential
        else:
            output_access_credential = {camel_to_snake(key): value for key, value in output_access_credential.items()}

            if str(output_access_credential) == str(input_access_credential):
                logger.info('input and output access credential are the same')
                output_ftp_credential = input_ftp_credential
            else:
                output_ftp_credential = FTPCredential(**output_access_credential)

        output_access_path = output_pin.access_path

        if output_access_path is None:
            logger.info('access path is not provided in output config')
            logger.info('setting random generated string as output folder name')
            output_folder = get_random_output_folder(input_folder)
        else:
            output_access_path = {camel_to_snake(key): value for key, value in output_access_path.items()}

            if 'resource_path' not in output_access_path:
                logger.info('missing "resource_path" value in output access path')
                logger.info('setting random generated string as output folder name')
                output_folder = get_random_output_folder(input_folder)
            else:
                output_folder = output_access_path['resource_path']
                logger.info('setting output folder based on output pin config "resource_path"=' + output_folder)
        # STOP # Establish output credentials and folder # STOP #
        # START # set output token values # START #
        output_token_values = {
            'AccessCredential': {snake_to_camel(key): value for key, value in output_access_credential.items()},
            'AccessPath': {
                'ResourcePath': output_folder
            },
        }
        # START # initialize connection for the input and output pins # START #
        logger.info('connecting to input ftp server: ' + input_ftp_credential.host)
        input_ftp = FTP()
        input_ftp.connect(input_ftp_credential.host, input_ftp_credential.port)
        input_ftp.sendcmd('USER ' + input_ftp_credential.user)
        input_ftp.sendcmd('PASS ' + input_ftp_credential.password)

        if output_ftp_credential != input_ftp_credential:
            logger.info('connecting to output ftp server: ' + output_ftp_credential.host)
            output_ftp = FTP()
            output_ftp.connect(output_ftp_credential.host, output_ftp_credential.port)
            output_ftp.sendcmd('USER ' + output_ftp_credential.user)
            output_ftp.sendcmd('PASS ' + output_ftp_credential.password)
        else:
            logger.info('using the same connection as output ftp')
            output_ftp = input_ftp
        # STOP # initialize connection for the input and output pins # STOP #
        # START # process and send files # START #
        logger.info('changing ftp working directory to "' + input_folder + '"')
        input_ftp.cwd(input_folder)
        logger.info('working directory changed')
        logger.info('listing files in the working directory ...')
        filenames: List[str] = input_ftp.nlst()
        logger.info('handling ' + str(len(filenames)) + ' files')
        os.makedirs('tmp', exist_ok=True)

        for filename in filenames:
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                logger.warning('wrong format of the file "' + filename + '", omitting')

            logger.info('downloading file "' + filename + '"')
            filepath = 'tmp/' + filename
            processed_filepath = 'tmp_processed/' + filename
            # Save the image locally
            with open(filepath, 'wb') as file:
                input_ftp.retrbinary("RETR " + filename, file.write)
            # Mark faces and save the image
            image = np.array(Image.open(filepath))
            im = Image.fromarray(image)
            im.save(filepath)
            height: int = image.shape[0]
            width: int = image.shape[1]
            dpi: int = 100
            faces_coords: List[Tuple[int]] = face_recognition.face_locations(image)
            figure = pyplot.figure(frameon=False, dpi=dpi)
            figure.set_size_inches(width / dpi, height / dpi)
            ax = pyplot.Axes(figure, [0., 0., 1., 1.])
            ax.set_axis_off()
            figure.add_axes(ax)
            ax.imshow(image)
            logger.info('adding ' + str(len(faces_coords)) + ' faces to image "' + filename + '"')
            fig = pyplot.gcf()
            fig.savefig(fname=filepath, dpi=dpi, bbox_inches='tight')

            for index in range(len(faces_coords)):
                x_start = faces_coords[index][3]
                y_start = faces_coords[index][0]
                x_width = (faces_coords[index][1] - faces_coords[index][3])
                y_height = (faces_coords[index][2] - faces_coords[index][0])
                rect = patches.Rectangle((x_start, y_start), x_width, y_height,
                                         edgecolor='r', facecolor="none")
                ax.add_patch(rect)

            #fig = pyplot.gcf()
            pyplot.savefig(fname=filepath, dpi=dpi, bbox_inches='tight')
            pyplot.close()
            # Send file to ftp
            with open(filepath, 'rb') as file:
                logger.info('uploading file "' + filename + '" into ' + output_folder)
                upload_file(filename, output_folder, output_ftp, file)
                file.close()  # close file and FTP

            input_ftp.cwd(input_folder)
        # STOP # process and send files # STOP #
        # START # quit connections # START #
        input_ftp.quit()

        if output_ftp_credential != input_ftp_credential:
            output_ftp.quit()
        # STOP # quit connections # STOP #
        # START # send final tokens # START #
        rest_client.send_ack_token(
            msg_uid=msg_uid,
            is_final=True,
            is_failed=False,
            note='data have been processed successfully'
        )
        rest_client.send_output_token(
            msg_uid=msg_uid,
            values=output_token_values,
            output_pin_name=output_pin.pin_name)
        # STOP # send final tokens # STOP #
