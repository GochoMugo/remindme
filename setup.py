'''
RemindMe
~~~~~~~~
A Command Line Application that reminds you of somethings you may end
up forgetting. Just add a `remindme` and in the future you could just
make RemindMe show you the content.

Licensed under the MIT License. For Open Source Initiative (OSI)

Contribute to the Project at https://github.com/GochoMugo/remindme
'''

from distutils.core import setup
import remindme


setup(
    name="remindme",
    version=remindme.__version__,
    author="Gocho Mugo I",
    author_email="gochomugo.developer@gmail.com",
    url="https://gochomugo.github.io/remindme/",
    download_url="https://github.com/GochoMugo/remindme/zipball/master",
    description="Command Line Application for reminding you of somethings",
    keywords=["remindme", "remind", "remember", "cli"],
    license="MIT",
    long_description=__doc__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4"
    ],
    packages=["remindme"],
    install_requires=[
        "argparse",
        "colorama"
    ],
    entry_points={
        'console_scripts': [
            'remindme = remindme.remindme:run',
        ]
    }
)
