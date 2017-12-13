#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# clipproxy.py
#
"""A small server copies the data it receives to the primary selection."""

import argparse
import json
import logging
import sys

from base64 import b64decode
from subprocess import PIPE, run, STDOUT

import pyperclip
import flask


log = logging.getLogger(__file__)
app = flask.Flask(__name__)

TOKEN = 'simsalabim'


def pipe(cmd, input='', stderr=None, **kwargs):
    """Get output of shell command piping input to stdin."""
    kwargs['stdout'] = PIPE
    kwargs['stderr'] = {'redirect': STDOUT, 'capture': PIPE, 'drop': PIPE}.get(stderr, stderr)
    kwargs.setdefault('encoding', 'utf-8' if isinstance(input, str) else None)
    res = run(cmd, input=input, **kwargs)
    return (res.stdout, res.stderr) if stderr == 'capture' else res.stdout


@app.route('/pushsel/', methods=['POST'])
def pushsel():
    data = json.loads(flask.request.data.decode('utf-8'))
    if data.get('token') == TOKEN:
        selection = b64decode(data.get('selection', ''))
        log.debug("Got selection: %s", selection)

        if selection:
            pyperclip.copy(selection.decode('utf-8'))
            return ('', 204)
        else:
            flask.abort(400)
    else:
        flask.abort(401)


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('-v', '--verbose', action="store_true",
        help="Be verbose")

    args = ap.parse_args(args if args is not None else sys.argv[1:])

    logging.basicConfig(format="%(name)s: %(levelname)s - %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO)

    app.run(host="0.0.0.0", port=8888, debug=args.verbose)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)

