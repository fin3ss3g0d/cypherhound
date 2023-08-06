from neo4j import GraphDatabase
import util
import log


class Driver:

    def __init__(self, user, password, db, u_search="", g_search="", c_search="", regex=""):
        try:
            self.driver = GraphDatabase.driver("neo4j://localhost:7687", auth=(user, password))
            self.database = db
            self.user_search = u_search
            self.group_search = g_search
            self.computer_search = c_search
            self.regex = regex
            self.queries = {
                '1': {
                    'query': 'MATCH (n:User) WHERE n.hasspn=true RETURN n.name AS result ORDER BY n.name',
                    'desc': 'List all kerberoastable users',
                    'message_generator': lambda r: (r.get('result') is not None) and f'{log.default}User {log.reset}{log.red}{r["result"]}{log.reset}{log.default} is kerberoastable{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '2': {
                    'query': 'match p=(u:User)-[:CanRDP]->(c:Computer) return u.name,c.name ORDER BY u.name',
                    'desc': 'List user CanRDP privileges',
                    'message_generator': lambda r: (r.get('u.name') is not None and r.get('c.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '3': {
                    'query': 'match p=(g:Group)-[:CanRDP]->(c:Computer) return g.name,c.name ORDER BY g.name',
                    'desc': 'List group CanRDP privileges',
                    'message_generator': lambda r: (r.get('g.name') is not None and r.get('c.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '4': {
                    'query': 'match p=(g:Group)-[:CanRDP]->(c:Computer) WHERE (g.objectid =~ "(?i)S-1-5-21-.*-513" OR g.objectid =~ "(?i).*-S-1-5-11" OR g.objectid =~ "(?i).*-S-1-1-0" OR g.objectid =~ "(?i).*-S-1-5-32-545") return g.name,c.name ORDER BY g.name',
                    'desc': 'List all CanRDP privileges for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': lambda r: (r.get('g.name') is not None and r.get('c.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '5': {
                    'query': 'match p=(m {owned: true})-[:CanRDP]->(c:Computer) return m.name,c.name,labels(m) ORDER BY m.name',
                    'desc': 'List all CanRDP privileges for owned principles',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('c.name') is not None) and f'{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },                
                '6': {
                    'query': 'MATCH (c:Computer {unconstraineddelegation:true}) return c.name ORDER BY c.name',
                    'desc': 'List all Unconstrained Delegation',
                    'message_generator': lambda r: (r.get('c.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["c.name"]}{log.reset}{log.default} has unconstrained delegation privilege{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '7': {
                    'query': 'MATCH (H:Computer) WHERE H.operatingsystem =~ \'.*(2000|2003|2008|xp|vista|7|me).*\' RETURN H.name,H.operatingsystem ORDER BY H.name',
                    'desc': 'List all unsupported OSs',
                    'message_generator': lambda r: (r.get('H.name') is not None and r.get('H.operatingsystem') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["H.name"]}{log.reset}{log.default} is unsupported with OS {log.reset}{log.red}{r["H.operatingsystem"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '8': {
                    'query': 'MATCH (g:Group) WHERE g.name =~ \'.*((?i)admin|adm).*\' RETURN g.name ORDER BY g.name',
                    'desc': 'List groups containing "admin"',
                    'message_generator': lambda r: (r.get('g.name') is not None) and f'{log.default}Admin group {log.reset}{log.red}{r["g.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '9': {
                    'query': 'MATCH (u:User) WHERE u.name =~ \'.*((?i)admin|adm).*\' RETURN u.name ORDER BY u.name',
                    'desc': 'List users containing "admin"',
                    'message_generator': lambda r: (r.get('u.name') is not None) and f'{log.default}Admin user {log.reset}{log.red}{r["u.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '10': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all user shortest paths to admin groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '11': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all group shortest paths to admin groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '12': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all computer shortest paths to admin groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '13': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE (m.objectid =~ "(?i)S-1-5-21-.*-513" OR m.objectid =~ "(?i).*-S-1-5-11" OR m.objectid =~ "(?i).*-S-1-1-0" OR m.objectid =~ "(?i).*-S-1-5-32-545") AND n.name =~ ".*((?i)admin|adm).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to admin groups for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '14': {
                    'query': 'MATCH p=shortestPath((m {owned: true})-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to admin groups for owned principles',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '15': {
                    'query': 'MATCH (g:Group) WHERE g.name =~ \'.*((?i)sql).*\' RETURN g.name ORDER BY g.name',
                    'desc': 'List groups containing "sql"',
                    'message_generator': lambda r: (r.get('g.name') is not None) and f'{log.default}SQL group {log.reset}{log.red}{r["g.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '16': {
                    'query': 'MATCH (u:User) WHERE u.name =~ \'.*((?i)sql).*\' RETURN u.name ORDER BY u.name',
                    'desc': 'List users containing "sql"',
                    'message_generator': lambda r: (r.get('u.name') is not None) and f'{log.default}SQL user {log.reset}{log.red}{r["u.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '17': {
                    'query': 'MATCH (c:Computer) WHERE c.name =~ \'.*((?i)sql).*\' RETURN c.name ORDER BY c.name',
                    'desc': 'List computers containing "sql"',
                    'message_generator': lambda r: (r.get('c.name') is not None) and f'{log.default}SQL computer {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '18': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all user shortest paths to SQL groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '19': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all group shortest paths to SQL groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '20': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all computer shortest paths to SQL groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '21': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE (m.objectid =~ "(?i)S-1-5-21-.*-513" OR m.objectid =~ "(?i).*-S-1-5-11" OR m.objectid =~ "(?i).*-S-1-1-0" OR m.objectid =~ "(?i).*-S-1-5-32-545") AND n.name =~ ".*((?i)SQL).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to SQL groups for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '22': {
                    'query': 'MATCH p=shortestPath((m {owned: true})-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to SQL groups for owned principles',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '23': {
                    'query': 'MATCH (u:User) WHERE u.name =~ \'.*((?i)svc|service).*\' RETURN u.name ORDER BY u.name',
                    'desc': 'List users containing "svc/service"',
                    'message_generator': lambda r: (r.get('u.name') is not None) and f'{log.default}Service user {log.reset}{log.red}{r["u.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '24': {
                    'query': 'MATCH (g:Group) WHERE g.name =~ \'.*((?i)svc|service).*\' RETURN g.name ORDER BY g.name',
                    'desc': 'List groups containing "svc/service"',
                    'message_generator': lambda r: (r.get('g.name') is not None) and f'{log.default}Service group {log.reset}{log.red}{r["g.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '25': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all user shortest paths to service groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '26': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all group shortest paths to service groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '27': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all computer shortest paths to service groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '28': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE (m.objectid =~ "(?i)S-1-5-21-.*-513" OR m.objectid =~ "(?i).*-S-1-5-11" OR m.objectid =~ "(?i).*-S-1-1-0" OR m.objectid =~ "(?i).*-S-1-5-32-545") AND n.name =~ ".*((?i)service|svc).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to service groups for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '29': {
                    'query': 'MATCH p=shortestPath((m {owned: true})-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to service groups for owned principles',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '30': {
                    'query': 'MATCH (u:User) WHERE u.name =~ \'.*((?i)web).*\' RETURN u.name ORDER BY u.name',
                    'desc': 'List users containing "web"',
                    'message_generator': lambda r: (r.get('u.name') is not None) and f'{log.default}Web user {log.reset}{log.red}{r["u.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '31': {
                    'query': 'MATCH (g:Group) WHERE g.name =~ \'.*((?i)web).*\' RETURN g.name ORDER BY g.name',
                    'desc': 'List groups containing "web"',
                    'message_generator': lambda r: (r.get('g.name') is not None) and f'{log.default}Web group {log.reset}{log.red}{r["g.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '32': {
                    'query': 'MATCH (c:Computer) WHERE c.name =~ \'.*((?i)web).*\' RETURN c.name ORDER BY c.name',
                    'desc': 'List computers containing "web"',
                    'message_generator': lambda r: (r.get('c.name') is not None) and f'{log.default}Web computer {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '33': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all user shortest paths to web groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '34': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all group shortest paths to web groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '35': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all computer shortest paths to web groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '36': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE (m.objectid =~ "(?i)S-1-5-21-.*-513" OR m.objectid =~ "(?i).*-S-1-5-11" OR m.objectid =~ "(?i).*-S-1-1-0" OR m.objectid =~ "(?i).*-S-1-5-32-545") AND n.name =~ ".*((?i)WEB).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to web groups for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '37': {
                    'query': 'MATCH p=shortestPath((m {owned: true})-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to web groups for owned principles',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '38': {
                    'query': 'MATCH (u:User) WHERE u.name =~ \'.*((?i)dev).*\' RETURN u.name ORDER BY u.name',
                    'desc': 'List users containing "dev"',
                    'message_generator': lambda r: (r.get('u.name') is not None) and f'{log.default}Dev user {log.reset}{log.red}{r["u.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '39': {
                    'query': 'MATCH (g:Group) WHERE g.name =~ \'.*((?i)dev).*\' RETURN g.name ORDER BY g.name',
                    'desc': 'List groups containing "dev"',
                    'message_generator': lambda r: (r.get('g.name') is not None) and f'{log.default}Dev group {log.reset}{log.red}{r["g.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '40': {
                    'query': 'MATCH (c:Computer) WHERE c.name =~ \'.*((?i)dev).*\' RETURN c.name ORDER BY c.name',
                    'desc': 'List computers containing "dev"',
                    'message_generator': lambda r: (r.get('c.name') is not None) and f'{log.default}Dev computer {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '41': {
                    'query': 'MATCH (u:User) WHERE u.name =~ \'.*((?i)prod).*\' RETURN u.name ORDER BY u.name',
                    'desc': 'List users containing "prod"',
                    'message_generator': lambda r: (r.get('u.name') is not None) and f'{log.default}Prod user {log.reset}{log.red}{r["u.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '42': {
                    'query': 'MATCH (g:Group) WHERE g.name =~ \'.*((?i)prod).*\' RETURN g.name ORDER BY g.name',
                    'desc': 'List groups containing "prod"',
                    'message_generator': lambda r: (r.get('g.name') is not None) and f'{log.default}Prod group {log.reset}{log.red}{r["g.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '43': {
                    'query': 'MATCH (c:Computer) WHERE c.name =~ \'.*((?i)prod).*\' RETURN c.name ORDER BY c.name',
                    'desc': 'List computers containing "prod"',
                    'message_generator': lambda r: (r.get('c.name') is not None) and f'{log.default}Prod computer {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '44': {
                    'query': 'MATCH (n:Group) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" WITH n MATCH p=(n)<-[r:MemberOf*1..]-(m) RETURN m.name ORDER BY m.name',
                    'desc': 'List all Domain Admins',
                    'message_generator': lambda r: (r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is MemberOf Domain Admins{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '45': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all user shortest paths to Domain Admins',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '46': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all group shortest paths to Domain Admins',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '47': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all computer shortest paths to Domain Admins',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '48': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE (m.objectid =~ "(?i)S-1-5-21-.*-513" OR m.objectid =~ "(?i).*-S-1-5-11" OR m.objectid =~ "(?i).*-S-1-1-0" OR m.objectid =~ "(?i).*-S-1-5-32-545") AND n.objectid =~ "(?i)S-1-5-21-.*-512" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Domain Admins for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '49': {
                    'query': 'MATCH p=shortestPath((m {owned: true})-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Domain Admins for owned principles',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '50': {
                    'query': 'MATCH (n:Group) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" WITH n MATCH p=(n)<-[r:MemberOf*1..]-(m) RETURN m.name ORDER BY m.name',
                    'desc': 'List all Enterprise Admins',
                    'message_generator': lambda r: (r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is MemberOf Enterprise Admins{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '51': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all user shortest paths to Enterprise Admins',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '52': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all group shortest paths to Enterprise Admins',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '53': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all computer shortest paths to Enterprise Admins',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '54': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE (m.objectid =~ "(?i)S-1-5-21-.*-513" OR m.objectid =~ "(?i).*-S-1-5-11" OR m.objectid =~ "(?i).*-S-1-1-0" OR m.objectid =~ "(?i).*-S-1-5-32-545") AND n.objectid =~ "(?i)S-1-5-21-.*-519" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Enterprise Admins for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '55': {
                    'query': 'MATCH p=shortestPath((m {owned: true})-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Enterprise Admins for owned principles',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '56': {
                    'query': 'MATCH p=(m:Computer)-[r:HasSession]->(n:User) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all sessions',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '57': {
                    'query': 'MATCH (u:User {dontreqpreauth: true}) RETURN u.name ORDER BY u.name',
                    'desc': 'List all AS-REP roastable users',
                    'message_generator': lambda r: (r.get('u.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is AS-REP roastable{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '58': {
                    'query': 'MATCH (m:Group {highvalue:true}) RETURN m.name ORDER BY m.name',
                    'desc': 'List all high-value groups',
                    'message_generator': lambda r: (r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is high value{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '59': {
                    'query': 'MATCH p=(n:User)-[r:MemberOf*1..]->(m:Group {highvalue:true}) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all members of high-value groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf high value group {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '60': {
                    'query': 'MATCH (m:User),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n return m.name,p ORDER BY m.name',
                    'desc': 'List all user shortest paths to high-value targets',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '61': {
                    'query': 'MATCH (m:Group),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n return m.name,p ORDER BY m.name',
                    'desc': 'List all group shortest paths to high-value targets',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '62': {
                    'query': 'MATCH (m:Computer),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n return m.name,p ORDER BY m.name',
                    'desc': 'List all computer shortest paths to high-value targets',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '63': {
                    'query': 'MATCH (m:Group),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE (m.objectid =~ "(?i)S-1-5-21-.*-513" OR m.objectid =~ "(?i).*-S-1-5-11" OR m.objectid =~ "(?i).*-S-1-1-0" OR m.objectid =~ "(?i).*-S-1-5-32-545") AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to high-value targets for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '64': {
                    'query': 'MATCH (m {owned: true}),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to high-value targets for owned principles',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '65': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all user shortest paths to Exchange groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '66': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all group shortest paths to Exchange groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '67': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all computer shortest paths to Exchange groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '68': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE (m.objectid =~ "(?i)S-1-5-21-.*-513" OR m.objectid =~ "(?i).*-S-1-5-11" OR m.objectid =~ "(?i).*-S-1-1-0" OR m.objectid =~ "(?i).*-S-1-5-32-545") AND n.name =~ ".*((?i)EXCHANGE).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NOT m=n AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Exchange groups for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '69': {
                    'query': 'MATCH p=shortestPath((m {owned: true})-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NOT m=n AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Exchange groups for owned principles',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '70': {
                    'query': 'MATCH p=(m:User)-[r:AdminTo]->(n:Computer) RETURN m.name, n.name ORDER BY m.name',
                    'desc': 'List user AdminTo privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '71': {
                    'query': 'MATCH p=(m:Group)-[r:AdminTo]->(n:Computer) RETURN m.name,n.name ORDER BY m.name',
                    'desc': 'List group AdminTo privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '72': {
                    'query': 'MATCH p=(m:Computer)-[r:AdminTo]->(n:Computer) RETURN m.name,n.name ORDER BY m.name',
                    'desc': 'List computer AdminTo privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '73': {
                    'query': 'MATCH p=(m:Group)-[r:AdminTo]->(n:Computer) WHERE (m.objectid =~ "(?i)S-1-5-21-.*-513" OR m.objectid =~ "(?i).*-S-1-5-11" OR m.objectid =~ "(?i).*-S-1-1-0" OR m.objectid =~ "(?i).*-S-1-5-32-545") RETURN m.name,n.name ORDER BY m.name',
                    'desc': 'List all AdminTo privileges for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '74': {
                    'query': 'MATCH p=(m {owned: true})-[r:AdminTo]->(n:Computer) RETURN m.name,n.name,labels(m) ORDER BY m.name',
                    'desc': 'List all AdminTo privileges for owned principles',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '75': {
                    'query': 'MATCH p=(n:User)-[r:ReadLAPSPassword]->(m:Computer) RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List user ReadLAPSPassword privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '76': {
                    'query': 'MATCH p=(n:Group)-[r:ReadLAPSPassword]->(m:Computer) RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List group ReadLAPSPassword privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '77': {
                    'query': 'MATCH p=(n:Computer)-[r:ReadLAPSPassword]->(m:Computer) RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List computer ReadLAPSPassword privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '78': {
                    'query': 'MATCH p=(n:Group)-[r:ReadLAPSPassword]->(m:Computer) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List all ReadLAPSPassword privileges for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '79': {
                    'query': 'MATCH p=(m {owned: true})-[r:ReadLAPSPassword]->(n:Computer) RETURN n.name,m.name,labels(m) ORDER by m.name',
                    'desc': 'List all ReadLAPSPassword privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '80': {
                    'query': 'MATCH p=(n:User)-[r:SyncLAPSPassword]->(m:Computer) RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List user SyncLAPSPassword privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '81': {
                    'query': 'MATCH p=(n:Group)-[r:SyncLAPSPassword]->(m:Computer) RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List group SyncLAPSPassword privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '82': {
                    'query': 'MATCH p=(n:Computer)-[r:SyncLAPSPassword]->(m:Computer) RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List computer SyncLAPSPassword privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '83': {
                    'query': 'MATCH p=(n:Group)-[r:SyncLAPSPassword]->(m:Computer) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List all SyncLAPSPassword privileges for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '84': {
                    'query': 'MATCH p=(m {owned: true})-[r:SyncLAPSPassword]->(n:Computer) RETURN n.name,m.name,labels(m) ORDER by m.name',
                    'desc': 'List all SyncLAPSPassword privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '85': {
                    'query': 'MATCH (n:User)-[:MemberOf*1..]->(g:Group) WHERE g.objectid ENDS WITH \'-512\' MATCH p = (c:Computer)-[:HasSession]->(n) return n.name,c.name ORDER BY n.name',
                    'desc': 'List Domain Admin sessions',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('c.name') is not None) and f'{log.default}Domain admin {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '86': {
                    'query': 'MATCH (n:User)-[:MemberOf*1..]->(g:Group) WHERE g.objectid ENDS WITH \'-519\' MATCH p = (c:Computer)-[:HasSession]->(n) return n.name,c.name ORDER BY n.name',
                    'desc': 'List Enterprise Admin sessions',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('c.name') is not None) and f'{log.default}Enterprise admin {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '87': {
                    'query': 'MATCH (n:User) return n.name ORDER BY n.name',
                    'desc': 'List all users',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '88': {
                    'query': 'MATCH (n:Group) return n.name ORDER BY n.name',
                    'desc': 'List all groups',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '89': {
                    'query': 'MATCH (n:Computer) return n.name ORDER BY n.name',
                    'desc': 'List all computers',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '90': {
                    'query': 'MATCH (n:Computer {enabled:TRUE}) return n.name ORDER BY n.name',
                    'desc': 'List all enabled computers',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is enabled{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '91': {
                    'query': 'MATCH (n:Computer {enabled:FALSE}) return n.name ORDER BY n.name',
                    'desc': 'List all disabled computers',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is disabled{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '92': {
                    'query': 'MATCH (n:Group) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" WITH n MATCH p=(n)<-[r:MemberOf*1..]-(m) RETURN m.name ORDER BY m.name',
                    'desc': 'List all Domain Controllers',
                    'message_generator': lambda r: (r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is a Domain Controller{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '93': {
                    'query': 'MATCH (n:Group) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" WITH n MATCH p=(n)<-[r:MemberOf*1..]-(m) RETURN m.name,m.operatingsystem ORDER BY m.name',
                    'desc': 'List all Domain Controllers OSs',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('m.operatingsystem') is not None) and f'{log.default}Domain Controller {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} OS {log.reset}{log.red}{r["m.operatingsystem"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '94': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all user shortest paths to Domain Controllers',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '95': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all group shortest paths to Domain Controllers',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '96': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all computer shortest paths to Domain Controllers',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '97': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE (m.objectid =~ "(?i)S-1-5-21-.*-513" OR m.objectid =~ "(?i).*-S-1-5-11" OR m.objectid =~ "(?i).*-S-1-1-0" OR m.objectid =~ "(?i).*-S-1-5-32-545") AND n.objectid =~ "(?i)S-1-5-21-.*-516" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Domain Controllers for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '98': {
                    'query': 'MATCH p=shortestPath((m {owned: true})-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Domain Controllers for owned principles',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'general',
                },
                '99': {
                    'query': 'MATCH (n:User {passwordnotreqd:true}) return n.name ORDER BY n.name',
                    'desc': 'List all users that don\'t require a password',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is not required to have a password{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '100': {
                    'query': 'MATCH (n:User {pwdneverexpires:true}) return n.name ORDER BY n.name',
                    'desc': 'List all users where password never expires',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}User\'s {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} password is set to never expire{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '101': {
                    'query': 'MATCH (u:User)-[:AllowedToDelegate]->(c:Computer) RETURN u.name,c.name ORDER BY u.name',
                    'desc': 'List user Constrained Delegation',
                    'message_generator': lambda r: (r.get('u.name') is not None and r.get('c.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '102': {
                    'query': 'MATCH (g:Group)-[:AllowedToDelegate]->(c:Computer) RETURN g.name,c.name ORDER BY g.name',
                    'desc': 'List group Constrained Delegation',
                    'message_generator': lambda r: (r.get('g.name') is not None and r.get('c.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '103': {
                    'query': 'MATCH (c1:Computer)-[:AllowedToDelegate]->(c2:Computer) RETURN c1.name,c2.name ORDER BY c1.name',
                    'desc': 'List computer Constrained Delegation',
                    'message_generator': lambda r: (r.get('c1.name') is not None and r.get('c2.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["c1.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c2.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '104': {
                    'query': 'Match (n:GPO) return n.name ORDER BY n.name',
                    'desc': 'List all GPOs',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}GPO {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '105': {
                    'query': 'Match (n:Domain) return n.name ORDER BY n.name',
                    'desc': 'List all domains',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}Domain {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '106': {
                    'query': 'MATCH p=(n:Domain)-[r:TrustedBy]->(m:Domain) RETURN r.trusttype,n.name,m.name ORDER by n.name',
                    'desc': 'List all domain trusts',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None and r.get('r.trusttype') is not None) and f'{log.default}Domain {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is trusted by {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}with type {log.reset}{log.red}{r["r.trusttype"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '107': {
                    'query': 'Match (c:Computer) WHERE c.haslaps = true return c.name ORDER BY c.name',
                    'desc': 'List computers with LAPS enabled',
                    'message_generator': lambda r: (r.get('c.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["c.name"]}{log.reset}{log.default} has LAPS enabled{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '108': {
                    'query': 'Match (c:Computer) WHERE c.haslaps = false return c.name ORDER BY c.name',
                    'desc': 'List computers with LAPS disabled',
                    'message_generator': lambda r: (r.get('c.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["c.name"]}{log.reset}{log.default} has LAPS disabled{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '109': {
                    'query': 'MATCH (u:User) WHERE u.description =~ \'.*((?i)pass|pw|:).*\' return u.name,u.description ORDER BY u.name',
                    'desc': 'List potential passwords in descriptions',
                    'message_generator': lambda r: (r.get('u.name') is not None and r.get('u.description') is not None) and f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} may have password in description {log.reset}{log.red}{r["u.description"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '110': {
                    'query': 'MATCH (m:User {highvalue:true}) RETURN m.name ORDER BY m.name',
                    'desc': 'List all high-value users',
                    'message_generator': lambda r: (r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is high value{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '111': {
                    'query': 'MATCH (m:User {sensitive:true}) RETURN m.name ORDER BY m.name',
                    'desc': 'List all sensitive users',
                    'message_generator': lambda r: (r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is sensitive{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '112': {
                    'query': 'MATCH (m:User {admincount:true}) return m.name ORDER BY m.name',
                    'desc': 'List all users with an admin count',
                    'message_generator': lambda r: (r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} has an admin count{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '113': {
                    'query': 'MATCH (m:Group {admincount:true}) return m.name ORDER BY m.name',
                    'desc': 'List all groups with an admin count',
                    'message_generator': lambda r: (r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} has an admin count{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '114': {
                    'query': 'MATCH (m:Computer {admincount:true}) return m.name ORDER BY m.name',
                    'desc': 'List all computers with an admin count',
                    'message_generator': lambda r: (r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} has an admin count{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '115': {
                    'query': 'MATCH p=(n:User)-[r:ReadGMSAPassword]->(m:User) RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List all user ReadGMSAPassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '116': {
                    'query': 'MATCH p=(n:Group)-[r:ReadGMSAPassword]->(m:User) RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List all group ReadGMSAPassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '117': {
                    'query': 'MATCH p=(n:Computer)-[r:ReadGMSAPassword]->(m:User) RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List all computer ReadGMSAPassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '118': {
                    'query': 'MATCH (n:Group)-[r:ReadGMSAPassword]->(m:User) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all ReadGMSAPassword privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },                
                '119': {
                    'query': 'MATCH p=(m {owned: true})-[r:ReadGMSAPassword]->(n:Computer) RETURN n.name,m.name,labels(m) ORDER by m.name',
                    'desc': 'List all ReadGMSAPassword privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '120': {
                    'query': 'MATCH (n:User)-[r:DCSync]->(m:Domain) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all user DCSync privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '121': {
                    'query': 'MATCH (n:Group)-[r:DCSync]->(m:Domain) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all group DCSync privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '122': {
                    'query': 'MATCH (n:Computer)-[r:DCSync]->(m:Domain) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all computer DCSync privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '123': {
                    'query': 'MATCH (n)-[r:DCSync]->(m:Domain) RETURN n.name,labels(n),m.name ORDER BY n.name',
                    'desc': 'List all DCSync privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '124': {
                    'query': 'MATCH (n:Group)-[r:DCSync]->(m:Domain) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all DCSync privileges for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.red}{r["n.name"]}{log.reset}{log.default} has DCSync privileges for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '125': {
                    'query': 'MATCH p=(m {owned: true})-[r:DCSync]->(n:Domain) RETURN n.name,m.name,labels(m) ORDER by m.name',
                    'desc': 'List all DCSync privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["m.name"]}{log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}{log.default} has DCSync privileges for {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '126': {
                    'query': 'MATCH (n:User)-[r:ForceChangePassword]->(m:User) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all user ForceChangePassword privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '127': {
                    'query': 'MATCH (n:Group)-[r:ForceChangePassword]->(m:User) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all group ForceChangePassword privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '128': {
                    'query': 'MATCH (n:Computer)-[r:ForceChangePassword]->(m:User) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all computer ForceChangePassword privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '129': {
                    'query': 'MATCH (n:Group)-[r:ForceChangePassword]->(m:User) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all ForceChangePassword privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has ForceChangePassword over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '130': {
                    'query': 'MATCH (n {owned: true})-[r:ForceChangePassword]->(m:User) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all ForceChangePassword privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has ForceChangePassword over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },                
                '131': {
                    'query': 'MATCH (n:User)-[r:AddMember]->(m:Group) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all user AddMember privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '132': {
                    'query': 'MATCH (n:Group)-[r:AddMember]->(m:Group) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all group AddMember privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '133': {
                    'query': 'MATCH (n:Computer)-[r:AddMember]->(m:Group) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all computer AddMember privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '134': {
                    'query': 'MATCH (n:Group)-[r:AddMember]->(m:Group) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all AddMember privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddMember over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '135': {
                    'query': 'MATCH (n {owned: true})-[r:AddMember]->(m:Group) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all AddMember privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has AddMember over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '136': {
                    'query': 'MATCH (n:User)-[r:AddSelf]->(m:Group) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all user AddSelf privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '137': {
                    'query': 'MATCH (n:Group)-[r:AddSelf]->(m:Group) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all group AddSelf privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '138': {
                    'query': 'MATCH (n:Computer)-[r:AddSelf]->(m:Group) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all computer AddSelf privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '139': {
                    'query': 'MATCH (n:Group)-[r:AddSelf]->(m:Group) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all AddSelf privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddSelf over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '140': {
                    'query': 'MATCH (n {owned: true})-[r:AddSelf]->(m:Group) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all AddSelf privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has AddSelf over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '141': {
                    'query': 'MATCH (n:User)-[r:SQLAdmin]->(m:Computer) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all user SQLAdmin privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '142': {
                    'query': 'MATCH (n:Group)-[r:SQLAdmin]->(m:Computer) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all group SQLAdmin privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '143': {
                    'query': 'MATCH (n:Computer)-[r:SQLAdmin]->(m:Computer) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all computer SQLAdmin privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '144': {
                    'query': 'MATCH (n:Group)-[r:SQLAdmin]->(m:Computer) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all SQLAdmin privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has SQLAdmin over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '145': {
                    'query': 'MATCH (n {owned: true})-[r:SQLAdmin]->(m:Computer) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all SQLAdmin privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has SQLAdmin over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '146': {
                    'query': 'MATCH (n:User)-[r:CanPSRemote]->(m:Computer) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all user CanPSRemote privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '147': {
                    'query': 'MATCH (n:Group)-[r:CanPSRemote]->(m:Computer) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all group CanPSRemote privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '148': {
                    'query': 'MATCH (n:Computer)-[r:CanPSRemote]->(m:Computer) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all computer CanPSRemote privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '149': {
                    'query': 'MATCH (n:Group)-[r:CanPSRemote]->(m:Computer) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all CanPSRemote privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has CanPSRemote over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '150': {
                    'query': 'MATCH (n {owned: true})-[r:CanPSRemote]->(m:Computer) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all CanPSRemote privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has CanPSRemote over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '151': {
                    'query': 'MATCH (n:User)-[r:ExecuteDCOM]->(m:Computer) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all user ExecuteDCOM privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '152': {
                    'query': 'MATCH (n:Group)-[r:ExecuteDCOM]->(m:Computer) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all group ExecuteDCOM privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '153': {
                    'query': 'MATCH (n:Computer)-[r:ExecuteDCOM]->(m:Computer) RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List all computer ExecuteDCOM privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '154': {
                    'query': 'MATCH (n:Group)-[r:ExecuteDCOM]->(m:Computer) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all ExecuteDCOM privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has ExecuteDCOM over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '155': {
                    'query': 'MATCH (n {owned: true})-[r:ExecuteDCOM]->(m:Computer) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all ExecuteDCOM privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has ExecuteDCOM over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '156': {
                    'query': 'MATCH (n:User)-[r:AllowedToAct]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all user AllowedToAct privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '157': {
                    'query': 'MATCH (n:Group)-[r:AllowedToAct]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all group AllowedToAct privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '158': {
                    'query': 'MATCH (n:Computer)-[r:AllowedToAct]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all computer AllowedToAct privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '159': {
                    'query': 'MATCH (n:Group)-[r:AllowedToAct]->(m:Computer) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all AllowedToAct privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllowedToAct over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '160': {
                    'query': 'MATCH (n {owned: true})-[r:AllowedToAct]->(m:Computer) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all AllowedToAct privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has AllowedToAct over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '161': {
                    'query': 'MATCH (n:User)-[r:Owns]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all user Owns privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '162': {
                    'query': 'MATCH (n:Group)-[r:Owns]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all group Owns privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '163': {
                    'query': 'MATCH (n:Computer)-[r:Owns]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all computer Owns privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '164': {
                    'query': 'MATCH (n:Group)-[r:Owns]->(m) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all Owns privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has Owns over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '165': {
                    'query': 'MATCH (n {owned: true})-[r:Owns]->(m) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all Owns privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has Owns over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '166': {
                    'query': 'MATCH (n:User)-[r:AllExtendedRights]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all user AllExtendedRights privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '167': {
                    'query': 'MATCH (n:Group)-[r:AllExtendedRights]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all group AllExtendedRights privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '168': {
                    'query': 'MATCH (n:Computer)-[r:AllExtendedRights]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all computer AllExtendedRights privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '169': {
                    'query': 'MATCH (n:Group)-[r:AllExtendedRights]->(m) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all AllExtendedRights privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '170': {
                    'query': 'MATCH (n {owned: true})-[r:AllExtendedRights]->(m) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all AllExtendedRights privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },                
                '171': {
                    'query': 'MATCH (n:User)-[r:MemberOf]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all user memberships',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '172': {
                    'query': 'MATCH (n:Group)-[r:MemberOf]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all group memberships',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '173': {
                    'query': 'MATCH (n:Computer)-[r:MemberOf]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all computer memberships',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '174': {
                    'query': 'MATCH (n:Group)-[r:MemberOf]->(m) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all memberships for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has MemberOf over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '175': {
                    'query': 'MATCH (n {owned: true})-[r:MemberOf]->(m) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all memberships for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has MemberOf over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '176': {
                    'query': 'MATCH (n:User)-[r:AddKeyCredentialLink]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all user AddKeyCredentialLink privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '177': {
                    'query': 'MATCH (n:Group)-[r:AddKeyCredentialLink]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all group AddKeyCredentialLink privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '178': {
                    'query': 'MATCH (n:Computer)-[r:AddKeyCredentialLink]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all computer AddKeyCredentialLink privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '179': {
                    'query': 'MATCH (n:Group)-[r:AddKeyCredentialLink]->(m) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all AddKeyCredentialLink privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '180': {
                    'query': 'MATCH (n {owned: true})-[r:AddKeyCredentialLink]->(m) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all AddKeyCredentialLink privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '181': {
                    'query': 'MATCH (n:User)-[r:GenericAll]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all user GenericAll privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '182': {
                    'query': 'MATCH (n:Group)-[r:GenericAll]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all group GenericAll privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '183': {
                    'query': 'MATCH (n:Computer)-[r:GenericAll]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all computer GenericAll privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '184': {
                    'query': 'MATCH (n:Group)-[r:GenericAll]->(m) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all GenericAll privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '185': {
                    'query': 'MATCH (n {owned: true})-[r:GenericAll]->(m) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all GenericAll privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '186': {
                    'query': 'MATCH (n:User)-[r:WriteDacl]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all user WriteDacl privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '187': {
                    'query': 'MATCH (n:Group)-[r:WriteDacl]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all group WriteDacl privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '188': {
                    'query': 'MATCH (n:Computer)-[r:WriteDacl]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all computer WriteDacl privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '189': {
                    'query': 'MATCH (n:Group)-[r:WriteDacl]->(m) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all WriteDacl privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '190': {
                    'query': 'MATCH (n {owned: true})-[r:WriteDacl]->(m) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all WriteDacl privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '191': {
                    'query': 'MATCH (n:User)-[r:WriteOwner]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all user WriteOwner privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '192': {
                    'query': 'MATCH (n:Group)-[r:WriteOwner]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all group WriteOwner privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '193': {
                    'query': 'MATCH (n:Computer)-[r:WriteOwner]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all computer WriteOwner privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '194': {
                    'query': 'MATCH (n:Group)-[r:WriteOwner]->(m) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all WriteOwner privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },                
                '195': {
                    'query': 'MATCH (n {owned: true})-[r:WriteOwner]->(m) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all WriteOwner privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },                
                '196': {
                    'query': 'MATCH (n:User)-[r:GenericWrite]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all user GenericWrite privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '197': {
                    'query': 'MATCH (n:Group)-[r:GenericWrite]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all group GenericWrite privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '198': {
                    'query': 'MATCH (n:Computer)-[r:GenericWrite]->(m) RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all computer GenericWrite privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '199': {
                    'query': 'MATCH (n:Group)-[r:GenericWrite]->(m) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List all GenericWrite privileges for Users, Domain Users, Authenticated Users, and Everyone groups',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },  
                '200': {
                    'query': 'MATCH (n {owned: true})-[r:GenericWrite]->(m) RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List all GenericWrite privileges for owned principles',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },          
                '201': {
                    'query': 'MATCH (u:User) return u.name,u.description ORDER BY u.name',
                    'desc': 'List all user descriptions',
                    'message_generator': lambda r: (r.get('u.description') is not None and r.get('u.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["u.description"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '202': {
                    'query': 'MATCH (g:Group) return g.name,g.description ORDER BY g.name',
                    'desc': 'List all group descriptions',
                    'message_generator': lambda r: (r.get('g.description') is not None and r.get('g.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["g.description"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '203': {
                    'query': 'MATCH (u:User) return u.name,u.email ORDER BY u.name',
                    'desc': 'List all emails',
                    'message_generator': lambda r: (r.get('u.email') is not None and r.get('u.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} email {log.reset}{log.red}{r["u.email"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '204': {
                    'query': 'MATCH (o:OU) RETURN o.name ORDER BY o.name',
                    'desc': 'List all OUs',
                    'message_generator': lambda r: (r.get('o.name') is not None) and f'{log.default}OU {log.reset}{log.red}{r["o.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '205': {
                    'query': 'MATCH (c:Container) return c.name ORDER BY c.name',
                    'desc': 'List all Containers',
                    'message_generator': lambda r: (r.get('c.name') is not None) and f'{log.default}Container {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '206': {
                    'query': 'Match (n:Domain) return n.name ORDER BY n.name',
                    'desc': 'List all Domains',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}Domain {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '207': {
                    'query': 'MATCH (d:Domain) return d.name,d.functionallevel ORDER BY d.name',
                    'desc': 'List all Domains functional level',
                    'message_generator': lambda r: (r.get('d.name') is not None and r.get('d.functionallevel') is not None) and f'{log.default}Domain {log.reset}{log.red}{r["d.name"]}{log.reset}{log.default} functional level {log.reset}{log.red}{r["d.functionallevel"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '208': {
                    'query': 'match (n)-[r:Owns|AllExtendedRights|WriteDacl|GenericAll|WriteOwner|GenericWrite]->(o:OU) return n.name,o.name,TYPE(r),labels(n) ORDER BY n.name',
                    'desc': 'List all object control over OUs',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('o.name') is not None) and f'({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]} {log.reset}{log.default}has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over OU {log.reset}{log.red}{r["o.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '209': {
                    'query': 'match (n)-[r:Owns|AllExtendedRights|WriteDacl|GenericAll|WriteOwner|GenericWrite]->(c:Container) return n.name,c.name,TYPE(r),labels(n) ORDER BY n.name',
                    'desc': 'List all object control over Containers',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('c.name') is not None) and f'{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]} {log.reset}{log.default}has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over Container {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '210': {
                    'query': 'match (n)-[r:Owns|AllExtendedRights|WriteDacl|GenericAll|WriteOwner|GenericWrite]->(g:GPO) return n.name,g.name,TYPE(r),labels(n) ORDER BY n.name',
                    'desc': 'List all object control over GPOs',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('g.name') is not None) and f'({r["labels(n)"][0]}/{r["labels(n)"][1]}) {log.red}{r["n.name"]} {log.reset}{log.default}has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over GPO {log.reset}{log.red}{r["g.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '211': {
                    'query': 'MATCH (g1)-[:GPLink]->(g2) RETURN g1.name,g2.name,labels(g2) ORDER BY g1.name',
                    'desc': 'List all GP Links',
                    'message_generator': lambda r: (r.get('g1.name') is not None and r.get('g2.name') is not None) and f'{log.default}GPO {log.reset}{log.red}{r["g1.name"]}{log.reset}{log.default} is linked to {log.reset}{log.red}{r["g2.name"]}{log.reset}{log.default} ({r["labels(g2)"][0]}/{r["labels(g2)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '212': {
                    'query': 'MATCH (n:User)-[r]->(m) RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)',
                    'desc': 'List all user privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '213': {
                    'query': 'MATCH (n:Group)-[r]->(m) RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)',
                    'desc': 'List all group privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '214': {
                    'query': 'MATCH (n:Computer)-[r]->(m) RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)',
                    'desc': 'List all computer privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '215': {
                    'query': 'MATCH (n:Group)-[r]->(m) WHERE (n.objectid =~ "(?i)S-1-5-21-.*-513" OR n.objectid =~ "(?i).*-S-1-5-11" OR n.objectid =~ "(?i).*-S-1-1-0" OR n.objectid =~ "(?i).*-S-1-5-32-545") RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)',
                    'desc': 'List all privileges for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '216': {
                    'query': 'MATCH (n {owned: true})-[r]->(m) RETURN n.name,TYPE(r),labels(m),labels(n),m.name ORDER BY TYPE(r)',
                    'desc': 'List all privileges for owned principles',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.red}{r["n.name"]} {log.reset}{log.default}({r["labels(n)"][0]}/{r["labels(n)"][1]}){log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '217': {
                    'query': 'match p=(u:User)-[:CanRDP]->(c:Computer) WHERE u.name =~ \'((?i)USER_SEARCH)\' return u.name,c.name',
                    'desc': 'List this user\'s RDP privileges',
                    'message_generator': lambda r: (r.get('u.name') is not None and r.get('c.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '218': {
                    'query': 'MATCH (n:User)-[:MemberOf]->(m:Group),(m)-[:CanRDP]->(c:Computer) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN DISTINCT n.name,m.name,c.name ORDER BY m.name',
                    'desc': 'List this user\'s group-delegated RDP privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None and r.get('c.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which CanRDP to {log.red}{r["c.name"]}{log.default}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '219': {
                    'query': 'MATCH p=(m:User)-[r:AdminTo]->(n:Computer) WHERE m.name =~ \'((?i)USER_SEARCH)\' RETURN m.name, n.name ORDER BY m.name',
                    'desc': 'List this user\'s AdminTo privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '220': {
                    'query': 'MATCH (n:User)-[:MemberOf]->(m:Group),(m)-[:AdminTo]->(c:Computer) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN DISTINCT n.name,m.name,c.name ORDER BY m.name',
                    'desc': 'List this user\'s group-delegated AdminTo privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None and r.get('c.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} which is AdminTo {log.red}{r["c.name"]}{log.default}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '221': {
                    'query': 'MATCH p=(m:Computer)-[r:HasSession]->(n:User) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name',
                    'desc': 'List this user\'s sessions',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} HasSession on {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '222': {
                    'query': 'MATCH p=(n:User)-[r:ReadLAPSPassword]->(m:Computer) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List this user\'s ReadLAPSPassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '223': {
                    'query': 'MATCH p=(n:User)-[r:SyncLAPSPassword]->(m:Computer) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List this user\'s SyncLAPSPassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '224': {
                    'query': 'MATCH p=(n:User)-[r:ReadGMSAPassword]->(m:User) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List this user\'s ReadGMSAPassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '225': {
                    'query': 'MATCH (u:User)-[:AllowedToDelegate]->(c:Computer) WHERE u.name =~ \'((?i)USER_SEARCH)\' RETURN u.name,c.name',
                    'desc': 'List this user\'s Constrained Delegation privileges',
                    'message_generator': lambda r: (r.get('u.name') is not None and r.get('c.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '226': {
                    'query': 'MATCH (n:User)-[r:ForceChangePassword]->(m:User) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this user\'s ForceChangePassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '227': {
                    'query': 'MATCH (n:User)-[r:AddMember]->(m:Group) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this user\'s AddMember privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '228': {
                    'query': 'MATCH (n:User)-[r:AddSelf]->(m:Group) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this user\'s AddSelf privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '229': {
                    'query': 'MATCH (n:User)-[r:SQLAdmin]->(m:Computer) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this user\'s SQLAdmin privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '230': {
                    'query': 'MATCH (n:User)-[r:CanPSRemote]->(m:Computer) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this user\'s CanPSRemote privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '231': {
                    'query': 'MATCH (n:User)-[r:ExecuteDCOM]->(m:Computer) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this user\'s ExecuteDCOM privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '232': {
                    'query': 'MATCH (n:User)-[r:AllowedToAct]->(m) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this user\'s AllowedToAct privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '233': {
                    'query': 'MATCH (n:User)-[r:Owns]->(m) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this user\'s Owns privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '234': {
                    'query': 'MATCH (n:User)-[r:AllExtendedRights]->(m) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this user\'s AllExtendedRights privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '235': {
                    'query': 'MATCH (n:User)-[r:AddKeyCredentialLink]->(m) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this user\'s AddKeyCredentialLink privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '236': {
                    'query': 'MATCH (n:User)-[r:GenericAll]->(m) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this user\'s GenericAll privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '237': {
                    'query': 'MATCH (n:User)-[r:WriteDacl]->(m) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this user\'s WriteDacl privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '238': {
                    'query': 'MATCH (n:User)-[r:WriteOwner]->(m) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this user\'s WriteOwner privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '239': {
                    'query': 'MATCH (n:User)-[r:GenericWrite]->(m) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this user\'s GenericWrite privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '240': {
                    'query': 'MATCH (u:User) WHERE u.name =~ \'((?i)USER_SEARCH)\' RETURN u.name,u.description ORDER BY u.name',
                    'desc': 'List this user\'s description',
                    'message_generator': lambda r: (r.get('u.description') is not None and r.get('u.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["u.description"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '241': {
                    'query': 'MATCH (u:User) WHERE u.name =~ \'((?i)USER_SEARCH)\' return u.name,u.email ORDER BY u.name',
                    'desc': 'List this user\'s email',
                    'message_generator': lambda r: (r.get('u.email') is not None) and f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} email {log.reset}{log.red}{r["u.email"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '242': {
                    'query': 'MATCH (n:User)-[r:MemberOf]->(m) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this user\'s group memberships',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '243': {
                    'query': 'MATCH (u:User {dontreqpreauth: true}) WHERE u.name =~ \'((?i)USER_SEARCH)\' RETURN u.name',
                    'desc': 'List if this user\'s AS-REP roastable',
                    'message_generator': lambda r: (r.get('u.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["u.name"]}{log.reset}{log.default} is AS-REP roastable{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '244': {
                    'query': 'MATCH (n:User) WHERE n.hasspn=true AND n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name AS result ORDER BY n.name',
                    'desc': 'List if this user\'s kerberoastable',
                    'message_generator': lambda r: (r.get('result') is not None) and f'{log.default}User {log.reset}{log.red}{r["result"]}{log.reset}{log.default} is kerberoastable{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '245': {
                    'query': 'MATCH (n:User)-[r]->(m) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)',
                    'desc': 'List all privileges for this user',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None and r.get('TYPE(r)') is not None and r.get('labels(m)') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'general',
                },
                '246': {
                    'query': 'MATCH (n:User)-[:MemberOf]->(m:Group),(m)-[r]->(v) WHERE n.name =~ \'((?i)USER_SEARCH)\' RETURN n.name,TYPE(r),labels(v),m.name,v.name ORDER BY m.name',
                    'desc': 'List all group-delegated privileges for this user',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('m.name') is not None and r.get('v.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["v.name"]} {log.reset}{log.default}({r["labels(v)"][0]}/{r["labels(v)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'user',
                },
                '247': {
                    'query': 'MATCH (m:User),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n AND m.name =~ \'((?i)USER_SEARCH)\' return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to high-value targets for this user',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'user',
                },
                '248': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND m.name =~ \'((?i)USER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Domain Admins for this user',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'user',
                },
                '249': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND m.name =~ \'((?i)USER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Enterprise Admins for this user',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'user',
                },
                '250': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND m.name =~ \'((?i)USER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Domain Controllers for this user',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'user',
                },
                '251': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND m.name =~ \'((?i)USER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Exchange groups for this user',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'user',
                },
                '252': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND m.name =~ \'((?i)USER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to admin groups for this user',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'user',
                },
                '253': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND m.name =~ \'((?i)USER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to sql groups for this user',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'user',
                },
                '254': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND m.name =~ \'((?i)USER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to web groups for this user',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'user',
                },
                '255': {
                    'query': 'MATCH p=shortestPath((m:User)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND m.name =~ \'((?i)USER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to service groups for this user',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'user',
                },
                '256': {
                    'query': 'MATCH p=shortestPath((m)-[r*1..]->(n:User)) WHERE n.name =~ \'((?i)USER_SEARCH)\' AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to this user',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'user',
                },
                '257': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:User)) WHERE (m.objectid =~ \"(?i)S-1-5-21-.*-513\" OR m.objectid =~ \"(?i).*-S-1-5-11\" OR m.objectid =~ \"(?i).*-S-1-1-0\" OR m.objectid =~ \"(?i).*-S-1-5-32-545\") AND n.name =~ \'((?i)USER_SEARCH)\' AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to this user for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'user',
                },
                '258': {
                    'query': 'MATCH p=shortestPath((m {owned: true})-[r*1..]->(n:User)) WHERE n.name =~ \'((?i)USER_SEARCH)\' AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to this user for owned principles',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'user',
                },                                
                '259': {
                    'query': 'match p=(g:Group)-[:CanRDP]->(c:Computer) WHERE g.name =~ \'((?i)GROUP_SEARCH)\' return g.name,c.name',
                    'desc': 'List this group\'s RDP privileges',
                    'message_generator': lambda r: (r.get('g.name') is not None and r.get('c.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} CanRDP to {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '260': {
                    'query': 'MATCH (n:Group)-[:MemberOf]->(m:Group),(m)-[:CanRDP]->(c:Computer) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN DISTINCT n.name,m.name,c.name ORDER BY m.name',
                    'desc': 'List this group\'s group-delegated RDP privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('c.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which CanRDP to {log.red}{r["c.name"]}{log.default}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '261': {
                    'query': 'MATCH p=(m:Group)-[r:AdminTo]->(n:Computer) WHERE m.name =~ \'((?i)GROUP_SEARCH)\' RETURN m.name, n.name ORDER BY m.name',
                    'desc': 'List this group\'s AdminTo privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '262': {
                    'query': 'MATCH (n:Group)-[:MemberOf]->(m:Group),(m)-[:AdminTo]->(c:Computer) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN DISTINCT n.name,m.name,c.name ORDER BY m.name',
                    'desc': 'List this group\'s group-delegated AdminTo privileges',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('c.name') is not None and r.get('m.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} which is AdminTo {log.red}{r["c.name"]}{log.default}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '263': {
                    'query': 'MATCH p=(n:Group)-[r:ReadLAPSPassword]->(m:Computer) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List this group\'s ReadLAPSPassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '264': {
                    'query': 'MATCH p=(n:Group)-[r:SyncLAPSPassword]->(m:Computer) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List this group\'s SyncLAPSPassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '265': {
                    'query': 'MATCH p=(n:Group)-[r:ReadGMSAPassword]->(m:User) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List this group\'s ReadGMSAPassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '266': {
                    'query': 'MATCH (g:Group)-[:AllowedToDelegate]->(c:Computer) WHERE g.name =~ \'((?i)GROUP_SEARCH)\' RETURN g.name,c.name',
                    'desc': 'List this group\'s Constrained Delegation privileges',
                    'message_generator': lambda r: (r.get('g.name') is not None and r.get('c.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '267': {
                    'query': 'MATCH (n:Group)-[r:ForceChangePassword]->(m:User) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this group\'s ForceChangePassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '268': {
                    'query': 'MATCH (n:Group)-[r:AddMember]->(m:Group) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this group\'s AddMember privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '269': {
                    'query': 'MATCH (n:Group)-[r:AddSelf]->(m:Group) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this group\'s AddSelf privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '270': {
                    'query': 'MATCH (n:Group)-[r:SQLAdmin]->(m:Computer) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this group\'s SQLAdmin privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '271': {
                    'query': 'MATCH (n:Group)-[r:CanPSRemote]->(m:Computer) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this group\'s CanPSRemote privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '272': {
                    'query': 'MATCH (n:Group)-[r:ExecuteDCOM]->(m:Computer) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this group\'s ExecuteDCOM privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '273': {
                    'query': 'MATCH (n:Group)-[r:AllowedToAct]->(m) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this group\'s AllowedToAct privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '274': {
                    'query': 'MATCH (n:Group)-[r:Owns]->(m) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this group\'s Owns privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '275': {
                    'query': 'MATCH (n:Group)-[r:AllExtendedRights]->(m) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this group\'s AllExtendedRights privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '276': {
                    'query': 'MATCH (n:Group)-[r:AddKeyCredentialLink]->(m) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this group\'s AddKeyCredentialLink privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '277': {
                    'query': 'MATCH (n:Group)-[r:GenericAll]->(m) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this group\'s GenericAll privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '278': {
                    'query': 'MATCH (n:Group)-[r:WriteDacl]->(m) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this group\'s WriteDacl privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '279': {
                    'query': 'MATCH (n:Group)-[r:WriteOwner]->(m) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this group\'s WriteOwner privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '280': {
                    'query': 'MATCH (n:Group)-[r:GenericWrite]->(m) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this group\'s GenericWrite privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '281': {
                    'query': 'MATCH (g:Group) WHERE g.name =~ \'((?i)GROUP_SEARCH)\' RETURN g.name,g.description ORDER BY g.name',
                    'desc': 'List this group\'s description',
                    'message_generator': lambda r: (r.get('g.description') is not None and r.get('g.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["g.name"]}{log.reset}{log.default} description {log.reset}{log.red}{r["g.description"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '282': {
                    'query': 'MATCH (n:Group)-[r:MemberOf]->(m) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this group\'s group memberships',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '283': {
                    'query': 'MATCH (n)-[r:MemberOf]->(m) WHERE m.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,m.name,labels(m),labels(n) ORDER BY n.name',
                    'desc': 'List this group\'s members',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.red}{r["n.name"]}{log.reset}{log.default} ({r["labels(n)"][0]}/{r["labels(n)"][1]}) is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '284': {
                    'query': 'MATCH (n:Group)-[r:AdminTo|HasSession|ForceChangePassword|AddMember|AddSelf|CanPSRemote|ExecuteDCOM|SQLAdmin|AllowedToDelegate|GenericAll|GenericWrite|WriteDacl|Owns|AddKeyCredentialLink|ReadLAPSPassword|SyncLAPSPassword|ReadGMSAPassword|AllExtendedRights|AllowedToAct]->(m) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)',
                    'desc': 'List all privileges for this group',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '285': {
                    'query': 'MATCH (n:Group)-[:MemberOf]->(m:Group),(m)-[r]->(v) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' RETURN n.name,TYPE(r),labels(v),m.name,v.name ORDER BY m.name',
                    'desc': 'List all group-delegated privileges for this group',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None and r.get('v.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["v.name"]} {log.reset}{log.default}({r["labels(v)"][0]}/{r["labels(v)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'group',
                },
                '286': {
                    'query': 'MATCH (m:Group),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n AND m.name =~ \'((?i)GROUP_SEARCH)\' return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to high-value targets for this group',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'group',
                },
                '287': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND NOT m=n AND m.name =~ \'((?i)GROUP_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Domain Admins for this group',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'group',
                },
                '288': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND NOT m=n AND m.name =~ \'((?i)GROUP_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Enterprise Admins for this group',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'group',
                },
                '289': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND NOT m=n AND m.name =~ \'((?i)GROUP_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Domain Controllers for this group',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'group',
                },
                '290': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND NOT m=n AND m.name =~ \'((?i)GROUP_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Exchange groups for this group',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'group',
                },
                '291': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND NOT m=n AND m.name =~ \'((?i)GROUP_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to admin groups for this group',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'group',
                },
                '292': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND NOT m=n AND m.name =~ \'((?i)GROUP_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to sql groups for this group',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'group',
                },
                '293': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND NOT m=n AND m.name =~ \'((?i)GROUP_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to web groups for this group',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'group',
                },
                '294': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND NOT m=n AND m.name =~ \'((?i)GROUP_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to service groups for this group',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'group',
                },
                '295': {
                    'query': 'MATCH p=shortestPath((m)-[r*1..]->(n:Group)) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to this group',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'group',
                },
                '296': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Group)) WHERE (m.objectid =~ "(?i)S-1-5-21-.*-513" OR m.objectid =~ "(?i).*-S-1-5-11" OR m.objectid =~ "(?i).*-S-1-1-0" OR m.objectid =~ "(?i).*-S-1-5-32-545") AND n.name =~ \'((?i)GROUP_SEARCH)\' AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to this group for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'group',
                },
                '297': {
                    'query': 'MATCH p=shortestPath((m {owned: true})-[r*1..]->(n:Group)) WHERE n.name =~ \'((?i)GROUP_SEARCH)\' AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to this group for owned principles',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'group',
                },
                '298': {
                    'query': 'MATCH p=(m:Computer)-[r:AdminTo]->(n:Computer) WHERE m.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN m.name, n.name ORDER BY m.name',
                    'desc': 'List this computer\'s AdminTo privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} is AdminTo {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '299': {
                    'query': 'MATCH (n:Computer)-[:MemberOf]->(m:Group),(m)-[:AdminTo]->(c:Computer) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN DISTINCT n.name,m.name,c.name ORDER BY m.name',
                    'desc': 'List this computer\'s group-delegated AdminTo privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None and r.get('c.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]}{log.reset}{log.default} which is AdminTo {log.red}{r["c.name"]}{log.default}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '300': {
                    'query': 'MATCH p=(n:Computer)-[r:ReadLAPSPassword]->(m:Computer) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List this computer\'s ReadLAPSPassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '301': {
                    'query': 'MATCH p=(n:Computer)-[r:SyncLAPSPassword]->(m:Computer) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List this computer\'s SyncLAPSPassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can sync LAPS passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '302': {
                    'query': 'MATCH p=(n:Computer)-[r:ReadGMSAPassword]->(m:User) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name ORDER by n.name',
                    'desc': 'List this computer\'s ReadGMSAPassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can read GMSA passwords for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '303': {
                    'query': 'MATCH (n:Computer)-[:AllowedToDelegate]->(c:Computer) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,c.name',
                    'desc': 'List this computer\'s Constrained Delegation privileges',
                    'message_generator': lambda r: (r.get('c.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is allowed to delegate for {log.reset}{log.red}{r["c.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '304': {
                    'query': 'MATCH (n:Computer)-[r:ForceChangePassword]->(m:User) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this computer\'s ForceChangePassword privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can force change password for {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '305': {
                    'query': 'MATCH (n:Computer)-[r:AddMember]->(m:Group) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this computer\'s AddMember privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add members to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '306': {
                    'query': 'MATCH (n:Computer)-[r:AddSelf]->(m:Group) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this computer\'s AddSelf privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can add itself to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '307': {
                    'query': 'MATCH (n:Computer)-[r:SQLAdmin]->(m:Computer) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this computer\'s SQLAdmin privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is SQLAdmin to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '308': {
                    'query': 'MATCH (n:Computer)-[r:CanPSRemote]->(m:Computer) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this computer\'s CanPSRemote privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can PSRemote to {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '309': {
                    'query': 'MATCH (n:Computer)-[r:ExecuteDCOM]->(m:Computer) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name ORDER BY n.name',
                    'desc': 'List this computer\'s ExecuteDCOM privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} can ExecuteDCOM on {log.reset}{log.red}{r["m.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '310': {
                    'query': 'MATCH (n:Computer)-[r:AllowedToAct]->(m) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this computer\'s AllowedToAct privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is AllowedToAct for {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '311': {
                    'query': 'MATCH (n:Computer)-[r:Owns]->(m) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this computer\'s Owns privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} Owns {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '312': {
                    'query': 'MATCH (n:Computer)-[r:AllExtendedRights]->(m) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this computer\'s AllExtendedRights privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AllExtendedRights over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '313': {
                    'query': 'MATCH (n:Computer)-[r:AddKeyCredentialLink]->(m) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this computer\'s AddKeyCredentialLink privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has AddKeyCredentialLink over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '314': {
                    'query': 'MATCH (n:Computer)-[r:GenericAll]->(m) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this computer\'s GenericAll privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericAll over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '315': {
                    'query': 'MATCH (n:Computer)-[r:WriteDacl]->(m) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this computer\'s WriteDacl privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteDacl over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '316': {
                    'query': 'MATCH (n:Computer)-[r:WriteOwner]->(m) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this computer\'s WriteOwner privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has WriteOwner over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '317': {
                    'query': 'MATCH (n:Computer)-[r:GenericWrite]->(m) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this computer\'s GenericWrite privileges',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has GenericWrite over {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '318': {
                    'query': 'MATCH (n:Computer)-[r:MemberOf]->(m) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,m.name,labels(m) ORDER BY n.name',
                    'desc': 'List this computer\'s group memberships',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '319': {
                    'query': 'MATCH (n:Computer)-[r]->(m) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,TYPE(r),labels(m),m.name ORDER BY TYPE(r)',
                    'desc': 'List all privileges for this computer',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}{log.default} has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["m.name"]} {log.reset}{log.default}({r["labels(m)"][0]}/{r["labels(m)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '320': {
                    'query': 'MATCH (n:Computer)-[:MemberOf]->(m:Group),(m)-[r]->(v) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' RETURN n.name,TYPE(r),labels(v),m.name,v.name ORDER BY m.name',
                    'desc': 'List all group-delegated privileges for this computer',
                    'message_generator': lambda r: (r.get('m.name') is not None and r.get('n.name') is not None and r.get('v.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}is MemberOf {log.reset}{log.red}{r["m.name"]} {log.reset}{log.default}which has {log.reset}{log.red}{r["TYPE(r)"]}{log.reset}{log.default} over {log.red}{r["v.name"]} {log.reset}{log.default}({r["labels(v)"][0]}/{r["labels(v)"][1]}){log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'computer',
                },
                '321': {
                    'query': 'MATCH (m:Computer),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") AND NOT m=n AND m.name =~ \'((?i)COMPUTER_SEARCH)\' return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to high-value targets for this computer',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'computer',
                },
                '322': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-512" AND m.name =~ \'((?i)COMPUTER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Domain Admins for this computer',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'computer',
                },
                '323': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-519" AND m.name =~ \'((?i)COMPUTER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Enterprise Admins for this computer',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'computer',
                },
                '324': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.objectid =~ "(?i)S-1-5-21-.*-516" AND m.name =~ \'((?i)COMPUTER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") return m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Domain Controllers for this computer',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'computer',
                },
                '325': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)EXCHANGE).*" AND m.name =~ \'((?i)COMPUTER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to Exchange groups for this computer',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'computer',
                },
                '326': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)admin|adm).*" AND m.name =~ \'((?i)COMPUTER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to admin groups for this computer',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'computer',
                },
                '327': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)SQL).*" AND m.name =~ \'((?i)COMPUTER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to sql groups for this computer',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'computer',
                },
                '328': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)WEB).*" AND m.name =~ \'((?i)COMPUTER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to web groups for this computer',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'computer',
                },
                '329': {
                    'query': 'MATCH p=shortestPath((m:Computer)-[r*1..]->(n:Group)) WHERE n.name =~ ".*((?i)service|svc).*" AND m.name =~ \'((?i)COMPUTER_SEARCH)\' AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to service groups for this computer',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'computer',
                },
                '330': {
                    'query': 'MATCH p=shortestPath((m)-[r*1..]->(n:Computer)) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to this computer',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'computer',
                },
                '331': {
                    'query': 'MATCH p=shortestPath((m:Group)-[r*1..]->(n:Computer)) WHERE (m.objectid =~ "(?i)S-1-5-21-.*-513" OR m.objectid =~ "(?i).*-S-1-5-11" OR m.objectid =~ "(?i).*-S-1-1-0" OR m.objectid =~ "(?i).*-S-1-5-32-545") AND n.name =~ \'((?i)COMPUTER_SEARCH)\' AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to this computer for Users, Domain Users, Authenticated Users, or Everyone groups',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'computer',
                },
                '332': {
                    'query': 'MATCH p=shortestPath((m {owned: true})-[r*1..]->(n:Computer)) WHERE n.name =~ \'((?i)COMPUTER_SEARCH)\' AND NOT m=n AND NONE (r IN relationships(p) WHERE type(r)= "GetChanges") AND NONE (r in relationships(p) WHERE type(r)="GetChangesAll") RETURN m.name,p ORDER BY m.name',
                    'desc': 'List all shortest paths to this computer for owned principles',
                    'message_generator': None,
                    'handler': self.handle_path_query,
                    'type': 'computer',
                },
                '333': {
                    'query': 'MATCH (n:Group) WHERE n.name =~ \'REGEX\' RETURN n.name ORDER BY n.name',
                    'desc': 'Search for groups matching the regex',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'regex',
                },
                '334': {
                    'query': 'MATCH (n:User) WHERE n.name =~ \'REGEX\' RETURN n.name ORDER BY n.name',
                    'desc': 'Search for users matching the regex',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'regex',
                },
                '335': {
                    'query': 'MATCH (n:Computer) WHERE n.name =~ \'REGEX\' RETURN n.name ORDER BY n.name',
                    'desc': 'Search for computers matching the regex',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'regex',
                },
                '336': {
                    'query': 'MATCH (n:User) WHERE n.description =~ \'REGEX\' RETURN n.name,n.description ORDER BY n.name',
                    'desc': 'Search for user descriptions matching the regex',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('n.description') is not None) and f'{log.default}User {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}description {log.reset}{log.red}{r["n.description"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'regex',
                },
                '337': {
                    'query': 'MATCH (n:Group) WHERE n.description =~ \'REGEX\' RETURN n.name,n.description ORDER BY n.name',
                    'desc': 'Search for group descriptions matching the regex',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('n.description') is not None) and f'{log.default}Group {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}description {log.reset}{log.red}{r["n.description"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'regex',
                },
                '338': {
                    'query': 'MATCH (n:Computer) WHERE n.operatingsystem =~ \'REGEX\' RETURN n.name,n.operatingsystem ORDER BY n.name',
                    'desc': 'Search for OSs matching the regex',
                    'message_generator': lambda r: (r.get('n.name') is not None and r.get('n.operatingsystem') is not None) and f'{log.default}Computer {log.reset}{log.red}{r["n.name"]} {log.reset}{log.default}OS {log.reset}{log.red}{r["n.operatingsystem"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'regex',
                },
                '339': {
                    'query': 'MATCH (n:GPO) WHERE n.name =~ \'REGEX\' RETURN n.name ORDER BY n.name',
                    'desc': 'Search for GPOs matching the regex',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}GPO {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'regex',
                },
                '340': {
                    'query': 'MATCH (n:Container) WHERE n.name =~ \'REGEX\' RETURN n.name ORDER BY n.name',
                    'desc': 'Search for Containers matching the regex',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}Container {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'regex',
                },
                '341': {
                    'query': 'MATCH (n:OU) WHERE n.name =~ \'REGEX\' RETURN n.name ORDER BY n.name',
                    'desc': 'Search for OUs matching the regex',
                    'message_generator': lambda r: (r.get('n.name') is not None) and f'{log.default}OU {log.reset}{log.red}{r["n.name"]}{log.reset}' or None,
                    'handler': self.handle_standard_query,
                    'type': 'regex',
                },
            }
                    
        except Exception as e:
            log.log_error(e)
            

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
    
    
    def search_queries(self, search_string):
        results = {k: v for k, v in self.queries.items() if search_string.lower() in v['desc'].lower()}
    
        if results:
            print(f'{log.green}Cypher matches for "{search_string}":{log.reset}')
            for key, value in results.items():
                print(f'{log.red}{key}.{log.reset} {value["desc"]}')
        else:
            print(f'{log.yellow}No matches found for "{search_string}".{log.reset}')
    
    
    def print_queries_by_type(self, type):
        if type == "all":
            self.print_all_queries()
            return
        print(f'{log.default}{type.capitalize()} Cyphers{log.reset}')
        for num, data in self.queries.items():
            if data['type'] == type:
                print(f'{log.default}{num}.) {log.reset}{data["desc"]}')

    def print_all_queries(self):
        print(f'{log.default}All Cyphers{log.reset}')
        for num, data in self.queries.items():
            print(f'{log.default}{num}.) {log.reset}{data["desc"]}')


    def replace_fillers_in_string(self, string):
        replacements = {
            'USER_SEARCH': self.user_search,
            'GROUP_SEARCH': self.group_search,
            'COMPUTER_SEARCH': self.computer_search,
            'REGEX': self.regex,
        }
    
        for filler, replacement in replacements.items():
            string = string.replace(filler, replacement)
    
        return string

    
    def handle_standard_query(self, query_data, f):
        try:
            with self.driver.session(database=self.database) as session:                
                results = session.run(self.replace_fillers_in_string(query_data['query']))
                if results.peek() is None:
                    log.log_no_results()
                else:
                    count = 0
                    for r in results:
                        msg = query_data['message_generator'](r)
                        if msg is None:
                            continue
                        self.handle_output(f, msg)
                        count += 1
                    if count == 0:
                        log.log_no_results()
                    if f:
                        util.handle_export(count, f) 
        except Exception as e:
            log.log_error(e)
            
    
    def handle_path_query(self, query_data, f):
        try:
            with self.driver.session(database=self.database) as session:
                results = session.run(self.replace_fillers_in_string(query_data['query']))                
                if results.peek() is None:
                    log.log_no_results()
                else:
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
                                self.handle_output(f, '*' * mid_len)
                                self.handle_output(f, f'*Path {p_count}* {path.start_node["name"]} -> {path.end_node["name"]}*')
                                self.handle_output(f, '*' * mid_len)
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
                                self.handle_output(f, final)
                                p_count += 1
                        count += 1
                    if count == 0:
                        log.log_no_results()
                    if f:
                        util.handle_export(count, f) 
        except Exception as e:
            log.log_error(e)


    def handle_output(self, f, message):
        if f == "":
            print(message)
        else:
            with open(f, 'a+') as file:  # Open file in append mode
                print(message)
                file.write(util.strip_ansi_escape_sequences(message) + '\n')


    def run_query(self, option, f):
        try:
            query_data = self.queries.get(option)
            if query_data is not None:
                query_data['handler'](query_data, f)
            else:
                log.log_error("Cypher does not exist!")
        except Exception as e:    
            log.log_error(e)