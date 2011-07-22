#!/usr/bin/env python

from distutils.core import setup
import colour

setup(name=colour.NAME,
		version=colour.VERSION,
		description=colour.DESCRIPTION,
		author=colour.AUTHOR,
		author_email=colour.AUTHOR_EMAIL,
		url=colour.URL,
		license=colour.LICENSE,
		py_modules=["colour"],
		)
