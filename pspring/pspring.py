context={}

import os

for item in os.environ:
    if item.startswith("pspring"):
        os.environ[item.replace("_",".")] = os.environ.get(item)

from .core.bean import *
from .core.autowired import *
from .core.context import *
from .core.config import *
from .core.configprovider import *
from .core.cacheprovider import *
