import socket
from pcre2_regex import Pcre2Regex


# 目标文本
target_text = "a;jhgoqoghqoj0329 u0tyu10hg0h9Y0Y9827342482y(Y0y(G)_)lajf;lqjfgqhgpqjopjqa=)*(^!@#$%^&*())9999999"

# 创建 PCRE2 正则表达式对象
regex = Pcre2Regex("(?<=\d{4})[^\s\d]{3,11}(?=[^\s])")

# 获取所有匹配结果
matches = regex.find_all_matches(target_text)

# 打印匹配结果
if matches:
    print("Found matches:")
    for match in matches:
        print(match)
else:
    print('No match found.')

# 创建 UDP 客户端
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 将匹配结果发送给 Bash 脚本
try:
    for match in matches:
        client_socket.sendto(match.encode(), ('127.0.0.1', 12345))
except Exception as e:
    print("Failed to send data:", e)
