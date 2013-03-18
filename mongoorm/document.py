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
	fields = {}

	def __new__(cls, **kwargs):

		obj =  super(Document, cls).__new__(cls, **kwargs)

		for fieldname, field in cls.__dict__.iteritems():
			if isinstance(field, BaseField):
				field.name = fieldname
				cls.fields[fieldname] = field

		#set `items` dict into obj, store concrete key/value
		setattr(obj, 'items', {})

		return obj

	def __init__(self, **kwargs):

		#init value `kwargs` passed in
		if kwargs:
			self._set_value_with_kwargs(**kwargs)

	def __repr__(self):
		representation = super(Document, self).__repr__()[:-1]
		for fieldname, field in self.fields.iteritems():
			representation += ('|'+fieldname+':'+repr(self.items.get(fieldname)))
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
		#insert
		error = yield Task(self._get_worker().insert, self.items)
		callback(error)

	@engine
	def update(self, callback=None, **kwargs):
		if kwargs:
			self._set_value_with_kwargs(**kwargs)
		error = yield Task(self._get_worker().update, {'_id':self._id}, self.items)
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

	@engine
	def _check_unique(self, callback):
		for fieldname, field in self.fields.iteritems():
			if field.unique:
				pre_find = yield Task(self.find1, {fieldname:self.items[fieldname]})
				if pre_find:
					raise ValueError(repr(self.__class__)+'|{'+fieldname+':'+repr(field.value)+'}'+' IS NOT UNIQUE')

		callback()

	def _check_required(self):
		for fieldname, field in self.fields.iteritems():
			if field.required and not self.items[fieldname]:
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
			if key in self.__class__.fields.iterkeys():
				self.fields[key].__set__(self, value)
			else:
				raise KeyError('key: <'+key+'> is not defined in '+repr(self.__class__))


