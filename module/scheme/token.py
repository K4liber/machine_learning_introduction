from .utils import JsonRepr


class XInputTokenMessage(JsonRepr):
    def __init__(self, MsgUid: str, PinName: str, Values: str, AccessType = None, TokenSeqStack = None):
        self.MsgUid = MsgUid                         # string
        self.PinName = PinName                       # string
        self.AccessType = AccessType                 # string
        self.Values = Values                         # dist/JSON

        if TokenSeqStack is None:
            self.SeqStack = None                     # null if not set
        else:
            seq_stac = []
            for seq_token in TokenSeqStack:
                seq_stac.append(XSeqToken(**seq_token))
            self.SeqStack = seq_stac                 # list of XSeqToken

    def __str__(self):
        return "TOKEN: MsgUid=%s, PinName=%s, AccessType=%s, Values=%s" % \
               (self.MsgUid, self.PinName, self.AccessType, self.Values)


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
