#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

exec(open("fishsound_finder/_version.py").read())

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


# automatically captured required modules for install_requires in requirements.txt
with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().split('\n')

setup_requirements = [ ]

test_requirements = [ ]

setup(
    name="fishsound_finder", # Replace with your own username
    version=__version__,
	author="Xavier Mouy",
    author_email="xaviermouy@uvic.ca",
    description="Python software to automatically detect fish sounds in passive acoustic recordings",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/x-rst",
    include_package_data=True,
	keywords='fish sounds',
	url="https://github.com/xaviermouy/FishSound_Finder",
    packages=find_packages(include=['fishsound_finder', 'fishsound_finder.*'],exclude=['docs']),
    #package_data={"/resources": ["/resources/67674121.181017060806.wav","/resources/config.yaml","/resources/deployment_info.csv","/resources/RF50_model.sav"], "": ["README.md","LICENSE"]},
    install_requires=requirements,
	setup_requires=setup_requirements,
    #entry_points={'console_scripts': ['fishsound_finder=fish-sound-detector:main',]},    
    entry_points='''
        [console_scripts]
        fishsound_finder=fishsound_finder.detector:main
    ''',
    license="BSD license",
	classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License", 
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires='>=3.7.0,<3.8.0',
	zip_safe=False,
)