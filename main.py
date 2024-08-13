import socket

# 域名
domain = 'cf-best.sino-v.xyz'

try:
    # 获取所有地址信息列表
    addresses = socket.getaddrinfo(domain, None)

    # 准备存储解析到的IP地址列表
    ip_addresses = []

    # 解析地址信息
    for addr in addresses:
        af, socktype, proto, canonname, sa = addr
        ip = sa[0]  # 获取IP地址
        ip_addresses.append(ip)

    print(f"当前{domain}的解析地址为{ip_addresses} ")

except socket.gaierror as e:
    print(f"无法解析域名: {e}")