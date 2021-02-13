import requests
import json
from .token import AckToken, OutputToken
from typing import List
str_list = List[str]


class JobRestClient:
    def __init__(self, url_token: str, url_ack: str, sender_uid: str):
        self.url_token = url_token
        self.url_ack = url_ack
        self.sender_uid = sender_uid

    def send_output_token(self, msg_uid: str, values: dict, output_pin_name, is_final=True):
        msg = OutputToken(
            PinName=output_pin_name,
            SenderUid=self.sender_uid,
            Values=json.dumps(values),
            MsgUid=msg_uid,
            IsFinal=is_final)

        JobRestClient.__send_msg_to_batch_manager(msg, self.url_token)

    def send_ack_token(self, msg_uid: str, is_final=False, is_failed=False, note=''):
        msg = AckToken(
            SenderUid=self.sender_uid,
            MsgUid=msg_uid,
            IsFinal=is_final,
            IsFailed=is_failed,
            Note=note)

        JobRestClient.__send_msg_to_batch_manager(msg, self.url_ack)

    @staticmethod
    def __send_msg_to_batch_manager(msg, url):
        requests.post(url, data=msg.to_json(), headers={'content-type': 'application/json'})
