from setuptools import setup

setup(
    name='app',
    packages=['app'],
    include_package_data=True,
    requires=['flask', 'flask-sqlalchemy']
)
