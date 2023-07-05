from setuptools import setup

setup(
   name='TestInstruments',
   version='0.03',
   description='A useful module to simulate behavior of lab instruments',
   author='Cesar Carrillo',
   author_email='crcg1995@hotmail.com',
   packages=['Generators','Indicators'],  #same as name
   install_requires=['numpy','pyvisa'], #external packages as dependencies
)
