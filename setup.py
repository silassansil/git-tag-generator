from setuptools import setup

setup(
    name="taggen",
    version='0.0.1',
    py_modules=['main'],
    install_requires=[
        'Click',
        'GitPython'
    ],
    entry_points='''
        [console_scripts]
        taggen=main:generate
    ''',
)
