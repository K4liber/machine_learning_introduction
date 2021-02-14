from ftplib import FTP, error_perm
from typing import IO, Union

from ..scheme.api import rest_client
from ..scheme.logger import logger
# Hacking the FTP library
_old_makepasv = FTP.makepasv


def _new_makepasv(self):
    host, port = _old_makepasv(self)
    host = self.sock.getpeername()[0]
    return host, port


FTP.makepasv = _new_makepasv
# Hacking the FTP library
MAX_CONNECTING_RETRIES = 10


def upload_file(filename: str, dir_name: str, ftp: FTP, file: IO) -> None:
    chdir(dir_name, ftp)
    ftp.storbinary('STOR ' + filename, file)


def chdir(dir_name: str, ftp: FTP) -> None:
    try:
        ftp.mkd(dir_name)
    except error_perm as ep:
        if 'exists' not in str(ep) and 'Create directory operation failed' not in str(ep):
            raise error_perm

    ftp.cwd(dir_name)


def get_connection(host: str, user: str, password: str, port: int = 21) -> FTP:
    retries = 0

    while retries < MAX_CONNECTING_RETRIES:
        retries += 1

        try:
            connection = FTP()
            connection.connect(host, port)
            connection.sendcmd('USER ' + user)
            connection.sendcmd('PASS ' + password)
            return connection
        except BaseException as exception:
            error_msg = 'connecting to FTP ' + str(retries) + ' retries, exception' + str(exception)
            logger.error(error_msg)
            rest_client.send_ack_token(
                msg_uid=error_msg,
                is_final=False,
                is_failed=False,
                note=error_msg
            )

    raise RuntimeError('connecting to FTP exceeded max retries = ' + str(retries))


