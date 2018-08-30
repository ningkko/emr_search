from extract import clear_up,refresh
from ui import *
from searcher import *
import sys,os
sys.path.append("../")  
import config




while True:

	if not "medical_records.json" in os.listdir("../data"):

		try:
			print("BUILDING DATA...")
			clear_up(config.config["data_path"]+"electronic-medical-record.json")

		except IOError:
			print("TARGET FILE NOT FOUND...")
			break

	else:

		init()
		ix = create_index(create_schema())
		print("DATA BASE BUILT")
		
		while True:
			
			search_term = get_search_term()
			#num = get_result_num()
			IDs = search(ix, search_term)
			status = input("Enter filter values?(y/n): ") 
			while status!= "y" and status !="n":
				status = input("Enter y or n: ")
			if status == "y":
				filter_term = get_filter_values()
				filtered_IDs = filter(IDs,filter_term)
				print("%d results found.\r----------------\r"%len(filtered_IDs))
				for ID in filtered_IDs:
					print(ID)

			else:
				print("%d results found.\r"%len(IDs))
				for ID in IDs:
					print(ID)
			print("----------SEARCHING DONE---------")
		
