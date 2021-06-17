from io import UnsupportedOperation
import logging
from os.path import exists
from shutil import copyfileobj
from zipfile import ZipFile

from requests import Session
from requests.models import HTTPError


timeout = 10


class GetPayloadError(Exception):
    ...


class UnzipFileError(Exception):
    ...


class AuthError(Exception):
    ...


def path_exists(path: str) -> bool:
    suffix = path.split('/')[-1]
    return suffix.endswith('.zip') and exists(path.removesuffix(suffix))


def get_payload(path: str, url: str, auth):
    logging.info('acessando %s', url)
    if not path_exists(path):
        err = 'Diretório inválido.'
        logging.error(err)
        raise GetPayloadError(err)

    with Session() as s:
        try:
            logging.info('autenticando %s', auth[0])
            res = s.post(auth[0], data=auth[1], timeout=timeout)
            res.raise_for_status()
            
            if res.url.split('/')[-1] != 'index.php?p=':
                logging.error('falha na autenticação')
                raise AuthError('falha na autenticação')

            logging.info('acessando %s', url)
            with s.get(url, stream=True, timeout=timeout) as res:
                res.raise_for_status()
                logging.info('baixando')
                with open(path, 'wb') as f:
                    copyfileobj(res.raw, f)
                    return path

        except (HTTPError, ConnectionError) as e:
            logging.error(e.strerror)
            raise GetPayloadError('Erro HTTP.') from e
        except (BlockingIOError, UnsupportedOperation) as e:
            logging.error(e.strerror)
            raise GetPayloadError('Erro no manipulador de arquivo.') from e


def unpack_payload(path: str):
    logging.info('descompactando %s', path)
    try:
        with ZipFile(path, 'r') as p:
            return p.extractall(path.removesuffix(path.split('/')[-1]))
    except Exception as e:
        logging.error(e)
        raise UnzipFileError(e)
