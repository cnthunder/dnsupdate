# 定义根据下载速度对IP数据进行排序的函数
def sort_ips_by_speed(ips):
    return sorted(ips, key=lambda x: x['平均延迟'], reverse=False)

# 定义选择下载速度最快的两个IP的函数
def select_top10_ips(sorted_ips):
    return [ip['IP 地址'] for ip in sorted_ips[:10]]

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
                ips.append(ip_info)
    except FileNotFoundError:
        print(f"文件 {filename} 未找到，请检查路径是否正确。")
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
    return ips

# 主函数
def get_fast_ip():
    filename = "/home/dnsupdate/httping.txt"  # 设置文件路径
    encoding = 'utf-8'  # 根据你的文件编码设置
    ips = parse_ips(filename)
    if ips:
        sorted_ips = sort_ips_by_speed(ips)
        iplist = select_top10_ips(sorted_ips)
        return iplist
    else:
        print("没有有效的IP数据可以处理。")
        return None

if __name__ == '__main__':
    top10ips = get_fast_ip()
    with open('/home/dnsupdate/httping_top10.txt', 'w') as file:
        # 遍历列表，写入每个IP地址，每个地址后面添加换行符
        for ip in top10ips:
            file.write(ip + '\n')