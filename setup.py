#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup (name="yacite",
       version="0.1",
       description="Managing your citations the UNIX way",
       author="Gejza Jenča",
       author_email="gejza.jenca@stuba.sk",
       url="http://bitbucket.org/gjenca/yacite",
       packages=['yacite','yacite.utils','yacite.command'],
       scripts=['bin/yacite','bin/bib2yaml']
      )
