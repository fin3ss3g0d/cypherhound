#!/usr/bin/env python3
import sys, yaml
from tempfile import template

from util import redify, deep_redify, greenify, yellowify, strip_ansi_escape_sequences, handle_export
from log import log_default, log_error, log_no_results, log_green, log_red, log_yellow

from neo4j import GraphDatabase
from collections import OrderedDict
from pathlib import Path

from jinja2 import Template, UndefinedError
from pathlib import Path


def _looks_like_path(obj) -> bool:
    """True if obj has the attributes we need for a Neo4j Path."""
    return (
        hasattr(obj, "start_node") and
        hasattr(obj, "end_node")   and
        hasattr(obj, "__iter__")   # paths are iterable over relationships
    )


class Driver:
    # --------------------------------------------------------------------- #
    # __init__
    # --------------------------------------------------------------------- #
    def __init__(self,
                 user: str,
                 password: str,
                 db: str,
                 template_file: str,
                 u_search="",
                 g_search="",
                 c_search="",
                 regex=""):

        self.driver  = GraphDatabase.driver("neo4j://localhost:7687",
                                            auth=(user, password))
        self.database        = db
        self.user_search     = u_search
        self.group_search    = g_search
        self.computer_search = c_search
        self.regex           = regex

        self.queries = self._load_queries(template_file)

    # --------------------------------------------------------------------- #
    # YAML loader
    # --------------------------------------------------------------------- #
    def _load_queries(self, path: str) -> OrderedDict[str, dict]:
        """Read queries.yaml → OrderedDict keyed '1', '2', …"""
        tpl = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        qlist = tpl.get("queries", [])

        # sort alphabetically by description
        qlist.sort(key=lambda x: x["desc"].lower())

        queries = OrderedDict()
        for idx, q in enumerate(qlist, 1):
            queries[str(idx)] = {
                "query":        q["cypher"],
                "desc":         q["desc"],
                "group":        q["group"],
                "msg_template": q.get("msg_template"),  # may be None
            }
        return queries


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
            log_green(f'Cypher matches for "{search_string}":')
            for key, value in results.items():
                print(f'{redify(key + ".")} {value["desc"]}')
        else:
            log_yellow(f'No matches found for "{search_string}".')


    def print_queries_by_group(self, group):
        if group == "all":
            self.print_all_queries()
            return
        log_green(f'{group.capitalize()} Cyphers:')
        for num, data in self.queries.items():
            if data['group'] == group:
                print(f'{redify(num + ".")} {data["desc"]}')


    def print_all_queries(self):
        log_green(f'All Cyphers:')
        for num, data in self.queries.items():
            print(f'{redify(num + ".")} {data["desc"]}')


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


    # --------------------------------------------------------------------- #
    # STANDARD query executor – Jinja2 templating
    # --------------------------------------------------------------------- #
    def handle_standard_query(self, query_data: dict, outfile: str):
        try:
            with self.driver.session(database=self.database) as session:
                cypher = self.replace_fillers_in_string(query_data["query"])
                results = session.run(cypher)

                if results.peek() is None:
                    log_no_results()
                    return

                # Pre-compile the template once
                template = None
                if query_data["msg_template"]:
                    template = Template(query_data["msg_template"])

                count = 0
                for rec in results:
                    raw = rec.data()

                    # colour every first-level value that is a str / int / float / bool
                    ctx = {
                        k: redify(v) if isinstance(v, (str, int, float, bool)) else v
                        for k, v in raw.items()
                    }

                    msg = template.render(**ctx) if template else str(raw)

                    if not msg:
                        continue
                    self.handle_output(outfile, msg)
                    count += 1

                if count == 0:
                    log_no_results()
                if outfile:
                    handle_export(count, outfile)

        except Exception as e:
            log_error(e)


    # --------------------------------------------------------------------- #
    # PATH query executor
    # --------------------------------------------------------------------- #
    def handle_path_query(self, query_data: dict, outfile: str):
        try:
            with self.driver.session(database=self.database) as session:
                cypher   = self.replace_fillers_in_string(query_data["query"])
                results  = session.run(cypher)

                if results.peek() is None:
                    log_no_results()
                    return

                template = Template(query_data["msg_template"]) \
                           if query_data["msg_template"] else None

                count = 0
                path_idx = 1
                for rec in results:
                    raw_path = next((v for v in rec.values() if _looks_like_path(v)), None)
                    if raw_path is None:
                        continue

                    ctx = rec.data()            # ← after we have extracted the path
                    ctx.update({
                        k: redify(v) if isinstance(v, (str, int, float, bool)) else v
                        for k, v in ctx.items()
                    })

                    # start/end names now come from raw_path
                    start_name = raw_path.start_node.get("name")
                    end_name   = raw_path.end_node.get("name")

                    # hops list
                    hops = [
                        {
                            "src": rel.start_node.get("name"),
                            "src_labels": list(rel.start_node.labels),
                            "type": rel.type,
                            "dst": rel.end_node.get("name"),
                            "dst_labels": list(rel.end_node.labels),
                        }
                        for rel in raw_path
                    ]

                    # 4. enrich the context
                    ctx.update({
                        "start_name": start_name,
                        "end_name":   end_name,
                        "hops":       hops,
                        "path_num":   path_idx,
                    })
                    ctx = deep_redify(ctx)

                    # 5. render or fallback
                    if template:
                        try:
                            msg = template.render(**ctx)
                        except UndefinedError as ue:
                            log_error(f"Template error: {ue}")
                            msg = None
                    else:
                        # default text – 1 line per hop
                        pieces = [f"*Path {path_idx}* {start_name} → {end_name}"]
                        for h in hops:
                            pieces.append(
                                f"{redify(h['src'])} ({'/'.join(h['src_labels'])}) "
                                f"--{h['type']}→ "
                                f"{redify(h['dst'])} ({'/'.join(h['dst_labels'])})"
                            )
                        msg = "\n".join(pieces)

                    if msg:
                        self.handle_output(outfile, msg)
                        count += 1
                        path_idx += 1

                if count == 0:
                    log_no_results()
                if outfile:
                    handle_export(count, outfile)

        except Exception as e:
            log_error(e)


    def handle_output(self, f, message):
        if f == "":
            print(message)
        else:
            with open(f, 'a+', encoding=sys.getfilesystemencoding(), errors='replace') as file:
                print(message)
                file.write(strip_ansi_escape_sequences(message) + '\n')


    def handle_query(self, query_data: dict, outfile: str):
        """Run a query and handle its output."""
        if "shortestpath" in query_data['query'].lower():
            self.handle_path_query(query_data, outfile)
        else:
            self.handle_standard_query(query_data, outfile)


    def run_query(self, option: str, outfile: str):
            try:
                q = self.queries.get(option)
                if q:
                    self.handle_query(q, outfile)
                else:
                    log_error("Cypher does not exist!")
            except Exception as e:
                log_error(e)
