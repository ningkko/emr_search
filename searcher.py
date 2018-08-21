import sys,os
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import json
import whoosh.reading

def search():

	sys.path.append("../")	
	
	data = _load_data("medical_records.json")

	objects = _init(data)
	ix = objects[0]
	searcher = objects[1]
	
	search_term = _get_search_term()
	num = int(input("Enter the number of results."))

	query = QueryParser("content", schema=ix.schema).parse(search_term)

	with ix.searcher() as searcher:
		results = searcher.search(query, limit = num)
		print(len(results))

		
def _load_data(file_name):

	with open(file_name) as file:
		for line in file:
			data = json.loads(line)
	
	return data


def _init(data):

	# create schema
	schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))
	if not os.path.exists("medical_record"):
		os.mkdir("medical_record")
	
	# create index
	ix = create_in("medical_record", schema) # for create new index
	
	# create searcher
	searcher = ix.searcher()
	#parser = QueryParser("content", schema=ix.schema)

	return[ix,searcher]


def _write_data(ix,data):

	writer = ix.writer()
	
	for i in range(0,len(data)):
	    writer.add_document(
	        title=data[i]["id"],
	        content=data[i]["body"]
	    )

	writer.commit()


def _get_search_term():

	search_term = input("Enter a keyword.")

	while True:
	
		q = input("Enter another keyword.(enter y to exit).")
		
		if q == "y":
			break
		else: search_term = search_term + q

	return search_term

def _get_filter_term():

	filter_terms = []
	while True:
		filter_term = []

		quit = input("quit?(y/n)")	

		if q == "q!":
			break

		else:
			filter_term.append(input("Name of the filter term: "))
			filter_term.append(input("Sign(>/</=): "))
			filter_term.append(input("Numerical value: "))

			filter_terms.append(filter_term)

	return filter_terms

search()
