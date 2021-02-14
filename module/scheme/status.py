import json
from enum import Enum


class ComputationStatus(Enum):
    Idle = 1,
    Working = 2,
    Completed = 3,
    Failed = 4,
    Rejected = 5,
    Aborted = 6,
    Neglected = 7


# TODO test this class and its methods
class JobStatus:
    def __init__(self, computation_status: ComputationStatus = ComputationStatus.Idle, job_progress: float = 0.0):
        self._computation_status = computation_status
        self._job_progress = job_progress

    def get_computation_status(self):
        return self._computation_status

    def get_job_progress(self):
        return self._job_progress

    def update(self, computation_status: ComputationStatus, job_progress: float):
        self.__init__(computation_status, job_progress)

    def to_json(self):
        baltic_stats = {
            'Status': self._status.value[0],
            'JobProgress': self._job_progress
        }
        return json.dumps(baltic_stats, default=lambda o: o.__dict__, indent=3)

    def __repr__(self):
        return self.to_json()
