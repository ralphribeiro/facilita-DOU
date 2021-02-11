from io import UnsupportedOperation
from logging import ERROR, INFO, Logger
from os.path import exists
from shutil import copyfileobj
from zipfile import ZipFile

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
        err = 'Diretório inválido.'
        logger.log(ERROR, err)
        raise GetPayloadError(err)

    with Session() as s:
        try:
            res = s.post(auth[0], data=auth[1])
            res.raise_for_status()
            if res.url.split('/')[-1] == 'index.php?p=':
                logger.log(INFO, '%s logado com sucesso.', auth[0])
                with s.get(url, stream=True) as res:
                    res.raise_for_status()
                    with open(path, 'wb') as f:
                        copyfileobj(res.raw, f)
                        return path
        except HTTPError as e:
            logger.log(ERROR, e.strerror)
            raise GetPayloadError('Erro HTTP.')
        except (BlockingIOError, UnsupportedOperation) as e:
            logger.log(ERROR, e.strerror)
            raise GetPayloadError('Erro no manipulador de arquivo.')


def unpack_payload(path: str):
    with ZipFile(path, 'r') as p:
        logger.log(INFO, 'descompactando %s', path)
        return p.extractall(path.removesuffix(path.split('/')[-1]))
