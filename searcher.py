import sys,os
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import json
import whoosh.reading

def searcher():
	
	sys.path.append("../")
	# load data
	with open("medical_records.json") as file:
		for line in file:
			data = json.loads(line)

	# create schema
	schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))
	if not os.path.exists("medical_record"):
		os.mkdir("medical_record")
	
	# create index
	ix = create_in("medical_record", schema) # for create new index
	
	# create searcher
	searcher = ix.searcher()
	parser = QueryParser("content", schema=ix.schema)

	# write data to the searcher
	writer = ix.writer()
	
	for i in range(0,len(data)):
	    writer.add_document(
	        title=data[i]["id"],
	        content=data[i]["body"]
	    )
	#    print(data[i][0]["id"])

	writer.commit()

	# get user input
	search_term = _get_search_term()

	qp = QueryParser("content", schema=ix.schema)
	q = qp.parse(search_term)

	with ix.searcher() as searcher:
		results = searcher.search(q, limit = 20)
		print(len(results))


def _get_search_term():

	search_term = input("Enter a keyword.(enter q! to exit).")

	while True:
	
		q = input("Enter another keyword.(enter q! to exit).")
		
		if q == "q!":
			break
		else:
			search_term = search_term + q

	return search_term

'''	while True:
		
			
	filter_term.append(input("Enter the name of the filter term."))
	filter_term.append(input("Enter the sign of the filter term(>/</=)."))
	filter_term.append(input("Enter the numerical value of the filter term."))
	return filter_term
		if q == "q!":
			break
		else:
			filter_terms.append(q)
'''

search()
