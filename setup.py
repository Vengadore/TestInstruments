from setuptools import setup

setup(
   name='TestInstruments',
   version='0.02',
   description='A useful module to simulate behavior of lab instruments',
   author='Cesar Carrillo',
   author_email='crcg1995@hotmail.com',
   packages=['Generators','Indicators'],  #same as name
   install_requires=['numpy'], #external packages as dependencies
)
