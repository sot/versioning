"""
Version numbering. The `major`, `minor`, and `bugfix`
variables hold the respective parts of the version number (bugfix is '0' if
absent). The `release` variable is True if this is a release, and False if this
is a development version. For the actual version string, use::

    from mica import version

or::

    from mica import __version__

NOTE: this code copied from astropy and modified.  Any license restrictions
therein are applicable.
"""

import os
from os import path

VERSION = (0, 1, None, False)  # Major, Minor, Bugfix, Dev

GIT_VERSION_FILENAME = 'GIT_VERSION'


class SemanticVersion(object):
    def __init__(self, major=0, minor=None, bugfix=None, dev=False):
        """
        Semantic version object with support for git revisions

        :param major: Major version
        :param minor: Minor version
        :param bugfix: Bugfix version
        :param dev: True if this is a development version
        :param version_filename: File name for package version.py
        """
        self.major = major
        self.minor = minor
        self.bugfix = bugfix
        self.dev = dev
        self.version_dir = path.abspath(path.split(__file__)[0])

    def _get_git_info(self):
        """
        Determines the number of revisions in this repository and returns "" if
        this is not possible.
        """
        from subprocess import Popen, PIPE

        p = Popen(['git', 'rev-list', 'HEAD'], cwd=self.version_dir,
                  stdout=PIPE, stderr=PIPE, stdin=PIPE)
        stdout, stderr = p.communicate()

        if p.returncode != 0:
            if os.path.exists(self.git_version_filename):
                with open(self.git_version_filename, 'r') as fh:
                    git_revs, git_sha = fh.read().strip().split()
                    git_revs = int(git_revs)
            else:
                git_revs, git_sha = None, None
        else:
            revs = stdout.split('\n')
            git_revs, git_sha = len(revs), revs[0][:7]

        return git_revs, git_sha

    @property
    def git_revs(self):
        if not hasattr(self, '_git_revs'):
            self._git_revs, self._git_sha = self._get_git_info()
        return self._git_revs

    @property
    def git_sha(self):
        if not hasattr(self, '_git_sha'):
            self._git_revs, self._git_sha = self._get_git_info()
        return self._git_sha

    @property
    def git_version_filename(self):
        return path.join(self.version_dir, GIT_VERSION_FILENAME)

    @property
    def semantic_version(self):
        _version = '{}'.format(self.major)
        if self.minor is not None:
            _version += '.{}'.format(self.minor)
        if self.bugfix is not None:
            _version += '.{}'.format(self.bugfix)
        if self.dev:
            _version += 'dev'
        return _version

    @property
    def git_version(self):
        """
        Get the full version with git hashtag and release from GIT_VERSION, e.g.
        0.5dev-r190-423abc1
        """
        if not hasattr(self, '_git_version'):
            self._git_version = self.semantic_version
            if self.git_revs and self.git_sha:
                self._git_version += '-r{0}-{1}'.format(self.git_revs, self.git_sha)

        return self._git_version

    @property
    def version(self):
        return self.git_version if self.dev else self.semantic_version

    def write_git_version_file(self):
        """
        Make the full version with git hashtag and release from GIT_VERSION,
        typically during `python setup.py sdist`
        """
        with open(self.git_version_filename, 'w') as fh:
            fh.write('{} {}'.format(self.git_revs, self.git_sha))


version = SemanticVersion(*VERSION)
__version__ = version.version