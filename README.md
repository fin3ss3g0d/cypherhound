# cypherhound

A `Python3` terminal application that contains `Neo4j` cyphers for BloodHound data sets and a `customqueries.json` file containing cyphers for the legacy GUI with a script to automate importing them into BloodHound CE.

![demo](images/demo%20output.png)

## Why?

`BloodHound` is a staple tool for every red teamer. However, there are some negative side effects based on its design. I will cover the biggest pain points I've experienced and what this tool aims to address:

1. My tools think in lists - until my tools parse exported `JSON` graphs, I need graph results in a line-by-line format `.txt` file
2. Copy/pasting graph results - this plays into the first but do we need to explain this one?
3. Graphs can be too large to draw - the information contained in any graph can aid our goals as the attacker and we *need* to be able to view *all* data efficiently
4. Manually running custom cyphers is time-consuming - let's automate it :)

This tool can also help blue teams to reveal detailed information about their Active Directory environments as well. Matter-of-fact, there are enough cyphers packaged within this project to allow complete visibility into an Active Directory environment. The nature of the cyphers allow the operator to enumerate the environment with scalpel precision, mapping virtually every and any attack path/privilege possible.

## Features

Take back control of your `BloodHound` data with `cypherhound`!

- Read cypher templates from a YAML file
  - Set cyphers to search based on user input (user, group, and computer-specific)
  - User-defined regex cyphers
- User-defined exporting of all results
  - Default export will be just end object to be used as target list with tools
  - Raw export option available in `grep/cut/awk`-friendly format
- `customqueries.json` file included
  - Run the same queries from the GUI - both legacy and CE

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

**YAML Keywords**

The program supports inserting keywords into the YAML file for dynamic searching at runtime. For example, if you would like a query to behave dynamically in order to search against a specific user, group, computer, or regular expression. An example of this is shown below:

```yaml
- group: user
  desc: List all shortest paths to admin groups for this user
  cypher: |-
    MATCH p=shortestPath((m:User)-[r*1..]->(n:Group))
    WHERE n.name =~ ".*((?i)admin|adm).*" AND m.name =~ '((?i)USER_SEARCH)' AND NONE (r IN relationships(p)
    WHERE type(r)= "GetChanges") AND NONE (r in relationships(p)
    WHERE type(r)="GetChangesAll") AND NONE (r in relationships(p)
    WHERE type(r)="GetChangesInFilteredSet")
    RETURN m.name AS m_name, p
    ORDER BY m.name
  msg_template: null
```

A table breakdown of the supported keywords and their descriptions can be seen below:

| Keyword | Description |
|---------|-------------|
| `USER_SEARCH` | This will be replaced by the user string you configure with the `set` command at runtime |
| `GROUP_SEARCH` | This will be replaced by the group string you configure with the `set` command at runtime |
| `COMPUTER_SEARCH` | This will be replaced by the group string you configure with the `set` command at runtime |
| `REGEX` | This will be replaced by the regular expression string you configure with the `set` command at runtime |

## Commands

The full command menu is shown below:

```
Command Menu
set - used to set search parameters for cyphers, double/single quotes not required for any sub-commands
    sub-commands
        user - the user to use in user-specific cyphers (MUST include @domain.name)
        group - the group to use in group-specific cyphers (MUST include @domain.name)
        computer - the computer to use in computer-specific cyphers (SHOULD include .domain.name or @domain.name)
        regex - the regex to use in regex-specific cyphers
    example
        set user svc-test@domain.local
        set group domain admins@domain.local
        set computer dc01.domain.local
        set regex .*((?i)web).*
run - used to run cyphers
    parameters
        cypher number - the number of the cypher to run
    example
        run 7
export - used to export cypher results to txt files
    parameters
        cypher number - the number of the cypher to run and then export
        output filename - the number of the output file, extension not needed
    example
        export 31 results
list - used to show a list of cyphers
    parameters
        list type - the type of cyphers to list (general, user, group, computer, regex, all)
    example
        list general
        list user
        list group
        list computer
        list regex
        list all
search - used to search the list of cyphers
    parameters
        search query - the search string
    example
        search domain admin
        search shortest
q, quit, exit, stop - used to exit the program
clear, cls - used to clear the terminal
help, ? - used to display this help menu
```

## customqueries.json

Almost all cyphers included in the terminal application have been ported over to `json` format for direct usage in the legacy GUI. There is also a [query-importer.py](scripts/bloodhound-ce/query-importer.py) script included in this project that will read the `customqueries.json` file and automate importing each of the queries into BloodHound CE.

![customqueries.json](images/gui-cypher-list.png)

Follow the instructions below in order to begin using them in BloodHound Legacy!

**Linux**

Copy the `customqueries.json` file to `~/.config/bloodhound/`

**Windows**

Copy the `customqueries.json` file to `C:\Users\<YourUsername>\AppData\Roaming\bloodhound\`

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

## BloodHound CE Integration

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

### scripts/bloodhound-ce/query-importer.py

This script will read the `customqueries.json` file and import all of them into the new version of BloodHound Community Edition with your API credentials.

**Usage**

```
usage: query-importer.py [-h] --token-id TOKEN_ID --token-key TOKEN_KEY --queries-file QUERIES_FILE [--base-url BASE_URL]
query-importer.py: error: the following arguments are required: --token-id, --token-key, --queries-file
```

### scripts/bloodhound-ce/purge-queries.py

This script will delete all saved queries from BloodHound in order to reset for future imports. It is for BloodHound CE.

**Usage**

```
usage: purge-queries.py [-h] --token-id TOKEN_ID --token-key TOKEN_KEY [--base-url BASE_URL]

Purge all imported BloodHound CE saved queries.

options:
  -h, --help            show this help message and exit
  --token-id TOKEN_ID   API token ID
  --token-key TOKEN_KEY
                        API token key
  --base-url BASE_URL   BloodHound API base URL
```

## Important Notes

- The program is configured to use the default `Neo4j` database and `URI`
- Built for `BloodHound 4.3.1`, certain edges will not work for previous versions
- `Windows` users must run `pip3 install pyreadline3`

## A Word About Sponsorship

On `July 15, 2023` I decided to make some changes to the project. After this date, this project will always be kept one version behind the private version for sponsors. Be sure to sponsor me for access to the latest cyphers, features, and bug fixes. By sponsoring me in this tier, you will also get access to additional private repositories I've not released to the public!

## Future Goals

- Add cyphers for `Azure` edges
- Continue to add cyphers when BloodHound releases updates
- Continue to add cyphers

## Issues and Support

Please be descriptive with any issues you decide to open and if possible provide output (if applicable).
