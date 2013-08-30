from pybuilder.core import use_plugin, init, Author

use_plugin("python.install_dependencies")
#use_plugin("copy_resources")
use_plugin("python.core")
#use_plugin("python.unittest")
#use_plugin("python.coverage")
#use_plugin("python.pylint")
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

default_task = ['analyze', 'publish']

@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os
    project.version = '%s-%s' % (project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['install_build_dependencies', 'publish']
    project.set_property('install_dependencies_index_url', os.environ.get('PYPIPROXY_URL'))
    project.set_property('install_dependencies_use_mirrors', False)