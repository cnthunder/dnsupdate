配合https://github.com/XIU2/CloudflareSpeedTest  用的

参考并借鉴了：

https://github.com/ymyuuu/IPDB

https://github.com/ZhiXuanWang/cf-speed-dns

https://github.com/ddgth/cf2dns

感谢以上大佬的无私分享~

get_sum_ip.py可以在action里跑，但是好像意义不大，我自己没用，因为在本地跑就够了。

dnsupdate脚本里有设置将下载测速大于50并且延迟低于80的IP保存到本地，方便建立自己的最快CF地址存档，等这个地址池够多了，应该就不需要再通过get_sum_ip去获取优选IP了，直接从这个文件里取IP就行，这就手动保存一次到sum_ip.txt里就行了，懒得再写一个脚本了

# sh脚本配置，通过crontab定时跑就行~

#!/bin/bash
cd /home/dnsupdate/py_script
# 汇总本地/线上的bestcf代理IP
#python /home/dnsupdate/py_script/get_sum_ip_local.py
python /home/dnsupdate/py_script/get_sum_ip_online.py
# 执行httping测速/改成tcping测试了
/home/dnsupdate/CloudflareST -f /home/dnsupdate/sum_ip.txt -dd -p 100 -n 1 -o /home/dnsupdate/httping.txt
# 整理httping测速结果，并输出延迟最低的top10
python /home/dnsupdate/py_script/get_httping_top10.py best1.xxx.com best2.xxx.com
# 针对top10以及既存A记录的IP进行下载测速
/home/dnsupdate/CloudflareST -f /home/dnsupdate/httping_top10.txt -p 20 -dn 20 -tl 200 -n 1 -o /home/dnsupdate/speed_top10.txt -url https://speed.xxx.com
# 根据下载测试排名，将速度最快的2个IP更新到A记录，并将best的记录写到best2nd中
# 有两个域名，需要跑两遍
python /home/dnsupdate/py_script/dnsupdate.py /home/dnsupdate/token.ini
#python /home/dnsupdate/py_script/dnsupdate.py /home/dnsupdate/token_2.ini
#python /home/dnsupdate/py_script/dnsupdate.py /home/dnsupdate/token_3.ini
#python /home/dnsupdate/py_script/dnsupdate.py /home/dnsupdate/token_4.ini
# 记录时间
date



# token.ini 配置

[CF]

CF_API_TOKEN = n1**********d

CF_ZONE_ID = c89*********8d

CF_DNS_NAME = best1.xxx.com

CF_DNS_NAME2ND = best2.xxx.com

PUSHPLUS_TOKEN = 9fe2************af1
