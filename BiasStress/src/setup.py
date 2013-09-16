'''
Created on Sep 16, 2013

@author: adminssteudel
'''

from setuptools import setup
setup(
    name='BiasStress',
    version='0.0.1',
    author='Incalza Dario',
    author_email='dario.incalza@gmail.com',
    packages=['be.imec.biasstress.hardware','be.imec.biasstress.models','be.imec.biasstress','be.imec.biasstress.views','be.imec.biasstress.util'],
    install_requires=['settings.xml'],
    classifiers=['Development Status :: 3 - Alpha'],
)