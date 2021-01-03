import json
from enum import Enum


class JsonRepr:
    def toJson(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=3)

    def __repr__(self):
        return self.toJson()


class XInputTokenMessage(JsonRepr):
    def __init__(self, msg_uid: str, PinName: str, Values: str, AccessType = None, SeqStack = None):
        self.MsgUid = msg_uid                         # string
        self.PinName = PinName                       # string
        self.AccessType = AccessType                 # string
        self.Values = Values                         # dist/JSON
        if SeqStack is None:
            self.SeqStack = None                     # null if not set
        else:
            seq_stac = []
            for seq_token in SeqStack:
                seq_stac.append(XSeqToken(**seq_token))
            self.SeqStack = seq_stac                 # list of XSeqToken


class XOutputTokenMessage(JsonRepr):
    def __init__(self, PinName, SenderUid, Values, BaseMsgUid: str, IsFinal):
        self.PinName = PinName            # string
        self.SenderUid = SenderUid        # string
        self.Values = Values              # dist/JSON
        self.BaseMsgUid = BaseMsgUid      # list of strings
        self.IsFinal = IsFinal            # bool


class XSeqToken(JsonRepr):
    def __init__(self, SeqUid: str, No: int, IsFinal: bool):
        self.SeqUid = SeqUid       # string
        self.No = No               # int
        self.IsFinal = IsFinal     # bool


class XAckToken(JsonRepr):
    def __init__(self, SenderUid, MsgUids):
        self.SenderUid = SenderUid       # string
        self.MsgUids = MsgUids           # list of string


class XJobStatus:
    def __init__(self, Status: Enum, JobProgress: int):
        self.Status = Status                # ComputationStatus(Enum)
        self.JobProgress = JobProgress      # long

    def toJson(self):
        _ = XJobStatus(self.Status.value[0], self.JobProgress)
        return json.dumps(_, default=lambda o: o.__dict__, indent=3)

    def __repr__(self):
        return self.toJson()


class PinMetaData(JsonRepr):
    def __init__(self, PinName: str, PinType: str, AccessType:str):
        self.PinName = PinName
        self.PinType = PinType
        self.AccessType = AccessType


class ComputationStatus(Enum):
    Idle = 1,
    Working = 2,
    Completed = 3,
    Failed = 4,
    Rejected = 5,
    Aborted = 6,
    Neglected = 7
