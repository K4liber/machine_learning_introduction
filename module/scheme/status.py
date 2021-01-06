from enum import Enum


class XJobStatus:
    def __init__(self, Status: Enum, JobProgress: int):
        self.Status = Status                # ComputationStatus(Enum)
        self.JobProgress = JobProgress      # long

    def to_json(self):
        _ = XJobStatus(self.Status.value[0], self.JobProgress)
        return json.dumps(_, default=lambda o: o.__dict__, indent=3)

    def __repr__(self):
        return self.to_json()


class ComputationStatus(Enum):
    Idle = 1,
    Working = 2,
    Completed = 3,
    Failed = 4,
    Rejected = 5,
    Aborted = 6,
    Neglected = 7