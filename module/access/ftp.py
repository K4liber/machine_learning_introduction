from ftplib import FTP, error_perm
from typing import IO


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
