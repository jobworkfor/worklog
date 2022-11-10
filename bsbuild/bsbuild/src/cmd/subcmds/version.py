from __future__ import print_function

import sys

from src.core.cmd.command import Command


class Version(Command):
    wrapper_version = None
    wrapper_path = None

    common = False
    helpSummary = "Display the version of repo"
    helpUsage = """
%prog
"""

    def execute(self, args):
        rp = self.manifest.repoProject
        rem = rp.GetRemote(rp.remote.name)

        print('repo version %s' % rp.work_git.describe(HEAD))
        print('       (from %s)' % rem.url)

        if Version.wrapper_path is not None:
            print('repo launcher version %s' % Version.wrapper_version)
            print('       (from %s)' % Version.wrapper_path)

        print(git.version().strip())
        print('Python %s' % sys.version)
