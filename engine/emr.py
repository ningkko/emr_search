from engine.extract import clear_up, refresh
from engine.ui import *
from engine.searcher import *
import sys, os
sys.path.append("../") 
import config

while True:

    if not "medical_records.json" in os.listdir(config.config["data_path"]):

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
            search(ix,search_term)
            print("----------SEARCHING DONE---------")
