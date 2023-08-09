#!/usr/bin/python3
# Author: Dylan Evans|fin3ss3g0d
from neo4j import GraphDatabase
import argparse
import json
import sys
import log


class Driver:

    def __init__(self, user, password, db):
        try:
            self.driver = GraphDatabase.driver("neo4j://localhost:7687", auth=(user, password))
            self.database = db
        except Exception as e:
            log.log_error(e)

    def close(self):
        self.driver.close()

    def set_property(self, tx, node_name, property_name, value):
        tx.run(f"MATCH (n {{name: $name}}) SET n.{property_name} = $value", name=node_name, value=value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python terminal app that runs Neo4j cyphers on BloodHound data sets in order to modify node properties.")
    parser.add_argument("-c", "--config", help="Config file", required=True)
    parser.add_argument("-l", "--list", help="List of node names", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-o", "--owned", help="Set target nodes as owned", action='store_true')
    group.add_argument("-v", "--high-value", help="Set target nodes as high-value", action='store_true')
    group.add_argument("-u", "--unset", help="Unset target nodes' owned/high-value property", choices=['owned', 'high_value'], type=str)

    args = parser.parse_args()

    try:
        with open(args.config) as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log.log_error(e)
        sys.exit(1)

    try:
        d = Driver(config["user"], config["pwd"], config["database"])
        with d.driver.session(database=d.database) as session:
            with open(args.list, "r") as file:
                for line in file:
                    try:
                        node_name = line.strip().upper()
                        if args.owned:
                            session.execute_write(lambda tx: d.set_property(tx, node_name, 'owned', True))
                            print(f'{log.green}[+] {node_name} successfully set to owned!{log.reset}')
                        elif args.high_value:
                            session.execute_write(lambda tx: d.set_property(tx, node_name, 'highvalue', True))
                            print(f'{log.green}[+] {node_name} successfully set to high-value!{log.reset}')
                        elif args.unset:
                            property_to_unset = 'owned' if args.unset == 'owned' else 'highvalue'
                            session.execute_write(lambda tx: d.set_property(tx, node_name, property_to_unset, False))
                            print(f'{log.green}[+] {node_name} successfully unset {property_to_unset}!{log.reset}')
                    except Exception as e:
                        log.log_error(e)

        d.driver.close()

    except Exception as e:
        log.log_error(e)