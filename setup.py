#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup module for the duallog package

This module configures setuptools so that it can create a distribution for the
package.
"""

# Import required standard libraries.
import io
import os
import setuptools

# Load the readme.
maindir = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(maindir, "README.md"), encoding="utf-8") as file:
    readme = file.read()

# Configure setuptools.
setuptools.setup(name="duallog_v2",
                 version="0.10",
                 description="Parallel logging to console and logfile",
                 long_description=readme,
                 long_description_content_type="text/markdown",
                 license="MIT",
                 url="https://github.com/andreeas26/duallog_v2",
                 author="Andreea Sandu",
                 author_email="acschaefer@users.noreply.github.com",
                 maintainer="Andreea Sandu",
                 include_package_data=False,
                 packages=["duallog_v2"],
                 classifiers=[
                     "License :: OSI Approved :: MIT License",
                     "Programming Language :: Python :: 2",
                     "Programming Language :: Python :: 2.6",
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: 3",
                     "Programming Language :: Python :: 3.3",
                     "Programming Language :: Python :: 3.4",
                     "Programming Language :: Python :: 3.5",
                     "Programming Language :: Python :: 3.6",
                     "Programming Language :: Python :: 3.7",
                     "Programming Language :: Python :: 3.8",
                     "Programming Language :: Python :: 3.9",
                     "Programming Language :: Python :: 3.10",
                     "Operating System :: OS Independent"])
