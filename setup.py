from setuptools import setup

setup(
    name='Ichiko',
    version='0.5.1',
    author='Falaina',
    author_email='falaina@falaina.net',
    url='kaworu.falaina.net:ichiko',
    packages=['ichiko'],
    description='Personal Utilities',
    install_requires=[
        'six==1.2.0',
        'path.py>=2.4.1',
        'bitstring>=3.0.2'
    ]
)
