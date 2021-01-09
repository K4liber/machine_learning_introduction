import time
from typing import List

from ..scheme.job_rest_client import JobRestClient
from ..scheme.pin import PinMetaData
from ..scheme.processing import ProcessingInterface
from ..scheme.utils import remove_prefix


class Processing(ProcessingInterface):
    def process(self, rest_client: JobRestClient,
                input_pin: PinMetaData, input_access_details: dict, output_pins: List[PinMetaData]):
        ###################################################################
        # PUT YOUR CODE HERE                                              #
        ###################################################################
        # 1) Use pin_input and input_access_details variable to read data #
        # 2) Preform operation on data                                    #
        # 3) Send output data to given output,                            #
        #    use pin_output variable to get credentials to output source  #
        # 4) [optional] You can use app_logger for debug                  #
        ###################################################################
        # TODO process data FINISH IT
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

        print(ftp.retrlines('LIST'))
        print('changing dir based on input token:' + input_access_details['dir'])
        ftp.cwd(input_access_details['dir'])  # change into "debian" directory
        print(ftp.retrlines('LIST'))
        # Simulate processing
        time.sleep(10)
        # Sending output token
        output_pin_name_to_pin = {output_pin.pin_name: output_pin for output_pin in output_pins}
        output_pin_name: str = 'Output'

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
