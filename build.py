from pybuilder.core import use_plugin, init, Author

use_plugin("python.install_dependencies")
use_plugin("copy_resources")
use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.pylint")
use_plugin("python.distutils")

authors = [Author('Marco Hoyer', 'marco.hoyer@immobilienscout24.de')]
description = """metricd - a simple proxy sending perfdata offered by nagios or icinga to graphite

for more documentation, visit https://github.com/marco-hoyer/metricd
"""

name = 'metricd'
license = 'GNU GPL v3'
summary = 'metricd - perfdata proxy for Nagios/Icinga'
url = 'https://github.com/marco-hoyer/metricd'
version = '1.0'

default_task = ['publish']

@init
def initialize(project):
    
    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').append('setup.cfg')
    project.set_property('dir_dist_scripts', 'scripts')

    project.install_file('/etc/metricd/', 'metricd/metricd.conf.sample')
    project.install_file('/etc/init.d/', 'metricd/metricd')
    project.install_file('/etc/logrotate.d/', 'metricd/metricd-logrotate')


@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os

    project.version = '%s-%s' % (project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['install_dependencies', 'package']
    project.set_property('install_dependencies_use_mirrors', False)
    project.get_property('distutils_commands').append('bdist_rpm')
