# JaiTools

Syntax highlighting, project-wide autocompletion, and Goto Symbol/Anything/Definition for the Jai language in Sublime Text 3. Thank you to GreenLightning for their contributions.

As you probably know, this language is not officially released yet, but the demonstrations of the language by Jonathan Blow and Abner Coimbre have been very promising, so the purpose of this package is to help people hit the ground running when the language is released.

All present and future features of JaiTools will always be exceedingly simple to use. This package strives to never interrupt your flow or waste your battery. Of course, JaiTools will be continually updated as the language evolves. Please be aware that some language features are not supported yet, as implementing and testing them properly requires access to the Jai compiler.

## Usage

For the best experience, make sure you set your other autocompletion packages to ignore .jai files, otherwise you might receive duplicate/unhelpful completion suggestions. Other than that, you're good to go!

Begin typing a procedure call to view the matching symbols in your project. Type more to narrow down the list, or use the arrow keys to pick the right procedure. Hit Tab to complete it and jump to its parameter, hit Tab again to jump to the second parameter, etc.

Goto Symbol (ctrl+R/cmd+R) shows all the top-level symbols in the file including procedure parameters, so you can easily tell the difference between multiple overloaded procedures. Nested procedures (procedures defined locally inside other procedures) are also shown with indentation to indicate the scope heirarchy. Goto Symbol in Project (shift+ctrl+R/shift+cmd+R) shows all top-level symbols in your project, but doesn't show procedure parameters (yet).

## Planned Work

- [x] More efficient completion indexing
- [x] Regex performance improvements
- [ ] Show procedure parameters in "Goto Symbol in Project" (shift+ctrl+R/shift+cmd+R)
- [ ] Gather completions for enum members correctly
- [ ] Improved handling of #hashtags and other metaprogramming labels
- [ ] Add support for structs with parameters
- [ ] Gather completions from Jai scratch buffers (files without a location on disk)
- [ ] Integrate with Sublime Text's build system in order to support in-code errors and warnings
- [ ] Better support for Jai's polymorphism features
- [ ] Smart struct-member and enum-member inspection

Suggestions, issues, pull requests and other contributions are very welcome!


