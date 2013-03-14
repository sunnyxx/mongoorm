mongoorm
========
Async Mongodb ORM under tornado framework, using 'motor' for default implement

Dependencies
-----------
*tornado
*motor(default implement)

Install
-----------
    python setup.py install 

Usage
-----------
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

		config = {
			#necessary:
			'dbname':"your db's name",
			'collection':"this collection's name",
			#optional
			'host':'localhost',#default
			'port':27017,#default
			'worker':MotorWorker,#default
			#optional(will pass on to implement class)
			'max_pool_size':20,#default
			#'other_key':'other value'
		}
	def test():
		user = User(
			name='sunnyxx',
			age=20,
			is_married=False,
			email='https://github.com/sunnyxx',
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
		#find1
		user = yield gen.Task(User.find1)
		#update
		user.weight = 100.0
		yield gen.Task(user.update)
		yield gen.Task(user.update, weight=200.0)#<-or
		#remove
		yield gen.Task(user.remove)	

	if __name__ == '__main__':
		test()
		ioloop.IOLoop.instance().start()


Auth
------------
	sunnyxx
