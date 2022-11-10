import sys
import os
import re
import subprocess
from argparse import ArgumentParser

pending_commits = []
params = {}

merged_commits = []
unchanged_commits = []
aborted_commits = []


class Merge():
    def print_list(list, prefix="", appendix="", idx_start=1):
        idx = idx_start
        for i in list:
            print(idx, "|", prefix, i, appendix)
            idx += 1

    def get_status_output(cmd, print_cmd=True, print_output=True):
        if print_cmd:
            print("output> " + cmd)

        p = subprocess.Popen(cmd, bufsize=4096, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (std_output, err_output) = p.communicate()

        if print_output:
            str_len = 500
            print(std_output[0:str_len])

        return std_output

    def process_arguments(argv):
        parser = ArgumentParser()
        parser.add_argument("--file", required=True, nargs=1, dest="file_path")
        parser.add_argument("--git_dir", required=True, nargs=1, dest="git_dir")
        parser.add_argument("--added", action='store_true', dest="added")

        args = parser.parse_args(argv[1:])

        params['file_path'] = args.file_path[0]
        params['git_dir'] = args.git_dir[0]
        params['added'] = args.added

    def scan_diff_file(file_path, call_back):
        commit_msg_fd = open(file_path, "rw")
        lines = commit_msg_fd.readlines()

        start_process = False

        for line_str in lines:
            if line_str.startswith("project"):
                if params['git_dir'] in line_str:
                    print(line_str)
                    start_process = True
                else:
                    start_process = False

            if start_process:
                call_back(line_str)

        commit_msg_fd.close()

    def line_call_back(line_str):
        if (params['added'] and line_str.startswith(">")) or (not params['added'] and line_str.startswith("<")):
            hash = get_hash(line_str)
            if not is_empty_commit(hash):
                pending_commits.append(hash)

    def get_hash(line_str):
        direction = '<'
        if params['added']:
            direction = '>'
        pattern = re.compile(direction + " \|\| (.*) \|\|")
        result = pattern.search(line_str)
        if result is not None:
            c = result.groups()
            hash = str(c[0]).strip()
            return hash

    def is_empty_commit(hash):
        print('-' * 75)
        result = get_status_output("git log -1 --oneline --stat " + hash, False, True)
        return "file changed" not in result

    def scan_pending_commits(call_back):
        pending_commits.reverse()
        print_list(pending_commits)
        print()
        print("=" * 75)

        for c in pending_commits:
            call_back(c)

    def cherry_pick_call_back(hash):
        result = get_status_output("git cherry-pick " + hash, True, False)
        if not result:
            get_status_output("git cherry-pick --abort")
            aborted_commits.append(hash)
        elif "nothing to commit" in result:
            get_status_output("git cherry-pick --abort")
            unchanged_commits.append(hash)
        else:
            merged_commits.append(hash)

        print(result)

    if __name__ == '__main__':
        os.system("git reset --hard zsgit/zsui_n")
        process_arguments(sys.argv)

        # get all valid commit from diff file
        scan_diff_file(params['file_path'], line_call_back)

        # cherry-pick each commits in pending_commits
        scan_pending_commits(cherry_pick_call_back)

        check_box = '<ul class="inline-task-list"><li data-inline-task-id=""><br data-mce-bogus="1"></li></ul>'

        print("=" * 75)
        print("id|hash|owner|merged to mp|merged to stable")
        print("-|-|-|-|-")
        print_list(merged_commits, "", "|| " + check_box + " | " + check_box)

        print_list(aborted_commits, "[*]", "|| " + check_box + " | " + check_box, len(merged_commits) + 1)

        print
        print("```")
        print("ignored commits")
        print_list(unchanged_commits)
        print("```")
