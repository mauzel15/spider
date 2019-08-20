import requests
from lxml import etree
import pymysql

class getip:

    def __init__(self):
        self.url = 'http://www.xicidaili.com/nn/'
        self.headers  = self.headers =  {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTA5OTY2NTlhYmQzYjY5YzgxZGU1ZTI4MTU4M2YzYjFiBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMU4wMU1pSmxHTlI5VS96VU9vV3c4UklWRDliS1NwVGN2bW5keWpZWU4xOW89BjsARg%3D%3D--db69602cff8bee13e1a49b7e0dd1dce20df7e648; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1564387243,1566177432,1566185580; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1566199598",
            "Host": "www.xicidaili.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }




        self.user = 'root'
        self.pwd = 'mysql'
        self.host = '127.0.0.1'

    def getHtml(self):
        res = requests.get(url=self.url,headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        self.parseHtml(html)
        print('获取网页成功')

    def parseHtml(self,html):
        lst = []
        #构建xpath解析对象
        parsehtml = etree.HTML(html)
        #获取ip元素对象
        iplist = parsehtml.xpath('//tr/td[2]')
        #获取port元素对象
        portlist = parsehtml.xpath('//tr/td[3]')
        #获取地区元素对象
        addrlist = parsehtml.xpath('//tr/td[4]')
        #获取代理协议类型对象
        typelist = parsehtml.xpath('//tr/td[6]')
        print(html)
        self.writeComment(iplist,portlist,addrlist,typelist)

    def writeComment(self,iplist,portlist,addrlist,typelist):
        conn = pymysql.connect(self.host,self.user,self.pwd)
        cursor = conn.cursor()
        #cursor.execute('create database if not exists ippool')
        cursor.execute('use ippool')
        #cursor.execute('create table if not exists ippool(id int primary key auto_increment,IP varchar(20),port varchar(10),address varchar(20),type1 varchar(10)) default charset = "utf8";')
        for x,y,z,m in zip(iplist,portlist,addrlist,typelist):
            if x.text and y.text and z.text and m.text:
                cursor.execute('insert into ippool(IP,port,address,type1) values ("%s","%s","%s","%s");'%(x.text, y.text, z.text ,m.text))
                conn.commit()




    def main(self):
        self.getHtml()


if __name__ == '__main__':
    get = getip()
    get.main()