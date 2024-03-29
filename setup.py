from bboard_downloader import __title__, __author__, __email__, __url__, __version__

import setuptools

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    required = f.readlines()

setuptools.setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="Recording downloader for Blackboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__url__,
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    setup_requires=['wheel'],
    install_requires=required,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        'console_scripts': [
            'bboard=bboard_downloader.bboard_downloader:main'
        ]
    }
)
