# JaiTools

Syntax highlighting, autocompletion, and Goto Symbol/Anything/Definition for the Jai language in Sublime Text 3. Thank you to GreenLightning for their contributions.

As you probably know, this language is not officially released yet, but the demonstrations of the language by Jonathan Blow and Abner Coimbre have been very promising, so the purpose of this package is to help people hit the ground running when the language is released.

All present and future features of JaiTools will always be exceedingly simple to use. This package strives to never interrupt your flow or waste your battery. Of course, JaiTools will be continually updated as the language evolves.

## Usage

### Autocomplete

JaiTools indexes your open files for completions. For the best experience, make sure you set your other autocompletion packages to ignore .jai files, otherwise you might receive duplicate/unhelpful completion suggestions. Other than that, no setup is required.

Begin typing a procedure call to view the matching symbols in your project. Type more to narrow down the list, or use the arrow keys to pick the right procedure. Hit Tab to complete it and jump to its parameter, hit Tab again to jump to the second parameter, etc.

In the future, your entire project including Jai's standard library will be indexed for completions. Efficiency improvements have to be made first.

### Goto

Goto Symbol (ctrl+R/cmd+R) shows all the top-level symbols in the file including procedure parameters, so you can easily tell the difference between multiple overloaded procedures. Nested procedures (procedures defined locally inside other procedures) are also shown with indentation to indicate the scope heirarchy. Goto Symbol in Project (shift+ctrl+R/shift+cmd+R) shows all top-level symbols in your project, but doesn't show procedure parameters (yet).

## Planned Work

- Investigation as to whether the compiler can be leveraged for completions. This will hopefully guarantee completion robustness and boost CPU efficiency. This should enable gathering completions from all files, not just the ones you have open.
- Consolidated syntax tests which can be executed by both Jai and Sublime Text. This is particularly important because the language's syntax isn't set in stone yet.
- Add Jai's standard library code to the autocompletion system.
- Hover over a struct to see its members.
- A "quick build" feature, for executing the compiler on the current Jai file.
- Syntax highlighting for Jai's build output.
- Features for enabling the user to add their custom building requirements to their project in a hassle-free way, including showing errors and warnings in-line with code.

Suggestions, issues, pull requests and other contributions are very welcome!


