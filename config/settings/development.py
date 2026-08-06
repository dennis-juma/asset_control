
from .base import *

# Some hosting environments expose their deployment channel as DEBUG (for
# example, ``DEBUG=release``).  Treat known production channel names as
# disabled debug mode while retaining normal boolean configuration locally.
_debug_value = config("DEBUG", default="true").strip().lower()
DEBUG = _debug_value not in {"0", "false", "no", "off", "release", "production", "prod"}


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]
