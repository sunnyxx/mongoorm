#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: sunnyxx
from tornado.gen import engine
import motor

from mongoorm.worker import Worker

class MotorWorker(Worker):
	""" Implement a worker with motor
	"""
	def __init__(self, **kwargs):
		super(MotorWorker, self).__init__(**kwargs)
		self.dbname = kwargs.pop('dbname')
		self.collection = kwargs.pop('collection')
		self.client = motor.MotorClient(**kwargs).open_sync()
		self.collection = self.client[self.dbname][self.collection]

	@engine
	def insert(self, data, callback):
		error = yield motor.Op(self.collection.insert, data)
		callback(error)
	@engine
	def update(self, spec, data, callback=None):
		error = yield motor.Op(self.collection.update, spec, data)
		callback(error)
	@engine
	def remove(self, spec, callback=None):
		error = yield motor.Op(self.collection.remove, spec)
		callback(error)		
	@engine
	def find(self, spec=None, count=0, callback=None):
		cursor = self.collection.find(spec).limit(count)
		docs = yield motor.Op(cursor.to_list)
		callback(docs)

	@engine
	def find1(self, spec=None, callback=None):
		doc = yield motor.Op(self.collection.find_one, spec)
		callback(doc)

		