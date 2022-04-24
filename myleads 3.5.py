"""
Script for easy report for whole team
"""
import requests
import json
import datetime
from datetime import timedelta
import os


today = datetime.date.today()
yesterday = today - timedelta(1)
year = str(today)
year = year[:5]
API_LIST = {"name1":"api1",
            "name2":"api2",
            "name3":"api3"
            }


def Start(geo_check):
    print(
"""s = ВКЛ/ВЫКЛ разбивка по гео
1 = Отчёт за сегодня
2 = Отчёт за вчера
Либо укажи временной период (временной формат - ММ-ДД):""")
    date_report_first = today
    date_report_second = today
    date_first = input("С: ")
    if date_first == "1":
        None
    elif date_first == "2":
        date_report_first = yesterday
        date_report_second = yesterday
    elif date_first == "s":
        if geo_check:
            geo_check = 0
            os.system('CLS')
            print ("Разбивка по гео отключена")
        else:
            geo_check = 1
            os.system('CLS')
            print ("Разбивка по гео включена")
        return geo_check
    else:
        date_second = input("По: ")
        date_report_first = year[:5]+date_first
        date_report_second = year[:5]+date_second
    os.system('CLS')

    geo_counter, result = {}, {}
    summall, total = [0,0], [0,0]
    for el in API_LIST.keys():
        result[el] = {}

    for name,key in API_LIST.items():
        url = f"https://api.hasoffers.com/Apiv3/json?api_key={key}&Target=Affiliate_Report&Method=getConversions&fields[]=Country.name&fields[]=Goal.name&filters[Stat.date][conditional]=BETWEEN&filters[Stat.date][values][]={date_report_first}&filters[Stat.date][values][]={date_report_second}&data_start=2021-01-01&hour_offset=-1&limit=50000"
        holder = Report(url)
        try:
            for el, i in holder.items():
                if i["Default"] or i["Deposit"] or i["TestAccount"]:
                    result[name][el] = i 
                    geo_counter[el] = {"Default":0,"Deposit":0,"TestAccount":0}
        except: return geo_check

    if date_first in ["1","2"]:
        print (f"{date_report_second}")
    else:
        print (f"{date_report_first} - {date_report_second}")
    for name,el in result.items():
        print (name)
        for i,a in el.items():
            try:
                geo_counter[i]["Default"] += a["Default"]
                geo_counter[i]["Default"] -= a["TestAccount"]
                geo_counter[i]["Deposit"] += a["Deposit"]
                a["Default"] -= a["TestAccount"]
            except: None
            try:
                if geo_check:
                    if a['Default'] > 0 or a['Deposit'] > 0:
                        print (f"{i} - Leads: {a['Default']} - Deposits: {a['Deposit']}")
                total[0] += a["Default"]
                total[1] += a['Deposit']
                summall[0] += a["Default"]
                summall[1] += a['Deposit']
            except: None
        print (f"Total - Leads: {total[0]} - Deposit: {total[1]}\n")
        total = [0,0]
    if len(API_LIST) > 1:
        print (f"All - Leads: {summall[0]} - Deposit: {summall[1]}")
        if geo_check:
            for i,a in geo_counter.items():
                if geo_counter[i]["Default"] > 0 or geo_counter[i]["Deposit"] > 0:
                    print (f"{i} - Leads: {a['Default']} - Deposits: {a['Deposit']}")
    return geo_check


def Report(url):
    r = requests.get(url)
    text = json.loads(r.text)
    country = {}

    try: 
        for el in text['response']["data"]["data"]:
            goal = el["Goal"]["name"]
            if el["Country"]["name"] not in country:
                country[el["Country"]["name"]] = {"Default":0, "Deposit":0, "TestAccount":0}
                country[el["Country"]["name"]][goal] = 1
            else:
                if goal not in country[el["Country"]["name"]]:
                    country[el["Country"]["name"]][goal] = 1
                else:
                    country[el["Country"]["name"]][goal] += 1
    except: return print ("\nНеверная дата\n")
    return country


if __name__ == "__main__":
    print ("Разбивка по гео включена")
    geo_check = 1
    while True:
        geo_check = Start(geo_check)
        print("\n")