import requests
import json

from .status import JobStatus, ComputationStatus
from .token import AckToken, OutputToken
from typing import List
str_list = List[str]


class JobRestClient:
    def __init__(self, url_token: str, url_ack: str, sender_uid: str):
        self._url_token = url_token
        self._url_ack = url_ack
        self._sender_uid = sender_uid
        self._module_status = JobStatus()

    def send_output_token(self, msg_uid: str, values: dict, output_pin_name, is_final=True):
        msg = OutputToken(
            PinName=output_pin_name,
            SenderUid=self._sender_uid,
            Values=json.dumps(values),
            MsgUid=msg_uid,
            IsFinal=is_final)
        JobRestClient.__send_msg_to_batch_manager(msg, self._url_token)

    def send_ack_token(self, msg_uid: str, is_final=False, is_failed=False, note=''):
        msg = AckToken(
            SenderUid=self._sender_uid,
            MsgUid=msg_uid,
            IsFinal=is_final,
            IsFailed=is_failed,
            Note=note)
        JobRestClient.__send_msg_to_batch_manager(msg, self._url_ack)

    def get_status(self) -> JobStatus:
        return self._module_status

    def get_computation_status(self) -> ComputationStatus:
        return self._module_status.get_computation_status()

    def update_status(self, msg_uid: str, job_progress: float, status: JobStatus = ComputationStatus.Working):
        self._module_status.update(status, job_progress)

        if status.get_computation_status() != ComputationStatus.Failed:
            self.send_ack_token(
                msg_uid=msg_uid,
                is_final=False,
                is_failed=False,
                note=''
            )

    @staticmethod
    def __send_msg_to_batch_manager(msg, url):
        requests.post(url, data=msg.to_json(), headers={'content-type': 'application/json'})
