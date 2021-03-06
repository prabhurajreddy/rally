# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pkg_resources
import re

from esrally import paths
from esrally.utils import git, io

__version__ = pkg_resources.require("esrally")[0].version

__RALLY_VERSION_PATTERN = re.compile(r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:.(.+))?$")


def version():
    """
    :return: The release version string and an optional suffix for the current git revision if Rally is installed in development mode.
    """
    release = __version__
    # noinspection PyBroadException
    try:
        if git.is_working_copy(io.normalize_path("%s/.." % paths.rally_root())):
            revision = git.head_revision(paths.rally_root())
            return "%s (git revision: %s)" % (release, revision.strip())
    except BaseException:
        pass
    # cannot determine head revision so user has probably installed Rally via pip instead of git clone
    return release


def release_version():
    """
    :return: The release version string split into its components: major, minor, patch and optional suffix.
    """

    matches = __RALLY_VERSION_PATTERN.match(__version__)
    if matches.start(4) > 0:
        return int(matches.group(1)), int(matches.group(2)), int(matches.group(3)), matches.group(4)
    elif matches.start(3) > 0:
        return int(matches.group(1)), int(matches.group(2)), int(matches.group(3)), None
