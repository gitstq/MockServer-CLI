#!/usr/bin/env python3
"""Setup script for MockServer-CLI."""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

setup(
    name="mockserver-cli",
    version="1.0.0",
    author="MockServer-CLI Team",
    author_email="mockserver@example.com",
    description="Lightweight Terminal HTTP API Mock Server - Zero-dependency CLI tool",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/MockServer-CLI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing :: Mocking",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "mockserver=mockserver_cli.mockserver:main",
            "mockserver-cli=mockserver_cli.mockserver:main",
        ],
    },
    keywords="mock server api http cli testing development zero-dependency",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/MockServer-CLI/issues",
        "Source": "https://github.com/gitstq/MockServer-CLI",
    },
)
