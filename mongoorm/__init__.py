#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: sunnyxx
from datetime import datetime

from tornado import ioloop,gen

from mongoorm.document import Document
from mongoorm.field import BoolField, IntField, FloatField, StringField, EmailField, DateTimeField, ObjectIdField
from mongoorm.motorworker import MotorWorker

class User(Document):

	_id = ObjectIdField()

	name = StringField(unique=True, required=True)
	age = IntField()
	birthday = DateTimeField()
	is_married = BoolField()
	weight = FloatField()
	email = EmailField(unique=True, required=True)

	config = {
		'dbname':"your db's name",
		'collection':"this collection's name",
		#optional
		'host':'localhost',
		'port':27017,
		'worker':MotorWorker,
		'max_pool_size':20,
	}
def test():
	user = User(
		name='sunnyxx',
		age=20,
		is_married=False,
		email='sunyuan1713@sina.com',
		birthday = datetime.now()
	)
	# or
	# user = User()
	# user.name = 'sunnyxx'
	# user.age = 20
	# ...

	#insert
	yield gen.Task(user.insert)
	#find
	users = yield gen.Task(User.find, count=2)
	print users
	#find1
	user = yield gen.Task(User.find1)
	print user
	#update
	user.weight = 100.0
	yield gen.Task(user.update)
	print user
	#update or
	yield gen.Task(user.update, weight=200.0)
	print user
	#remove
	yield gen.Task(user.remove)	

if __name__ == '__main__':
	test()
	ioloop.IOLoop.instance().start()