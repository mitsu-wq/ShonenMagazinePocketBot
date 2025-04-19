import re
import itertools
import unicodedata
from typing import Any
from .exception import GetChapterFailed

CCHARS = ''.join(map(chr, itertools.chain(range(0x00,0x20), range(0x7f,0xa0))))
CCHARS_RE = re.compile('[%s]' % re.escape(CCHARS))

def sanitize_text(s: str):
    """Remove control characters and normalize Unicode text.

    Args:
        s (str): Input string to sanitize.

    Returns:
        str: Sanitized string with control characters removed and Unicode normalized.
    """
    return unicodedata.normalize("NFKD", CCHARS_RE.sub('', s)).strip()

def ddir(d: dict[Any, Any], dir: str, de: Any={}) -> Any:
    """Retrieve dictionary value using recursive indexing with a string.

    Example:
        `ddir({"data": {"attr": {"ch": 1}}}, "data/attr/ch")` returns `1`.

    Args:
        d (dict): Dictionary to retrieve the value from.
        dir (str): Directory path of the value (e.g., "key1/key2").
        de (Any, optional): Default value if the path is not found. Defaults to {}.

    Returns:
        Any: Retrieved value or default value if not found.

    Raises:
        GetChapterFailed: If a key in the path is not found.
    """
    op = d
    for a in dir.split("/"):
        try: op = op[a]
        except: raise GetChapterFailed('Chapter not purchased')
    return op or de

def is_number(s: str) -> bool:
    """Check if a string is a valid integer.

    Args:
        s (str): Input string to check.

    Returns:
        bool: True if the string is a valid integer, False otherwise.
    """
    return s.isdigit()