from setuptools import find_packages, setup

package_name = 'first_package'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Leonor Guedes',
    maintainer_email='leonorecaguedes@gmail.com',
    description='Introductory ROS 2 communication nodes: publishers, subscribers, services, and dynamic parameters.',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'simple_publisher_node = first_package.simple_publisher:main',
            'simple_subscriber_node = first_package.simple_subscriber:main',
            'simple_pubsub_node = first_package.simple_pubsub_node:main',
            'simple_service = first_package.simple_service:main',
            'simple_service_parameter = first_package.simple_service_parameter:main',
        ],
    },
)
