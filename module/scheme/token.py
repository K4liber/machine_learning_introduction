from typing import List, Union

from .utils import JsonRepr

UNKNOWN_MSG_UID = "unknown"


class InputToken(JsonRepr):
    def __init__(self, MsgUid: str, PinName: str, Values: str,
                 AccessType: Union[dict, None] = None, TokenSeqStack: Union[List[dict], None] = None):
        self.MsgUid = MsgUid
        self.PinName = PinName
        self.AccessType = AccessType
        self.Values = Values

        if TokenSeqStack is None:
            self.SeqStack = None
        else:
            seq_stac = []
            for seq_token in TokenSeqStack:
                seq_stac.append(XSeqToken(**seq_token))
            self.SeqStack = seq_stac

    def __str__(self):
        return "TOKEN: MsgUid=%s, PinName=%s, AccessType=%s, Values=%s, TokenSeqStack=%s" % \
               (self.MsgUid, self.PinName, self.AccessType, self.Values, self.SeqStack)


class OutputToken(JsonRepr):
    def __init__(self, PinName: str, SenderUid: str, Values: str, MsgUid: str, IsFinal):
        self.PinName = PinName
        self.SenderUid = SenderUid
        self.Values = Values
        self.MsgUid = MsgUid
        self.IsFinal = IsFinal


class XSeqToken(JsonRepr):
    def __init__(self, SeqUid: str, No: int, IsFinal: bool):
        self.SeqUid = SeqUid       # string
        self.No = No               # int
        self.IsFinal = IsFinal     # bool


class AckToken(JsonRepr):
    def __init__(self, SenderUid: str, MsgUid: str, Note: str, IsFinal: bool = False, IsFailed: bool = False):
        self.SenderUid = SenderUid
        self.MsgUid = MsgUid
        self.Note = Note
        self.IsFinal = IsFinal
        self.IsFailed = IsFailed
