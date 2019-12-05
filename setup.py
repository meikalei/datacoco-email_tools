import os
import re
from setuptools import setup, find_packages

requires = ["boto3==1.10.28"]


def get_version():
    version_file = open(os.path.join("datacoco_email_tools", "__version__.py"))
    version_contents = version_file.read()
    return re.search('__version__ = "(.*?)"', version_contents).group(1)


setup(
    name="datacoco-email_tools",
    packages=find_packages(exclude=["tests*"]),
    version=get_version(),
    license="MIT",
    description="AWS Simple Email Service wrapper",
    long_description=open("README.rst").read(),
    author="Equinox Fitness",
    url="https://github.com/equinoxfitness/datacoco-email_tools",
    install_requires=requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
)
