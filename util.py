import log
import re
import os


list_options = ["general", "user", "group", "computer", "regex", "all"]
set_options = ["user", "group", "computer", "regex"]


def validate_export_command(f):
    result = 'exports/' + re.sub(r'(.txt|/)', '', f) + '.txt'
    return result


def validate_list_command(c):
    if c not in list_options:
        return False
    else:
        return True


def validate_set_option(option):
    if option not in set_options:
        return False
    else:
        return True


# Will validate for group, user, computer, and regex input
def validate_common_config(c):
    if c == "":
        return False
    else:
        return True


def validate_user_input(i):
    special_characters = ['{', '}', '[', ']', '(', ')', '^', '$', '.', '*', '+', '?', '\\', '|', '\'', '\"']
    for character in special_characters:
        if character in i:
            i = i.replace(character, '\\' + character)
    return i


def handle_export(count, path):
    file = open(path, 'a+')
    if count == 0:
        file.close()
        os.remove(path)
        log.log_no_results()
    else:
        file.close()
        log.log_successful_export(path)
        

def strip_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)        