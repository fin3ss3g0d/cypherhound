import os
import sys
import log
import help
import util
import database


OPTIONS = ['set', 'run', 'export', 'list', 'q', 'quit', 'exit', 'clear', 'cls', '?', 'stop', 'help', 'general', 'user', 'group', 'computer', 'regex', 'all', 'search']
    

class Completer:
    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [
                    s
                    for s in self.options
                    if s and s.startswith(text)
                ]
            else:
                self.matches = self.options[:]
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


class Terminal:
    def __init__(self, user, pwd, db, yaml_file):
        try:
            self.driver = database.Driver(user, pwd, db, template_file=yaml_file)
        except Exception as e:
            log.log_error(e)
            
    def input_loop(self):
        try:             
            while True:
                line = input(': ')            
                if line == 'q' or line == 'quit' or line == 'exit' or line == 'stop':
                    self.driver.close()
                    sys.exit(0)
                elif line == 'help' or line == '?' or line == '':
                    help.print_help()
                    continue
                elif line == 'clear' or line == 'cls':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                command = line.split(" ")
                if command[0] not in OPTIONS:
                    log.log_command_invalid(line)
                    continue
                if command[0] == "set":
                    if len(command) < 3:
                        log.log_command_invalid(line)
                        continue
                    else:
                        option = command[1]
                        if not util.validate_set_option(option):
                            log.log_invalid_option(option)
                            continue
                        else:
                            if option == "user":
                                user_in = line[9:]
                                if util.validate_common_config(user_in):
                                    util.validate_user_input(user_in)
                                    self.driver.set_user_param(user_in)
                                    log.log_successful_set("user", user_in)
                                else:
                                    log.log_error("User is empty or is missing @!")
                            elif option == "group":
                                group_in = line[10:]
                                if util.validate_common_config(group_in):
                                    util.validate_user_input(group_in)
                                    self.driver.set_group_param(group_in)
                                    log.log_successful_set("group", group_in)
                                else:
                                    log.log_error("Group is empty or is missing @!")
                            elif option == "computer":
                                c_in = line[13:]
                                if util.validate_common_config(c_in):
                                    util.validate_user_input(c_in)
                                    self.driver.set_computer_param(c_in)
                                    log.log_successful_set("computer", c_in)
                                else:
                                    log.log_error("Computer is empty or is missing @!")
                            elif option == "regex":
                                r_in = line[10:]
                                if util.validate_common_config(r_in):
                                    util.validate_user_input(r_in)
                                    self.driver.set_regex(r_in)
                                    log.log_successful_set("regex", r_in)
                                else:
                                    log.log_error("Regex is empty!")                        
                            else:
                                log.log_command_invalid(line)
                                continue                        
                elif command[0] == "run":
                    if len(command) != 2:
                        log.log_command_invalid(line)
                        continue
                    else:
                        option = command[1]
                        if not 1 <= int(option) <= len(self.driver.queries):
                            log.log_invalid_option(option)
                            continue
                        else:
                            self.driver.run_query(option, "")
                elif command[0] == "export":
                    if len(command) < 3:
                        log.log_command_invalid(line)
                        continue
                    else:
                        option = command[1]
                        fname = command[2]
                        if not 1 <= int(option) <= len(self.driver.queries):
                            log.log_invalid_option(option)
                            continue
                        else:
                            if len(command) == 3:
                                f = util.validate_export_command(fname)
                                self.driver.run_query(option, f)
                            else:
                                log.log_command_invalid(line)
                                continue
                elif command[0] == "list":
                    if len(command) < 2:
                        log.log_command_invalid(line)
                        continue
                    else:
                        option = command[1]
                        if not util.validate_list_command(option):
                            log.log_invalid_option(option)
                        else:
                            self.driver.print_queries_by_group(option)
                elif command[0] == "search":
                    if len(command) < 2:
                        log.log_command_invalid(line)
                        continue
                    else:
                        search = line[7:]
                        self.driver.search_queries(search)
                else:
                    log.log_command_invalid(line)
                    continue                                                  
                
        except Exception as e:
            log.log_error(e)