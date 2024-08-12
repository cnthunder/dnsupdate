配合https://github.com/XIU2/CloudflareSpeedTest  用的

#!/bin/bash

#汇总线上的bestcf代理IP

python /home/dnsupdate/py_script/get_sum_ip.py

#执行tcping测速(httping貌似容易被临时阻断，还是用tcping好了)

/home/dnsupdate/CloudflareST -f sum_ip.txt -dd -p 100 -n 1 -o httping.txt

#整理httping测速结果，并输出延迟最低的top10

python /home/dnsupdate/py_script/get_httping_top10.py

#针对top10的IP进行下载测速

/home/dnsupdate/CloudflareST -f httping_top10.txt -p 10 -httping -n 1 -o speed_top10.txt

#根据下载测试排名，将速度最快的2个IP更新到A记录

python /home/dnsupdate/py_script/dnsupdate.py

get_sum_ip.py可以在action里跑，但是好像意义不大，
