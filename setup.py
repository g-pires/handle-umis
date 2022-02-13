#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from setuptools import setup, find_packages

import handle_umis

setup(
        name='handle_umis',

        version=handle_umis.__version__,

        packages=find_packages(),

        author='Gabriel Pires',

        author_email='gabriel.pires081196@gmail.com',

        description='Module that handle UMIs for the pipeline SAIP using smCounter2',

        long_description=open('README.md').read(),

        install_requires = [
            "setuptools>=1.1",
            "pysam>=0.15.2"],

        include_package_data=True,

        scripts=['handle-umis'],

        classifiers=[
            "Programming Language :: Python",
            "Development Status :: 1", 
            "Natural Language :: English", 
            "Operating System :: LINUX", 
            "Programming Language :: Python :: 3.7.3",
            "Topic :: Bioinfo",
        ], 

        license="",
)
