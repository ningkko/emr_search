import sys,os
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import json

def search():
	
	sys.path.append("../")

	# load data
	data = []
	with open("medical_records.json") as file:
		for line in file:
			data.append(json.loads(line))

	# create schema
	schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))
	if not os.path.exists("medical_record"):
		os.mkdir("medical_record")

	# create index
	ix = create_in("medical_record", schema) # for create new index

	# create searcher
	searcher = ix.searcher()

	# write data to the searcher
	writer = ix.writer()
	for i in range(0,len(data)):
	    writer.add_document(
	        title=data[i][0]["id"],
	        content=data[i][3]["body"]
	    )
	writer.commit()

	# get user input
	search_term,filter_term = _get_input()[0],_get_input()[1]


	qp = QueryParser(search_term, schema=ix.schema)
	q = qp.parse(search_term)
	with ix.searcher() as s:

		results = s.search(q, limit = 20)

	print(results)

def _get_input():

	search_term = input("Enter a keyword.(enter q! to exit).")
	filter_term=[]

	while True:
	
		q = input("Enter another keyword.(enter q! to exit).")
		if q == "q!":
			break
		else:
			search_term = search_term + q

	def _get_filter_term():
		
		filter_term[0] = input("Enter the name of the filter term.")
		filter_term[1] = input("Enter the sign of the filter term(>/</=).")
		filter_term[2] = input("Enter the numerical value of the filter term.")
		return filter_term

	while True:

		q = input("Enter the filter term (Enter q! to exit).")
		if q == "q!":
			break
		else:
			filter_term.append(_get_filter_term())


	return[search_term,filter_term]
