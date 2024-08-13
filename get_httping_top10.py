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
    filename = "httping.txt"  # 设置文件路径
    encoding = 'utf-8'  # 根据你的文件编码设置
    ips = parse_ips(filename)
    if ips:
        sorted_ips = sort_ips_by_speed(ips)
        iplist = select_top10_ips(sorted_ips)
        return set(iplist)
    else:
        print("没有有效的IP数据可以处理。")
        return None

# 将当前DNS解析结果也加进来
import socket

def get_now_ip(domain):
    try:
        # 获取所有地址信息列表
        now_ip_dns = socket.getaddrinfo(domain, None)
        # 使用集合来存储解析到的IP地址，自动去重
        now_ips_set = set()

        # 解析地址信息，提取IP地址，并添加到集合中
        for addr in now_ip_dns:
            af, socktype, proto, canonname, sa = addr
            ip = sa[0]  # 获取IP地址
            now_ips_set.add(ip)

        # 打印当前解析的IP地址
        print(f"当前{domain}的解析地址为: {now_ips_set}")

        # 将集合转换为列表（如果需要的话），并返回
        return set(now_ips_set)

    except Exception as e:
        # 打印错误信息，并返回空列表
        print(f"解析发生错误：{e}")
        return set()



if __name__ == '__main__':
    top10ips = get_fast_ip()
    now_ips = get_now_ip('cf-best.sino-v.xyz')
    now_ips2nd = get_now_ip('cf-best2nd.sino-v.xyz')
    # 当前DNS的2个IP与top10的10个IP合并，去重后并写入文件
    top10_now_ips_set = top10ips | now_ips | now_ips2nd
    top10_now_ips = list(top10_now_ips_set)
    with open('httping_top10.txt', 'w') as file:
        # 遍历列表，写入每个IP地址，每个地址后面添加换行符
        for ip in top10_now_ips:
            file.write(ip + '\n')
    print('完成写入httping_top10.txt')