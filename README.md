# cypherhound

A `Python3` terminal application that contains 270+ `Neo4j` cyphers for BloodHound data sets.

## Why?

`BloodHound` is a staple tool for every red teamer. However, there are some negative side effects based on its design. I will cover the biggest pain points I've experienced and what this tool aims to address:

1. My tools think in lists - until my tools parse exported `JSON` graphs, I need graph results in a line-by-line format `.txt` file
2. Copy/pasting graph results - this plays into the first but do we need to explain this one?
3. Graphs can be too large to draw - the information contained in any graph can aid our goals as the attacker and we *need* to be able to view *all* data efficiently
4. Manually running custom cyphers is time-consuming - let's automate it :)

This tool can also help blue teams to reveal detailed information about their Active Directory environments as well. Matter-of-fact, there are enough cyphers packaged within this project to allow complete visibility into an Active Directory environment. The nature of the cyphers allow the operator to enumerate the environment with scalpel precision, mapping virtually every and any attack path/privilege possible.

## Features

Take back control of your `BloodHound` data with `cypherhound`!

- 272 cyphers as of date
  - Set cyphers to search based on user input (user, group, and computer-specific)
  - User-defined regex cyphers
- User-defined exporting of all results
  - Default export will be just end object to be used as target list with tools
  - Raw export option available in `grep/cut/awk`-friendly format
- `customqueries.json` file included
  - Run the same queries from the GUI

## Installation

Make sure to have `python3` installed and run:

`python3 -m pip install -r requirements.txt`

## Usage

Start the program with: `python3 cypherhound.py -u <neo4j_username> -p <neo4j_password>`

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
        raw - write raw output or just end object (optional)
    example
        export 31 results
        export 42 results2 raw
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
q, quit, exit - used to exit the program
clear - used to clear the terminal
help, ? - used to display this help menu

```

## customqueries.json

Almost all cyphers included in the terminal application (254 to be exact) have been ported over to `json` format for direct usage in the GUI. Follow the instructions below in order to begin using them!

![customqueries.json](images/gui-cypher-list.png)

### Linux

Copy the `customqueries.json` file to `~/.config/bloodhound/`

### Windows

 Copy the `customqueries.json` file to `C:\Users\<YourUsername>\AppData\bloodhound\`

## Important Notes

- The program is configured to use the default `Neo4j` database and `URI`
- Built for `BloodHound 4.3.1`, certain edges will not work for previous versions
- `Windows` users must run `pip3 install pyreadline3`
- Shortest paths exports are all the same (`raw` or not) due to their unpredictable number of nodes

## A Word About Sponsorship

On `July 15, 2023` I decided to make some changes to the project. After this date, this project will always be kept one version behind the private version for sponsors. Be sure to sponsor me for access to the latest cyphers, features, and bug fixes. By sponsoring me in this tier, you will also get access to additional private repositories I've not released to the public!

## Future Goals

- Add cyphers for `Azure` edges
- Continue to add cyphers when BloodHound releases updates

## Issues and Support

Please be descriptive with any issues you decide to open and if possible provide output (if applicable).
