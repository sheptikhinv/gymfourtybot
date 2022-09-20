from os import getenv
from typing import Final

from dotenv import load_dotenv

load_dotenv()


class TgKeys:
    TOKEN: Final = getenv('TOKEN', 'define me!')


class NetSchoolKeys:
    LOGIN: Final = getenv('NSLOGIN')
    PASSWORD: Final = getenv('NSPASS')


class AdminKeys:
    ADMID: Final = getenv('ADMID')
