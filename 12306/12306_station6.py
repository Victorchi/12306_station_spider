# -*- coding: utf-8 -*-

import time,datetime,json
import requests

def fetch_station (t,start,end,train_no,code,fd):
    url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?"
    params = u"train_no=" + train_no + u"&from_station_telecode=" + start + u"&to_station_telecode=" + end + u"&depart_date=" + t
    try:
        s = requests.get(url, params=params, verify=False)
    except Exception, e:
        print 'requests url fail.' + url
        raise e

    stations = json.loads(s.content)
    out = u"------------------------------------------\n"
    out += code +u"\n"
    for station in stations["data"]["data"]:
        out += station["station_no"]
        out += u" " + station["station_name"]
        out += u" " + station["arrive_time"]
        out += u" " + station["start_time"]
        out += u" " + station["stopover_time"]
        out += u"\n"

    s = out.encode("utf-8")
    fd.write("\n")
    fd.write(s)
    print s


def fetch_price(t,start,end,train_no,seat_types,src_name,des_name,train_code,fd):
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?'
    params = u'train_no=' + train_no  + u"&from_station_no=" + start + u"&to_station_no=" + end + u"&seat_types="+ seat_types + u"&train_date=" + t
    try:
        s = requests.get(url,params = params,verify = False)
    except Exception, e:
        print "requests url fail." + url
        raise e

    prices = json.loads(s.content)

    price = prices['data']
    out = u"----------------------------------\n"
    out += train_code + u" " + src_name + u" " + des_name + u"\n"
    if "A9" in price:
        out += price["A9"]
    else:
        out += u" --"
    if "P" in price:
        out += u" " + price["P"]
    else:
        out += u" --"
    if "M" in price:
        out += u" " + price["M"]
    else:
        out += u" --"
    if "O" in price:
        out += u" " + price["O"]
    else:
        out += u" --"
    if "A6" in price:
        out += u" " + price["A6"]
    else:
        out += u" --"
    if "A4" in price:
        out += u" " + price["A4"]
    else:
        out += u" --"
    if "A3" in price:
        out += u" " + price["A3"]
    else:
        out += u" --"
    if "A2" in price:
        out += u" " + price["A2"]
    else:
        out += u" --"
    if "A1" in price:
        out += u" " + price["A1"]
    else:
        out += u" --"
    if "WZ" in price:
        out += u" " + price["WZ"]
    else:
        out += u" --"
    if "MIN" in price:
        out += u" " + price["MIN"]
    else:
        out += u" --"

    s = out.encode("utf-8")
    fd.write(s)
    fd.write('\n')
    print s



def fetch_data(t,start,end,fd1,fd2,existed_code):
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?'
    params = u"leftTicketDTO.train_date=" + t + u"&leftTicketDTO.from_station=" + start + u"&leftTicketDTO.to_station=" + end + u"&purpose_codes=ADULT"

    try:
        s = requests.get(url, params=params.encode('utf-8'), verify=False)
    except Exception, e:
        print 'requests url fail.', url
        return

    datas = json.loads(s.content)

    # if datas['data'] == []:
    #     print 'no train', t, start.encode("utf-8"), end.encode("utf-8")
    #     return

    for data in datas['data']:
        data = data['queryLeftNewDTO']
        code = data["station_train_code"]
        src_name = data["from_station_name"]
        des_name = data["end_station_name"]
        no = data["train_no"]

        is_fetch_station = False  # 这句话没有看明白
        if no in existed_code:
            if (src_name,des_name) in existed_code[no]:
                continue
            else:
                is_fetch_station = True
                existed_code[no] = set([(src_name,des_name)])

            time.sleep(2)
            fetch_price(t,data['from_station_no'],data['to_station_no'],no,data["seat_types"],data["from_station_name"],data['to_station_name'],code,fd2)

            if is_fetch_station:
                time.sleep(2)
                fetch_station(t,start,end,no,code,fd1)


def fetch_stations_code():
    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9002"

    try:
        s = requests.get(url,verify = False)
    except Exception,e:
        print 'requests url fail.' + url
        raise e

    station_str = s.content.decode("utf-8")

    stations = station_str.split(u'@')

    results = []
    with open('15.code.txt','w') as fd:
        for i in range(1,len(stations)):
            station = stations[i].split(u"|")
            results.append((station[1],station[2]))
            fd.write((station[1] + u" " + station[2] + u"\n").encode("utf-8"))

    return results


def deal_and_store(existed_codes):
    result = set()
    with open("15.routes.txt",'w') as fd:
        for code in existed_code:
            routes = existed_code[code]
            for route in routes:
                if route not in result:
                    result.add(route)
                    out = route[0] + u" "+route[1] + u"\n"
                    fd.write(out.encode("utf-8"))

def fetch_trains_stactic_info(existed_code):
    stations = fetch_stations_code()

    size = len(stations)
    with open ('15.train_code','w') as fd1:
        with open('15.train_price.txt','w') as fd2:
            for i in range(0,size-1):
                for j in range(i+1,size):
                    t = (datetime.datetime.now() + datetime.timedelta(days= 3)).strftime("%Y-&m-%d")
                    src = stations[i][1]
                    des = stations[j][1]

                    time.sleep(2)
                    fetch_data(t,src,des,fd1,fd2,existed_code)

    return existed_code
if __name__ == '__main__':

    existed_code = {}
    fetch_trains_stactic_info(existed_code)
    deal_and_store(existed_code)