from os import X_OK
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import options
from datetime import datetime
import time
import string
import requests
from bs4 import BeautifulSoup
import zipfile
import smtplib
from selenium.webdriver.chrome.service import Service


# takes out all parts with id= in it
def ids(a):
    b = []
    for i in a:
        if "id=" in i:
            b.append(i)
    return b


def weird(a):
    return f'"{a}"'


def remover(x):
    for i in x[:]:
        if "id=" in i:
            x.remove(i)
            break
        else:
            x.remove(i)
    return x


def adder(a):
    b = []
    for i in a:
        if "id=" in i:
            break
        else:
            b.append(i)
    return b


def mulsplicer(a, key1, key2):
    x = []
    y = []
    for i in a:
        hi = i.split(f"{key1}")
        x.append(hi[1])
    for i in x:
        hi2 = i.split(f'{key2}')
        y.append(hi2[0])
    return y


def solosplicer(a, key1, key2):
    x = a.split(f"{key1}")
    y = x[1].split(f"{key2}")
    return y[0]


def configclear(a, key):
    hi = a.rstrip("\n")
    hi2 = hi.lstrip(f"{key}")
    hi3 = hi2.strip()
    return (hi3)


def configmode(a, key):
    y = 0
    for i in a:
        if f"{key}" in i and any(x in i for x in string.digits):
            y = i
        else:
            pass
    if y == 0:
        if key == "time.sleep=":
            return (3600)
        elif key == "time.wait=":
            return(10)
        elif key == "time.preset=":
            return(0)
        else:
            pass
    else:
        x = configclear(y, key)
        x = int(x)
        return x


# def email():
#     sender, pwd = "[sender email]", "[sender email password]"
#     receiver = "[receiver email]"

#     with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
#         smtp.ehlo()
#         smtp.starttls()
#         smtp.ehlo()
#         smtp.login(sender, pwd)
#         subject = "Python Crypto Bot"
#         body = """[Insert Content]"""
#         message = f"Subject: {subject}\n\n{body}"
#         smtp.sendmail(sender, receiver, message)


def Program(accountname, timenow):
    try:
        # This part defines the webdriver path and the website.
        now = datetime.now()
        times = now.strftime('%Y/%m/%d %H:%M')
        s=Service('/Users/marcuslai/Desktop/Codes/Python/Crypto/chromedriver')
        driver = webdriver.Chrome(service=s)
        driver.get(f"https://debank.com/profile/{accountname}")
        ff = 0

        # This part confirms that the data is present before extration of data (no contingency yet)
        # list1 is a list of source code seperated by "<"
        while True:
            x = str(driver.page_source)
            print(f"checking times= {ff}")
            if "Data updated" in x:
                list1 = x.split("<")
                break
            elif ff >=60:
                raise Exception
            else:
                ff += 1
                time.sleep(1)

        list2 = []
        list4 = []
        search = ['id="', "Assets", " + ", "title=", "$", "%"]
        search2 = []

        # this line reads the names of crypto, making sure that it's identified as a crypto when data is extracted
        with open("crypto key.txt", "r") as f:
            x = f.readlines()
            x = list(set(x))

            # this line makes sure the baseline cryptos are included in the key file
            if len(x) < 12:
                print("Error, crypto key incomplete.")
            for i in x:
                y = i.rstrip("\n")
                search.append(y)

        # collects pieces of source code with key in it given hred is not in it or if span and "." are both in it (list2)
        for i in list1:
            for j in search:
                if j in i and "href" not in i:
                    list2.append(i)
                elif "span" in i and "." in i:
                    list2.append(i)

        # for a key, if it contains both letters and numbers, put them in quotation marks.
        for i in search:
            if any(x in i for x in string.ascii_letters) and any(x in i for x in string.digits):
                searches = i.strip()
                y = weird(searches)
                search2.append(y)

        # makes sure there's no immediate duplicates in list2
        list2 = [v for i, v in enumerate(list2) if i == 0 or v != list2[i-1]]

        # removing tags unless they have id and title in them and removes empty tags without id and title in them
        for i in list2:
            list3 = i.split(">")
            if "id=" in i or "title=" in i:
                list4.append(list3[0])
            else:
                if list3[1] == "":
                    pass
                else:
                    list4.append(list3[1])

        blocks = []
        # taking all parts with id in them, but removing the first 3
        id = [i for i in list4 if "ProjectTitle_projectTitle__BAmfZ flex_flexRow__2Uu_s ProjectTitle_container__zlcQV " in i]

        # seperates out the blocks
        while True:
            if list4 != []:
                if adder(list4) != []:
                    blocks.append(adder(list4))
                list4 = remover(list4)
            else:
                break

        # takes out the trueid from the tag, and capitalizes it
        trueid = mulsplicer(id, 'id="', '"')
        for i in trueid[:]:
            trueid.remove(i)
            x = weird(i)
            trueid.append(x.upper())

        # puts total as first id
        trueid.insert(0, '"TOTAL"')

        # clears out random text in blocks
        trueblocks = []
        for i in blocks:
            temp = []
            for j in i:
                if "title=" in j:
                    x = solosplicer(j, 'title="', '"')
                    y = weird(x)
                    temp.append(y)
                else:
                    y = weird(j)
                    temp.append(y)
            temp = [v for i, v in enumerate(temp) if i == 0 or v != temp[i-1]]
            trueblocks.append(temp)

        with open(f"{accountname}.csv", "a") as f:
            n = 0
            while n < len(trueid):
                if n == 0:
                    f.write(times)
                    f.write("\n")
                    f.write(times)
                    f.write(",")
                    f.write(f"{trueid[n]}")
                    f.write(",")
                else:
                    f.write(times)
                    f.write(",")
                    f.write(f"{trueid[n]}")
                    f.write(",")
                for i in trueblocks[n+1]:
                    try:
                        if any(x in i for x in string.ascii_letters):
                            if i in search2:
                                f.write("\n")
                                f.write(times)
                                f.write(",")
                                f.write(f"{i}")
                                f.write(",")
                            elif " + " in i:
                                f.write("\n")
                                f.write(times)
                                f.write(",")
                                f.write(f"{i}")
                                f.write(",")
                            elif any(x in string.digits for x in i):
                                f.write(f"{i}")
                                f.write(f",")
                            else:
                                f.write("\n")
                                f.write(times)
                                f.write(",")
                                f.write(f"{i}")
                                f.write(",")
                        else:
                            f.write(f"{i}")
                            f.write(f",")
                    except UnicodeEncodeError:
                        f.write("\n")
                        f.write(times)
                        f.write(",")
                        f.write('"USDT"')
                        f.write(",")
                        continue

                f.write("\n")

                n += 1
        with open ("log.txt", "a") as f:
            f.write(f"{timenow} success\n")
    finally:
        driver.quit()
        hey = configmode(config, "time.wait=")
        print(f"time.wait= {hey}")
        time.sleep(hey)


config = []

with open("config.txt", "r") as f:
    x = f.readlines()
    config = x

preset = configmode(config, "time.preset=")
print(f"time.preset= {preset}")
time.sleep(preset)

while True:
    now = datetime.now()
    timenow = now.strftime('%Y/%m/%d %H:%M')
    with open("account.txt", "r") as f:
        x = f.readlines()
        # in case no IDs exist
        if x == []:
            print("Error, no IDs found.")
        else:
            # tries to run program
            # try:
                for i in x:
                    if "\n" in i:
                        y = i.rstrip("\n")
                        Program(y, timenow)
                    else:
                        Program(i, timenow)

            # for errors, email me
            # except:
            #     email()
            #     with open ("log.txt", "a") as f:
            #         f.write(f"{timenow} fail \n")
            #     break
    # to print current time in terminal, also how long it's sleeping for
    print(f"time.now= {timenow}")
    hey2 = configmode(config, "time.sleep=")
    print(f"time.sleep= {hey2}")
    time.sleep(hey2)
