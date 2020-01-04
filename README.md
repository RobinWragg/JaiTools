# JaiTools

Syntax highlighting, autocompletion, and Goto Symbol/Anything/Definition for the Jai language in Sublime Text 3.

Planned work:
* Syntax for here-strings
* Improved handling of #hashtags and other metaprogramming labels

Issues, pull requests and other contributions are very welcome!

As you probably know, this language is not officially released yet, but the demonstrations that Jonathan Blow and Abner Coimbre have shown have been very promising, so the purpose of this package is to help people hit the ground running when the language is released.

Current features are fully-functioning assuming the language's syntax doesn't change, and I plan to implement integration with Sublime Text's build system in order to support in-code errors and warnings. Some preliminary development as been done on this already.

Autocompletion scans the current file you are working on, but this will be expanded to all your open files and folders, as well as any standard Jai modules.

