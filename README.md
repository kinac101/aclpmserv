aclpmserv
=========

[![Join the chat at https://gitter.im/kinac101/aclpmserv](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/kinac101/aclpmserv?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
Brought to you by the AssaultCube KiN clan

License: GPL2

**aclpmserv** (*AssaultCube log parser for multiple servers*) is an extension of
[DenBeke's AC log parser tool](https://github.com/DenBeke/AC-Log-Parser) for
managing the (i.) parsing of `*.log` files; and (ii.) the merging of multiple
parsed `*.log` files (in `*.json` format) upon receiving them  from different
servers. The tool runs on Python 2.7.

To install dependencies

    sudo pip install -U jsonpickle

To parse `*.log` file

    python parser.py < server_1.log > server_1.json

To combine multiple *.json files

    python parser.py combine > sample-combine.json

**Authors**

* Mathias Beke ([denbeke.be](https://denbeke.be)) made the initial version of
the log parser. Kindly refer to
[his project](https://github.com/DenBeke/AC-Log-Parser) for more information
* Kinac101 ([kinac.ml](http://www.kinac.ml)) added the parsing of lastseen
timestamp and the merging of multiple *.json files

Want to know more about KiN? See [kinac.ml](http://www.kinac.ml) for more
information.
