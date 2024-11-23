import random
import ipaddress

def read_subnets_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def generate_random_ip(subnet):
    # 创建IP网络对象
    network = ipaddress.ip_network(subnet, strict=False)
    # 转换为IP地址列表
    ips = list(network.hosts())
    # 随机选择一个IP地址
    return random.choice(ips)

def generate_ips_from_subnets(subnets, count):
    # 如果count不超过子网列表的数量，直接随机选择子网
    if count <= len(subnets):
        selected_subnets = random.sample(subnets, count)
    else:
        # 如果count超过子网列表的数量，循环随机选择子网
        selected_subnets = random.choices(subnets, k=count)
    # 从每个子网中随机挑选一个IP地址
    random_ips = [generate_random_ip(subnet) for subnet in selected_subnets]
    return random_ips

# 从文件中读取子网列表
subnets = read_subnets_from_file('../../hk_cidr_best.txt')
print(subnets)
# 指定需要的IP数量
count = 10

# 生成随机IP地址
random_ips = generate_ips_from_subnets(subnets, count)
print(random_ips)
# 打印结果
with open('../../sum_ip.txt', 'w') as file:
    # 遍历列表，写入每个IP地址，每个地址后面添加换行符
        for ip in random_ips:
            print(ip)
            file.write(str(ip) + '\n')
print('完成写入sum_ip.txt')