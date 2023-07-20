from setuptools import setup

setup(
   name='TestInstruments',
   version='1.0',
   description='A useful module to control lab instruments',
   author='Cesar Carrillo',
   author_email='crcg1995@hotmail.com',
   packages=['Generators','Indicators'],
   install_requires=['numpy','pyvisa'],
)
