import subprocess
import shlex

from src.util.helper_log import Log
from src.util.wrapper_thread import ThreadWrapper

_ = (Log)


class AbsTerminal(object):
    def __init__(self):
        raise RuntimeError('abstract class Can not be instanted!')

    def runCmd(self, cmdStr, stdoutListner=None, stderrListner=None):
        Log.d("runCmd:", cmdStr)
        process = subprocess.Popen(shlex.split(cmdStr), bufsize=4096, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        t1 = ThreadWrapper("thread-stdout", self.handleStdout, process.stdout, stdoutListner)
        t2 = ThreadWrapper("thread-stderr", self.handleStderr, process.stderr, stderrListner)
        t1.start()
        t2.start()

        t1.join()
        t2.join()

        return process.poll()

    def handleStdout(self, params):
        reader = params[0]
        listener = params[1]
        while True:
            if len(reader.peek()) <= 0:
                break
            line = reader.readline().decode(encoding="utf-8", errors="strict").strip()
            if listener is not None:
                listener(line)
            else:
                Log.v(line)
        return

    def handleStderr(self, params):
        reader = params[0]
        listener = params[1]
        while True:
            if len(reader.peek()) <= 0:
                break
            line = reader.readline().decode(encoding="utf-8", errors="strict").strip()
            if listener is not None:
                listener(line)
            else:
                Log.w(line)
        return
