#!/usr/bin/python3
# Author: Dylan Evans|fin3ss3g0d
import re
import sys
import os
import collections

def process_file(filename, domain):
    user_group_dict = collections.defaultdict(set)

    try:
        with open(filename, 'r', encoding='cp1252') as file:
            for line in file:
                match = re.match(r'User ([\w.-]+)@' + domain + r' is MemberOf (.*?)@' + domain + r' (\(Group/Base\)|\(Base/Group\))', line, re.IGNORECASE)
                if match:
                    username = match.group(1).lower()
                    group = match.group(2).strip()
                    user_group_dict[username].add(group)

        print("user_group_dict contents:")
        for key, values in user_group_dict.items():
            print(f"{key}: {', '.join(values)}")

    except Exception as e:
        print(f"Error processing file: {e}")

    return user_group_dict

def process_ntds_file(filename, user_group_dict, output_dir):
    group_files = set()

    try:
        with open(filename, 'r', encoding='cp1252') as file:
            for line in file:
                match = re.match(r'(.*?)\\([\w.-]*):.*', line)
                if match:
                    domain = match.group(1).lower()
                    username = match.group(2).lower()
                    print(f"Checking for match: {username}")
                    if username in user_group_dict:
                        for group in user_group_dict[username]:
                            print(f"Match found for user '{username}' in group '{group}': {line.strip()}")
                            group_name = group.replace(' ', '_')
                            output_file_path = os.path.join(output_dir, f'{group_name}.txt')
                            group_files.add(output_file_path)
                            with open(output_file_path, 'a') as output_file:
                                output_file.write(f"{domain}\\{username}\n")

    except Exception as e:
        print(f"Error processing NTDS file: {e}")

    print("\nCommandline arguments for DPAT (run from output dir):")
    print("-g", end=' ')
    for file_path in group_files:
        print(f'"{os.path.basename(file_path)}"', end=' ')
    print()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"Usage: python {sys.argv[0]} <memberships_filename> <domain> <ntds_filename> <output_directory>")
        sys.exit(1)

    try:
        user_group_dict = process_file(sys.argv[1], sys.argv[2])
        process_ntds_file(sys.argv[3], user_group_dict, sys.argv[4])
    except Exception as e:
        print(f"Error running script: {e}")
