from src.util.helper_log import Log

_ = (Log)


class CmdManager(object):
    def __init__(self):
        self.allCommands = []
        return

    def init(self, allCommands):
        self.allCommands = allCommands
        return

    def execute(self, args):
        if len(args) == 0:
            Log.e("CmdManager.execute(), args is empty.")
            return

        cmd = self.allCommands[args[0]]
        cmd.init()
        cmd.execute(args[1:])
        return
