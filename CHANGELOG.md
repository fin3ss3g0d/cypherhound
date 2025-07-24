# 07/28/2023

Added the `parse-memberships.py` script to provide group files for the tool [DPAT](https://github.com/clr2of8/DPAT), allowing operators to produce group-specific statistics for every group in a domain.

# 08/04/2023

Performed a complete re-factor of the entire code base, removing thousands of lines of unnecessary code making the project easier to maintain or expand moving forward. Along with this were some additional features, including the addition of a `json` configuration file allowing users to now specify a specific `Neo4j` database. Another feature was the addition of a search command, allowing operators to search the list of cyphers for easier navigation of the menu and execution of commands. An additional script was added to the project `add-owned.py` for marking users as owned or high-value in the database from a list file.

# 08/05/2023

Added cyphers for the Users, Domain Users, Authenticated Users, and Everyone groups as well as a cypher for users with passwords set to never expire.

# 08/06/2023

Added additional cyphers for the Users, Domain Users, Authenticated Users, and Everyone groups as well as owned principals.

# 08/07/2023

Expanded cyphers for owned principals as well as the Users, Domain Users, Authenticated Users, and Everyone groups. Added additional cyphers for domains including cross-domain paths.

# 08/08/2023

Added group-delegated CanRDP/Adminto cyphers for the Users, Domain Users, Authenticated Users, and Everyone groups as well as owned principals.

# 08/09/2023

Added cyphers for additional relationships including: `WriteSPN`, `WriteAccountRestrictions`, `HasSIDHistory`, and `DumpSMSAPassword`. Made a modification to the `add-owned.py` script to allow operators to unset node properties that have been previously modified.

# 01/30/2024

Added cyphers for cross-domain `DCSync` privileges as well as `AdminTo` privileges to domain controllers. Also fixed some bugs.

# 07/23/2025

Added `query-importer.py` for importing queries from `customqueries.json` into BloodHound CE via API which was only supported for BloodHound legacy prior.

# 07/24/2025

Added `purge-queries.py` which will delete all saved queries from BloodHound in order to reset for future imports. It is for BloodHound CE.
