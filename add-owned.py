#!/usr/bin/python3
# Author: Dylan Evans|fin3ss3g0d
from neo4j import GraphDatabase
import argparse
import json
import sys
import log


class Driver:


    def __init__(self, user,  password, db):
        try:
            self.driver = GraphDatabase.driver("neo4j://localhost:7687", auth=(user, password))
            self.database = db
        except Exception as e:
            log.log_error(e)
            

    def close(self):        
        self.driver.close()    
        

    def set_owned(self, tx, node_name):
        tx.run("MATCH (n {name: $name}) SET n.owned = true", name=node_name)
        
        
    def set_high_value(self, tx, node_name):
        tx.run("MATCH (n {name: $name}) SET n.highvalue = true", name=node_name)
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python terminal app that runs Neo4j cyphers on BloodHound data sets in order to modify node properties.")
    parser.add_argument("-c", "--config", help="Config file", required=True)
    parser.add_argument("-l", "--list", help="List of node names", required=True)
    parser.add_argument("-o", "--owned", help="Set target nodes as owned", required=False, action='store_true')
    parser.add_argument("-v", "--high-value", help="Set target nodes as high-value", required=False, action='store_true')
    args = parser.parse_args()
    
    if not args.owned and not args.high_value or args.owned and args.high_value:
        parser.print_help()
        sys.exit(1)
    
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
                    node_name = line.strip().upper()
                    if args.owned:                        
                        session.execute_write(lambda tx: d.set_owned(tx, node_name))
                        print(f'{log.green}[+] {node_name} successfully set to owned!{log.reset}')
                    else:
                        session.execute_write(lambda tx: d.set_high_value(tx, node_name))
                        print(f'{log.green}[+] {node_name} successfully set to high-value!{log.reset}')
                    
        d.driver.close()

    except Exception as e:
        log.log_error(e)