import urllib.request
import json

import urllib.request, json
with urllib.request.urlopen("https://pastebin.com/raw/A4vfxrW3") as url:
    data = json.loads(url.read().decode())
    print(data["Version"])








#import KyloBot