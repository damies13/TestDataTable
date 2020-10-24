import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="testdatatable",
	version="0.2.2",
	author="damies13",
	author_email="damies13+TestDataTable@gmail.com",
	description="Test Data Table",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/damies13/TestDataTable",
	packages=setuptools.find_packages(),
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Test Automators",
		"Programming Language :: Python :: 3.7",
		"License :: OSI Approved :: GNU GPL 3",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.7',
	project_urls={
	    'Getting Help': 'https://github.com/damies13/TestDataTable#getting-help',
	    'Say Thanks!': 'https://github.com/damies13/TestDataTable#donations',
	    'Source': 'https://github.com/damies13/TestDataTable',
	},
)
