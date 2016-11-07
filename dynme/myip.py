#!/usr/bin/env python3

import requests

URL = "https://api.ipify.org"

if __name__ == "__main__":
    print(requests.get(URL).text)
