#!/bin/bash

URL="https://pypi.org/search?q="

pkg=$(termux-dialog -t "PyPI Project")
if [ -n "$pkg" ]; then
  pkg=$(echo $pkg | tr ' ' '+')
  termux-open-url "${URL}${pkg}"
fi
