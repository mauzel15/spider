import pymysql
import requests

conn = pymysql.connect(host="localhost",user="root",passwd="mysql",db="ippool",charset="utf8")
cursor = conn.cursor()
class IpUtils(object):

    # 删除无效ip
    def delete_ip(self,ip):
        sql ="delete from ippool where IP='{0}'".format(ip)
        cursor.execute(sql)
        conn.commit()
        return True

    # 判断ip是否可用
    def judge_ip(self,type1,IP,port):
        http_url ="http://www.baidu.com"
        proxy_url ={'{0}':'{1}:{2}'.format(type1,IP,port)}

        try:
            proxy_dict = {
                type: type1, # type 为https 或者http 数据库存储的
            }
            response = requests.get(http_url,proxies=proxy_url)
            code = response.status_code
            if code >= 200 and code < 300:
                print("effective ip")
                return True
        except Exception as e:

            #self.delete_ip(IP)
            print("invalid ip and port")
            return False

        else:
            print("invalid ip and port")
            self.delete_ip(IP)
            return False
    # 随机获取IP
    def get_random_ip(self):
        random_sql ="""
            SELECT type1, IP, port FROM ippool
            ORDER BY RAND()
            LIMIT 1
        """
        cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            type1 = ip_info[0]
            ip = ip_info[1]
            port = ip_info[2]
            judge_re = self.judge_ip(type1,ip,port)
            if judge_re:

                return "{0}:{1}:{2}".format(type1,ip,port)

            else:

                return self.get_random_ip()

if __name__ == "__main__":
    Ip = IpUtils()
    print(Ip.get_random_ip())