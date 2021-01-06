from typing import List

from .scheme.job_rest_client import JobRestClient
from .scheme.pin import PinMetaData
from .scheme.processing import ProcessingInterface


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
        # TODO process data
        # TODO send output tokens
        # example of output_data_access_details
        output_data_access_details = {'db_table_name': 'sometable',
                                      'db_file_uid': '123file456uid'}
        rest_client.send_blsc_token(
            output_data_access_details=output_data_access_details,
            output_pin_name=output_pins[0].pin_name,
            is_final=True)
        rest_client.send_blsc_ack()
