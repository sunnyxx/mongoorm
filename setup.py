from distutils.core import setup

setup(
	name = 'mongoorm',
	version = '1.0.0',
	author = 'sunnyxx', 
	author_email = 'sunyuan1713@gmail.com',
	url = 'https://github.com/sunnyxx/mongoorm',
	description = 'Async Mongodb ORM under tornado framework, using `motor` for default implement',
	license = 'Apache License, Version 2.0',
	packages = [ 'mongoorm' ],
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Development Status :: 1 - Beta',
		'Environment :: Other Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
		'Operating System :: OS Independent',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
)