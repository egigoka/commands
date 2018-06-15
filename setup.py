from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='commands',
    version='9.0.0-alpha38',
    description='Mine commands',
    license="MIT",
    long_description=long_description,
    author='Egor Egorov',
    author_email='egigoka@gmail.com',
    url="https://www.github.com/egigoka/commands",
    packages=['commands'],  # same as name
    install_requires=[
        'termcolor',
        'copypaste',
        'paramiko'],
    extras_require={
        ':platform_system!="Linux"': ['pyautogui'],
        ':platform_system=="Windows"': ['pywin32', 'colorama'],
        ':python_version < "3.6" and platform_system=="Windows"': ['win_unicode_console'],
        }
    # scripts=[
    #         'scripts/cool',
    #         'scripts/skype',
    #        ]
)
