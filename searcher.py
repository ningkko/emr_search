import sys,os
import json
from ui import *
from whoosh import qparser
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser


def init():

	sys.path.append("../")	
	
	data = _load_data("medical_records.json")

	# create schema
	global schema
	schema = Schema(ID=ID(stored=True), NAME=TEXT(stored=True), BODY_TEXT=TEXT(stored=True))
	if not os.path.exists("data_base"):
		os.mkdir("data_base")
	
	# create index
	global 
	ix = create_in("data_base", schema) # for create new index
	
	# create searcher
	global searcher
	searcher = ix.searcher()
	#parser = QueryParser("content", schema=ix.schema)

	_write_data(ix,data)
	
	search_term = ui.get_search_term()

	num = int(input("Number of results to show: "))


def search( search_term ):
	'''
	and_search
	or_search
	fuzzy_search
	'''

	parser = QueryParser("content", schema = ix.schema).parse(search_term)
	
	with ix.searcher() as searcher:
		results = searcher.search(parser, limit = num)
		print(len(results))


def _load_data(file_name):

	with open(file_name) as file:
		for line in file:
			data = json.loads(line)
	
	return data


def _write_data(ix,data):

	writer = ix.writer()
	
	for i in range(0,len(data)):
	    writer.add_document(
	        ID = data[i]["id"],
	        NAME = data[i]["name"],
	        BODY_TEXT = data[i]["body"]
	    )

	writer.commit()

