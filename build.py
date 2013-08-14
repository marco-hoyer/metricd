from pybuilder.core import use_plugin

use_plugin("python.install_dependencies")
use_plugin("copy_resources")
use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.pylint")
use_plugin("python.distutils")
default_task = "publish"
