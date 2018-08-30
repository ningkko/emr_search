from functools import reduce
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
	

def search( ix, search_term ,num = 100):
	'''
	and_search
	or_search
	fuzzy_search
	'''

	parser = QueryParser("BODY_TEXT", schema = ix.schema).parse(search_term)
	
	with ix.searcher() as searcher:
		results = searcher.search(parser, limit = num)
		print("%d results found.\r"%len(results))
		ID = []
		for result in results:
			ID.append(result["ID"])

	return ID


def _float(s):
    '''changes string to float
    '''
    #=================helper functions=======================
    def _char2num(s):
        return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]
    
    def _str2int(s):
        return reduce(lambda x,y:x*10+y,map(_char2num,s))
    
    def _intLen(i):
        return len('%d'%i)
    
    def _int2dec(i):
        return i/(10**_intLen(i))

    #========================================
    return reduce(lambda x,y:x+_int2dec(y), map(_str2int,s.split('.')))


def filter(IDs,filter_terms):

	results = []
	data = _load_data(config.config["data_path"]+"medical_records.json")
	# check all raw IDs' values
	for ID in IDs:
		status = True
		for i in range(len(data)):
			if data[i]['id'] == ID:
				# check all filter terms
				for filter_term in filter_terms:
					expected_value = filter_terms[filter_term]
					actual_value = data[i]["jyxm"][filter_term]
					# if len==1, accurate value
					if len(expected_value)==1:
						if _float(expected_value[0])!=actual_value:
							status = False
					elif len(expected_value)==2:
						if _float(expected_value[0])>actual_value or _float(expected_value[1])<actual_value:
							status = False
		if status == True:
			results.append(ID)
	return results
							


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
	
	
