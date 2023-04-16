import urllib.request as request
from bs4 import BeautifulSoup as bs
import re
import json
import time

import streamlit as st
import streamlit.components.v1 as components

# url="https://api.thingspeak.com/channels/2108652/feeds.json?results=2";
# # data=ur11ib.urlopen("https://api.thingspeak.com/upate?apt_key=7TL3I8UCM99A5RH3&field1="+str(900));
# # print data;

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
# req = request.Request(url, headers = headers)
# datafromwebsite=request.urlopen(req);
# print(datafromwebsite);

# bootstrap 4 collapse example
components.html(
    """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <div id="accordion">
      <div class="card">
        <div class="card-header" id="headingOne">
          <h3 id="RESULT">
            SAFE
          </h3>
        </div>
      </div>
    </div>
    """,
    height=600,
)


def tempCheck():
    TS = request.urlopen("http://api.thingspeak.com/channels/2108652/feeds/last.json?api_key=7TL3I8UCM99A5RH3")

    response = TS.read()
    data=json.loads(response)

    # print(data);
    a = data['created_at']
    b = data['field1']
    c = data['field2']

    ambient=0;
    object=0;
    print("\n");
    print(a);
    print("\n");
    if(b!=None):
        ambient=float(b);
        print(b);
        print("\n");
    
    if(c!=None):
        object=float(c);
        print(c);
        print("\n");  

    if((ambient>100.4) or (object>100.4)):
        old=bs.find("h3", {"id":"RESULT"})
        new=old.find(text=re.compile("SAFE")).replace_with("UNSAFE")
    else:
        old=bs.find("h3", {"id":"RESULT"})
        new=old.find(text=re.compile("UNSAFE")).replace_with("SAFE")

    TS.close()

tempCheck()