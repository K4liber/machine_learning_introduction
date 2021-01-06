import requests
import json
from module.scheme.token import XAckToken, XOutputTokenMessage
from typing import List
str_list = List[str]


class JobRestClient:
    def __init__(self, url_token: str, url_ack: str, sender_uid: str, base_msg_uids: str_list):
        self.url_token = url_token
        self.url_ack = url_ack
        self.sender_uid = sender_uid
        self.base_msg_uids = base_msg_uids

    def send_blsc_token(self, output_data_access_details, output_pin_name, is_final=True):
        msg = XOutputTokenMessage(
            PinName=output_pin_name,
            SenderUid=self.sender_uid,
            Values=json.dumps(output_data_access_details),
            BaseMsgUid=self.base_msg_uids[0],
            IsFinal=is_final)

        JobRestClient.__send_msg_to_batch_manager(msg, self.url_token)

    def send_blsc_ack(self):
        msg = XAckToken(
            SenderUid=self.sender_uid,
            MsgUids=self.base_msg_uids)

        JobRestClient.__send_msg_to_batch_manager(msg, self.url_ack)

    @staticmethod
    def __send_msg_to_batch_manager(msg, url):
        requests.post(url, data=msg.toJson(), headers={'content-type': 'application/json'})
