# -*- coding: utf-8 -*-

import requests
import datetime,json,time

def fetch_stations(fd):
    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9002"

    try:
        s = requests.get(url,verify = False)
    except Exception,e:
        print 'requests url fail.' + url
        raise e

    station_str = s.content.decode("utf-8")

    stations = station_str.split(u'@')

    for i in range(1,len(stations)):
        station = stations[i].split(u"|")
        out = station[1] + u" " + station[2] + u"\n"
        fd.write(out.encode("utf-8"))
        # fd.write('\n')
        print out



if __name__ == '__main__':
    with open('stations.txt','w') as fd:
        fetch_stations(fd)