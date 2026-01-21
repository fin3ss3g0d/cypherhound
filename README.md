# CypherHound

![logo](images/logo.png)

A `Python3` terminal application that contains `Neo4j` cyphers for BloodHound data sets with a script to automate importing them into BloodHound CE.

## Output Samples

**Terminal**

![demo](images/demo%20output.png)

**HTML Report**

![report summary](images/report%20summary.png)

**HTML Report (continued)**

![details sample](images/adminto%20report%20sample.png)

## Why?

[BloodHound](https://github.com/SpecterOps/BloodHound) is a staple tool for every penetration tester. However, there are some negative side effects based on its design. I will cover the biggest pain points I've experienced and what this tool aims to address:

1. **My tools think in lists** - until my tools parse exported `JSON` graphs, I need graph results in a line-by-line format `.txt` file *to actually attack things from other tools*
2. **Copy/pasting graph results** - this plays into the first but *do we need to really explain this one*?
3. **Graphs can be too large to draw** -  Large AD environments, multiple shortest paths being drawn on the same graph, etc. The information contained in ***any*** graph can aid our goals as the attacker and we ***need*** to be able to view ***all*** data efficiently.
4. **Manually running custom cyphers is time-consuming** - let's automate it :)

This tool can provide significant value for both red and blue teams.

## Features

Take back control of your `BloodHound` data with `CypherHound`!

- Read cypher templates from a YAML file
  - Set cyphers to search based on user input (user, group, and computer-specific)
  - User-defined regex cyphers
- User-defined exporting of all results
  - Examples provided in `grep/cut/awk`-friendly format
  - Export any combination of cyphers to a modern, sleek HTML report
- Run the same queries from the BloodHound CE GUI
  - YAML -> JSON converter and automated BloodHound CE query importer
  - BloodHound Legacy `customqueries.json` importer script into BloodHound CE included

## Installation

Make sure to have `python3` installed and run:

`python3 -m pip install -r requirements.txt`

## Usage

Start the program with: `python3 cypherhound.py -c config.json -y queries.yaml`

## config.json

The program will read a configuration file in `json` format. An example of this file is shown below:

```json
{
    "user": "neo4j",
    "pwd": "password",
    "database": "neo4j"
}
```

where:
- `user` is your `Neo4j` username
- `pwd` is your `Neo4j` password
- `database` is your `Neo4j` database

## YAML Format

The program reads queries from a YAML file in the format below. [ad-queries.yaml](ad-queries.yaml) has been provided as an example containing queries related to Active Directory. ***msg_template is not required for shortest paths queries but they must return the variable containing the path***

```yaml
queries:
- group: general
  desc: List all AddKeyCredentialLink privileges for owned principals
  cypher: |-
    MATCH (n {owned: true})-[r:AddKeyCredentialLink]->(m)
    RETURN n.name AS n_name, m.name AS m_name, labels(m) AS labels_m, labels(n) AS labels_n
    ORDER BY n.name
  msg_template: |-
    {{ n_name }} ({{ labels_n[0] }}/{{ labels_n[1] }}) has AddKeyCredentialLink over {{ m_name }} ({{
    labels_m[0] }}/{{ labels_m[1] }})
```

A table breakdown of the keys/value pairs can be seen below:

| Key          | Description                                                                                       |
|--------------|---------------------------------------------------------------------------------------------------|
| `group`        | The group this query belongs to, groups are user-defined e.g. "general"                         |
| `desc`         | The description of the query                                                                      |
| `cypher`       | The query itself in Neo4j format                                                                  |
| `msg_template` | Jinja2 template for the terminal output based on cypher variables, **use aliases for Neo4j variables to avoid Jinja attempting to render as nested variables** |

## Dynamic Parameters in Cypher (Jinja2 `params.*`)

The program uses **Jinja2** to render Cypher. Define runtime parameters with the `set` command and reference them in YAML as `{{ params.<key> }}`.

**CLI**
```
set <key> <value...> # e.g., set user john.doe@example.com
unset <key> # optional
show # optional
```

**YAML Example**

```yaml
- group: user
  desc: List all privileges for this user
  cypher: |-
    MATCH (n:User)-[r]->(m)
    WHERE n.name =~ '((?i){{ params.user }})'
    RETURN n.name AS n_name, TYPE(r) AS rel_type, labels(m) AS labels_m, m.name AS m_name
    ORDER BY TYPE(r)
  msg_template: |-
    User {{ n_name }} has {{ rel_type }} over {{ m_name }} ({{ labels_m[0] }}/{{ labels_m[1] }})
```

**Common Param Patterns**
| Param key            | Example value                         | Use in Cypher                                    |
|----------------------|---------------------------------------|--------------------------------------------------|
| `params.user`        | `john.doe@example.com`                | `= {{ params.user }}`                            |
| `params.user_regex`  | `(?i)john\.doe(@example\.com)?`       | `=~ '{{ params.user_regex }}'`                   |
| `params.group`       | `Domain Admins@example.com`           | `= {{ params.group }}`                           |
| `params.prefix`      | `ACME-`                               | `STARTS WITH {{ params.prefix }}`                |

## JSON Format

This repository provides a [query-importer.py](scripts/bloodhound-ce/query-importer.py) script to automate importing queries into the BloodHound CE UI from a JSON file. [bh_query_converter.py](scripts/bloodhound-ce/bh_query_converter.py) has also been provided to convert a YAML file intended for the terminal application to the JSON format expected by [query-importer.py](scripts/bloodhound-ce/query-importer.py) & BloodHound CE. An example of the required JSON format can be seen below:

```json
{
  "queries": [
    {
      "name": "List all AddKeyCredentialLink privileges for owned principals",
      "description": "List all AddKeyCredentialLink privileges for owned principals - General",
      "query": "MATCH p=(n {owned: true})-[r:AddKeyCredentialLink]->(m)\nRETURN p\nORDER BY n.name"
    },
    {
      "name": "List all AddKeyCredentialLink privileges for Users, Domain Users, Authenticated Users, and Everyone groups",
      "description": "List all AddKeyCredentialLink privileges for Users, Domain Users, Authenticated Users, and Everyone groups - General",
      "query": "MATCH p=(n:Group)-[r:AddKeyCredentialLink]->(m)\nWHERE (n.objectid =~ \"(?i)S-1-5-21-.*-513\" OR n.objectid =~ \"(?i).*-S-1-5-11\" OR n.objectid =~ \"(?i).*-S-1-1-0\" OR n.objectid =~ \"(?i).*-S-1-5-32-545\")\nRETURN p\nORDER BY n.name"
    }
  ]
}
```

## Commands

The full command menu is shown below:

```
Documented commands (use 'help -v' for verbose/'help <topic>' for details):
======================================================================================================
alias                 Manage aliases
clear                 Clear the terminal.
cls                   Clear the terminal.
edit                  Run a text editor and optionally open a file with it
export                Run a query and save its results
help                  List available commands or provide detailed help for a specific command
history               View, run, edit, save, or clear previously entered commands
list                  List queries by group.
macro                 Manage macros
report                Run multiple queries and generate a HTML report
run                   Execute a query
run_pyscript          Run a Python script file inside the console
run_script            Run commands in script file that is encoded as either ASCII or UTF-8 text
search                Full-text search through stored queries.
set                   Set a dynamic search parameter (set <TARGET> <VALUE...>)
shell                 Execute a command as if at the OS prompt
shortcuts             List available shortcuts
show                  Show dynamic search parameters
unset                 Unset a dynamic search parameter (unset <TARGET>)

Undocumented commands:
======================
exit  q  quit  stop
```

## BloodHound CE Integration

![custom searches](images/custom%20searches.png)

### scripts/bloodhound-ce/query-importer.py

The [query-importer.py](scripts/bloodhound-ce/query-importer.py) script will automate importing queries into the BloodHound CE UI from a JSON file. [bh_query_converter.py](scripts/bloodhound-ce/bh_query_converter.py) has also been provided to convert a YAML file intended for the terminal application to the JSON format expected by [query-importer.py](scripts/bloodhound-ce/query-importer.py) & BloodHound CE.

### scripts/bloodhound-ce/bh_query_converter.py

This script will convert a YAML intended for the terminal application into a JSON file for easy importing into BloodHound CE via the [query-importer.py](scripts/bloodhound-ce/query-importer.py) script. [ad-queries.json](ad-queries.json) has been provided as an example for what an output file looks like and is ready to go for [query-importer.py](scripts/bloodhound-ce/query-importer.py) and importing the queries into BloodHound CE.

### scripts/bloodhound-ce/legacy-query-importer.py

This script will read a `customqueries.json` file from BloodHound Legacy and import all of them into the new version of BloodHound Community Edition with your API credentials. It is provided so that queries you have created for BloodHound Legacy can still be used with Community Edition.

### scripts/bloodhound-ce/purge-queries.py

This script will delete all saved queries from BloodHound in order to reset for future imports. It is for BloodHound CE.

### scripts/bloodhound-ce/add-owned.py

This script will read a list of node names from a `.txt` file and mark them as either owned or high-value in the database.

**Usage**

To use the script, you should have two files ready:

- A line by line `.txt` file containing node names in the `BloodHound` format
  - For users: `USER@DOMAIN.LOCAL`
  - For groups: `GROUP@DOMAIN.LOCAL`
  - For computers: `COMPUTER.DOMAIN.LOCAL`
- Your configuration file in `json` format containing your `Neo4j` username, password, and database (example shown above)

The script has the following options:

```
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file
  -l LIST, --list LIST  List of node names
  -o, --owned           Set target nodes as owned
  -v, --high-value      Set target nodes as high-value
```

You need to specify at least `-o` or `-v`

## BloodHound Query Library Integration

### scripts/bhql/query-importer.py (BloodHound Query Library Importer)

This script imports the **SpecterOps BloodHoundQueryLibrary** saved queries into **BloodHound Community Edition** using the BloodHound CE API.

* Supports loading queries from:
  * A local `Queries.json` / `Queries.zip`
  * A URL to `Queries.json` / `Queries.zip`
  * The official **latest release** artifacts published by SpecterOps
* Optionally filters queries by `platforms` (case-insensitive)
* Submits each query to BloodHound CE as a saved query (`/api/v2/saved-queries`)
* Includes retry logic for API rate limiting (HTTP `429`) using `Retry-After` when present

> SpecterOps publishes `Queries.json` and `Queries.zip` as release artifacts (not stored in the repo). The latest release download URLs are:
>
> - `https://github.com/SpecterOps/BloodHoundQueryLibrary/releases/latest/download/Queries.json`
> - `https://github.com/SpecterOps/BloodHoundQueryLibrary/releases/latest/download/Queries.zip`

**Usage (local file)**

```bash
python3 scripts/bhql/query-importer.py \
  --token-id "<TOKEN_ID>" \
  --token-key "<TOKEN_KEY>" \
  --queries-file "/path/to/Queries.json" \
  --base-url "http://127.0.0.1:8080"
````

**Usage (direct URL)**

```bash
python3 scripts/bhql/query-importer.py \
  --token-id "<TOKEN_ID>" \
  --token-key "<TOKEN_KEY>" \
  --queries-url "https://github.com/SpecterOps/BloodHoundQueryLibrary/releases/latest/download/Queries.json" \
  --base-url "http://127.0.0.1:8080"
```

**Usage (auto: latest release)**

```bash
python3 scripts/bhql/query-importer.py \
  --token-id "<TOKEN_ID>" \
  --token-key "<TOKEN_KEY>" \
  --bhql-latest \
  --base-url "http://127.0.0.1:8080"
```

**Platform-filtered import (examples)**

```bash
# Only import queries that support Active Directory
python3 scripts/bhql/query-importer.py \
  --token-id "<TOKEN_ID>" \
  --token-key "<TOKEN_KEY>" \
  --bhql-latest \
  --platforms "Active Directory" \
  --base-url "http://127.0.0.1:8080"

# Import queries for multiple platforms (any match)
python3 scripts/bhql/query-importer.py \
  --token-id "<TOKEN_ID>" \
  --token-key "<TOKEN_KEY>" \
  --bhql-latest \
  --platforms "Active Directory" "Azure" \
  --base-url "http://127.0.0.1:8080"
```

> Tip: You can create a token in BloodHound CE and use its Token ID/Key here. If you want to “start fresh” before importing, use the included purge script (see `scripts/bloodhound-ce/purge-queries.py`).

## Helper Scripts

### scripts/helpers/format_yaml_queries.py

Re-format an *existing* BloodHound queries YAML so that:

- dotted RETURN columns are aliased (foo.bar → foo_bar, labels(x) → labels_x[0])
- message templates are rewritten to use the aliases
- Cypher is pretty-printed (one major clause per line)
- long strings are literal block scalars (|) and wrapped to 100 chars

## DPAT Integration

If you do not see the cypherhound functionality merged into the original [DPAT](https://github.com/clr2of8/DPAT) repository, please access my [DPAT fork](https://github.com/fin3ss3g0d/DPAT) which will have it.

### scripts/DPAT/parse-memberships.py

This script will parse a raw export from the terminal application, specifically the cypher to list all user group memberships as an example for how this tool's output can be parsed. You will pass this export as a parameter to the script, a `NTDS.dit` file, and an output directory. It will then produce `.txt` files in the output directory for every group name with entries in `DOMAIN\USER` format, compatible with DPAT. You will then pass this directory with the the `-g` commandline argument to DPAT, allowing the operator to produce group-specific statistics for every group in a domain.

To use the script, you should have two files ready:

1. The raw export from the terminal application that retrieves all user group memberships
2. A `NTDS.dit` file with lines in the following format: `domain\user:RID:LMhash:NTLMhash:::`

**Usage**

```
usage: parse-memberships.py [-m MEMBERSHIPS_FILE] [-d DOMAIN] [-n NTDS_FILE] [-o OUTPUT_DIR] [--netbios NETBIOS] [--encoding ENCODING]
                            [--debug] [--no-index] [-h]

Map users to groups from memberships file and match against NTDS dump.

options:
  -m, --memberships-file MEMBERSHIPS_FILE
                        Path to memberships file (BloodHound-style lines) (default: None)
  -d, --domain DOMAIN   FQDN domain (e.g., EXAMPLE.COM) used in the membership regex (default: None)
  -n, --ntds-file NTDS_FILE
                        Path to NTDS dump (DOMAIN\user:hash or pwdump-style) (default: None)
  -o, --output-dir OUTPUT_DIR
                        Directory to write per-group output files (default: None)
  --netbios NETBIOS     NETBIOS/short domain to prefix when NTDS lines lack a domain (pwdump) (default: None)
  --encoding ENCODING   Encoding for input files (default: cp1252)
  --debug               Enable verbose debug output (default: False)
  --no-index            Name group files after the group instead of numbered files (unsafe chars replaced) (default: False)
  -h, --help            Show this help message and exit
```

### scripts/DPAT/parse-kerberoastable.py

This script will parse the raw export for listing all kerberoastable users, match the users up with entries in a `NTDS.dit`, and produce an output file containing all of the kerberoastable user hash entries from the dump. You then pass this output file to DPAT with the flag `-kz` for providing cracked kerberoastable account statistics.

**Usage**

```
usage: parse-kerberoastable.py [-k KERB_FILE] [-n NTDS_FILE] [-d DOMAIN] [-o OUTPUT] [--encoding ENCODING] [--debug] [-h]

Match kerberoastable usernames against an NTDS.dit dump file

options:
  -k, --kerb-file KERB_FILE
                        Path to Kerberoast output file (default: None)
  -n, --ntds-file NTDS_FILE
                        Path to NTDS dump file (default: None)
  -d, --domain DOMAIN   Domain (e.g., EXAMPLE.COM) for regex matching (default: None)
  -o, --output OUTPUT   Path to write matches (default: None)
  --encoding ENCODING   File encoding to use when reading input files (default: cp1252)
  --debug               Enable verbose debug output (default: False)
  -h, --help            Show this help message and exit
```

## Important Notes

- The program is configured to use the default `Neo4j` database and `URI`
- Built for versions at or above `BloodHound 4.3.1`, certain edges will not work for previous versions

## A Word About Sponsorship

On `July 15, 2023` I decided to make some changes to the project. After this date, this project will always be kept one version behind the private version for sponsors. Be sure to sponsor me for access to the latest cyphers, features, and bug fixes. By sponsoring me in this tier, you will also get access to additional private repositories I've not released to the public!

## Future Goals

- Add cyphers for `Azure` edges
- Continue to add cyphers when BloodHound releases updates
- Continue to add cyphers

## Issues and Support

Please be descriptive with any issues you decide to open and if possible provide output (if applicable).
