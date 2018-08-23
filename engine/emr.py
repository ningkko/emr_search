from extract import clear_up,relaod
from ui import get_search_term
from searcher import init,search

if not "medical_records.json" in os.listdir("/data/"):
	try:

		extract.clear_up("electronic-medical-record.json")

	except IOError:

		print("** Target file not found under /data/ **")

else:

	print("Seacrhing engine set up...Start.")
	searcher.init()
	while True:
		
		search_term = ui.get_search_term()
		searcher.search(search_term)
		print("----------SEARCHING DONE---------")