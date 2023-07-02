from neo4j import GraphDatabase
import util
import log


class Driver:

    def __init__(self, user, password, u_search="", g_search="", c_search="", regex=""):
        self.driver = GraphDatabase.driver("neo4j://localhost:7687", auth=(user, password))
        self.user_search = u_search
        self.group_search = g_search
        self.computer_search = c_search
        self.regex = regex

    def close(self):
        self.driver.close()

    def set_user_param(self, param):
        self.user_search = param

    def get_user_param(self):
        return self.user_search

    def set_group_param(self, param):
        self.group_search = param

    def get_group_param(self):
        return self.group_search

    def set_computer_param(self, param):
        self.computer_search = param

    def get_computer_param(self):
        return self.computer_search

    def set_regex(self, r):
        self.regex = r

    def get_regex(self):
        return self.regex

    def find_all_kerberoastable(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User) WHERE n.hasspn=true RETURN n.name AS result ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["result"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["result"]}{log.reset}{log.default} is kerberoastable{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["result"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["result"]}{log.reset}{log.default} is kerberoastable{log.reset}')
                                file.write(f'{r["result"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["result"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["result"]}{log.reset}{log.default} is kerberoastable{log.reset}')
                                file.write(f'User {r["result"]} is kerberoastable\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_rdp(self, f, raw):
        with self.driver.session() as session:
            results = session.run('match p=(u:User)-[:CanRDP]->(c:Computer) return u.name,c.name ORDER BY u.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'User {r["u.name"]} CanRDP to {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_rdp(self, f, raw):
        with self.driver.session() as session:
            results = session.run('match p=(g:Group)-[:CanRDP]->(c:Computer) return g.name,c.name ORDER BY g.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'Group {r["g.name"]} CanRDP to {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_unconstrained(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (c:Computer {unconstraineddelegation:true}) return c.name ORDER BY c.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["c.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["c.name"]}{log.reset}{log.default} has unconstrained delegation privilege{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["c.name"]}{log.reset}{log.default} has unconstrained delegation privilege{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["c.name"]}{log.reset}{log.default} has unconstrained delegation privilege{log.reset}')
                                file.write(f'Computer {r["c.name"]} has unconstrained delegation privilege\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_unsupported(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (H:Computer) WHERE H.operatingsystem =~ '.*(2000|2003|2008|xp|vista|7|me).*' RETURN H.name,H.operatingsystem ORDER BY H.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["H.name"] is not None and r["H.operatingsystem"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["H.name"]}{log.reset}{log.default} is unsupported with OS {log.reset}{log.red}{r["H.operatingsystem"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["H.name"] is not None and r["H.operatingsystem"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["H.name"]}{log.reset}{log.default} is unsupported with OS {log.reset}{log.red}{r["H.operatingsystem"]}{log.reset}')
                                file.write(f'{r["H.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["H.name"] is not None and r["H.operatingsystem"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["H.name"]}{log.reset}{log.default} is unsupported with OS {log.reset}{log.red}{r["H.operatingsystem"]}{log.reset}')
                                file.write(f'Computer {r["H.name"]} is unsupported with OS {r["H.operatingsystem"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_admin_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (g:Group) WHERE g.name =~ '.*((?i)admin|adm).*' RETURN g.name ORDER BY g.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g.name"] is not None:
                            print(f'{log.default}Admin group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None:
                                print(f'{log.default}Admin group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'{r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None:
                                print(f'{log.default}Admin group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'Admin group {r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_admin_users(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (u:User) WHERE u.name =~ '.*((?i)admin|adm).*' RETURN u.name ORDER BY u.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None:
                            print(f'{log.default}Admin user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}Admin user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                                file.write(f'{r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}Admin user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                                file.write(f'Admin user {r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_sql_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (g:Group) WHERE g.name =~ '.*((?i)sql).*' RETURN g.name ORDER BY g.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g.name"] is not None:
                            print(f'{log.default}SQL group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None:
                                print(f'{log.default}SQL group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'{r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None:
                                print(f'{log.default}SQL group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'SQL group {r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_sql_users(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (u:User) WHERE u.name =~ '.*((?i)sql).*' RETURN u.name ORDER BY u.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None:
                            print(f'{log.default}SQL user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}SQL user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                                file.write(f'{r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}SQL user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                                file.write(f'SQL user {r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_sql_computers(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (c:Computer) WHERE c.name =~ '.*((?i)sql).*' RETURN c.name ORDER BY c.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["c.name"] is not None:
                            print(f'{log.default}SQL computer {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}SQL computer {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}SQL computer {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'SQL computer {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_service_users(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (u:User) WHERE u.name =~ '.*((?i)svc|service).*' RETURN u.name ORDER BY u.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None:
                            print(f'{log.default}Service user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}Service user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                                file.write(f'{r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}Service user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                                file.write(f'Service user {r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_service_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (g:Group) WHERE g.name =~ '.*((?i)svc|service).*' RETURN g.name ORDER BY g.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g.name"] is not None:
                            print(f'{log.default}Service group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None:
                                print(f'{log.default}Service group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'{r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None:
                                print(f'{log.default}Service group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'Service group {r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_web_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (g:Group) WHERE g.name =~ '.*((?i)web).*' RETURN g.name ORDER BY g.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g.name"] is not None:
                            print(f'{log.default}Web group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None:
                                print(f'{log.default}Web group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'{r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None:
                                print(f'{log.default}Web group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'Web group {r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_web_users(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (u:User) WHERE u.name =~ '.*((?i)web).*' RETURN u.name ORDER BY u.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None:
                            print(f'{log.default}Web user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}Web user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                                file.write(f'{r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}Web user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                                file.write(f'Web user {r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_web_computers(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (c:Computer) WHERE c.name =~ '.*((?i)web).*' RETURN c.name ORDER BY c.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["c.name"] is not None:
                            print(f'{log.default}Web computer {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Web computer {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Web computer {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'Web computer {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_dev_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (g:Group) WHERE g.name =~ '.*((?i)dev).*' RETURN g.name ORDER BY g.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g.name"] is not None:
                            print(f'{log.default}Dev group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None:
                                print(f'{log.default}Dev group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'{r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None:
                                print(f'{log.default}Dev group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'Dev group {r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_dev_users(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (u:User) WHERE u.name =~ '.*((?i)dev).*' RETURN u.name ORDER BY u.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None:
                            print(f'{log.default}Dev user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}Dev user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                                file.write(f'{r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}Dev user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                                file.write(f'Dev user {r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_dev_computers(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (c:Computer) WHERE c.name =~ '.*((?i)dev).*' RETURN c.name ORDER BY c.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["c.name"] is not None:
                            print(f'{log.default}Dev computer {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Dev computer {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Dev computer {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'Dev computer {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_prod_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (g:Group) WHERE g.name =~ '.*((?i)prod).*' RETURN g.name ORDER BY g.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g.name"] is not None:
                            print(f'{log.default}Prod group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None:
                                print(f'{log.default}Prod group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'{r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None:
                                print(f'{log.default}Prod group {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'Prod group {r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_prod_users(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (u:User) WHERE u.name =~ '.*((?i)prod).*' RETURN u.name ORDER BY u.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None:
                            print(f'{log.default}Prod user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}Prod user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                                file.write(f'{r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}Prod user {log.reset}{log.red}{r["u.name"]}{log.reset}')
                                file.write(f'Prod user {r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_prod_computers(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (c:Computer) WHERE c.name =~ '.*((?i)prod).*' RETURN c.name ORDER BY c.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["c.name"] is not None:
                            print(f'{log.default}Prod computer {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Prod computer {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Prod computer {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'Prod computer {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_domain_admins(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" WITH n MATCH p=(n)<-[r:MemberOf*1..]-(m) RETURN m.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is MemberOf Domain Admins{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is MemberOf Domain Admins{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is MemberOf Domain Admins{log.reset}')
                                file.write(f'User {r["m.name"]} is MemberOf Domain Admins\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_user_sp_to_das(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_das_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND m.name =~ \'((?i)' + self.user_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_group_sp_to_das(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_das_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND NOT m=n AND m.name =~ \'((?i)' + self.group_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_computer_sp_to_das(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_das_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND m.name =~ \'((?i)' + self.computer_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_enterprise_admins(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" WITH n MATCH p=(n)<-[r:MemberOf*1..]-(m) RETURN m.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is MemberOf Enterprise Admins{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is MemberOf Enterprise Admins{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is MemberOf Enterprise Admins{log.reset}')
                                file.write(f'User {r["m.name"]} is MemberOf Enterprise Admins\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_user_sp_to_eas(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_eas_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND m.name =~ \'((?i)' + self.user_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_group_sp_to_eas(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_eas_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND NOT m=n AND m.name =~ \'((?i)' + self.group_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_computer_sp_to_eas(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_eas_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND m.name =~ \'((?i)' + self.computer_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_user_sp_to_high_value(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (m:User),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_high_value_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (m:User),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n AND m.name =~ \'((?i)' + self.user_search + ')\' return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_group_sp_to_high_value(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (m:Group),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_high_value_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (m:Group),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n AND m.name =~ \'((?i)' + self.group_search + ')\' return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_computer_sp_to_high_value(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (m:Computer),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_high_value_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (m:Computer),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n AND m.name =~ \'((?i)' + self.computer_search + ')\' return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_user_sp_to_exchange_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_exchange_groups_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND m.name =~ \'((?i)' + self.user_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_group_sp_to_exchange_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_exchange_groups_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND NOT m=n AND m.name =~ \'((?i)' + self.group_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_computer_sp_to_exchange_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_exchange_groups_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND m.name =~ \'((?i)' + self.computer_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_user_sp_to_sql_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_sql_groups_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND m.name =~ \'((?i)' + self.user_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_group_sp_to_sql_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_sql_groups_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND NOT m=n AND m.name =~ \'((?i)' + self.group_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_computer_sp_to_sql_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_sql_groups_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND m.name =~ \'((?i)' + self.computer_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_user_sp_to_web_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_web_groups_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND m.name =~ \'((?i)' + self.user_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_group_sp_to_web_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_web_groups_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND NOT m=n AND m.name =~ \'((?i)' + self.group_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_computer_sp_to_web_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_web_groups_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND m.name =~ \'((?i)' + self.computer_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_user_sp_to_admin_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_admin_groups_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND m.name =~ \'((?i)' + self.user_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_group_sp_to_admin_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_admin_groups_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND NOT m=n AND m.name =~ \'((?i)' + self.group_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_computer_sp_to_admin_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_admin_groups_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND m.name =~ \'((?i)' + self.computer_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_user_sp_to_service_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_service_groups_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND m.name =~ \'((?i)' + self.user_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_sp_to_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m)-[r*1..]->(n:User)) WHERE n.name =~ \'((?i)' + self.user_search + ')\' AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_sp_to_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m)-[r*1..]->(n:Group)) WHERE n.name =~ \'((?i)' + self.group_search + ')\' AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_sp_to_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m)-[r*1..]->(n:Computer)) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_group_sp_to_service_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_service_groups_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND NOT m=n AND m.name =~ \'((?i)' + self.group_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_computer_sp_to_service_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_service_groups_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND m.name =~ \'((?i)' + self.computer_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_user_sp_to_dcs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_dcs_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND m.name =~ \'((?i)' + self.user_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                           
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_group_sp_to_dcs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_dcs_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND NOT m=n AND m.name =~ \'((?i)' + self.group_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_all_computer_sp_to_dcs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sp_to_dcs_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND m.name =~ \'((?i)' + self.computer_search + ')\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    p_count = 1
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""       
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            n_count += 1
                                print(final)
                                p_count += 1
                        count += 1
                else:
                    count = 0
                    p_count = 1
                    file = open(f, 'w+')
                    for r in results:
                        if r["m.name"] is not None and r["p"] is not None:
                            path = r["p"]
                            if path.start_node["name"] is not None and path.end_node["name"] is not None:
                                n_count = 0                            
                                p_len = len(path)
                                final = ""
                                final_w = ""      
                                mid_len = len(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                print(f'{log.default}*Path {log.reset}{log.red}{p_count}{log.reset}{log.default}* {log.reset}{log.red}{path.start_node["name"]}{log.reset}{log.default} -> {log.reset}{log.red}{path.end_node["name"]}{log.reset}{log.default}*{log.reset}')
                                print(f'{log.default}*' * mid_len + f'{log.reset}')
                                file.write('*' * mid_len + '\n')
                                file.write(f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*\n')
                                file.write('*' * mid_len + '\n')
                                for rel in path:
                                    if rel.start_node["name"] is not None and rel.end_node["name"] is not None:
                                        s_labels = list(rel.start_node.labels)
                                        e_labels = list(rel.end_node.labels)
                                        if n_count != p_len - 1:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}) and {log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]}) and '
                                            n_count += 1
                                        else:
                                            final += f'{log.red}{rel.start_node["name"]}{log.reset}{log.default} ({s_labels[0]}/{s_labels[1]}) has {log.red}{rel.type}{log.reset} over {log.reset}{log.red}{rel.end_node["name"]} {log.reset}{log.default}({e_labels[0]}/{e_labels[1]}){log.reset}'
                                            final_w += f'{rel.start_node["name"]} ({s_labels[0]}/{s_labels[1]}) has {rel.type} over {rel.end_node["name"]} ({e_labels[0]}/{e_labels[1]})'
                                            n_count += 1
                                print(final)
                                file.write(final_w + '\n')
                                p_count += 1
                        count += 1
                    util.handle_export(file, count, f)

    def find_sessions(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(m:Computer)-[r:HasSession]->(n:User) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} HasSession on {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_asrep_roastable(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (u:User {dontreqpreauth: true}) RETURN u.name ORDER BY u.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is AS-REP roastable{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is AS-REP roastable{log.reset}')
                                file.write(f'{r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is AS-REP roastable{log.reset}')
                                file.write(f'User {r["u.name"]} is AS-REP roastable\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_highvalue_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (m:Group {highvalue:true}) RETURN m.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is high value{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is high value{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is high value{log.reset}')
                                file.write(f'Group {r["m.name"]} is high value\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_highvalue_members(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:User)-[r:MemberOf*1..]->(m:Group {highvalue:true}) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf high value group {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf high value group {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf high value group {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} is MemberOf high value group {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_localadmin(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(m:User)-[r:AdminTo]->(n:Computer) RETURN m.name, n.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'User {r["m.name"]} is AdminTo {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_localadmin(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(m:Group)-[r:AdminTo]->(n:Computer) RETURN m.name,n.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'Group {r["m.name"]} is AdminTo {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_laps(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:User)-[r:ReadLAPSPassword]->(m:Computer) RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can read LAPS passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_laps(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Group)-[r:ReadLAPSPassword]->(m:Computer) RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can read LAPS passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_laps(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Computer)-[r:ReadLAPSPassword]->(m:Computer) RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can read LAPS passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
    
    def find_user_sync_laps(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:User)-[r:SyncLAPSPassword]->(m:Computer) RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can sync LAPS passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
    
    def find_group_sync_laps(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Group)-[r:SyncLAPSPassword]->(m:Computer) RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can sync LAPS passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_sync_laps(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Computer)-[r:SyncLAPSPassword]->(m:Computer) RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can sync LAPS passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_da_sessions(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (n:User)-[:MemberOf*1..]->(g:Group) WHERE g.objectid ENDS WITH '-512' MATCH p = (c:Computer)-[:HasSession]->(n) return n.name,c.name ORDER BY n.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}Domain admin {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Domain admin {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Domain admin {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'Domain admin {r["n.name"]} HasSession on {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_ea_sessions(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (n:User)-[:MemberOf*1..]->(g:Group) WHERE g.objectid ENDS WITH '-519' MATCH p = (c:Computer)-[:HasSession]->(n) return n.name,c.name ORDER BY n.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}Enterprise admin {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Enterprise admin {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Enterprise admin {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'Enterprise admin {r["n.name"]} HasSession on {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_users(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (n:User) return n.name ORDER BY n.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_groups(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (n:Group) return n.name ORDER BY n.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_computers(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (n:Computer) return n.name ORDER BY n.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_enabled_computers(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (n:Computer {enabled:TRUE}) return n.name ORDER BY n.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is enabled{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is enabled{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is enabled{log.reset}')
                                file.write(f'Computer {r["n.name"]} is enabled\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_disabled_computers(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (n:Computer {enabled:FALSE}) return n.name ORDER BY n.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is disabled{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is disabled{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is disabled{log.reset}')
                                file.write(f'Computer {r["n.name"]} is disabled\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_dcs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" WITH n MATCH p=(n)<-[r:MemberOf*1..]-(m) RETURN m.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is a Domain Controller{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is a Domain Controller{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is a Domain Controller{log.reset}')
                                file.write(f'Computer {r["m.name"]} is a Domain Controller\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_dcs_oss(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" WITH n MATCH p=(n)<-[r:MemberOf*1..]-(m) RETURN m.name,m.operatingsystem ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["m.operatingsystem"] is not None:
                            print(f'{log.default}Domain Controller {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} OS {log.reset}{log.red}{r["m.operatingsystem"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["m.operatingsystem"] is not None:
                                print(f'{log.default}Domain Controller {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} OS {log.reset}{log.red}{r["m.operatingsystem"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["m.operatingsystem"] is not None:
                                print(f'{log.default}Domain Controller {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} OS {log.reset}{log.red}{r["m.operatingsystem"]}{log.reset}')
                                file.write(f'Domain Controller {r["m.name"]} OS {r["m.operatingsystem"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_password_not_reqd(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User {passwordnotreqd:true}) return n.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is not required to have a password{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is not required to have a password{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is not required to have a password{log.reset}')
                                file.write(f'User {r["n.name"]} is not required to have a password\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_constrained(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (u:User)-[:AllowedToDelegate]->(c:Computer) RETURN u.name,c.name ORDER BY u.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'User {r["u.name"]} is allowed to delegate for {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_constrained(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (g:Group)-[:AllowedToDelegate]->(c:Computer) RETURN g.name,c.name ORDER BY g.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'Group {r["g.name"]} is allowed to delegate for {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_constrained(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (c1:Computer)-[:AllowedToDelegate]->(c2:Computer) RETURN c1.name,c2.name ORDER BY c1.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["c1.name"] is not None and r["c2.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["c1.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c2.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c1.name"] is not None and r["c2.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["c1.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c2.name"]}{log.reset}')
                                file.write(f'{r["c2.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c1.name"] is not None and r["c2.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["c1.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c2.name"]}{log.reset}')
                                file.write(f'Computer {r["c1.name"]} is allowed to delegate for {r["c2.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_gpos(self, f, raw):
        with self.driver.session() as session:
            results = session.run('Match (n:GPO) return n.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}GPO {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}GPO {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}GPO {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'GPO {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_domains(self, f, raw):
        with self.driver.session() as session:
            results = session.run('Match (n:Domain) return n.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}Domain {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Domain {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Domain {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'Domain {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_domain_trusts(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Domain)-[r:TrustedBy]->(m:Domain) RETURN r.trusttype,n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None and r["r.trusttype"] is not None:
                            print(f'{log.default}Domain {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is trusted by {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}with type {log.reset}{log.red}{r["r.trusttype"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None and r["r.trusttype"] is not None:
                                print(f'{log.default}Domain {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is trusted by {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}with type {log.reset}{log.red}{r["r.trusttype"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None and r["r.trusttype"] is not None:
                                print(f'{log.default}Domain {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is trusted by {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}with type {log.reset}{log.red}{r["r.trusttype"]}{log.reset}')
                                file.write(f'Domain {r["n.name"]} is trusted by {r["m.name"]} with type {r["r.trusttype"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_laps_enabled(self, f, raw):
        with self.driver.session() as session:
            results = session.run('Match (c:Computer) WHERE c.haslaps = true return c.name ORDER BY c.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["c.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["c.name"]}{log.reset}{log.default} has LAPS enabled{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["c.name"]}{log.reset}{log.default} has LAPS enabled{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["c.name"]}{log.reset}{log.default} has LAPS enabled{log.reset}')
                                file.write(f'Computer {r["c.name"]} has LAPS enabled\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_laps_disabled(self, f, raw):
        with self.driver.session() as session:
            results = session.run('Match (c:Computer) WHERE c.haslaps = false return c.name ORDER BY c.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["c.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["c.name"]}{log.reset}{log.default} has LAPS disabled{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["c.name"]}{log.reset}{log.default} has LAPS disabled{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["c.name"]}{log.reset}{log.default} has LAPS disabled{log.reset}')
                                file.write(f'Computer {r["c.name"]} has LAPS disabled\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_description_pwds(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (u:User) WHERE u.description =~ '.*(pass|pw|:).*' return u.name,u.description ORDER BY u.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None and r["u.description"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} may have password in description {log.reset}{log.red}{r["u.description"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None and r["u.description"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} may have password in description {log.reset}{log.red}{r["u.description"]}{log.reset}')
                                file.write(f'{r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None and r["u.description"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} may have password in description {log.reset}{log.red}{r["u.description"]}{log.reset}')
                                file.write(f'User {r["u.name"]} may have password in description {r["u.description"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_highvalue_users(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (m:User {highvalue:true}) RETURN m.name ORDER BY m.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is high value{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is high value{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is high value{log.reset}')
                                file.write(f'User {r["m.name"]} is high value\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_sensitive_users(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (m:User {sensitive:true}) RETURN m.name ORDER BY m.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is sensitive{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is sensitive{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is sensitive{log.reset}')
                                file.write(f'User {r["m.name"]} is sensitive\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_admincount(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (m:Group {admincount:true}) return m.name ORDER BY m.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} has an admin count{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} has an admin count{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} has an admin count{log.reset}')
                                file.write(f'Group {r["m.name"]} has an admin count\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_admincount(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (m:User {admincount:true}) return m.name ORDER BY m.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} has an admin count{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} has an admin count{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} has an admin count{log.reset}')
                                file.write(f'User {r["m.name"]} has an admin count\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_admincount(self, f, raw):
        with self.driver.session() as session:
            results = session.run("MATCH (m:Computer {admincount:true}) return m.name ORDER BY m.name")
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} has an admin count{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} has an admin count{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} has an admin count{log.reset}')
                                file.write(f'Computer {r["m.name"]} has an admin count\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_localadmin(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(m:Computer)-[r:AdminTo]->(n:Computer) RETURN m.name,n.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'Computer {r["m.name"]} is AdminTo {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_gmsa(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:User)-[r:ReadGMSAPassword]->(m:User) RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can read GMSA passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_gmsa(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Group)-[r:ReadGMSAPassword]->(m:User) RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can read GMSA passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_gmsa(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Computer)-[r:ReadGMSAPassword]->(m:User) RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can read GMSA passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_dcsync(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:DCSync]->(m:Domain) RETURN n.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges{log.reset}')
                                file.write(f'User {r["n.name"]} has DCSync privileges\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_dcsync(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:DCSync]->(m:Domain) RETURN n.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges{log.reset}')
                                file.write(f'Group {r["n.name"]} has DCSync privileges\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_dcsync(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:DCSync]->(m:Domain) RETURN n.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges{log.reset}')
                                file.write(f'Computer {r["n.name"]} has DCSync privileges\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_dcsync(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n)-[r:DCSync]->(m:Domain) RETURN n.name,labels(n) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges{log.reset}')
                                file.write(f'({r["labels(n)"][0]}/{r["labels(n)"][1]}) {r["n.name"]} has DCSync privileges\n')
                                count += 1
                        util.handle_export(file, count, f)                        

    def find_user_force_change_pwd(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:ForceChangePassword]->(m:User) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can force change password for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_force_change_pwd(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:ForceChangePassword]->(m:User) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can force change password for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_force_change_pwd(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:ForceChangePassword]->(m:User) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can force change password for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_add_member(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:AddMember]->(m:Group) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can add members to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_add_member(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:AddMember]->(m:Group) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can add members to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_add_member(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:AddMember]->(m:Group) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can add members to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_add_self(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:AddSelf]->(m:Group) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can add itself to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_add_self(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:AddSelf]->(m:Group) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can add itself to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_add_self(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:AddSelf]->(m:Group) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can add itself to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_sql_admin(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:SQLAdmin]->(m:Computer) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} is SQLAdmin to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_sql_admin(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:SQLAdmin]->(m:Computer) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} is SQLAdmin to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_sql_admin(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:SQLAdmin]->(m:Computer) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} is SQLAdmin to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_ps_remote(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:CanPSRemote]->(m:Computer) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can PSRemote to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_ps_remote(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:CanPSRemote]->(m:Computer) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can PSRemote to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_ps_remote(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:CanPSRemote]->(m:Computer) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can PSRemote to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_exec_dcom(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:ExecuteDCOM]->(m:Computer) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can ExecuteDCOM on {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_exec_dcom(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:ExecuteDCOM]->(m:Computer) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can ExecuteDCOM on {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_exec_dcom(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:ExecuteDCOM]->(m:Computer) RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can ExecuteDCOM on {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_allowed_to_act(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:AllowedToAct]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} is AllowedToAct for {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_allowed_to_act(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:AllowedToAct]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} is AllowedToAct for {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_allowed_to_act(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:AllowedToAct]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} is AllowedToAct for {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_owns(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:Owns]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} Owns {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_owns(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:Owns]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} Owns {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_owns(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:Owns]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} Owns {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_all_extended(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:AllExtendedRights]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has AllExtendedRights over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_all_extended(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:AllExtendedRights]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has AllExtendedRights over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_all_extended(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:AllExtendedRights]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has AllExtendedRights over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_member_of(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:MemberOf]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} is MemberOf {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_member_of(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:MemberOf]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} is MemberOf {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_member_of(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:MemberOf]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} is MemberOf {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_add_key_cred_link(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:AddKeyCredentialLink]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has AddKeyCredentialLink over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_add_key_cred_link(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:AddKeyCredentialLink]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has AddKeyCredentialLink over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_add_key_cred_link(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:AddKeyCredentialLink]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has AddKeyCredentialLink over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_generic_all(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:GenericAll]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has GenericAll over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_generic_all(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:GenericAll]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has GenericAll over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_generic_all(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:GenericAll]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has GenericAll over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_write_dacl(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:WriteDacl]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has WriteDacl over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_write_dacl(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:WriteDacl]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has WriteDacl over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_write_dacl(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:WriteDacl]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has WriteDacl over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_write_owner(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:WriteOwner]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has WriteOwner over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_write_owner(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:WriteOwner]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has WriteOwner over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_write_owner(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:WriteOwner]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has WriteOwner over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_generic_write(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:GenericWrite]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has GenericWrite over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_generic_write(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:GenericWrite]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has GenericWrite over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computer_generic_write(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:GenericWrite]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has GenericWrite over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_user_descriptions(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (u:User) return u.name,u.description ORDER BY u.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.description"] is not None and r["u.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["u.description"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.description"] is not None and r["u.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["u.description"]}{log.reset}')
                                file.write(f'{r["u.description"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.description"] is not None and r["u.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["u.description"]}{log.reset}')
                                file.write(f'User {r["u.name"]} description {r["u.description"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_group_descriptions(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (g:Group) return g.name,g.description ORDER BY g.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g.description"] is not None and r["g.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["g.description"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.description"] is not None and r["g.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["g.description"]}{log.reset}')
                                file.write(f'{r["g.description"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.description"] is not None and r["g.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["g.description"]}{log.reset}')
                                file.write(f'Group {r["g.name"]} description {r["g.description"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_emails(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (u:User) return u.name,u.email ORDER BY u.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.email"] is not None and r["u.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} email {log.reset}{log.red}{r["u.email"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.email"] is not None and r["u.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} email {log.reset}{log.red}{r["u.email"]}{log.reset}')
                                file.write(f'{r["u.email"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.email"] is not None and r["u.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} email {log.reset}{log.red}{r["u.email"]}{log.reset}')
                                file.write(f'User {r["u.name"]} email {r["u.email"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_ous(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (o:OU) RETURN o.name ORDER BY o.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["o.name"] is not None:
                            print(f'{log.default}OU {log.reset}{log.red}{r["o.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["o.name"] is not None:
                                print(f'{log.default}OU {log.reset}{log.red}{r["o.name"]}{log.reset}')
                                file.write(f'{r["o.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["o.name"] is not None:
                                print(f'{log.default}OU {log.reset}{log.red}{r["o.name"]}{log.reset}')
                                file.write(f'OU {r["o.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_containers(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (c:Container) return c.name ORDER BY c.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["c.name"] is not None:
                            print(f'{log.default}Container {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Container {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None:
                                print(f'{log.default}Container {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'Container {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_domains(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (d:Domain) return d.name ORDER BY d.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["d.name"] is not None:
                            print(f'{log.default}Domain {log.reset}{log.red}{r["d.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["d.name"] is not None:
                                print(f'{log.default}Domain {log.reset}{log.red}{r["d.name"]}{log.reset}')
                                file.write(f'{r["d.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["d.name"] is not None:
                                print(f'{log.default}Domain {log.reset}{log.red}{r["d.name"]}{log.reset}')
                                file.write(f'Domain {r["d.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_domains_flevel(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (d:Domain) return d.name,d.functionallevel ORDER BY d.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["d.name"] is not None and r["d.functionallevel"] is not None:
                            print(f'{log.default}Domain {log.reset}{log.red}{r["d.name"]}{log.reset}{log.default} functional level {log.reset}{log.red}{r["d.functionallevel"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["d.name"] is not None and r["d.functionallevel"] is not None:
                                print(f'{log.default}Domain {log.reset}{log.red}{r["d.name"]}{log.reset}{log.default} functional level {log.reset}{log.red}{r["d.functionallevel"]}{log.reset}')
                                file.write(f'{r["d.functionallevel"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["d.name"] is not None and r["d.functionallevel"] is not None:
                                print(f'{log.default}Domain {log.reset}{log.red}{r["d.name"]}{log.reset}{log.default} functional level {log.reset}{log.red}{r["d.functionallevel"]}{log.reset}')
                                file.write(f'Domain {r["d.name"]} functional level {r["d.functionallevel"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_rdp_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('match p=(u:User)-[:CanRDP]->(c:Computer) WHERE u.name =~ \'((?i)' + self.user_search + ')\' return u.name,c.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'User {r["u.name"]} CanRDP to {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_rdp_gd_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[:MemberOf]->(m:Group),(m)-[:CanRDP]->(c:Computer) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN DISTINCT n.name,m.name,c.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which CanRDP to {log.red}{r["c.name"]}{log.default}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which CanRDP to {log.red}{r["c.name"]}{log.default}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which CanRDP to {log.red}{r["c.name"]}{log.default}{log.reset}')
                                file.write(f'User {r["n.name"]} is MemberOf {r["m.name"]} which CanRDP to {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_localadmin_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(m:User)-[r:AdminTo]->(n:Computer) WHERE m.name =~ \'((?i)' + self.user_search + ')\' RETURN m.name, n.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'User {r["m.name"]} is AdminTo {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_localadmin_gd_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[:MemberOf]->(m:Group),(m)-[:AdminTo]->(c:Computer) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN DISTINCT n.name,m.name,c.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} which is AdminTo {log.red}{r["c.name"]}{log.default}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} which is AdminTo {log.red}{r["c.name"]}{log.default}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} which is AdminTo {log.red}{r["c.name"]}{log.default}{log.reset}')
                                file.write(f'User {r["n.name"]} is MemberOf {r["m.name"]} which is AdminTo {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_sessions_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(m:Computer)-[r:HasSession]->(n:User) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} HasSession on {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_laps_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:User)-[r:ReadLAPSPassword]->(m:Computer) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can read LAPS passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_sync_laps_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:User)-[r:SyncLAPSPassword]->(m:Computer) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can sync LAPS passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_gmsa_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:User)-[r:ReadGMSAPassword]->(m:User) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can read GMSA passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_constrained_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (u:User)-[:AllowedToDelegate]->(c:Computer) WHERE u.name =~ \'((?i)' + self.user_search + ')\' RETURN u.name,c.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'User {r["u.name"]} is allowed to delegate for {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_force_change_pwd_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:ForceChangePassword]->(m:User) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can force change password for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_add_member_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:AddMember]->(m:Group) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can add members to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_add_self_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:AddSelf]->(m:Group) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can add itself to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_sql_admin_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:SQLAdmin]->(m:Computer) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} is SQLAdmin to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_ps_remote_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:CanPSRemote]->(m:Computer) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can PSRemote to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_exec_dcom_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:ExecuteDCOM]->(m:Computer) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]} can ExecuteDCOM on {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_allowed_to_act_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:AllowedToAct]->(m) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} is AllowedToAct for {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_owns_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:Owns]->(m) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} Owns {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_extended_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:AllExtendedRights]->(m) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has AllExtendedRights over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_add_key_cred_link_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:AddKeyCredentialLink]->(m) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has AddKeyCredentialLink over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_generic_all_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:GenericAll]->(m) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has GenericAll over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_write_dacl_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:WriteDacl]->(m) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has WriteDacl over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_write_owner_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:WriteOwner]->(m) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has WriteOwner over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_generic_write_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:GenericWrite]->(m) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has GenericWrite over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_description_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (u:User) WHERE u.name =~ \'((?i)' + self.user_search + ')\' RETURN u.name,u.description ORDER BY u.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.description"] is not None and r["u.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["u.description"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.description"] is not None and r["u.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["u.description"]}{log.reset}')
                                file.write(f'{r["u.description"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.description"] is not None and r["u.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["u.description"]}{log.reset}')
                                file.write(f'User {r["u.name"]} description {r["u.description"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_email_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (u:User) WHERE u.name =~ \'((?i)' + self.user_search + ')\' return u.name,u.email ORDER BY u.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.email"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} email {log.reset}{log.red}{r["u.email"]}{log.reset}')
                            count += 1                       
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.email"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} email {log.reset}{log.red}{r["u.email"]}{log.reset}')
                                file.write(f'{r["u.email"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.email"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} email {log.reset}{log.red}{r["u.email"]}{log.reset}')
                                file.write(f'User {r["u.name"]} email {r["u.email"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_member_of_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r:MemberOf]->(m) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} is MemberOf {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_asrep_roastable_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (u:User {dontreqpreauth: true}) WHERE u.name =~ \'((?i)' + self.user_search + ')\' RETURN u.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["u.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is AS-REP roastable{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is AS-REP roastable{log.reset}')
                                file.write(f'{r["u.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["u.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is AS-REP roastable{log.reset}')
                                file.write(f'User {r["u.name"]} is AS-REP roastable\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_kerberoastable_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User) WHERE n.hasspn=true AND n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name AS result ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["result"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["result"]}{log.reset}{log.default} is kerberoastable{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["result"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["result"]}{log.reset}{log.default} is kerberoastable{log.reset}')
                                file.write(f'{r["result"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["result"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["result"]}{log.reset}{log.default} is kerberoastable{log.reset}')
                                file.write(f'User {r["result"]} is kerberoastable\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_ou_oc(self, f, raw):
        with self.driver.session() as session:
            results = session.run('match (n)-[r:Owns|AllExtendedRights|WriteDacl|GenericAll|WriteOwner|GenericWrite]->(o:OU) return n.name,o.name,TYPE(r),labels(n) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["o.name"] is not None:
                            print(f'({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]} {log.reset}{log.default}has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over OU {log.reset}{log.red}{r["o.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["o.name"] is not None:
                                print(f'({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]} {log.reset}{log.default}has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over OU {log.reset}{log.red}{r["o.name"]}{log.reset}')
                                file.write(f'{r["o.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["o.name"] is not None:
                                print(f'({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]} {log.reset}{log.default}has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over OU {log.reset}{log.red}{r["o.name"]}{log.reset}')
                                file.write(f'({r["labels(n)"][0]}/{r["labels(n)"][1]}) {r["n.name"]} has {r["TYPE(r)"]} over OU {r["o.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_container_oc(self, f, raw):
        with self.driver.session() as session:
            results = session.run('match (n)-[r:Owns|AllExtendedRights|WriteDacl|GenericAll|WriteOwner|GenericWrite]->(c:Container) return n.name,c.name,TYPE(r),labels(n) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]} {log.reset}{log.default}has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over Container {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]} {log.reset}{log.default}has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over Container {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]} {log.reset}{log.default}has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over Container {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'({r["labels(n)"][0]}/{r["labels(n)"][1]}) {r["n.name"]} has {r["TYPE(r)"]} over Container {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_gpo_oc(self, f, raw):
        with self.driver.session() as session:
            results = session.run('match (n)-[r:Owns|AllExtendedRights|WriteDacl|GenericAll|WriteOwner|GenericWrite]->(g:GPO) return n.name,g.name,TYPE(r),labels(n) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["g.name"] is not None:
                            print(f'({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]} {log.reset}{log.default}has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over GPO {log.reset}{log.red}{r["g.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["g.name"] is not None:
                                print(f'({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]} {log.reset}{log.default}has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over GPO {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'{r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["g.name"] is not None:
                                print(f'({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]} {log.reset}{log.default}has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over GPO {log.reset}{log.red}{r["g.name"]}{log.reset}')
                                file.write(f'({r["labels(n)"][0]}/{r["labels(n)"][1]}) {r["n.name"]} has {r["TYPE(r)"]} over GPO {r["g.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r]->(m) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has {r["TYPE(r)"]} over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_gd_us(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[:MemberOf]->(m:Group),(m)-[r]->(v) WHERE n.name =~ \'((?i)' + self.user_search + ')\' RETURN n.name,TYPE(r),labels(v),m.name,v.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["m.name"] is not None and r["v.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["v.name"]} {log.reset}{log.default}({r["labels(v)"][0]}/{r["labels(v)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None and r["v.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["v.name"]} {log.reset}{log.default}({r["labels(v)"][0]}/{r["labels(v)"][1]}){log.reset}')
                                file.write(f'{r["v.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["m.name"] is not None and r["v.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["v.name"]} {log.reset}{log.default}({r["labels(v)"][0]}/{r["labels(v)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} is MemberOf {r["m.name"]} which has {r["TYPE(r)"]} over {r["v.name"]} ({r["labels(v)"][0]}/{r["labels(v)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_gp_links(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (g1)-[:GPLink]->(g2) RETURN g1.name,g2.name,labels(g2) ORDER BY g1.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g1.name"] is not None and r["g2.name"] is not None:
                            print(f'{log.default}GPO {log.reset}{log.red}{r["g1.name"]}{log.reset}{log.default} is linked to {log.reset}{log.red}{r["g2.name"]}{log.reset}{log.default} ({r["labels(g2)"][0]}/{r["labels(g2)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g1.name"] is not None and r["g2.name"] is not None:
                                print(f'{log.default}GPO {log.reset}{log.red}{r["g1.name"]}{log.reset}{log.default} is linked to {log.reset}{log.red}{r["g2.name"]}{log.reset}{log.default} ({r["labels(g2)"][0]}/{r["labels(g2)"][1]}){log.reset}')
                                file.write(f'{r["g2.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g1.name"] is not None and r["g2.name"] is not None:
                                print(f'{log.default}GPO {log.reset}{log.red}{r["g1.name"]}{log.reset}{log.default} is linked to {log.reset}{log.red}{r["g2.name"]}{log.reset}{log.default} ({r["labels(g2)"][0]}/{r["labels(g2)"][1]}){log.reset}')
                                file.write(f'GPO {r["g1.name"]} is linked to {r["g2.name"]} ({r["labels(g2)"][0]}/{r["labels(g2)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_user_privs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User)-[r]->(m) RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'User {r["n.name"]} has {r["TYPE(r)"]} over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_group_privs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r]->(m) RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has {r["TYPE(r)"]} over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_computer_privs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r]->(m) RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has {r["TYPE(r)"]} over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_rdp_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('match p=(g:Group)-[:CanRDP]->(c:Computer) WHERE g.name =~ \'((?i)' + self.group_search + ')\' return g.name,c.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'Group {r["g.name"]} CanRDP to {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_rdp_gd_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[:MemberOf]->(m:Group),(m)-[:CanRDP]->(c:Computer) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN DISTINCT n.name,m.name,c.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["c.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which CanRDP to {log.red}{r["c.name"]}{log.default}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["c.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which CanRDP to {log.red}{r["c.name"]}{log.default}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["c.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which CanRDP to {log.red}{r["c.name"]}{log.default}{log.reset}')
                                file.write(f'Group {r["n.name"]} is MemberOf {r["m.name"]} which CanRDP to {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_localadmin_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(m:Group)-[r:AdminTo]->(n:Computer) WHERE m.name =~ \'((?i)' + self.group_search + ')\' RETURN m.name, n.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'Group {r["m.name"]} is AdminTo {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_localadmin_gd_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[:MemberOf]->(m:Group),(m)-[:AdminTo]->(c:Computer) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN DISTINCT n.name,m.name,c.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["c.name"] is not None and r["m.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} which is AdminTo {log.red}{r["c.name"]}{log.default}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["c.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} which is AdminTo {log.red}{r["c.name"]}{log.default}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["c.name"] is not None and r["m.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} which is AdminTo {log.red}{r["c.name"]}{log.default}{log.reset}')
                                file.write(f'Group {r["n.name"]} is MemberOf {r["m.name"]} which is AdminTo {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_laps_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Group)-[r:ReadLAPSPassword]->(m:Computer) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can read LAPS passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_sync_laps_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Group)-[r:SyncLAPSPassword]->(m:Computer) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can sync LAPS passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_gmsa_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Group)-[r:ReadGMSAPassword]->(m:User) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can read GMSA passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_constrained_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (g:Group)-[:AllowedToDelegate]->(c:Computer) WHERE g.name =~ \'((?i)' + self.group_search + ')\' RETURN g.name,c.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'Group {r["g.name"]} is allowed to delegate for {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_force_change_pwd_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:ForceChangePassword]->(m:User) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can force change password for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_add_member_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:AddMember]->(m:Group) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can add members to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_add_self_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:AddSelf]->(m:Group) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can add itself to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_sql_admin_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:SQLAdmin]->(m:Computer) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} is SQLAdmin to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_ps_remote_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:CanPSRemote]->(m:Computer) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can PSRemote to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_exec_dcom_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:ExecuteDCOM]->(m:Computer) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} can ExecuteDCOM on {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_allowed_to_act_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:AllowedToAct]->(m) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} is AllowedToAct for {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_owns_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:Owns]->(m) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} Owns {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_extended_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:AllExtendedRights]->(m) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has AllExtendedRights over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_add_key_cred_link_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:AddKeyCredentialLink]->(m) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has AddKeyCredentialLink over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_generic_all_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:GenericAll]->(m) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has GenericAll over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_write_dacl_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:WriteDacl]->(m) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has WriteDacl over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_write_owner_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:WriteOwner]->(m) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has WriteOwner over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_generic_write_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:GenericWrite]->(m) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has GenericWrite over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_description_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (g:Group) WHERE g.name =~ \'((?i)' + self.group_search + ')\' RETURN g.name,g.description ORDER BY g.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["g.description"] is not None and r["g.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["g.description"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.description"] is not None and r["g.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["g.description"]}{log.reset}')
                                file.write(f'{r["g.description"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["g.description"] is not None and r["g.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["g.description"]}{log.reset}')
                                file.write(f'Group {r["g.name"]} description {r["g.description"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_member_of_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:MemberOf]->(m) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} is MemberOf {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_members_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n)-[r:MemberOf]->(m) WHERE m.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.red}{r["n.name"]}{log.reset}{log.default} ({r["labels(n)"][0]}/{r["labels(n)"][1]}) is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.red}{r["n.name"]}{log.reset}{log.default} ({r["labels(n)"][0]}/{r["labels(n)"][1]}) is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.red}{r["n.name"]}{log.reset}{log.default} ({r["labels(n)"][0]}/{r["labels(n)"][1]}) is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["n.name"]} ({r["labels(n)"][0]}/{r["labels(n)"][1]}) is MemberOf {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[r:AdminTo|HasSession|ForceChangePassword|AddMember|AddSelf|CanPSRemote|ExecuteDCOM|SQLAdmin|AllowedToDelegate|GenericAll|GenericWrite|WriteDacl|Owns|AddKeyCredentialLink|ReadLAPSPassword|ReadGMSAPassword|AllExtendedRights|AllowedToAct]->(m) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} has {r["TYPE(r)"]} over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_gd_gs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group)-[:MemberOf]->(m:Group),(m)-[r]->(v) WHERE n.name =~ \'((?i)' + self.group_search + ')\' RETURN n.name,TYPE(r),labels(v),m.name,v.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None and r["v.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["v.name"]} {log.reset}{log.default}({r["labels(v)"][0]}/{r["labels(v)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None and r["v.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["v.name"]} {log.reset}{log.default}({r["labels(v)"][0]}/{r["labels(v)"][1]}){log.reset}')
                                file.write(f'{r["v.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None and r["v.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["v.name"]} {log.reset}{log.default}({r["labels(v)"][0]}/{r["labels(v)"][1]}){log.reset}')
                                file.write(f'Group {r["n.name"]} is MemberOf {r["m.name"]} which has {r["TYPE(r)"]} over {r["v.name"]} ({r["labels(v)"][0]}/{r["labels(v)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_localadmin_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(m:Computer)-[r:AdminTo]->(n:Computer) WHERE m.name =~ \'((?i)' + self.computer_search + ')\' RETURN m.name, n.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'Computer {r["m.name"]} is AdminTo {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_localadmin_gd_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[:MemberOf]->(m:Group),(m)-[:AdminTo]->(c:Computer) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN DISTINCT n.name,m.name,c.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None and r["c.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} which is AdminTo {log.red}{r["c.name"]}{log.default}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} which is AdminTo {log.red}{r["c.name"]}{log.default}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None and r["c.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} which is AdminTo {log.red}{r["c.name"]}{log.default}{log.reset}')
                                file.write(f'Computer {r["n.name"]} is MemberOf {r["m.name"]} which is AdminTo {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_laps_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Computer)-[r:ReadLAPSPassword]->(m:Computer) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can read LAPS passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_sync_laps_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Computer)-[r:SyncLAPSPassword]->(m:Computer) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can sync LAPS passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_gmsa_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH p=(n:Computer)-[r:ReadGMSAPassword]->(m:User) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name ORDER by n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can read GMSA passwords for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_constrained_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[:AllowedToDelegate]->(c:Computer) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,c.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["c.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'{r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["c.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} is allowed to delegate for {r["c.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_force_change_pwd_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:ForceChangePassword]->(m:User) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can force change password for {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_add_member_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:AddMember]->(m:Group) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can add members to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_add_self_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:AddSelf]->(m:Group) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can add itself to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_sql_admin_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:SQLAdmin]->(m:Computer) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} is SQLAdmin to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_ps_remote_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:CanPSRemote]->(m:Computer) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can PSRemote to {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_exec_dcom_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:ExecuteDCOM]->(m:Computer) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} can ExecuteDCOM on {r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_allowed_to_act_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:AllowedToAct]->(m) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} is AllowedToAct for {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_owns_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:Owns]->(m) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} Owns {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_extended_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:AllExtendedRights]->(m) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has AllExtendedRights over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_add_key_cred_link_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:AddKeyCredentialLink]->(m) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has AddKeyCredentialLink over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_generic_all_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:GenericAll]->(m) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has GenericAll over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_write_dacl_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:WriteDacl]->(m) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has WriteDacl over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_write_owner_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:WriteOwner]->(m) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has WriteOwner over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_generic_write_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:GenericWrite]->(m) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has GenericWrite over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_member_of_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r:MemberOf]->(m) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,m.name,labels(m) ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} is MemberOf {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[r]->(m) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'{r["m.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} has {r["TYPE(r)"]} over {r["m.name"]} ({r["labels(m)"][0]}/{r["labels(m)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_all_gd_cs(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer)-[:MemberOf]->(m:Group),(m)-[r]->(v) WHERE n.name =~ \'((?i)' + self.computer_search + ')\' RETURN n.name,TYPE(r),labels(v),m.name,v.name ORDER BY m.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["m.name"] is not None and r["n.name"] is not None and r["v.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["v.name"]} {log.reset}{log.default}({r["labels(v)"][0]}/{r["labels(v)"][1]}){log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None and r["v.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["v.name"]} {log.reset}{log.default}({r["labels(v)"][0]}/{r["labels(v)"][1]}){log.reset}')
                                file.write(f'{r["v.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["m.name"] is not None and r["n.name"] is not None and r["v.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["v.name"]} {log.reset}{log.default}({r["labels(v)"][0]}/{r["labels(v)"][1]}){log.reset}')
                                file.write(f'Computer {r["n.name"]} is MemberOf {r["m.name"]} which has {r["TYPE(r)"]} over {r["v.name"]} ({r["labels(v)"][0]}/{r["labels(v)"][1]})\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_groups_r(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group) WHERE n.name =~ \'' + self.regex + '\' RETURN n.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'Group {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_users_r(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User) WHERE n.name =~ \'' + self.regex + '\' RETURN n.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'User {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_computers_r(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer) WHERE n.name =~ \'' + self.regex + '\' RETURN n.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_u_descriptions_r(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:User) WHERE n.description =~ \'' + self.regex + '\' RETURN n.name,n.description ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["n.description"] is not None:
                            print(f'{log.default}User {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}description {log.reset}{log.red}{r["n.description"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["n.description"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}description {log.reset}{log.red}{r["n.description"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["n.description"] is not None:
                                print(f'{log.default}User {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}description {log.reset}{log.red}{r["n.description"]}{log.reset}')
                                file.write(f'User {r["n.name"]} description {r["n.description"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_g_descriptions_r(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Group) WHERE n.description =~ \'' + self.regex + '\' RETURN n.name,n.description ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["n.description"] is not None:
                            print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}description {log.reset}{log.red}{r["n.description"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["n.description"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}description {log.reset}{log.red}{r["n.description"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["n.description"] is not None:
                                print(f'{log.default}Group {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}description {log.reset}{log.red}{r["n.description"]}{log.reset}')
                                file.write(f'Group {r["n.name"]} description {r["n.description"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_oss_r(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Computer) WHERE n.operatingsystem =~ \'' + self.regex + '\' RETURN n.name,n.operatingsystem ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None and r["n.operatingsystem"] is not None:
                            print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}OS {log.reset}{log.red}{r["n.operatingsystem"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["n.operatingsystem"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}OS {log.reset}{log.red}{r["n.operatingsystem"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None and r["n.operatingsystem"] is not None:
                                print(f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}OS {log.reset}{log.red}{r["n.operatingsystem"]}{log.reset}')
                                file.write(f'Computer {r["n.name"]} OS {r["n.operatingsystem"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_gpos_r(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:GPO) WHERE n.name =~ \'' + self.regex + '\' RETURN n.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}GPO {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}GPO {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}GPO {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'GPO {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_containers_r(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:Container) WHERE n.name =~ \'' + self.regex + '\' RETURN n.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}Container {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Container {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}Container {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'Container {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)

    def find_ous_r(self, f, raw):
        with self.driver.session() as session:
            results = session.run('MATCH (n:OU) WHERE n.name =~ \'' + self.regex + '\' RETURN n.name ORDER BY n.name')
            if results.peek() is None:
                log.log_no_results()
            else:
                if f == "":
                    count = 0
                    for r in results:
                        if r["n.name"] is not None:
                            print(f'{log.default}OU {log.reset}{log.red}{r["n.name"]}{log.reset}')
                            count += 1
                    if count == 0:
                        log.log_no_results()
                else:
                    if not raw:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}OU {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'{r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)
                    else:
                        count = 0
                        file = open(f, 'w+')
                        for r in results:
                            if r["n.name"] is not None:
                                print(f'{log.default}OU {log.reset}{log.red}{r["n.name"]}{log.reset}')
                                file.write(f'OU {r["n.name"]}\n')
                                count += 1
                        util.handle_export(file, count, f)