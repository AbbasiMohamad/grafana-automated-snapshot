from constants import (APP_NAME, PKG_VERSION, USER_HOME)
import sys
from main import main as executer
# {from: "now-7d", to: "now"}
docstring = """
{0} {1}
Usage:
    
    grafana-snapshot-backup --version
Options:
    -h --help                               Show this help message and exit
    --version                               Get version information and exit
    --weekly                                Run and backup weekly, idempotently.
    --monthly                               Run and backup monthly, idempotently.

""".format(APP_NAME, PKG_VERSION)


def main():
    if sys.argv is None or len(sys.argv) < 2:
        print(docstring)
        sys.exit()
    else:
        command = sys.argv[1]

    if command == "-h" or sys.argv[1] == "--help":
        print(docstring)
        sys.exit()
    elif command == "--version":
        print("version: {0}".format(PKG_VERSION))
        sys.exit()
    elif command == "--weekly":
        executer()
        sys.exit()
    else:
        print(docstring)
        sys.exit()


if __name__ == '__main__':
    main()
