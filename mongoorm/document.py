#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: sunnyxx

from tornado.gen import engine, Task

from field import BaseField
from worker import Worker
from motorworker import MotorWorker #for default worker

"""
Usage:
	class User(Document):
		name 	 = StringField()
		age 	 = IntField()
		birthday = DateTimeField()
		married  = BoolField()
		weight 	 = FloatField()
		email 	 = EmailField()

		config = {# name `config` is exactly
			
			'db':'db name', 					 #necessary!
			'collection':'collection name', 	 #necessary!
			'host':'mongodb host ip', 			 #default `localhost`
			'port':'mongodb port', 				 #default `27017`
			'worker': 'implemented worker class' #default `MotorWorker`
			
		}

	if __name__ == '__main__':
		user = User()
		user.name = 'sunnyxx'
		user.age = 22
		user.is_married = 'guess' #<-this will raise a `TypeError` exception
		...
		error = yield tornado.gen.Task(user.insert)
		#check error if you want

"""
class Document(object):
	''' Document defines `collection` in mongodb,
	and uses a `Worker` to process operations about mongodb (etc. `insert`,`find`).
	'''
	
	default_config = {
		'host': 'localhost',
		'port': 27017,
		'dbname': None,
		'collection': None,

		'worker': MotorWorker,
		'max_pool_size':20,
	}
	worker = None

	def __new__(cls, **kwargs):
		return super(Document, cls).__new__(cls, **kwargs)

	def __init__(self, **kwargs):
		#find all fields
		self.fields = {}
		for fieldname, field in self.__class__.__dict__.iteritems():
			if isinstance(field, BaseField):
				self.fields[fieldname] = field
		#init value `kwargs` passed in
		if kwargs:
			self._set_value_with_kwargs(**kwargs)

	def __repr__(self):
		representation = super(Document, self).__repr__()[:-1]
		for fieldname, field in self.fields.iteritems():
			representation += ('|'+fieldname+':'+repr(field.value))
		return representation + '>'

	''' Mongodb operation jobs.
	Operate with concrete subclass of `Worker`

	'''
	@engine
	def insert(self, callback):

		#requirement check
		self._check_required()
		#unique check
		yield Task(self._check_unique)
		#generate doc
		doc = self.get_dict()
		#insert
		error = yield Task(self._get_worker().insert, doc)
		callback(error)

	@engine
	def update(self, callback=None, **kwargs):
		if kwargs:
			self._set_value_with_kwargs(**kwargs)
		doc = self.get_dict()
		print self._id
		error = yield Task(self._get_worker().update, {'_id':self._id}, doc)
		callback(error)

	@engine
	def remove(self, callback=None):
		error = yield Task(self._get_worker().remove, {'_id':self._id})
		callback(error)

	@classmethod
	@engine
	def find(cls, query=None, count=0, callback=None):
		docs = yield Task(cls._get_worker().find, query, count)
		objs = [cls(**doc) for doc in docs] if docs is not None else None
		callback(objs)

	@classmethod
	@engine
	def find1(cls, query=None, callback=None):
		doc = yield Task(cls._get_worker().find1, query)
		obj = cls(**doc) if doc is not None else None
		callback(obj)

	''' Helpers
	'''
	def get_dict(self):
		doc = {}
		for fieldname, field in self.fields.iteritems():
			if field.value is not None:
				doc[fieldname] = field.value
		return doc

	@engine
	def _check_unique(self, callback):
		for fieldname, field in self.fields.iteritems():
			if field.unique:
				pre_find = yield Task(self.find1, {fieldname:field.value})
				if pre_find:
					raise ValueError(repr(self.__class__)+'|{'+fieldname+':'+repr(field.value)+'}'+' IS NOT UNIQUE')

		callback()

	def _check_required(self):
		for fieldname, field in self.fields.iteritems():
			if field.required and not field.value:
				raise Exception(repr(self.__class__)+':FIELD <'+fieldname+'> IS REQUIRED BUT NONE')

	@classmethod
	def _get_worker(cls):
		#get singleton worker instance by config
		if not cls.worker:
			if 'config' not in cls.__dict__:
				raise Exception('a `config` dict is required with `dbname` and `collection` at least')
		
			config = cls.default_config
			config.update(cls.__dict__['config'])
			if filter(lambda key:key is None, config.itervalues()):
				raise ValueError('value of some key in config is None and not in default')

			worker_class = config.pop('worker')
			if not issubclass(worker_class, Worker) or worker_class is Worker:
				raise TypeError(repr(worker_class) + ' is not subclass of Worker')
			#create singleton, remaining kwargs pass on
			cls.worker = worker_class(**config)

		return cls.worker

	def _set_value_with_kwargs(self, **kwargs):
		for key, value in kwargs.iteritems():
			if key in self.fields.iterkeys():
				self.fields[key].__set__(self, value)
			else:
				raise KeyError('key: <'+key+'> is not defined in '+repr(self.__class__))


