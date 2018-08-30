from extract import exist
def get_search_term():

    search_term = input("Enter a keyword: ")

    while True:

        sign = ""
        while sign != "a" and sign !="o" and sign != "n" and sign != "y":
            sign = input("a(nd) | o(r) | n(ot) | y=exit: ").lower()
            
        if sign == "y":
            break

        elif sign == "a":

            search_term+= " AND %s"%input(  "Enter another keyword(enter y to exit): ")
        
        elif sign == "o":

            search_term+= " OR %s"%input(  "Keyword(enter y to exit): ")
        
        elif sign == "n":
            search_term+= " NOT %s"%input(  "Keyword(enter y to exit): ")

    return search_term


def get_result_num():

    return int(input("Number of results to show: "))



def get_filter_values():
    '''
    filter_values = {
                    filter_term:[value]
                    filter_term:[value1,value2]
                    ...
                    }
    '''

    filter_values = {}

    while True:
        
        filter_term = input("Input a valued term (y = exit): ")
        
        if filter_term=="y":
            break

        else:
        
            if exist(filter_term):
                mode = ""
                while mode != "a" and mode!="i":
                    mode = input("a(ccurate mode) | i(nterval mode): ")

                if  mode == "a":

                    filter_value = input("Enter the value: ")
                    print("----------------")
                    filter_values[filter_term]=[filter_value]

                else: 
                    filter_value_1 = input("Bigger than: ")
                    filter_value_2 = input("Smaller than: ")
                    print("----------------")
                    filter_values[filter_term]=[filter_value_1,filter_value_2]

            else: print("TERM NOT EXIST...\r----------------")

    return filter_values     


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
