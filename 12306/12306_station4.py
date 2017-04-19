#conding:utf-8
import time
import json
import datetime
import requests

def fetch_stations(t,start,end,train_no,fd):
    url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?"
    params = u"train_no=" + train_no + u"&from_station_telecode=" + start + u"&to_station_telecode=" + end + u"&depart_date=" + t
    try:
        s = requests.get(url,params = params , verify = False)
    except Exception, e :
        print 'requests url fail.' + url
        raise e

    stations = json.loads(s.content)

    for station in stations["data"]["data"] :
        out = u""
        out += station["station_no"]
        out += u" " + station["station_name"]
        out += u" " + station["arrive_time"]
        out += u" " + station["start_time"]
        out += u" " + station["stopover_time"]

        s = out.encode("utf-8")
        fd.write("\n")
        fd.write(s)
        print s
    fd.write("\n")

def fetch_price(t,start,end,train_no,fd):
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?'
    params = u'train_no=' + train_no  + u"&from_station_no=" + start + u"&to_station_no=" + end + u"&seat_types=OM9" + u"&train_date=" + t
    try:
        s = requests.get(url,params = params,verify = False)
    except Exception, e:
        print "requests url fail." + url
        raise e

    prices = json.loads(s.content)

    price = prices['data']
    out = u"\n"
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


def fetch_data(t,start,end,fd):
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?'
    params = u"leftTicketDTO.train_date=" + t + u"&leftTicketDTO.from_station=" + start + u"&leftTicketDTO.to_station="+ end + u"&purpose_codes=ADULT"
    # url =('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-04-20&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT')
    try:
        s = requests.get(url,params=params.encode('utf-8'),verify = False)
        # s = requests.get(url,verify = False)
    except Exception, e :
        print 'requests url fail.',url
        return

    datas = json.loads(s.content)

    # print datas
    if  datas['data'] == []:
        print 'no train' ,t , start.encode("utf-8"),end.encode("utf-8")
        return


    for data in datas['data']:
        data = data['queryLeftNewDTO']
        out = u"-------------------------------------\n"
        out += data["start_station_name"]
        out += u" " + data["end_station_name"]
        out += u" " + data["station_train_code"]
        out += u"\n" + data["swz_num"]
        out += u" " + data["tz_num"]
        out += u" " + data["zy_num"]
        out += u" " + data["ze_num"]
        out += u" " + data["gr_num"]
        out += u" " + data["rw_num"]
        out += u" " + data["yw_num"]
        out += u" " + data["rz_num"]
        out += u" " + data["yz_num"]
        out += u" " + data["wz_num"]
        out += u" " + data["qt_num"]

        s = out.encode("utf-8")
        fd.write(s)
        fd.write("\n")
        print s

        time.sleep(2)
        fetch_price(t,data['from_station_no'],data['to_station_no'],data['train_no'],fd)

        time.sleep(2)
        fetch_stations(t,start,end,data['train_no'],fd)

        time.sleep(2)


if __name__ == '__main__':

    with open('13.txt','w') as fd:
        fetch_data((datetime.datetime.now() + datetime.timedelta(days = 3)).strftime('%Y-%m-%d'), 'BJP','SHH',fd)
