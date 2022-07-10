#!/usr/bin/env python3
# 通过检索 Linux 系统中的包来寻找适合的 fuzz 对象

import os
import re
import csv
import datetime


class Package:

    year_pattern = re.compile(r' ([12][90][89012]\d) ')   # 查找数字

    def __init__(self, name, count):
        self.name = name
        self.count = count

    def get_changelog(self):
        """
        输入包名，返回 changlog
        注意，本函数需联网
        """
        changelog = os.popen("apt changelog {}".format(self.name)).read()
        self.cve_count = changelog.count('CVE') + changelog.count('cve')
        years = Package.year_pattern.findall(changelog)
        self.year_count = len(years)
        years.sort()
        self.oldest_year = years[0]
        self.latest_year = years[-1]

    def get_status(self):
        """
        执行 dpkg-query -s 命令查询包信息
        """
        status = os.popen("dpkg-query -s {}".format(self.name)).read().split('\n')
        in_description = False
        for line in status:
            if line.startswith('Section: '):
                self.section = line[9:]
            elif line.startswith('Source: '):
                self.source = line[8:]
            elif line.startswith('Version: '):
                self.version = line[9:]
            elif line.startswith('Homepage: '):
                self.homepage = line[10:]
            elif line.startswith('Description: '):
                self.description = line[13:]
                in_description = True
                continue
            elif line.startswith(' .'):
                if in_description:
                    self.description += '\n'
                    continue
            elif line.startswith(' '):
                if in_description:
                    self.description += line[1:]
                    continue
            in_description = False

    def save_to_csv(self, dict_writer):
        """
        将包信息保存到 csv 文件
        """
        dict_writer.writerow(vars(self))


def filename2pkg(filename):
    """
    输入文件名，返回文件所属的包
    若找不到对应的包，将返回空字符串，并输出错误信息到 stderr
    """
    return os.popen("dpkg-query -S {} | head -n 1 | cut -d ':' -f 1".format(filename)).read().split('\n')[0]


def parse_sort_rn(data):
    """
    处理 sort -rn 命令的输出
    """
    results = list()
    for line in data.split('\n'):
        line = line.strip().split(' ')
        if len(line) < 2:
            continue
        count = int(line[0])
        item = line[1]
        results.append((item, count))
    return results


def list_lib_link(directory):
    """
    执行 bash 命令，列出当前主机上不同的动态链接库的引用频率，按从高到低保存到文件中
    """
    print("[+] start list_lib_link_count")
    data = os.popen("find {}/ -perm /u+x -type f 2>/dev/null | xargs ldd 2>/dev/null | grep \"=>\" | awk '{{print \"basename \"$3}}' | sh | sort | uniq -c | sort -rn".format(directory)).read()
    print("[+] finish list_lib_link_count")
    return parse_sort_rn(data)


def list_suid_files(directory):
    """
    执行 bash 命令，列出当前主机上所有设置了 suid 标志位的可执行文件
    """
    print("[+] start list_suid_files")
    data = os.popen("find {} -user root -perm -4000 -type f 2>/dev/null | awk '{{print \"basename \"$1}}' | sh | sort | uniq -c | sort -rn".format(directory)).read()
    print("[+] finish list_suid_files")
    return parse_sort_rn(data)


def file2pkg(file_count_tuples):
    """
    查出文件所属的包
    """
    print("[+] start file2pkg")
    results = dict()
    for filename, count in file_count_tuples:
        pkg = filename2pkg(filename)
        if pkg == '':
            continue
        if pkg not in results:
            results[pkg] = 0
        results[pkg] += count
    print("[+] finish file2pkg, total {}".format(len(results)))   
    return results


if __name__ == '__main__':
    directory = "/"
    
    # results = list_lib_link(directory)
    results = list_suid_files(directory)
    
    results = file2pkg(results)

    i = 1
    with open("results.csv", 'w', newline="") as csvfile:
        for pkg in results:
            print("[+][{}] now to query {} infomation".format(i, pkg))
            p = Package(pkg, results[pkg])
            p.get_status()
            p.get_changelog()
            if i == 1:
                writer = csv.DictWriter(csvfile, fieldnames = list(vars(p).keys()))
                writer.writeheader()
            p.save_to_csv(writer)
            i = i + 1
