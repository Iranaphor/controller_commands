from setuptools import setup
from glob import glob
import os

package_name = 'controller_commands'
pkg = package_name

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', [f'resource/{pkg}']),
        ('share/{pkg}', ['package.xml']),
        (f"share/{pkg}/config", glob(os.path.join('config', '*'))),
        (f"share/{pkg}/launch", glob(os.path.join('launch', '*launch.[pxy][yml]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='james',
    maintainer_email='primordia@live.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            f'joy_driver.py = {pkg}.joy_driver:main',
        ],
    },
)
