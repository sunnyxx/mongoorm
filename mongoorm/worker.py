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
	def update(self, data, callback=None):
		raise NotImplementedError
	@engine
	def remove(self, query, callback=None):
		raise NotImplementedError
	@engine
	def find(self, query, count=None, callback=None):
		raise NotImplementedError
	@engine
	def find1(self, query, callback=None):
		raise NotImplementedError
