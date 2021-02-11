
EMAIL = ''
PASSWORD = ''


AUTH = (
    'https://inlabs.in.gov.br/logar.php',
    {'email': EMAIL, 'password': PASSWORD}
)


def get_uri(date_: str, payload_suffix: str):
    # print(date.today().isoformat())
    return f'https://inlabs.in.gov.br/index.php?p={date_}&dl={date_}-{payload_suffix}.zip'
