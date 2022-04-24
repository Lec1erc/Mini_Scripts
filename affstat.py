"""
Script for easy reports
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
API_LIST = {"NAME":"API_KEY",

            }


def Start(geo_check):
    print(
"""1 = Отчёт за сегодня
2 = Отчёт за вчера
Либо укажи временной период (временной формат - ММ-ДД):""")
    result = {}
    date_report_first = today
    date_report_second = today
    date_first = input("С: ")
    if date_first == "1":
        None
    elif date_first == "2":
        date_report_first = yesterday
        date_report_second = yesterday
    else:
        date_second = input("По: ")
        date_report_first = year[:5]+date_first
        date_report_second = year[:5]+date_second
    os.system('CLS')

    for name,key in API_LIST.items():
        url = f"https://hasoffers.com/Apiv3/json?api_key={key}&Target=Affiliate_Report&Method=getConversions&fields[]=Stat.affiliate_info1&fields[]=OfferUrl.name&fields[]=Goal.name&filters[Stat.date][conditional]=BETWEEN&filters[Stat.date][values][]={date_report_first}&filters[Stat.date][values][]={date_report_second}&limit=5000"
        holder = Report(url)
        result[name] = holder
        response = {"name":name, "source_id":{}}
        for source,aff_sub in result[name].items():
            response["source_id"][source] = {"aff_sub":aff_sub}
        return print (json.dumps(response))


def Report(url):
    r = requests.get(url)
    text = json.loads(r.text)
    source = {}
    result = {}
    mostwanted = ["Default","Deposit","TestAccount"]

    try: 
        for el in text['response']["data"]["data"]:
            if el["Goal"]["name"] in mostwanted:
                goal = el["Goal"]["name"]
                aff_sub = el["Stat"]["affiliate_info1"]
                offer_url = el["OfferUrl"]["name"][-8:]
                if offer_url not in source:
                    source[offer_url] = {aff_sub:{"Default":0, "Deposit":0, "TestAccount":0}}
                if aff_sub not in source[offer_url]:
                    source[offer_url][aff_sub] = {"Default":0, "Deposit":0, "TestAccount":0}
                if goal not in source[offer_url][aff_sub]:
                    source[offer_url][aff_sub][goal] = 1
                else:
                    source[offer_url][aff_sub][goal] += 1

        for key in source:
            for i in source[key]:
                test = source[key][i].pop("TestAccount")
                source[key][i]["Default"] -= test
                result[key] = dict(source[key])
                if source[key][i]["Default"] < 1 and source[key][i]["Deposit"] < 1:
                    result[key].pop(i)

    except: return print ("\nНеверная дата\n")
    return result


if __name__ == "__main__":
    geo_check = 1
    while True:
        geo_check = Start(geo_check)
        print("\n")