import log


def print_help():
    print()
    print(f'{log.default}Command Menu{log.reset}')
    print(f'{log.default}set{log.reset} - used to set search parameters for cyphers, double/single quotes not required for any sub-commands')
    print(f'{log.default}    sub-commands{log.reset}')
    print(f'{log.default}        user{log.reset} - the user to use in user-specific cyphers (MUST include @domain.name)')
    print(f'{log.default}        group{log.reset} - the group to use in group-specific cyphers (MUST include @domain.name)')
    print(f'{log.default}        computer{log.reset} - the computer to use in computer-specific cyphers (SHOULD include .domain.name or @domain.name)')
    print(f'{log.default}        regex{log.reset} - the regex to use in regex-specific cyphers')
    print(f'{log.default}    example{log.reset}')
    print('        set user svc-test@domain.local')
    print('        set group domain admins@domain.local')
    print('        set computer dc01.domain.local')
    print('        set regex .*((?i)web).*')
    print(f'{log.default}run{log.reset} - used to run cyphers')
    print(f'{log.default}    parameters{log.reset}')
    print(f'{log.default}        cypher number{log.reset} - the number of the cypher to run')
    print(f'{log.default}    example{log.reset}')
    print('        run 7')
    print(f'{log.default}export{log.reset} - used to export cypher results to txt files')
    print(f'{log.default}    parameters{log.reset}')
    print(f'{log.default}        cypher number{log.reset} - the number of the cypher to run and then export')
    print(f'{log.default}        output filename{log.reset} - the number of the output file, extension not needed')    
    print(f'{log.default}    example{log.reset}')
    print(f'        export 31 results')    
    print(f'{log.default}list{log.reset} - used to show a list of cyphers')
    print(f'{log.default}    parameters{log.reset}')
    print(f'{log.default}        list type{log.reset} - the type of cyphers to list (general, user, group, computer, regex, all)')
    print(f'{log.default}    example{log.reset}')
    print(f'        list general')
    print(f'        list user')
    print(f'        list group')
    print(f'        list computer')
    print(f'        list regex')
    print(f'        list all')
    print(f'{log.default}search{log.reset} - used to search the list of cyphers')
    print(f'{log.default}    parameters{log.reset}')
    print(f'{log.default}        search query{log.reset} - the search string')
    print(f'{log.default}    example{log.reset}')
    print(f'        search domain admin')
    print(f'        search shortest')
    print(f'{log.default}q, quit, exit, stop{log.reset} - used to exit the program')
    print(f'{log.default}clear, cls{log.reset} - used to clear the terminal')
    print(f'{log.default}help, ?{log.reset} - used to display this help menu')
    print()
