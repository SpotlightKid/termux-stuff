#!/usr/bin/python

import json
from base64 import b64encode
from subprocess import CalledProcessError, DEVNULL, call, check_output
from urllib.request import Request, urlopen


TOKEN = "simsalabim"
PUSHSEL_URL = "http://192.168.1.100:8888/pushsel/"
# For Termux
CMD_CLIPBOARD_GET = ["termux-clipboard-get"]
CMD_ALERT = ["termux-toast"]
# For Linux
# CMD_CLIPBOARD_GET = ["xclip", "-o"]
# CMD_ALERT = ["zenity", "--width", "300", "--info", "--no-markup", "--text"]


def get_sel():
    try:
        return check_output(CMD_CLIPBOARD_GET, stderr=DEVNULL)
    except (CalledProcessError, FileNotFoundError):
        pass


def push_sel(data):
    data = json.dumps(dict(token=TOKEN, selection=b64encode(data).decode()))
    req = Request(PUSHSEL_URL, data=data.encode('utf-8'))
    req.add_header('Content-type', 'application/json')
    res = urlopen(req)
    if not res.getcode() == 204:
        raise IOError("Request failed!")


def alert(msg, *args):
    msg = msg.format(*args)
    try:
        call(CMD_ALERT+ [msg.encode("utf-8")], stderr=DEVNULL)
    except (CalledProcessError, FileNotFoundError):
        print(msg)


def main():
    data = get_sel()
    if data:
        try:
            push_sel(data)
        except Exception as exc:
            alert("Could not push selection!\n\nError: {}", exc)
        else:
            alert("Selection pushed to server.")
    else:
        alert("No selection in clipboard!")


if __name__ == '__main__':
    main()
