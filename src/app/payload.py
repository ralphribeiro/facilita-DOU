from io import UnsupportedOperation
from logging import ERROR, Logger
from os.path import exists
from shutil import copyfileobj
# from zipfile import is_zipfile,

from requests import Session
from requests.models import HTTPError


logger = Logger(__file__)


class GetPayloadError(Exception):
    ...


def path_exists(path: str) -> bool:
    suffix = path.split('/')[-1]
    return suffix.endswith('.zip') and exists(path.removesuffix(suffix))
    


def get_payload(path: str, url: str, auth):
    if not path_exists(path):
        raise GetPayloadError('Diretório inválido')

    with Session() as s:
        try: 
            res = s.post(auth[0], data=auth[1])
            res.raise_for_status()
            if res.status_code in (200, 201):
                with s.get(url, stream=True) as res:
                    res.raise_for_status()
                    with open(path, 'wb') as f:
                        return res.status_code, copyfileobj(res.raw, f)
            else:
                return res.status_code, None
        except HTTPError as e:
            logger.log(ERROR, e.strerror)
            raise GetPayloadError('Erro HTTP')
        except (BlockingIOError, UnsupportedOperation) as e:
            logger.log(ERROR, e.strerror)
            raise GetPayloadError('Erro no manipulador de arquivo')

# def unpack(path: str):
