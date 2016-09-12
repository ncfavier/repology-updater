# Copyright (C) 2016 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import subprocess
import sys

from .common import RepositoryProcessor
from ..util import SplitPackageNameVersion

class PkgSrcPackagesSHA512Processor(RepositoryProcessor):
    src = None
    path = None

    def __init__(self, path, src):
        self.path = path
        self.src = src

    def IsUpToDate(self):
        return os.path.isfile(self.path)

    def Download(self):
        subprocess.check_call("wget -qO- %s | bunzip2 > %s" % (self.src, self.path), shell = True)

    @staticmethod
    def SanitizeVersion(version):
        match = re.match("(.*)nb[0-9]+", version)
        if not match is None:
            version = match.group(1)

        return version

    def Parse(self):
        result = []

        with open(self.path) as file:
            data = {}
            for line in file:
                pkgname = line[12:-137]

                if pkgname.find('-') == -1:
                    continue

                name, version = SplitPackageNameVersion(pkgname)

                result.append({
                    'name': name,
                    'version': self.SanitizeVersion(version),
                })

        return result
