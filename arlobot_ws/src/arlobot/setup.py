from setuptools import setup

package_name = 'arlobot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Arlo Team',
    maintainer_email='example@example.com',
    description='ROS 2 package for Arlo robot on Kria KV260',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motor_controller = arlobot.motor_controller:main',
            'encoder_logger = arlobot.encoder_logger:main',
            'odom_node = arlobot.odom_node:main',
        ],
    },
)
