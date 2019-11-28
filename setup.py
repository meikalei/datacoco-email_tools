from setuptools import setup, find_packages

from datacoco_email_tools import VERSION

requires = ["boto3==1.10.28"]

setup(
    name="datacoco-email_tools",
    packages=find_packages(exclude=["tests*"]),
    version=VERSION,
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
