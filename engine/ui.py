def get_search_term():

	search_term = input("Enter a keyword: ")

	while True:

		sign = ""
		while sign != "a" and sign ! ="o" and sign != "n" and sign != "y":
			sign = input("a(nd) | o(r) | n(ot) | y=exit: ")

		if sign == "y":
			break

		elif sign == "a"

			search_term+= " AND %s"%input(  "Enter another keyword(enter y to exit): ")
		
		elif sign == "o":

			search_term+= " OR %s"%input(  "Keyword(enter y to exit): ")
		
		elif sign == "n":
			search_term+= " NOT %s"%input(  "Keyword(enter y to exit): ")

	return search_term

def get_filter_term():

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

def add_new_words(target_dict, multi_time):

    if multi_time == "m":

        while True:

            new_word = input("Enter a new word (q! = QUIT): ")
            if new_word == "q!":
                break

            yn = input("y=CONFIRM | n=CANCEL: ")
            if yn != "n":

                with open(target_dict,"a") as file:
                    file.write("\r%s"%new_word)

    else:

        with open(target_dict,"a") as file:
            file.write("\r%s"%new_word)

