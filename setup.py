from setuptools import setup, find_packages
import os

# Read the contents of README.md file
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="i18n-checker",
    version="0.1.0",
    description="A tool for detecting unused and missing localization keys across multiple programming languages and frameworks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="i18n-checker Team",
    author_email="example@example.com",
    url="https://github.com/yourusername/i18n-checker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Internationalization",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "i18n-checker=i18n_checker.cli:main",
        ],
    },
) 