# -*- coding: utf-8 -*-
import time
import json,requests,datetime

def fetch_stations(t,train_code,train_no,routes,fd):
    url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo"

    params = u"train_no=" + train_no + u"&from_station_telecode=BBB&to_station_telecode=BBB&depart_date=" + t
    try:
        s = requests.get(url, params=params.encode("utf-8"), verify=False)
    except Exception, e:
        print "fetch stations fail. " + url
        raise e
    stations = json.loads(s.content)

    out = u"-------------------------------\n"
    out += train_code + u"\n"
    datas = stations["data"]["data"]
    size = len(datas)

    for i in range(0,size):
        A = datas[i]
        if i != size:
            for j in range (i+1,size):
                B = datas[j]
                routes.add((A["station_name"],B["station_name"]))

        out += A['station_no']
        out += u" " + A["station_name"]
        out += u" " + A["arrive_time"]
        out += u" " + A["start_time"]
        out += u" " + A["stopover_time"]
        out += u"\n"

    s = out.encode("utf-8")
    fd.write(s)
    fd.write("\n")

    print s


def fetch_all_train_info(routes):
    t = (datetime.datetime.now() + datetime.timedelta(days= 3)).strftime("%Y-%m-%d")
    url = 'https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName'
    try:
        s = requests.get(url,params = {"date":t},verify = False)
    except Exception, e:
        print 'requetst url fail.' + url
        return

    datas = json.loads(s.content)

    with open("16.train_codes.txt",'w') as fd:
        fd.write(s.content)

    with open("16.train_infos.txt",'w') as fd:
        for data in datas["data"]:
            time.sleep(2)
            fetch_stations(t, data["station_train_code"], data["train_no"], routes, fd)


def store_routes(routes):
    with open("16.routes.txt",'w') as fd:
        for route in routes:
            out = route[0] + u" " + route[1] + u"\n"
            fd.write(out.encode('utf-8'))


if __name__ == '__main__':
    routes = set()
    fetch_all_train_info(routes)
    store_routes(routes)
