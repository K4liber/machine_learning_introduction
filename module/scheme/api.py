import threading

from flask import Flask, request, Response
import json
import os

from .token import InputToken
from .job_rest_client import JobRestClient
##############################################################################
# import file(s) with function(s) that will perform calculation for a pin(s) #
# Data content function for pins could be                                    #
# implemented in same or a different files.                                  #
##############################################################################
# \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ #
from ..content.processing import Processing

# Variables that start with "SYS_" are system variables and
# will be set by CAL execution engine during container creation.
from .pin import load_pins
from .logger import logger

SYS_APP_IP = os.getenv('SYS_APP_IP', '0.0.0.0')
SYS_APP_PORT = os.getenv('SYS_APP_PORT', 9100)
SYS_MODULE_INSTANCE_UID = os.getenv('SYS_MODULE_INSTANCE_UID', 'module_uid')
SYS_BATCH_MANAGER_TOKEN_ENDPOINT = os.getenv('SYS_BATCH_MANAGER_TOKEN_ENDPOINT', 'http://127.0.0.1:7000/token')
SYS_BATCH_MANAGER_ACK_ENDPOINT = os.getenv('SYS_BATCH_MANAGER_ACK_ENDPOINT', 'http://127.0.0.1:7000/ack')
SYS_MODULE_NAME = os.getenv('SYS_MODULE_NAME', 'Face recognition')
SYS_MODULE_DESCRIPTION = os.getenv('SYS_MODULE_DESCRIPTION', 'Find and mark human faces on the given images set.')
SYS_PIN_CONFIG_FILE_PATH = os.getenv('SYS_PIN_CONFIG_FILE_PATH', '/app/module/configs/pins.json')

# Loading pins metadata from a configuration file that is provided by module creator
# during module registration. Pins metadata are extended by 'AccessCredential' field
# that contains credentials to pin input source.
# Variable for storing status value.
logger.info('working on path=' + os.getcwd())
files_in_cwd = {f for f in os.listdir('.')}
logger.info('files in cwd=' + str(files_in_cwd))
# Load rest client
rest_client = JobRestClient(
    url_token=SYS_BATCH_MANAGER_TOKEN_ENDPOINT,
    url_ack=SYS_BATCH_MANAGER_ACK_ENDPOINT,
    sender_uid=SYS_MODULE_INSTANCE_UID)

#################################################################
# Mapping pins meta data to instance of the pins class.          #
##################################################################
# \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ #
INPUT_PINS, OUTPUT_PINS = load_pins(SYS_PIN_CONFIG_FILE_PATH, rest_client)
# /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ #
##################################################################
input_pin_name_to_value = {input_pin.pin_name: input_pin for input_pin in INPUT_PINS}
logger.info('input pins from config:' + str(input_pin_name_to_value))
app = Flask(__name__)


@app.route('/token', methods=['POST'])
def process_balticlsc_token():
    logger.info('received request: ' + str(request.json))

    try:
        input_token = InputToken(**request.json)
    except TypeError as type_error:
        error_msg = 'error while loading input token: ' + str(type_error)
        logger.error(error_msg)
        rest_client.send_ack_token(
            msg_uid='unknown',
            is_final=True,
            is_failed=True,
            note=error_msg,
        )
        return Response(json.dumps({'success': False, 'data': error_msg}), status=400,
                        mimetype='application/json')
    # Create an instance of JobRestClient that will be used for sending a proper token message
    # after data content will finish.
    logger.info('input token: ' + str(input_token))
    input_token_values = json.loads(input_token.Values)
    ###############################################################################################################
    # Switch-case for preforming different calculation for different input pins.                                  #
    # Change according to a number of INPUT pins.                                                                 #
    ###############################################################################################################
    # \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ #

    if input_token.PinName not in input_pin_name_to_value:
        logger.info('missing pin with name: ' + input_token.PinName)
        return Response(json.dumps({'success': False,
                                    'data': 'missing pin with name ' + input_token.PinName + ' in module config'}),
                        status=400, mimetype='application/json')
    else:
        input_pin = input_pin_name_to_value[input_token.PinName]
        module_processing = Processing(output_pins=OUTPUT_PINS)
        logger.info('running token on pin with name=' + input_token.PinName)
        pin_task = threading.Thread(target=module_processing.run,
                                    name=input_token.PinName + ' task for msg: ' + input_token.MsgUid,
                                    args=(rest_client, input_token.MsgUid, input_pin, input_token_values))

    pin_task.daemon = True
    pin_task.start()

    return Response(status=200)
    # /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ #
    ###############################################################################################################


# Endpoint responsible for providing current job status.
@app.route('/status', methods=['GET'])
def get_status():
    return rest_client.get_status().to_json()
