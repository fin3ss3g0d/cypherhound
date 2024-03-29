# 07/02/2023

Added cyphers for the `SyncLAPSPassword` edge, domain trusts, as well as a bug fix. If user input for setting a group, user, or computer contained parentheses or other special characters it would break cyphers. Additional filtering has been added for these inputs. Some of the command list ordering was also changed to be more user-friendly.

# 07/15/2023

Made the announcement of my transition into `GitHub Sponsors` and additional announcements for the future of this project. Changes include keeping this public version of the project one version behind the private version for sponsors.

# 07/23/2023

Added `customqueries.json` so all cyphers are now available to run in the GUI! Also made some minor adjustments to some cyphers.

# 08/04/2023

Performed a complete re-factor of the entire code base, removing thousands of lines of unnecessary code making the project easier to maintain or expand moving forward. Along with this were some additional features, including the addition of a `json` configuration file allowing users to now specify a specific `Neo4j` database. Another feature was the addition of a search command, allowing operators to search the list of cyphers for easier navigation of the menu and execution of commands. Two additional scripts were also added to the project: `add-owned.py` and `parse-memberships.py` which are covered in the `README.md`.

# 08/05/2023

Added cyphers for the Users, Domain Users, Authenticated Users, and Everyone groups as well as a cypher for users with passwords set to never expire.

# 08/06/2023

Added additional cyphers for the Users, Domain Users, Authenticated Users, and Everyone groups as well as owned principals.

# 08/07/2023

Expanded cyphers for owned principals as well as the Users, Domain Users, Authenticated Users, and Everyone groups. Added additional cyphers for domains including cross-domain paths.

# 08/09/2023

Added group-delegated CanRDP/Adminto cyphers for the Users, Domain Users, Authenticated Users, and Everyone groups as well as owned principals. Added cyphers for additional relationships including: `WriteSPN`, `WriteAccountRestrictions`, `HasSIDHistory`, and `DumpSMSAPassword`. Made a modification to the `add-owned.py` script to allow operators to unset node properties that have been previously modified.