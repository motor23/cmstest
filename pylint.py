#! /usr/bin/env python3
import re
import sys

import manage
from pylint import run_pylint

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(run_pylint())
