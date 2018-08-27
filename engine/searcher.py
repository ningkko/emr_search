import json
from whoosh import qparser,index
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import sys,os
sys.path.append("../")  
import config


def init():

	dbPath = config.path["data_base"]
	if not os.path.exists(dbPath):
		os.mkdir(dbPath)
		schema = create_schema()
		ix = create_index(schema)
		write_data(ix)

def create_schema():

	return Schema(ID=ID(stored=True), NAME=TEXT(stored=True), BODY_TEXT=TEXT(stored=True))
	
def create_index(schema):
	
	dbPath = config.path["data_base"]
	# create index	
	if index.exists_in(dbPath):
		return index.open_dir(dbPath)
	else:
		return create_in(dbPath,schema)
	

def search( ix, search_term ,num = 10):
	'''
	and_search
	or_search
	fuzzy_search
	'''

	parser = QueryParser("BODY_TEXT", schema = ix.schema).parse(search_term)
	
	with ix.searcher() as searcher:
		results = searcher.search(parser, limit = num)
		print("%d results found.\r"%len(results))
		for result in results:
			print(result["ID"])


def _load_data(file_name):

	with open(file_name) as file:
		for line in file:
			data = json.loads(line)
	
	return data


def write_data(ix):

	data = _load_data(config.config["data_path"]+"medical_records.json")

	writer = ix.writer()
	
	for i in range(0,len(data)):
	    writer.add_document(
	        ID = data[i]["id"],
	        NAME = data[i]["name"],
	        BODY_TEXT = data[i]["text_body"]
	    )

	writer.commit()
