from setuptools import setup, find_packages
import os

setup(
    name="dir2llm",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "dir2llm=dir2llm.cli:main",  # This ensures the command is available globally
        ],
    },
    include_package_data=True,  # Add this to include non-Python files
    python_requires=">=3.6",
    author="Chandan H",
    author_email="chandanh.mailbox@gmail.com",
    description="A CLI tool to display directory structure and file contents",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/mr-chandan/dir2llm",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
)