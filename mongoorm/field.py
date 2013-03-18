#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: sunnyxx

import re #regex
from datetime import datetime
from bson import ObjectId

""" Fields provided for Document
"""
class BaseField(object):

	def __init__(self, required=False, unique=False):
		self.required = required
		self.unique = unique
		self.name = None

	''' Using descriptor to set/get `value` property'''
	def __get__(self, obj, type=None):
		return obj.items.get(self.name)

	def __set__(self, obj, value):
		self.validate(value)
		obj.items[self.name] = value

	''' Abstract method for value validating.
	Called when `Document().xxx = value` called
	'''
	def validate(self, value):
		pass

	def _raise_type_error(self, value):
		raise TypeError(str(self.__class__.__name__)+' NOT MATCHES VALUE:'+repr(value))

class BaseTypeField(BaseField):

	def __init__(self, datatype=None, **kwargs):
		super(BaseTypeField, self).__init__(**kwargs)
		self.datatype = datatype

	def validate(self, value):
		super(BaseTypeField, self).validate(value)
		if not isinstance(value, self.datatype):
			self._raise_type_error(value)

#simple types
class BoolField(BaseTypeField):
	def __init__(self, **kwargs):
		super(BoolField, self).__init__(datatype=bool, **kwargs)
class IntField(BaseTypeField):
	def __init__(self, **kwargs):
		super(IntField, self).__init__(datatype=(int, long), **kwargs)
class FloatField(BaseTypeField):
	def __init__(self, **kwargs):
		super(FloatField, self).__init__(datatype=float, **kwargs)
class StringField(BaseTypeField):
	def __init__(self, **kwargs):
		super(StringField, self).__init__(datatype=(str, unicode), **kwargs)
class DateTimeField(BaseTypeField):
	def __init__(self, **kwargs):
		super(DateTimeField, self).__init__(datatype=datetime, **kwargs)
class ObjectIdField(BaseTypeField):
	def __init__(self, **kwargs):
		super(ObjectIdField, self).__init__(datatype=ObjectId, **kwargs)

#email
class EmailField(StringField):
	def validate(self, value):
		super(EmailField, self).validate(value)
		regex = re.compile(
		    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
		    # quoted-string, see also http://tools.ietf.org/html/rfc2822#section-3.2.5
		    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
		    r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$)'  # domain
		    r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$', re.IGNORECASE 
		)
		if not re.match(regex, value):
			self._raise_type_error(value)

#nested types
class ListField(BaseTypeField):
	def __init__(self, **kwargs):
		super(DateTimeField, self).__init__(datatype=list, **kwargs)
class DictField(BaseTypeField):
	def __init__(self, **kwargs):
		super(DateTimeField, self).__init__(datatype=dict, **kwargs)

