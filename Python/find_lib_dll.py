# 找出 Windows 中 libXXX.dll 文件

import os
import sys


def walk_lib_dll(dirs):
    for dir in dirs:
        for paths,dirnames,filenames in os.walk(dir):
            for file in filenames:
                if file.lower().startswith('lib') and \
                        file.lower().endswith('.dll'):
                    yield os.path.join(paths,file), file


def find_lib_dll(dirs):
    results = dict()
    for path, file in walk_lib_dll(dirs):
        if file not in results:
            sys.stderr.write(f'find new lib {file}\n')
            sys.stderr.flush()
            results[file] = set()
        results[file].add(path)
    return results


def statistics(results):
    l = list()
    for key in results:
        l.append((key, len(results[key])))
    s = sorted(l, key=lambda lib: lib[1], reverse=True)
    for lib in s:
        print(f'{lib[1]}\t{lib[0]}')


if __name__ == '__main__':
    results = find_lib_dll(['C:\\Program Files', 'C:\\Program Files (x86)'])
    statistics(results)
