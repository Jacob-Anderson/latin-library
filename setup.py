from setuptools import setup, find_packages

setup(
    name='latin-library',
    version='1.0',
    description='''Parse, index, and create a search/translation interface 
                   for a collection of Latin text.''',
    long_description=open('README.md').read(),
    author='Jacob Anderson',
    author_email='jake.anderson.ou@gmail.com',
    url='https://github.com/Jacob-Anderson/latin-library',
    packages=find_packages(exclude=('tests', 'docs'))
)
