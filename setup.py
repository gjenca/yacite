#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup,find_packages

setup (name="yacite",
       version="1.0",
       description="Managing your citations the UNIX way",
       author="Gejza Jenča",
       author_email="gejza.jenca@stuba.sk",
       url="http://bitbucket.org/gjenca/yacite",
       #packages=['yacite','yacite.utils','yacite.command'],
       install_requires=[
            "pyyaml","pybtex","jinja2"
        ],
       packages=find_packages(),
       scripts=['scripts/yacite','scripts/bib2yaml']
      )
