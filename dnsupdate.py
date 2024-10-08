import configparser
import traceback
import json
import requests
import time

# API 密钥
token_ini = configparser.ConfigParser()
token_ini.read('token.ini')
token = token_ini['CF']
CF_API_TOKEN = token['CF_API_TOKEN']
CF_ZONE_ID = token['CF_ZONE_ID']
CF_DNS_NAME = token['CF_DNS_NAME']
PUSHPLUS_TOKEN = token['PUSHPLUS_TOKEN']

# 定义headers
headers = {
    'Authorization': f'Bearer {CF_API_TOKEN}',
    'Content-Type': 'application/json'
}

#定义筛选的最低速度MB/s
speed_limit = 8
#定义测试结果文件名
speed_top10 = 'speed_top10.txt'

# 定义根据下载速度对IP数据进行排序的函数
def sort_ips_by_speed(ips):
    return sorted(ips, key=lambda x: x['下载速度 (MB/s)'], reverse=True)

# 定义选择下载速度最快的两个IP的函数
def select_top_two_ips(sorted_ips):
    return [ip['IP 地址'] for ip in sorted_ips[:2]]

# 定义解析IP数据的函数
def parse_ips(filename, encoding='utf-8'):
    ips = []
    try:
        with open(filename, 'r', encoding=encoding) as file:
            headers = file.readline().strip().split(',')  # 读取标题行
            for line in file:
                parts = line.strip().split(',')
                ip_info = {}
                for i, value in enumerate(parts):
                    if headers[i] in ['已发送', '已接收']:  # 整数列
                        ip_info[headers[i]] = int(value)
                    elif headers[i] == '丢包率':  # 浮点数列
                        ip_info[headers[i]] = float(value)
                    elif headers[i] == '平均延迟':  # 浮点数列
                        ip_info[headers[i]] = float(value)
                    elif headers[i] == '下载速度 (MB/s)':  # 浮点数列
                        ip_info[headers[i]] = float(value)
                    elif headers[i] == 'IP 地址':  # IP地址列
                        ip_info[headers[i]] = value
                if ip_info['下载速度 (MB/s)'] > speed_limit:
                    ips.append(ip_info)
    except FileNotFoundError:
        print(f"文件 {filename} 未找到，请检查路径是否正确。")
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
    return ips

# 主函数
def get_fast_ip():
    filename = speed_top10
    encoding = 'utf-8'  # 根据你的文件编码设置
    ips = parse_ips(filename)
    if ips:
        sorted_ips = sort_ips_by_speed(ips)
        iplist = select_top_two_ips(sorted_ips)
        return iplist
    else:
        print("没有有效的IP数据可以处理。")
        return None

# 获取 DNS 记录
def get_dns_records(name):
    dns_records_info = []
    url = f'https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        records = response.json()['result']
        for record in records:
            if record['name'] == name:
                # 将记录的 name 和 content 添加到结果列表中
                dns_record = {
                    'id': record['id'],
                    'content': record['content']
                }
                dns_records_info.append(dns_record)
        return dns_records_info
    else:
        print('Error fetching DNS records:', response.text)
        return None

# 更新 DNS 记录
def update_dns_record(record_id, name, cf_ip):
    url = f'https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records/{record_id}'
    data = {
        'type': 'A',
        'name': name,
        'content': cf_ip
    }

    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()  # 如果响应状态码不是 200，将抛出 HTTPError 异常

        # 如果成功
        print(f"cf_dns_change success: ---- Time: " + str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " ---- ip：" + str(cf_ip))
        return "ip:" + str(cf_ip) + "解析" + str(name) + "成功"
    except requests.exceptions.HTTPError as http_err:
        # 处理 HTTP 错误
        print(f"HTTP error occurred: {http_err} - Status code: {response.status_code}")
    except requests.exceptions.ConnectionError as conn_err:
        # 处理连接错误
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        # 处理请求超时
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        # 处理请求异常
        print(f"Request error occurred: {req_err}")
    except Exception as e:
        # 处理其他所有可能的异常
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()  # 打印 traceback

    # 返回错误信息
    print(f"cf_dns_change ERROR: ---- Time: " + str(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return "ip:" + str(cf_ip) + "解析" + str(name) + "失败"

# 注意：上面的代码片段假定 headers 变量已经被定义，并且包含了正确的 Authorization 和 Content-Type 头信息。

# 消息推送
def push_plus(content):
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": PUSHPLUS_TOKEN,
        "title": "IP优选DNSCF推送",
        "content": content,
        "template": "markdown",
        "channel": "wechat"
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=headers)

# 主函数
def main():
    # 获取最新优选IP
    ip_addresses = get_fast_ip()
    if ip_addresses == None:
        print(f"测速结果低于{speed_limit},不更新")
        push_plus(f"测速结果低于{speed_limit},不更新")
        return None
    else:
        dns_records = get_dns_records(CF_DNS_NAME)
        # 创建一个空列表来存储所有的id
        dns_records_id = []
        dns_records_ip = []
        for record in dns_records:
            dns_records_id.append(record['id'])
            dns_records_ip.append(record['content'])
        dns_records_ip_set = set(dns_records_ip)
        ip_addresses_set = set(ip_addresses)
        common_ips = dns_records_ip_set & ip_addresses_set
        if len(common_ips) == 2:
            common_ips = list(common_ips)
            print(f"DNS记录IP地址未变，不更新：\n{common_ips[0]}, {common_ips[1]}")
            push_plus(f"DNS记录IP地址未变，不更新：\n{common_ips[0]}, {common_ips[1]}")
        elif len(common_ips) == 1:
            single_ip_set = set(ip_addresses) - common_ips
            single_ip = list(single_ip_set)
            common_ips = list(common_ips)
            print(f'已存在的一条解析不更新：{common_ips[0]}')
            push_plus_content = [f'已存在的一条解析不更新：{common_ips[0]}']
            for comm_ip in dns_records:
                if comm_ip['content'] != common_ips[0]:
                    single_dns_records_id = comm_ip['id']
                    dns = update_dns_record(single_dns_records_id, CF_DNS_NAME, single_ip[0])
                    push_plus_content.append(dns + '\n')
            push_plus('\n'.join(push_plus_content))
        else:
            push_plus_content = []
            # 遍历 IP 地址列表
            for index, ip_address in enumerate(ip_addresses):
                # 执行 DNS 变更
                dns = update_dns_record(dns_records_id[index], CF_DNS_NAME, ip_address)
                push_plus_content.append(dns + '\n')
            push_plus('\n'.join(push_plus_content))

if __name__ == '__main__':
    main()