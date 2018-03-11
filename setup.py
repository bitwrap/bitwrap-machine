from setuptools import setup, find_packages

setup(
    name="bitwrap-machine",
    version="0.3.0",
    author="Matthew York",
    author_email="myork@stackdump.com",
    description="Petri-Net State Machines",
    license='MIT',
    keywords='PNML petri-net state-machine bitwrap',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    long_description="""
Bitwrap-machine provides a means of loading PNML documents as P/T net state machines.
""",
    url="http://getbitwrap.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Database :: Database Engines/Servers",
        "License :: OSI Approved :: MIT License"
    ],
)
