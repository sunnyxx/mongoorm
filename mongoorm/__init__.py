#!/usr/bin/python
# -*- coding: utf-8 -*-
from mongoorm.document import Document
from mongoorm.field import BoolField, IntField, FloatField, StringField, EmailField, DateTimeField, ObjectIdField
from datetime import datetime
from tornado import ioloop,gen

class User(Document):

	_id = ObjectIdField()

	name = StringField(unique=True, required=True)
	age = IntField()
	birthday = DateTimeField()
	is_married = BoolField()
	weight = FloatField()
	email = EmailField(unique=True, required=True)

	# config = {
	# 	'host':'localhost',
	# 	'port':27017,
	# 	'dbname':'db1',
	# 	'collection':'user',

	# 	'worker':MotorWorker,
	# 	'max_pool_size':20,
	# }
	config = {
		'dbname':'db1',
		'collection':'user'
	}
@gen.engine
def test():
	# user = User(email='123@11.con')
	# user.name = '1234'
	# user.age = 20
	# user.is_married = False
	# user.weight = 10.0
	# user.email = '1231@1223.com'
	# user.birthday = datetime.now()
	user = User(
		name='sunnyxx',
		age=20,
		is_married=False,
		email='https://github.com/sunnyxx',
		birthday = datetime.now()
	)
	yield gen.Task(user.insert)
	user = yield gen.Task(user.find1, count=2)
	print user
	user.weight = 10.0
	yield gen.Task(user.update, age=30)
	yield gen.Task(user.remove)
	print 'after test'


if __name__ == '__main__':
	
	test()
	ioloop.IOLoop.instance().start()



