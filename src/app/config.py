from configparser import ConfigParser


cfg = ConfigParser()
cfg.read('config.ini')
cfg.get('auth', 'EMAIL')

EMAIL = cfg.get('auth', 'EMAIL')
PASSWORD = cfg.get('auth', 'PASSWORD')

AUTH = (
    'https://inlabs.in.gov.br/logar.php',
    {'email': EMAIL, 'password': PASSWORD}
)


def get_uri(date_: str, payload_suffix: str):
    # print(date.today().isoformat())
    return f'https://inlabs.in.gov.br/index.php?p={date_}&dl={date_}-{payload_suffix}.zip'
