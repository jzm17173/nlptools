__version__ = "0.1.0"

from .fs import read_file
from .fs import write_file
from .fs import read_json
from .fs import write_json
from .fs import mkdir
from .fs import rmdir
from .fs import rmfile
from .fs import file_tail
from .fs import file_uniq
from .fs import concat_file

from .date import now
from .date import timestamp
from .date import datetime2string
from .date import string2datetime
from .date import datetime_add
from .date import start_time
from .date import get_delta

from .validator import is_int
from .validator import is_float
from .validator import is_email
from .validator import verify
from .validator import verify_page

from .http import serialize
from .http import get
from .http import post
from .http import fetch

from .crypto import AESCrypto

from .calc import num_add
from .calc import num_sub
from .calc import num_multi
from .calc import num_div

from .number import normalize_num
from .number import pad_num

from .utils import load_dict
from .utils import load_syn_dict
from .utils import clean_text
from .utils import clean_word
from .utils import generate_name

from .fullhalf import full2half

from .freq_dist import FreqDist

from .syn import syn_cleaning

from .correcter import typos_cleaning
from .correcter import stock_cleaning

from .crawler import ArticleCrawler
