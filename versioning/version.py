"""
Version numbering template.

This file is intended to be copied into a project and provide version information,
including git version values.  It is copied instead of used as a module to ensure
that projects can always run their setup.py with no external dependency.

The `major`, `minor`, and `bugfix` variables hold the respective parts
of the version number.  Basic usage is to copy this file into your package directory
alongside __init__.py.  Then use as follows::

  from package.version import version_object
  from package.version import __version__  # version_object.version

In addition to ``major``, ``minor``, ``bugfix``, and ``dev`` attributes, the object
``version_object`` has a number of useful attributes::

  version            Including git info if dev=True    0.5 or 0.5dev-r21-123acf1
  git_version        Always including git info         0.5dev-r21-123acf1
  semantic_version   Never including git info          0.5dev
  git_sha            Git 7-digit SHA tag               123acf1
  git_revs           Git revision count                21

See ``setup.py`` in the ``versioning`` package for an example of what needs to
be done there.  The key step is ``version_object.write_git_version_file()``
in order to create a package file ``git_version.py`` alongside ``version.py``
which retains the git information outside of the git repo.
"""

import os

############################
### SET THESE VALUES
############################
# Major, Minor, Bugfix, Dev
VERSION = (0, 1, None, False)


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
        self.version_dir = os.path.abspath(os.path.dirname(__file__))

    def _get_git_info(self):
        """
        Determines the number of revisions in this repository and returns "" if
        this is not possible.
        """
        try:
            # First try getting git version from ./git_version.py
            from . import git_version
            git_revs = git_version.revs
            git_sha = git_version.sha

        except:
            from subprocess import Popen, PIPE
            p = Popen(['git', 'rev-list', 'HEAD'], cwd=self.version_dir,
                      stdout=PIPE, stderr=PIPE, stdin=PIPE)
            stdout, stderr = p.communicate()

            if p.returncode == 0:
                revs = stdout.split('\n')
                git_revs, git_sha = len(revs), revs[0][:7]
            else:
                git_revs, git_sha = None, None

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
        Get the full version with git hashtag and release, e.g.
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
        git_version_filename = os.path.join(self.version_dir, 'git_version.py')
        git_revs = self.git_revs
        git_sha = self.git_sha
        with open(git_version_filename, 'w') as fh:
            fh.write('revs={!r}; sha={!r}'.format(git_revs, git_sha))


version_object = SemanticVersion(*VERSION)
__version__ = version_object.version
