## 题目

一、题意
- 使用任一开发语言调用 pcre2 (源码地址：https://github.com/PhilipHazel/pcre2)  ，必须亲自动手使用 FFI 绑定 C 接口，不得使用现成的三方库
- 从 **目标文本** 中筛选出符合 **筛选规则** 的 **结果字符串**，
- 将 **结果字符串** 发送给一个 bash 脚本，
- 在这个 bash 脚本中接收并打印接收到的结果，
- 转输过程中要求使用 UDP 协议。

二、目标文本

"a;jhgoqoghqoj0329 u0tyu10hg0h9Y0Y9827342482y(Y0y(G)_)lajf;lqjfgqhgpqjopjqa=)*(^!@#$%^&*())9999999"

三、筛选规则

1. **结果字符串** 自身不包含数字和任何类型的空白字符（如空格、回车等等），其长度为 3 至 11 个字符
2. **结果字符串** 左侧相邻的字符串是4个数字
3. **结果字符串** 右侧相邻的字符串不为空
4. 正则匹配的次数越少越好，尽可能只使用一个正则表达式

注：以上 4 条规则须同时满足。

## 实现语言（python）
```python
#FFI部分代码（详情见ffi.py文件）
def pcre2_match(self, code, subject, match_data):
    subject_bytes = subject.encode("utf-8")
    subject_ptr = (ctypes.c_ubyte * len(subject_bytes))(*subject_bytes)
    result = self.lib.pcre2_match_8(
        code, subject_ptr, len(subject_bytes), 0, 0, match_data, None)
    return result

# 调用封装pcre2_regex.py（部分）
def find_all_matches(self, subject):
    matches = []
    offset = 0
    subject_len = len(subject)
    while offset < subject_len:
        match_data = self.ffi.pcre2_match_data_create(self.code)
        result = self.ffi.pcre2_match(self.code, subject[offset:], match_data)
        if result > 0:
            ovector = self.ffi.pcre2_get_ovector_pointer(match_data)
            start = ovector[0]
            end = ovector[1]
            match_str = subject[offset + start:offset + end]
            matches.append(match_str)
            offset += end
        else:
            break
        self.ffi.pcre2_match_data_free(match_data)
    return matches
```
## 使用方式
### 1. 安装pcre2(推荐方式)
- 在 Ubuntu 或 Debian 上安装 PCRE2
    可以使用以下命令在 Ubuntu 或 Debian 系统上安装 PCRE2：
    ```bash
    sudo apt-get update
    sudo apt-get install libpcre2-dev
    ```
- 在 CentOS 或 RHEL 上安装 PCRE2
    可以使用以下命令在 CentOS 或 RHEL 系统上安装 PCRE2：
    ```
    sudo yum install pcre2-devel
    ```
- 在 macOS 上安装 PCRE2
    可以使用 Homebrew 在 macOS 上安装 PCRE2。首先安装 Homebrew，然后运行以下命令：
    ```
    brew install pcre2 
    ```
- 在 Windows 上安装 PCRE2

    在 Windows 上安装 PCRE2 可以通过下载预编译的二进制文件来完成。您可以从 PCRE2 官方网站下载 Windows 版本的安装包，然后按照说明进行安装。通常情况下，您只需下载并解压缩文件，然后将其路径添加到系统的 PATH 环境变量中即可。
### 2. 安装python3
- 在 Ubuntu 或 Debian 上安装 Python 3：
    ```
    sudo apt-get update
    sudo apt-get install python3
    ```
- 在 CentOS 或 RHEL 上安装 Python 3：
    ```
    sudo yum install python3
    ```
- 在 macOS 上安装 Python 3：
- 使用 pyenv
    pyenv 是一个 Python 版本管理工具，可以方便地安装和管理多个 Python 版本。

- 在 macOS 上安装 pyenv：
    使用 Homebrew 安装 pyenv：
    ```
    brew install pyenv
    ```
### 3. 下载源码
    git clone https://github.com/kai648846760/ffi_test-python-.git
### 4. 授权脚本 & 执行
    chmod +x receive.sh && ./receive.sh
### 5. 执行python脚本
    python3 ./main.py

## 执行结果
python
```
Found matches:
y(Y
```
bash
```
Listening on UDP port 12345
y(Y
```
