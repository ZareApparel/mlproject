from setuptools import find_packages, setup
from typing import List
# Setuptools is a python library that helps us "PACKAGE" our Python Project so that other can use it by just writing pip
# find_package is a module in this library through which we can find all our folders which have __init__.py file and those folders will be included in our final package
# setup is main function through which we will define our project's name, etc..
h='-e .'
def get_req(path_file:str) -> List[str]:

    '''
    this function will return list of requirements
    '''

    requirements=[]
    with open(path_file) as f:
        requirements=f.readlines()
        requirements= [r.replace('\n', '') for r in requirements]
        if h in requirements:
            requirements.remove(h)
    return requirements




setup(
    name='mlproject',
    version='0.0.1',
    author='Zare',
    author_email='sahibetakhtdilsoz@gmail.com',
    install_requires=get_req('requirements.txt')

)


