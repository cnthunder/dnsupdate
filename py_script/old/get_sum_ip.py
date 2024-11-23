import requests
import traceback

def get_optimization_ip(timeout=5, max_retries=3):
    for attempt in range(max_retries):
        try:
            headers = headers = {'Content-Type': 'application/json'}
            data = {"key": "o1zrmHAF", "type": "v4"}
            response = requests.post('https://api.hostmonit.com/get_optimization_ip', json=data, headers=headers, timeout=timeout)
            if response.status_code == 200:
                optimization_ip_json = response.json()
                optimization_ips = []
                for provider in optimization_ip_json['info']:
                    for item in optimization_ip_json['info'][provider]:
                      optimization_ips.append(item['ip'])
                return optimization_ips
            else:
                print("CHANGE OPTIMIZATION IP ERROR: REQUEST STATUS CODE IS NOT 200")
                return []
        except Exception as e:
            traceback.print_exc()
            print(f"get_optimization_ip Request failed (attempt {attempt + 1}/{max_retries}): {e}")
    return []

def get_iptop_ip(timeout=5, max_retries=3):
    for attempt in range(max_retries):
        try:
            # 发送 GET 请求，设置超时
            response = requests.get('https://ip.164746.xyz/ipTop.html', timeout=timeout)
            # 检查响应状态码
            iptop_src = response.text
            iptop_ips = iptop_src.split(',')
            return iptop_ips
        except Exception as e:
            traceback.print_exc()
            print(f"get_cf_speed_test_ip Request failed (attempt {attempt + 1}/{max_retries}): {e}")
    # 如果所有尝试都失败，返回 None 或者抛出异常，根据需要进行处理
    return []

def get_besfcf_ip(timeout=5, max_retries=3):
    for attempt in range(max_retries):
        try:
            # 发送 GET 请求，设置超时
            response = requests.get('https://ipdb.api.030101.xyz/?type=bestcf', timeout=timeout)
            # 检查响应状态码
            besfcf_src = response.text
            besfcf_ips = besfcf_src.split()
            return besfcf_ips
        except Exception as e:
            traceback.print_exc()
            print(f"get_cf_speed_test_ip Request failed (attempt {attempt + 1}/{max_retries}): {e}")
    # 如果所有尝试都失败，返回 None 或者抛出异常，根据需要进行处理
    return []
#
if __name__ == '__main__':
    cfips = get_optimization_ip()
    if cfips != []:
        print('cfips获取成功')
    else:
        print('cfips获取失败')
    iptop = get_iptop_ip()
    if iptop != []:
        print('iptop获取成功')
    else:
        print('iptop获取失败')
    bestcf = get_besfcf_ip()
    if bestcf != []:
        print('bestcf获取成功')
    else:
        print('bestcf获取失败')
    sum_ip_set = set(cfips + iptop + bestcf)
    sum_ip = list(sum_ip_set)

    with open('../../sum_ip.txt', 'w') as file:
        # 遍历列表，写入每个IP地址，每个地址后面添加换行符
        for ip in sum_ip:
            file.write(ip + '\n')
    print('完成写入sum_ip.txt')
