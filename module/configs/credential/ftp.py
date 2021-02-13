class FTPCredential:
    def __init__(self, host: str, user: str, password: str, port=21):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
