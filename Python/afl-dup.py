# -*- coding: UTF-8 –*- 
import os
import re
import shutil
import argparse
import subprocess


def read_cmdline(cmdlien_file_path):
    args = list()
    with open(cmdlien_file_path, 'r') as f:
        for line in f.readlines():
            args.append(line.rstrip('\n'))
    return args


def analyse_core(core_path, exe_path):
    out_bytes = subprocess.check_output(['gdb', '-ex', 'bt', '-ex', 'quit', '-c', core_path, exe_path], shell=False)
    stack = list()
    flag = 0
    p = re.compile('0x[0-9a-f]+')
    for line in out_bytes.decode('utf-8').split('\n'):
        if line.startswith('#0'):
            flag += 1
        if flag >= 2:
            stack.append(p.sub('0xXXXX', line))
    return '\n'.join(stack)


def save_results(results, crashes_dir, out_dir, ext):
    readme = '# Duplicated crashes\n\n\n'
    for stack in results:
        filename = results[stack]
        shutil.copyfile(os.path.join(crashes_dir, filename), os.path.join(out_dir, filename+ext))
        readme += '## {}\n\nfilename: `{}`\n\nstack: \n\n```\n{}```\n\n\n'.format(filename[3:9], filename, stack)
    with open(os.path.join(out_dir, 'README.md'), 'w') as f:
        f.write(readme)


def main(in_dir, out_dir, ext):
    if os.path.exists(out_dir):
        print("directory {} already exists".format(out_dir))
        exit(-1)
    os.mkdir(out_dir)
    tmp_path = os.path.join(out_dir, 'tmp')
    os.mkdir(tmp_path)
    core_path = os.path.join(tmp_path, 'core')
    if ext is None:
        ext = ''
    else:
        ext = '.' + ext
    fuzz = 'default'    # TODO
    args = read_cmdline(os.path.join(in_dir, fuzz, 'cmdline'))
    crashes_dir = os.path.join(in_dir, fuzz, 'crashes')
    results = dict()
    for filename in os.listdir(crashes_dir):
        if filename == 'README.txt':
            continue
        target_file = os.path.join(tmp_path, filename+ext)
        shutil.copyfile(os.path.join(crashes_dir, filename), target_file)
        args_tmp = list()
        for arg in args:
            args_tmp.append(arg.replace('@@', target_file))      
        subprocess.run(args_tmp, shell=False)
        stack = analyse_core(core_path, args_tmp[0])
        if stack not in results:
            results[stack] = filename
            print("Found new stack, case: {}\n{}".format(filename, stack))
    save_results(results, crashes_dir, out_dir, ext)
    shutil.rmtree(tmp_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='duplicate afl crash. Please execute `ulimit -c unlimited` first')
    parser.add_argument('-i', type=str, required=True, help='directory for fuzzer findings')
    parser.add_argument('-o', type=str, required=True, help='output directory for duplicate result')
    parser.add_argument('-e', type=str, required=False, help='file extension for the fuzz test input file (if needed)')
    args = parser.parse_args()
    main(args.i, args.o, args.e)
