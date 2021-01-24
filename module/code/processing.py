import copy
import os
from typing import List, Tuple

import face_recognition
import matplotlib
from matplotlib import pyplot, patches

from ..access.ftp import upload_file
from ..scheme.job_rest_client import JobRestClient
from ..scheme.pin import PinMetaData, AccessTypes, MissingPin, MissingPinValue
from ..scheme.processing import ProcessingInterface


class Processing(ProcessingInterface):
    def process(self, rest_client: JobRestClient,
                input_pin: PinMetaData, input_access_details: dict, output_pins: List[PinMetaData]):
        ###################################################################
        # PUT YOUR CODE HERE                                              #
        ###################################################################
        # 1) Use input_pin and input_access_details variable to read data #
        # 2) Preform operation on data                                    #
        # 3) Send output data to given output,                            #
        #    use output_pins variable to get credentials to output source #
        ###################################################################
        output_pin_name_to_pin = {output_pin.pin_name: output_pin for output_pin in output_pins}
        output_pin_name: str = 'Output'

        if output_pin_name not in output_pin_name_to_pin:
            raise MissingPin(output_pins, 'missing pin with name "' + output_pin_name + '"')

        output_pin = output_pin_name_to_pin[output_pin_name]
        output_data_access_details = output_pin.values

        if 'dir' not in output_data_access_details:
            raise MissingPinValue(output_data_access_details, 'missing "dir" value in pin')

        output_folder = output_data_access_details['dir']

        if input_pin.access_type == AccessTypes.FTP:
            print(input_access_details)
            from ftplib import FTP
            from urllib.parse import urlparse
            url = urlparse(input_pin.access_credential['connectionstring'])
            ftp_url: str = url[1].split("@")[-1]
            print('connecting to ' + ftp_url)
            ftp = FTP(ftp_url)  # connect to host, default port
            credentials: str = ''.join(url[1].split("@")[:-1]).split(":")

            if len(credentials) > 1:
                username: str = credentials[0]
                password: str = credentials[1]
                print('username: ' + username + ', password:' + password)
                ftp.login(user=username, passwd=password)
            else:
                print('missing login credentials')

            print('changing dir based on input token:' + input_access_details['dir'])
            ftp.cwd(input_access_details['dir'])  # change into "debian" directory
            filenames: List[str] = ftp.nlst()
            print('handling ' + str(len(filenames)) + ' files')
            os.makedirs('tmp', exist_ok=True)

            for filename in filenames:
                print('downloading file "' + filename + '"')
                filepath: str = 'tmp/' + filename
                # Mark faces and save the image
                with open(filepath, 'wb') as file:
                    ftp.retrbinary("RETR " + filename, file.write)
                    image = face_recognition.load_image_file(filepath)
                    height: int = image.shape[0]
                    width: int = image.shape[1]
                    dpi: int = 100
                    faces_coords: List[Tuple[int]] = face_recognition.face_locations(image)
                    figure = pyplot.figure(frameon=False, dpi=dpi)
                    figure.set_size_inches(width/dpi, height/dpi)
                    ax = pyplot.Axes(figure, [0., 0., 1., 1.])
                    ax.set_axis_off()
                    figure.add_axes(ax)
                    img = matplotlib.image.imread(filepath)
                    ax.imshow(img)
                    print('adding ' + str(len(faces_coords)) + ' faces to image "' + filename + '"')

                    for index in range(len(faces_coords)):
                        x_start = faces_coords[index][3]
                        y_start = faces_coords[index][0]
                        x_width = (faces_coords[index][1] - faces_coords[index][3])
                        y_height = (faces_coords[index][2] - faces_coords[index][0])
                        rect = patches.Rectangle((x_start, y_start), x_width, y_height,
                                                 edgecolor='r', facecolor="none")
                                                 #edgecolor='r', zorder=1000,
                                                 #facecolor="none", transform=figure.transFigure, figure=figure)
                        ax.add_patch(rect)

                    pyplot.savefig(fname=filepath, dpi=dpi)
                    pyplot.close(fig=figure)
                # Send file to ftp
                with open(filepath, 'rb') as file:
                    print('uploading file "' + filename + '" into ' + output_folder)
                    upload_file(filename, output_folder, ftp, file)
                    file.close()  # close file and FTP

                ftp.cwd(input_access_details['dir'])

            ftp.quit()

        else:
            print('module do not support "' + input_pin.access_type + '" access type')

        # Sending output token
        if output_pin_name in output_pin_name_to_pin:
            output_pin = output_pin_name_to_pin[output_pin_name]
            # Sending output Token
            rest_client.send_blsc_token(
                output_data_access_details=input_access_details,
                output_pin_name=output_pin.pin_name,
                is_final=True)
            rest_client.send_blsc_ack()
        else:
            print('missing required output pin with name "' + output_pin_name + '"')
