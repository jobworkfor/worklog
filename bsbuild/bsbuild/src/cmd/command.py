#
# Copyright (C) 2008 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys


class Command(object):
    """Base class for any command line action in repo.
    """

    def __init__(self):
        return

    def init(self):
        return

    def execute(self, args):
        """Perform the action, after option parsing is complete.
        """
        raise NotImplementedError

    def usage(self):
        """Display usage and terminate.
        """
        self.OptionParser.print_usage()
        sys.exit(1)
