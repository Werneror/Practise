#!/usr/bin/env python3

import re
import os
import argparse
import subprocess


def match(pattern, string):
    result = re.search(pattern, string)
    if result:
        return result.group(1)
    else:
        raise RuntimeError(f'not match {pattern} in {string}')


class Crash:

    def __init__(self, cmd_template, crash_path):
        self.cmd_template = cmd_template
        self.crash_path = crash_path

    def run(self):
        result = subprocess.run(self.cmd_template.replace('@@', self.crash_path), shell=True, text=True, capture_output=True)
        self.returncode = result.returncode
        self.stderr = result.stderr
        self.stdout = result.stdout
        if self.returncode == 0:
            raise RuntimeError('return is 0, maybe not crash')
        if self.stderr is None:
            raise RuntimeError('stderr is none, maybe not crash')
        if 'AddressSanitizer' not in self.stderr:
            raise RuntimeError('AddressSanitizer not in stderr')

    def analysis_asan(self):
        asan_report = self.stderr.split('=================================================================', 1)[1]
        lines = asan_report.split('\n')
        if len(lines) < 4:
            raise RuntimeError('stderr is too short')
        if 'LeakSanitizer: detected memory leaks' in lines[1]:
            # ==3186345==ERROR: LeakSanitizer: detected memory leaks
            self.crash_name = 'memory-leaks'
            self.crash_type = ''
            self.crash_size = 0
        else:
            # ==15097==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffdbe404230 at pc 0x0000004d21b2 bp 0x7ffdbe403f30 sp 0x7ffdbe403f28
            self.crash_name = match(r'ERROR: AddressSanitizer: (.*?) on', lines[1])
            if 'of size' in lines[2]:
                # WRITE of size 1 at 0x7ffdbe404230 thread T0
                self.crash_type = lines[2].split(' ', 1)[0]
                self.crash_size = int(match(r'of size (.*?) at', lines[2]))
            else:
                self.crash_type = ''
                self.crash_size = 0
        #     #0 0x4d21b1 in get_key_value /home/kali/Code/afl-training/challenges/cyber-grand-challenge/CROMU_00007/src/timecard.c:381:16
        for line in lines[3:]:
            line = line.strip()
            if line.startswith('#') and 'BuildId' not in line:
                split = line.split(' ')
                self.func_name = split[3]
                self.code_location = split[4]
                # Sometimes the output is as follows. What we want is the second line.
                #     #0 0x557f58b4e7c6 in __interceptor_realloc (/root/libemf2svg/asan/emf2svg-conv+0xa47c6) (BuildId: c039a59088744a65db1e80eb05fb48085d6727b4)
                #     #1 0x7f6521069d17 in _IO_mem_finish libio/./libio/memstream.c:131:26
                if self.code_location.startswith('('):
                    continue
                break

    def __str__(self):
        ret = f'crash_name={self.crash_name}, '
        if self.crash_type:
            ret += f'type={self.crash_type}, '
        if self.crash_size:
            ret += f'size={self.crash_size}, '
        ret += f'func={self.func_name}, location={self.code_location}'
        return ret


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--command", help="bash command, @@ will be substituted for each crashfile", type=str)
    parser.add_argument("-d", "--directory", help="afl-fuzz output directory", type=str)
    args = parser.parse_args()

    crashes_pathes = list()
    for dir in os.listdir(args.directory):
        crashes_path = os.path.join(args.directory, dir, 'crashes')
        if os.path.isdir(crashes_path):
            crashes_pathes.append(crashes_path)

    crashes = dict()

    for crashes_path in crashes_pathes:
        for path in os.listdir(crashes_path):
            if not path.startswith('id'):
                    continue
            crash_path = os.path.join(crashes_path, path)
            print(f'[*]now to check {crash_path}')
            try:
                crash = Crash(args.command, crash_path)
                crash.run()
                crash.analysis_asan()
                key = crash.__str__()
                if key not in crashes:
                    crashes[key] = list()
                    print(f'[+]found now crash {key}')
                crashes[key].append(crash)
            except RuntimeError as err:
                print(f'[!]{err}')
                if str(err) == 'return is 0, maybe not crash':
                    if str(err) not in crashes:
                        crashes[str(err)] = list()
                    crashes[str(err)].append(crash)

    print('\n=================================================================\n')

    for key in crashes:
        print(f'{key}, count={len(crashes[key])}, crash_files=')
        for crash in crashes[key]:
            print(f'\t{crash.crash_path}')
