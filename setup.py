from setuptools import setup

setup(
    name='cronhub',
    version='0.1',
    license="BSD",
    author="Tigran Hakobyan",
    author_email="tigran@cronhub.io",
    maintainer_email="tigran@cronhub.io",
    description="Cronhub command line interface toolkit",
    py_modules=['cronhub'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        cronhub=cronhub:cli
    ''',
)