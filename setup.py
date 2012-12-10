from setuptools import setup

setup(
    name='Ichiko',
    version='0.6.0',
    author='Falaina',
    author_email='falaina@falaina.net',
    url='http://github.com/Falaina/ichiko',
    packages=['ichiko'],
    description='Personal Utilities',
    install_requires=[
        'six==1.2.0',
        'path.py>=2.4.1',
        'bitstring>=3.0.2'
    ]
)
