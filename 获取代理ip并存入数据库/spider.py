
# -*- coding:utf8 -*-
from bs4 import BeautifulSoup
import requests
import checkip
from lxml import etree
import pymysql
import DBUtils


url = 'http://odds.500.com/europe_jczq.shtml'
#url = 'http://odds.500.com/europe_jczq.shtml'
headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "zh",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Cookie": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTA5OTY2NTlhYmQzYjY5YzgxZGU1ZTI4MTU4M2YzYjFiBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMU4wMU1pSmxHTlI5VS96VU9vV3c4UklWRDliS1NwVGN2bW5keWpZWU4xOW89BjsARg%3D%3D--db69602cff8bee13e1a49b7e0dd1dce20df7e648; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1564387243,1566177432,1566185580; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1566199598",
                "Host": "odds.500.com",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
}
#
Ip = checkip.IpUtils()
proxylist = Ip.get_random_ip().split(':',1)
#proxyiplist = proxyip.split(':',1)
proxyip = {'{0}':'{1}'.format(proxylist[0],proxylist[1])}
#print(proxyip)

# def getHtml():
#     res = requests.get(url=url,headers=headers,proxies=proxyip)
#     #res.encoding = 'utf-8'
#     #html = res.text.encode("gbk")
#     html = res.text
#     soup = BeautifulSoup(html,'lxml')
#     #id = soup.find('table',attrs={'class':'bet-tb bet-tb-dg'})
#     print(html)
# getHtml()

def cra_data_url(url=url,encoding="gb2312"):

    session = requests.session()
    response = session.get(url=url,headers=headers,proxies=proxyip)
    content = response.content.decode(encoding,errors="ignore")
    return content

def cra_oupei_page():
    content  = cra_data_url()
    selector  = etree.HTML(content)

    elemtsid = selector.xpath('//tbody[@id="main-tbody"]''//input[@type="checkbox"]'
                              '/../../../@data-fid')

    elemts1 = selector.xpath('//tbody[@id="main-tbody"]'
                              '//input[@type="checkbox"]/../text()')
    elemtsTime = selector.xpath('//tbody[@id="main-tbody"]//input[@type="checkbox"]'
                                '/../../../@date-dtime')
    elemtswin = selector.xpath('//tbody[@id="main-tbody"]//input[@type="checkbox"]'
                                '/../../../@data-win')
    elemtsdraw = selector.xpath('//tbody[@id="main-tbody"]//input[@type="checkbox"]'
                               '/../../../@data-draw')
    elemtslost = selector.xpath('//tbody[@id="main-tbody"]//input[@type="checkbox"]'
                                '/../../../@data-lost')

    elemtsTeam1 = selector.xpath('//tbody[@id="main-tbody"]//input[@type="checkbox"]'
                                 '/../../following-sibling::*[4]/a/text()')
    # 隐藏的第六列 比赛队名2
    elemtsTeam2 = selector.xpath('//tbody[@id="main-tbody"]//input[@type="checkbox"]'
                                 '/../../following-sibling::*[6]/a/text()')

    elemtstest = selector.xpath('//tbody[@id="main-tbody"]//text()')
   # db = pymysql.connect("127.0.0.1", "root", "mysql", "fdata", charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    #cursor = db.cursor()

    #sql = "insert into foot_data(game_id,game_time,start_time,win_bo,dogfall_bo,lose_bo,team1,team2) values (%s,%s,%s,%s,%s,%s,%s,%s)"




    # print(elemtsid)
    # print(elemts1)
    # print(elemtsTime)
    # print(elemtswin)
    # print(elemtsdraw)
    # print(elemtslost)
    #
    #
    # print(elemtsTeam1)
    # print(elemtsTeam2)

    #sql = "insert into foot_data(`game_id`,`game_time`,`start_time`,`win_bo`,`dogfall_bo`,`lost_bo`,`team1`,`team2`) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                                           # zip(elemtsid,elemts1,elemtsTime,elemtswin,elemtsdraw,elemtslost,elemtsTeam1,elemtsTeam2)
    exe_result = DBUtils.DBUtils.executeMany("replace into foot_data(`game_id`,`game_week`,`start_time` ,`win_bo` ,`dogfall_bo`,`lost_bo`,`team1`,`team2`) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                                            zip(elemtsid, elemts1, elemtsTime, elemtswin, elemtsdraw, elemtslost, elemtsTeam1, elemtsTeam2))

    print("result:" + str(exe_result))
    for el in zip(elemtsid,elemts1,elemtsTime,elemtswin,elemtsdraw,elemtslost,elemtsTeam1,elemtsTeam2):
        print(el)


cra_oupei_page()
