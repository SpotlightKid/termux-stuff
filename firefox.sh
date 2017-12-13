#!/bin/bash

exec am start --user 0 -a android.intent.action.VIEW -n org.mozilla.firefox/.App -d "$1" >/dev/null
