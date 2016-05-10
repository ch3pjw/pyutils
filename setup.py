from setuptools import setup

setup(
    name='pyutils',
    description=(
        'Some basic utility functions abstracted out for re-use across '
        'projects.'),
    author='Paul Weaver',
    author_email='paul@ruthorn.co.uk',
    version='0.01',
    packages=['pyutils'],
    install_requires=[],
    extras_require={
        'dev': [
            'coverage',
            'pytest',
        ]
    },
)
