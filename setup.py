'''
Setup script for RemindMe
'''

from setuptools import setup
import remindme


def get_requirements():
    '''Return a list of requirements for installation as listed in the
    requirements.txt file'''
    with open("requirements.txt", "r") as reqsFile:
      reqs = reqsFile.read()
      return reqs.strip().split("\n")


setup(
    name="remindme",
    version=remindme.__version__,
    author="Gocho Mugo I",
    author_email="mugo@forfuture.co.ke",
    url="https://github.com/GochoMugo/remindme",
    download_url="https://github.com/GochoMugo/remindme/zipball/master",
    description="Command Line Application for reminding you of something",
    keywords=["remindme", "remind", "remember", "cli"],
    license="MIT",
    long_description=remindme.__doc__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4"
    ],
    packages=["remindme"],
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'remindme = remindme.cli:run',
        ]
    }
)
