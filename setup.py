from setuptools import setup

setup(

	with open("README", 'r') as f:
   		long_description = f.read()

	name = "emrs",
	version = "1.0",
	description = "A search tool for medical records.",
	author = "Nene",
	author_email = "makiasagawa@gmail.com",
	packages = ["emrs"],
	install_requires = ["whoosh","jieba"],
	scripts =["emr_search"]

	)