from setuptools import find_packages, setup

package_name = 'f7_udp'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'listener = f7_udp.PS4_listener:main',
        '4_omni = f7_udp.W4_Omni_Driver:main',
        'setoshio = f7_udp.yolov8_setoshio_pub:main',
        'setoshio_gui = f7_udp.yolo_setoshio_gui:main',
        'cr24_main = f7_udp.cr24_main:main',
        'cr24_test = f7_udp.cr24_test:main',
        ],
    },
)
