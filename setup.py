#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup (name="yacite",
       version="1.0",
       description="Managing your citations the UNIX way",
       author="Gejza Jenča",
       author_email="gejza.jenca@stuba.sk",
       url="http://bitbucket.org/gjenca/yacite",
       packages=['yacite','yacite.utils','yacite.command'],
       scripts=['scripts/yacite','scripts/bib2yaml']
      )
