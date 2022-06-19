
file_log = 'log.txt'

def add_in_log(str_log):
    with open(file_log,'a', encoding = 'UTF-8') as file:
        string_to_file = str_log +'\n'
        file.write(string_to_file)
