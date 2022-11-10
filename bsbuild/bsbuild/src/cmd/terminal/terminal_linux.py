from src.util.helper_log import Log
from src.core.cmd.terminal.abstrace_terminal import AbsTerminal


class LinuxTerminal(AbsTerminal):
    def __init__(self):
        return

    # def runCmd(self, cmdStr):
    #     Log.d("$ " + cmdStr)
    #     os.system(cmdStr)

    def get_status_output(self, cmd, print_cmd=True, print_output=True, exit_on_error=True):
        if print_cmd:
            ezlog.warning("output> " + cmd)

        p = subprocess.Popen(cmd, bufsize=4096, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (std_output, err_output) = p.communicate()

        if print_output:
            str_len = 500
            Log.d(std_output[0:str_len])
            Log.d(err_output[0:str_len])

        if err_output != "":
            if exit_on_error:
                from __common.Global import Global
                exit(Global.EXIT_CODE_ABNORMAL_SHELL)
            else:
                std_output += err_output

        return std_output
