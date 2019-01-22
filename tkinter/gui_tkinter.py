"""
게임의 동작 원리: 게임화면을 렌딩하는데 `틱`이라는 단위를 기준으로 새롭게 화면을 불러온다.

GUI의 원리 게임의 동작 원리와 같다.

tkinter를 통해 GUI를 구축하고

py2exe를 통해 실행 가능한 프로그램으로 변환한다.

py2exe 관련 포스트
https://spoqa.github.io/2013/05/21/py2exe-and-py2app.html
"""
from bs4 import BeautifulSoup as BTS
from functools import partial
from tkinter import *
from datetime import datetime

import webbrowser
import requests
import time

root = Tk()

def bitbucket():
    webbrowser.open("http://bitbucket.org/ssafy-seoul/python_basic")

def search_naver(word):
    url = f"https://search.naver.com/search.naver?query={word}"
    webbrowser.open(url)

def pop_keyword():
    url = "https://www.naver.com/"
    res = requests.get(url)
    doc = BTS(res.text, 'html.parser')
    selector_pop_keyword = "#PM_ID_ct > div.header > div.section_navbar > div.area_hotkeyword.PM_CL_realtimeKeyword_base > div.ah_roll.PM_CL_realtimeKeyword_rolling_base > div > ul"
    pop_keywords = doc.select_one(selector_pop_keyword)
    pop_keywords = pop_keywords.select("li > a.ah_a")
    form_rk = lambda x: (x.select_one("span.ah_r").text, x.select_one("span.ah_k").text)
    pop_keywords = list(map(form_rk, pop_keywords))
    pop_keywords = list(map(lambda x: x[0].zfill(2) + "  " + x[1], pop_keywords))
    lb_dt.config(text=datetime.now().strftime("%Y%m%dT%H%M"))
    for idx in range(20):
        do_sn = partial(search_naver, pop_keywords[idx][3:])
        btn_popks[idx].config(text=pop_keywords[idx], command=do_sn)


lb_title = Label(root, text="네이버 인기검색")
lb_dt = Label(root, text=datetime.now().strftime("%Y%m%dT%H%M"))
lb_title.pack()
lb_dt.pack()

btn_popks = [Button(root, text="{}".format(str(ind).zfill(2))) for ind in range(20)]
for popk in btn_popks:
    popk.pack()

button1 = Button(root, text="ssafy-seoul/python_basic", command=bitbucket)
button1.pack()
button2 = Button(root, text="scraping", command=pop_keyword)
button2.pack()

root.mainloop()