from setuptools import setup
import setuptools

setup(
    name = 'license',
    version = '1.0',
    py_modules = ['Era'],
    install_requires = [
        'Click', 'Requests', 'BeautifulSoup', 'lxml'
    ],
    description = "A Command Line Interface which gives details of a user on giving their respective details.",
    entry_points = '''
                    [console_scripts]
                    Era = Era:cli
                    '''
)