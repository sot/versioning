from setuptools import setup

# from this_package.version import package_version object
from versioning.version import package_version

# Write GIT revisions and SHA tag into <this_package/git_version.py>
# (same directory as version.py)
package_version.write_git_version_file()

# DO NOT INSTALL the versioning package.  See README for usage.

setup(name='this_package',
      version=package_version.version,
      description='This package',
      author='Your name',
      author_email='your_email@cfa.harvard.edu',
      url='http://www.python.org/',
      packages=['versioning'],  # ['this_package']
      package_data={'versioning': ['GIT_VERSION']},  # {'this_package': ['GIT_VERSION']}
      )
