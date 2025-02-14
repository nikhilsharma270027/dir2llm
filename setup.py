from setuptools import setup, find_packages

setup(
    name="dir2llm",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "dir2llm=dir2llm.cli:main",
        ],
    },
    author="Chandan H",
    author_email="chandanh.mailbox@gmail.com",
    description="A CLI tool to display directory structure and file contents",
    url="https://github.com/mr-chandan/dir2llm",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
