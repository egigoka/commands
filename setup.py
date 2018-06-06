from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='commands',
   version='9.0.0-alpha2',
   description='Mine commands',
   license="MIT",
   long_description=long_description,
   author='Man Foo',
   author_email='egigoka@gmail.com',
   #url="http://www.foopackage.com/",
   packages=['commands'],  #same as name
   #install_requires=['bar', 'greek'], #external packages as dependencies
   #scripts=[
   #         'scripts/cool',
   #         'scripts/skype',
   #        ]
)
