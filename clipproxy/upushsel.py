#!/home/bin/micropython

import ujson as json
import urequests as requests
from os import popen
from base64 import b64encode


TOKEN = "simsalabim"
PUSHSEL_URL = "http://denkbett:8888/pushsel/"


def get_sel():
    try:
        p = popen("termux-clipboard-get")
        res = p.read()
        p.close()
        return res
    except:
        pass


def push_sel(data):
    data = b64encode(data.encode('utf-8')).decode()
    data = dict(token=TOKEN, selection=data)
    req = requests.post(PUSHSEL_URL, json=data)
    if not res.status_code == 204:
        raise IOError("Request failed!")


def info(msg, title=None):
    p = popen("termux-toast", 'w')
    p.write(msg.encode("utf-8"))
    p.close()


def main():
    data = get_sel()
    if data:
        try:
            push_sel(data)
        except OSError as exc:
            info("Could not push selection: {}".format(exc))
        else:
            info("Selection pushed to server.")
    else:
        info("No selection in clipboard!")


if __name__ == '__main__':
    main()