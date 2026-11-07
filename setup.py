from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'arm_vla'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your_email@example.com',
    description='ROS 2 package for VLA-based robotic arm control',
    license='MIT',
    entry_points={
        'console_scripts': [
            'observation_manager = arm_vla.observation_manager:main',
            'inference_node = arm_vla.inference_node:main',
        ],
    },
)