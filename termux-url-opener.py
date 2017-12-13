#!/usr/bin/python

import json
import sys
from os import environ
from os.path import join
from subprocess import CalledProcessError, call, check_output, PIPE

preferred_formats = [
    ('mp4', 'hd720'),
    ('mp4', 'medium'),
    ('ogg', None),
    ('mp3', None),
]

try:
    url = sys.argv[1]
except IndexError:
    sys.exit("Usage: termux-you-get URL")

storage_dir = join(environ['HOME'], 'storage')
workon_home = environ.get('WORKON_HOME', join(environ['HOME'], '.virtualenvs'))
you_get = join(workon_home, 'you-get', 'bin', 'you-get')

try:
    info = json.loads(check_output([you_get, '--json', url]).decode('utf-8'))
except CalledProcessError:
    info = {}

if info.get('streams'):
    title = info.get('title', 'Unknown')
    streams = {(stream.get('container'), stream.get('quality')): id
               for id, stream in info['streams'].items()}

    for fmt in preferred_formats:
        if fmt in streams:
            stream = info['streams'][streams[fmt]]
            break
    else:
        call(['termux-notification', '--id', title, '--title', title,
              '--content', "No suitable format found."])
        sys.exit(1)

    format = fmt[1]
    output_fn = title.replace('/', '_')
    itag = stream.get('itag')

    if format in ('ac3', 'aac', 'flac', 'mp3', 'ogg', 'wav'):
        dest_dir = join(storage_dir, 'music')
    else:
        dest_dir = join(storage_dir, 'movies')

    try:
        call(['termux-notification', '--id', title, '--title', title,
              '--content', "Starting download."])
        cmd = [you_get, '-o', dest_dir, '-O', output_fn]
        if itag:
            cmd += ['--itag', itag]
        call(cmd + [url], stdout=PIPE)
    except CalledProcessError as exc:
        msg = "Download failed: {}".format(exc)
        call(['termux-notification', '--id', title, '--title', title,
              '--content', msg])
    else:
        output_path = join(dest_dir, "{}.{}".format(output_fn, format))
        call(['termux-open', '--view', output_path])
else:
    print(info)
