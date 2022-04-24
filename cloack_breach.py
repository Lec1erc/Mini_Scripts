"""
Script trying to breach cloaking (For advertise)
"""
import requests

with open("cloack_breach.txt", "r") as f:
    folder_list = f.read().split("\n")
suff_list = [".html", ".php"]
#hot_words = ["config"]

def check(url):
    for folder in folder_list:
        for suff in suff_list:
            r = requests.get(url+folder+suff)
            text = r.text
            if str(r) == "<Response [200]>":
                #for el in hot_words:
                    #if el in text:
                print (url+folder+suff)
            
                

if __name__ == "__main__":
    url = input("Введите домен: ")
    check(url)
    print ("Готово")