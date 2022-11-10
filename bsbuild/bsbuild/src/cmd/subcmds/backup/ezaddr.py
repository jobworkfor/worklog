#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import re
import os
import argparse
import subprocess

# *******************
# dependent libraries
# *******************

"""
termcolor 1.1.0

ANSII Color formatting for output in terminal.
https://pypi.python.org/pypi/termcolor
"""
__ALL__ = ['colored', 'cprint']

VERSION = (1, 1, 0)

ATTRIBUTES = dict(
    list(zip([
        'bold',
        'dark',
        '',
        'underline',
        'blink',
        '',
        'reverse',
        'concealed'
    ],
        list(range(1, 9))
    ))
)
del ATTRIBUTES['']

HIGHLIGHTS = dict(
    list(zip([
        'on_grey',
        'on_red',
        'on_green',
        'on_yellow',
        'on_blue',
        'on_magenta',
        'on_cyan',
        'on_white'
    ],
        list(range(40, 48))
    ))
)

COLORS = dict(
    list(zip([
        'grey',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white',
    ],
        list(range(30, 38))
    ))
)

RESET = '\033[0m'


def colored(text, color=None, on_color=None, attrs=None):
    """Colorize text.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.

    Example:
        colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink'])
        colored('Hello, World!', 'green')
    """
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)

        if on_color is not None:
            text = fmt_str % (HIGHLIGHTS[on_color], text)

        if attrs is not None:
            for attr in attrs:
                text = fmt_str % (ATTRIBUTES[attr], text)

        text += RESET
    return text


def cprint(text, color=None, on_color=None, attrs=None, end='\n', **kwargs):
    """print(colorize text.
    It accepts arguments of print(function.
    """
    text = str(text)
    print((colored(text, color, on_color, attrs)), end=end, **kwargs)


# **********************************************************************************************************************

b = {
    "BANNER_STR": "ezaddr.py ver 0.5.1",
    "symbol_dir": "",
    "source_dir": None,
    "source_offset_line": 5,
    "debug": False,
}


def type_symbol_dir(string):
    if os.path.isdir(string):
        b["symbol_dir"] = string
    else:
        msg = "%r is not a invalid symbol directory!" % string
        raise argparse.ArgumentTypeError(msg)


def type_source_dir(string):
    if os.path.isdir(string):
        b["source_dir"] = string
    else:
        msg = "%r is not a invalid source directory!" % string
        raise argparse.ArgumentTypeError(msg)


def parse_arg(argv):
    parser = argparse.ArgumentParser(description=b['BANNER_STR'])
    parser.add_argument("symbol_dir", nargs='?', type=type_symbol_dir,
                        help="specify your symbol root directory.")
    parser.add_argument('--debug', action='store_true',
                        help="show debug infos.")
    parser.add_argument('-s', '--source', nargs=1, type=type_source_dir,
                        help="specify your source root directory if you need to show the code directly.")
    parser.add_argument('-o', '--offset', nargs=1, type=int, dest='offset_line',
                        help="specify the offset lines around the hitting code line.")

    args = parser.parse_args(argv)
    b["debug"] = args.debug

    if args.offset_line is not None:
        b["source_offset_line"] = args.offset_line[0]

    if b["debug"]:
        cprint("(debug)" + "-" * 75)
        cprint("(debug)symbol_dir: " + str(b["symbol_dir"]))
        cprint("(debug)source_dir: " + str(b["source_dir"]))
        cprint("(debug)source_offset_line: " + str(b["source_offset_line"]))
        cprint("(debug)" + "-" * 75)


def parse_stack(crash_line):
    trace_line = re.compile(
        # Random start stuff.
        ".*"

        # Frame number.
        "\#(?P<frame>[0-9]+)"

        # (space)pc(space).
        "[ \t]+..[ \t]+"

        # Offset (hex number given without 0x prefix).
        "(?P<offset>[0-9a-f]+?)[ \t]+"

        # Library name.
        "(?P<dso>\[[^\]]+\]|[^\r\n \t]*)"

        # function
        " \((.*)\)"
    )

    m = trace_line.match(crash_line)
    if m:
        frame = m.groups()[0]
        addr = m.groups()[1]
        so_path = m.groups()[2]
        fname = m.groups()[3]
        return frame, addr, so_path, fname

    return None, None, None, None


def get_hit_code(output):
    file_path = None
    line_no = None
    for line in output.split('\n'):
        rule = re.compile("(.*):([\d]*)( \(discriminator [\d]*\)|$|\n)")
        m = rule.match(line)
        if m:
            if b['debug']:
                print(m.groups())
            file_path = m.groups()[0]
            line_no = m.groups()[1]
    return file_path, line_no


def main():
    if len(sys.argv) <= 1:
        parse_arg(["--help"])
        exit(0)

    parse_arg(sys.argv[1:])

    cprint('================================')
    cprint(b['BANNER_STR'])
    cprint('')
    cprint("Paste your stack logs here and ")
    cprint("press ENTER(s) to run addr2line.")
    cprint('================================')

    text = sys.stdin.readline().strip()
    while len(text.strip()) <= 0:
        text = sys.stdin.readline().strip()

    stacks = []
    while len(text.strip()) > 0:
        stacks.append(text)
        text = sys.stdin.readline().strip()

    cprint('')
    cprint('=' * 75)
    cprint('parsing logs with addr2line...')
    cprint('=' * 75)
    cprint('')

    if b["debug"]:
        cprint("(debug)" + "-" * 75)
        for s in stacks:
            cprint("(debug) >>> " + str(s))
        cprint("(debug)" + "-" * 75)

    frame_stamp = 0
    for line in stacks:
        if not line.strip():
            continue

        frame, stack_addr, so_path, fname = parse_stack(line)

        if stack_addr is None:
            continue

        # print empty line among stacks
        if frame_stamp > int(frame):
            cprint('')
        frame_stamp = int(frame)

        # cprint('')
        cmd = 'addr2line -fCe ' + str(b["symbol_dir"]) + str(so_path) + ' ' + str(stack_addr)
        index_str = "#%s " % (frame)
        if b["debug"]:
            index_str = "#%s [%s]\n" % (frame, cmd)
        cprint(index_str, color='green', on_color='on_grey', end='')

        # os.system(cmd)
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=open(os.devnull, 'wb'), shell=True).communicate()
        # cprint('\n' + output[0][:-1], on_color='on_red')

        info = str(output[0])
        if len(info) == 0:
            cprint("<unknown>", color='yellow', end=' ')
            cprint(fname)
        else:
            infoArr = info.split("\n")
            cprint(infoArr[1], color='cyan', end='  ')
            cprint(infoArr[0])

        if len(info) == 0:
            continue

        source_path, source_line = get_hit_code(output[0])

        if source_path is not None and b['source_dir'] is not None:
            source_path = source_path.replace("/proc/self/cwd/", "")
            source_path = os.path.join(b['source_dir'], source_path)
            if os.path.isfile(source_path):
                cprint('-' * 75, 'white')

                from_line = int(source_line) - int(b['source_offset_line'])
                if from_line <= 0:
                    from_line = 1

                cmd = 'sed -n \'%d,%dp\' %s' % (int(from_line), int(source_line) - 1, source_path)

                output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
                cprint(output[0][:-1], 'white')

                cmd = 'sed -n \'%d,%dp\' %s' % (int(source_line), int(source_line), source_path)
                output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
                # cprint(output[0][:-1], on_color='on_green')
                cprint(output[0][:-1], 'yellow')

                to_line = int(source_line) + int(b['source_offset_line'])
                cmd = 'sed -n \'%d,%dp\' %s' % (int(source_line) + 1, to_line, source_path)
                output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
                cprint(output[0][:-1], 'white')


if __name__ == '__main__':
    main()
