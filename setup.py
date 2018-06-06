from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='commands',
    version='9.0.0-alpha10',
    description='Mine commands',
    license="MIT",
    long_description=long_description,
    author='Egor Egorov',
    author_email='egigoka@gmail.com',
    # url="http://www.foopackage.com/",
    packages=['commands'],  # same as name
    install_requires=[
        # 'win_unicode_console;python_version<"3.6";platform_system=="Windows"',
        # 'pywin32;platform_system=="Windows"',
        # 'colorama;platform_system=="Windows"',
        'termcolor',
        'copypaste',
        'pyautogui',
        'paramiko'],
    extras_require={
        ':platform_system=="Windows"': ['pywin32', 'colorama'],
        ':python_version < "3.6" and platform_system=="Windows"': ['win_unicode_console'],
        }
    # scripts=[
    #         'scripts/cool',
    #         'scripts/skype',
    #        ]
)
