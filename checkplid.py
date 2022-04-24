"""
Script used on work for fast checking for internal AD metrics
"""
import requests
import re
import random

print ("""В папке со скриптом должен быть текстовый файл domainlist.txt
в файле на каждой новой строке должен быть домен и плид через пробел без http
пример: domain.com S73
Если на домене плид будет отличаться от прописанного в файле - результат False
если совпадает с файлом - результат True
""")


def checkplid():
    input("\nEnter - что бы начать проверку доменов")
    domainlist = get_domain_list()
    tail = f"/js/FormJS/files/en/config.js?{random.randint(100000, 999999)}"
    for domain in domainlist:
        try:
            r = requests.get("https://"+domain+tail)
            text = r.text
            params = re.search(r"&aff_sub=\w+", text)
            params = params.group(0)
            if params[9:] != domainlist[domain]:
                print (domain + f" - False - {params[9:]}")
            else:
                print (domain + " - True")
        except:
            print (f"Не удалось проверить {domain}")


def get_domain_list():
    f = open("domainlist.txt")
    result = {}
    domains = []
    for line in f:
        domains.append(line.split())
    for el in domains:
        result[el[0]] = el[1]
    f.close()
    return result
    

if __name__ == "__main__":
    while True:
        checkplid()