from setuptools import setup

__version__ = "undefined"  # if setup fails read it from _version.py and to please PyCharm
with open("README.md", 'r') as f:
    long_description = f.read()
exec(open('commands/_version.py').read())

setup(
    name='commands',
    version=__version__,
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
        'pyperclip',
        'paramiko',
        'chardet',
        'psutil'],
    extras_require={
        ':platform_system!="Linux"': ['pyautogui'],
        ':platform_system=="Windows"': ['pywin32', 'colorama', 'win10toast', 'pywinrm'],
        ':python_version < "3.6" and platform_system=="Windows"': ['win_unicode_console'],
        },
    include_package_data=True,
)
