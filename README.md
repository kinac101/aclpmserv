aclpmserv
=========
Brought to you by the AssaultCube KiN clan

License: GPL2

**aclpmserv** (*AssaultCube log parser for multiple servers*) is an extension of
DenBeke's AC log parser tool for managing the (i.) parsing of `*.log` files; and
(ii.) the merging of multiple parsed `*.log` files (in `*.json` format) upon
receiving them  from different servers. The tool runs on Python 2.7.

To parse `*.log` file

    $  python parser.py < server_1.log

To combine multiple *.json files

    $  python parser.py combine

Output for both of these features is written to an automatically generated
`output.json` file.

Want to know more about KiN? See [kinac.ml](http://www.kinac.ml) for more
information. We are recruiting.
