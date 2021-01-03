from .data_model import PinMetaData, XJobStatus, ComputationStatus
from .job_rest_client import JobRestClient


def face_recognition(rest_client: JobRestClient, module_status: XJobStatus, access_details: dict,
                     pin_input: PinMetaData, pin_output: PinMetaData):
    module_status.Status = ComputationStatus.Working
    ##################################################################
    # PUT YOUR CODE HERE                                             #
    ##################################################################
    # 1) Use pin_input and access_details variable to read data      #
    # 2) Preform operation on data                                   #
    # 3) Send output data to given output,                           #
    #    use pin_output variable to get credentials to output source #
    # 4) [optional] You can use app_logger for debug                 #
    ##################################################################

    # example of output_data_access_details
    output_data_access_details = {'db_table_name': 'sometable',
                                  'db_file_uid': '123file456uid'}

    rest_client.send_blsc_token(
        output_data_access_details=output_data_access_details,
        output_pin_name=pin_output.PinName,
        is_final=True)

    rest_client.send_blsc_ack()
    module_status.Status = ComputationStatus.Idle
