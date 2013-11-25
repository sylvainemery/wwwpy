#!d:\Dev\wwwpy\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'honcho==0.4.2','console_scripts','honcho'
__requires__ = 'honcho==0.4.2'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('honcho==0.4.2', 'console_scripts', 'honcho')()
    )
