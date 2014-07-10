'''
RemindMe
~~~~~~~~
A Command Line Application that reminds you of somethings you may end
up forgetting. Just add a `remindme` and in the future you could just
make RemindMe show you the content.

Licensed under the MIT License. For Open Source Initiative (OSI)

Contribute to the Project at https://github.com/GochoMugo/RemindMe/
'''

from distutils.core import setup
import remindme


setup(
    name="RemindMe",
    version=remindme.__version__,
    author="Gocho Mugo I",
    author_email="gochomugo.developer@gmail.com",
    url="https://gochomugo.github.io/RemindMe/",
    download_url="https://github.com/GochoMugo/RemindMe/zipball/master",
    description="Command Line Application for reminding you of somethings",
    keywords=["remind", "remember", "cli"],
    license="MIT",
    long_description=__doc__,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    packages=["remindme"],
    install_requires=[
        "colorama"
    ]
)
