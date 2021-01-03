import threading
from flask import Flask, request, Response
import json
import os
from .data_model import XInputTokenMessage, PinMetaData, XJobStatus, ComputationStatus
from .job_rest_client import JobRestClient
##############################################################################
# import file(s) with function(s) that will perform calculation for a pin(s) #
# Data processing function for pins could be                                 #
# implemented in same or a different files.                                  #
##############################################################################
# \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ #
from .processing import face_recognition

# /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ #
##############################################################################

# Variables that start with "SYS_" are system variables and
# will be set by CAL execution engine during container creation.
SYS_APP_IP = os.getenv('SYS_APP_IP', '0.0.0.0')
SYS_APP_PORT = os.getenv('SYS_APP_PORT', 9100)
SYS_MODULE_INSTANCE_UID = os.getenv('SYS_MODULE_INSTANCE_UID', 'alfanumeric123uid')
SYS_BATCH_MANAGER_TOKEN_ENDPOINT = os.getenv('SYS_BATCH_MANAGER_TOKEN_ENDPOINT', 'http://127.0.0.1:7000/token')
SYS_BATCH_MANAGER_ACK_ENDPOINT = os.getenv('SYS_BATCH_MANAGER_ACK_ENDPOINT', 'http://127.0.0.1:7000/ack')
SYS_MODULE_NAME = os.getenv('SYS_MODULE_NAME', 'Face recognition')
SYS_MODULE_DESCRIPTION = os.getenv('SYS_MODULE_DESCRIPTION', 'Find and mark human faces on the given images set.')
SYS_PIN_CONFIG_FILE_PATH = os.getenv('SYS_PIN_CONFIG_FILE_PATH', './configs/pins.json')

# Loading pins metadata from a configuration file that is provided by module creator
# during module registration. Pins metadata are extended by 'AccessCredential' field
# that contains credentials to pin input source.
with open(SYS_PIN_CONFIG_FILE_PATH) as json_file:
    pin_description_json = json.load(json_file)

##################################################################
# Mapping pins meta data to instance of the pins class.          #
# Change according to a number of input and output pins.         #
##################################################################
# \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ #
PIN_METADATA_INPUT = [PinMetaData(**pin_description_json[0])]
PIN_METADATA_OUTPUT = [PinMetaData(**pin_description_json[2])]
# /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ #
##################################################################

# Variable for storing status value.
module_status = XJobStatus(ComputationStatus.Idle, -1)

app = Flask(__name__)


@app.route('/token', methods=['POST'])
def process_balticlsc_token():
    # mapping input message
    try:
        blsc_token = XInputTokenMessage(**request.json)
    except:
        return Response(json.dumps({'success': False, 'data': 'Can not parse token.'}), status=400, mimetype='application/json')

    # Create an instance of JobRestClient that will be used for sending a proper token message
    # after data processing will finish.
    rest_client = JobRestClient(
        url_token=SYS_BATCH_MANAGER_TOKEN_ENDPOINT,
        url_ack=SYS_BATCH_MANAGER_ACK_ENDPOINT,
        sender_uid=SYS_MODULE_INSTANCE_UID,
        base_msg_uids=[blsc_token.MsgUid])

    access_details = json.loads(blsc_token.Values)

    ###############################################################################################################
    # Switch-case for preforming different calculation for different input pins.                                  #
    # Change according to a number of INPUT pins.                                                                 #
    ###############################################################################################################
    # \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ #
    if PIN_METADATA_INPUT[0].PinName == blsc_token.PinName:
        pin_input = PIN_METADATA_INPUT[0]
        pin_output = PIN_METADATA_OUTPUT[0]

        # Implementation of data_processing function or equivalent
        # should be done in separate file(use import) according to the example
        pin_task = threading.Thread(target=face_recognition,
                                    name=PIN_METADATA_INPUT[0].PinName + ' task for msg: ' + blsc_token.MsgUid,
                                    args=(rest_client, module_status, access_details, pin_input, pin_output))

    else:
        return Response(json.dumps({'success': False}), status=400, mimetype='application/json')

    pin_task.daemon = True
    pin_task.start()

    return Response(status=200)
    # /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ #
    ###############################################################################################################


# Endpoint responsible for providing current job status.
@app.route('/status', methods=['GET'])
def get_status():
    return module_status.toJson()
