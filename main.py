import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import datetime

USERNAME = ""
PASSWORD = ""

BASE_URL = 'http://mis.sse.ustc.edu.cn'
VALID_URL = BASE_URL + '/ValidateCode.aspx'
SSE_URL = BASE_URL + '/default.aspx'
HOME_PAGE = BASE_URL + '/homepage/StuHome.aspx'

NOTICE_URL = "https://api.day.app"
NOTICE_TOKEN = ""


def calculate_code(codes):
    return sum([int(code) for code in codes])


def parse_notice(html):
    notices = []
    soup = BeautifulSoup(html, 'lxml')
    notice_nodes = soup.find(
        id="global_LeftPanel_UpRightPanel_ContentPanel2_ContentPanel3_content").find_all('tr')
    for node in notice_nodes:
        title = node.find_all('td')[0].text
        author = node.find_all('td')[1].text
        time = node.find_all('td')[2].text
        link = BASE_URL + node.find_all('td')[0].a['href']
        notices.append([title, author, time, link])

    return notices


def main():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    cur_date = str(year) + "-" + str(month) + "-" + str(day)
    with requests.Session() as s:
        res = s.get(VALID_URL)
        codes = res.cookies['CheckCode']
        code = calculate_code(codes)
        data = {
            '__EVENTTARGET': 'winLogin$sfLogin$ContentPanel1$btnLogin',
            'winLogin$sfLogin$txtUserLoginID': USERNAME,
            'winLogin$sfLogin$txtPassword': PASSWORD,
            'winLogin$sfLogin$txtValidate': code,
        }
        s.post(SSE_URL, data=data)
        res = s.get(HOME_PAGE)
        notices = parse_notice(res.text)
        for notice in notices:
            if notice[2] == cur_date:
                send_notice(notice)


def send_notice(notice):
    title = quote(notice[0])
    link = notice[3]
    url = f"{NOTICE_URL}/{NOTICE_TOKEN}/{title}?url={link}"
    requests.get(url)


if __name__ == '__main__':
    main()
