import setuptools

with open("README_PyPi.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="testdatatable",
	version="0.2.3",
	author="damies13",
	author_email="damies13+TestDataTable@gmail.com",
	description="TestDataTable",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/damies13/TestDataTable",
	packages=setuptools.find_packages(),
	# packages=setuptools.find_packages(include=['configparser', 'setuptools', 'HTTPServer', 'sqlite3worker']),
	# packages=setuptools.find_packages(include=['configparser', 'HTTPServer', 'sqlite3worker']),
	install_requires=['configparser', 'HTTPServer', 'sqlite3worker'],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Topic :: Software Development :: Testing",
		"Programming Language :: Python :: 3.7",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.7',
	project_urls={
		'Getting Help': 'https://github.com/damies13/TestDataTable#getting-help',
		'Say Thanks!': 'https://github.com/damies13/TestDataTable#donations',
		'Source': 'https://github.com/damies13/TestDataTable',
	},
)
