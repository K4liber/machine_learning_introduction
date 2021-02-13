from typing import List

from .job_rest_client import JobRestClient
from .pin import PinMetaData
from .status import XJobStatus, ComputationStatus


class ProcessingInterface:
    def __init__(self, module_status: XJobStatus, output_pins: List[PinMetaData]):
        self._module_status = module_status
        self._output_pins = output_pins

    def run(self, rest_client: JobRestClient, msg_uid: str, input_pin: PinMetaData,
            input_access_details: dict):
        self._pre_process()
        self.process(rest_client, msg_uid, input_pin, input_access_details, self._output_pins)

        if self._module_status != ComputationStatus.Failed:
            self._post_process()

    def _pre_process(self):
        self._module_status.Status = ComputationStatus.Working

    def _post_process(self):
        self._module_status.Status = ComputationStatus.Idle

    def process(self, rest_client: JobRestClient, msg_uid: str,
                input_pin: PinMetaData, input_access_details: dict, output_pins: List[PinMetaData]):
        """Process input token and send the output (data + tokens)."""
        pass
