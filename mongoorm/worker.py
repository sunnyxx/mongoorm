#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: sunnyxx

from tornado.gen import engine

class Worker(object):

	''' Abstract class that helps `Document` to operate mongodb.
	'''
	def __init__(self, **kwargs):
		pass

	'''Subclass should override all methods below.'''
	@engine
	def insert(self, data, callback=None):
		raise NotImplementedError
	@engine
	def update(self, spec, data, callback=None):
		raise NotImplementedError
	@engine
	def remove(self, spec, callback=None):
		raise NotImplementedError
	@engine
	def find(self, spec, count=None, callback=None):
		raise NotImplementedError
	@engine
	def find1(self, spec, callback=None):
		raise NotImplementedError
