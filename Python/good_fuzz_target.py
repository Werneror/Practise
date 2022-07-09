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


def lib2pkg(lib):
    """
    输入 libXXX.so 文件，返回文件所属的包
    若找不到对应的包，将返回空字符串，并输出错误信息到 stderr
    """
    return os.popen("dpkg-query -S {} | head -n 1 | cut -d ':' -f 1".format(lib)).read().split('\n')[0]


def list_lib_link_count(directory, path='/tmp/lib.count'):
    """
    执行 bash 命令，列出当前主机上不同的动态链接库的引用频率，按从高到低保存到文件中
    """
    print("[+] start list_lib_link_count")
    os.system("find {}/ -perm /u+x -type f 2>/dev/null | xargs ldd 2>/dev/null | grep \"=>\" | awk '{{print \"basename \"$3}}' | sh | sort | uniq -c | sort -rn > {}".format(directory, path))
    results = list()
    with open(path) as f:
        for line in f.readlines():
            line = line.strip().split(' ')
            count = int(line[0])
            lib = line[1]
            results.append((lib, count))
    print("[+] finish list_lib_link_count")
    return results


def list_pkg_frequency(lib_link_count):
    """
    查出 libXXX.so 所属的包
    """
    print("[+] start list_pkg_frequency")
    temp = dict()
    for lib, count in lib_link_count:
        pkg = lib2pkg(lib)
        if pkg == '':
            continue
        if pkg not in temp:
            temp[pkg] = 0
        temp[pkg] += count
    print("[+] finish list_pkg_frequency")
    results = list()
    for pkg in temp:
        print("[+] now to query {} infomation".format(pkg))
        p = Package(pkg, temp[pkg])
        p.get_status()
        p.get_changelog()
        results.append(p)
   
    return results


def save_pkgs(pkgs, path):
    if len(pkgs) == 0:
        return
    with open(path, 'w', newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = list(vars(pkgs[0]).keys()))
        writer.writeheader()
        for pkg in pkgs:
            writer.writerow(vars(pkg))


if __name__ == '__main__':
    directory = "/"
    pkgs = list_pkg_frequency(list_lib_link_count(directory))
    save_pkgs(pkgs, "results.csv")
