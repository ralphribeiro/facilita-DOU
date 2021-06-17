from argparse import ArgumentParser
from datetime import date
import logging
from os.path import join
import tempfile

from app.config import AUTH, get_uri
from app.payload import get_payload, unpack_payload
from app.parser_xml import get_items


logging.getLogger().setLevel(logging.INFO)

today = date.today().isoformat()


def main():
    td = tempfile.TemporaryDirectory(prefix='facdou', suffix=today)

    parser = ArgumentParser(description='Busca no diário oficial da união.')
    parser.add_argument('-t', '--tipo', help='ex: licitação', type=str, required=True)
    parser.add_argument('-p', '--padrao', help='padrão de busca', type=str, required=True)
    args = parser.parse_args()
    logging.info('iniciando busca <%s, %s>', args.tipo, args.padrao)

    num_do = 'DO3'
    path = join(td.name, f'{today}-{num_do}.zip')
    url = get_uri(today, num_do)
    
    get_payload(path, url, AUTH)
    unpack_payload(path)

    pattern = (args.tipo, args.padrao)
    items = get_items(td.name, pattern)
    for i in items:
        print(i.identifica, i.url)


if __name__ == "__main__":
    main()
