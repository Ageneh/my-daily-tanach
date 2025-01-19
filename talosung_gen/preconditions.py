import argparse, sys
from datetime import datetime
from os import path, makedirs

YEAR = None
current_dir = path.dirname(__file__)

_parser = argparse.ArgumentParser()
_parser.add_argument("--year", help="Define the year.")
_parser.add_argument("--out", help="Define the output directory.")
_args = None

_DE = "de"
_EN = "en"
_HE = "he"
_GR = "gr"
LANGS = [_DE, _EN, _HE, _GR]
langs = {_HE, _EN, _DE, _GR}

BOOK_NAME_PATTERN = "^(.*) (\\d+,.*)"

def get_res_path(file):
    return "{}/resources/{}".format(current_dir, file)

def get_out_path(file=""):
    out = _args.out if _args.out is not None else "out/{}".format(YEAR)
    return "{}/{}/{}".format(current_dir, out, file)


def get_res_dir():
    return "{}/resources".format(current_dir)

def generate_dirs():
    print("Generate path/dir/file:", get_out_path())
    makedirs(path.dirname(get_out_path()), exist_ok=True)


def parse_args():
    global _parser, _args, YEAR
    _args = _parser.parse_args()

    YEAR = _args.year
    if YEAR is None:
        YEAR = datetime.now().year

    generate_dirs()

    return {
        "year": YEAR
    }

def set_arg(key, val):
    _parser.add_argument(key, val)


parse_args()