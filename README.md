# JaiTools

Syntax highlighting, autocompletion, and Goto Symbol/Anything/Definition for the Jai language in Sublime Text 3. Thank you to GreenLightning for their contributions.

As you probably know, this language is not officially released yet, but the demonstrations of the language by Jonathan Blow and Abner Coimbre have been very promising, so the purpose of this package is to help people hit the ground running when the language is released.

All present and future features of JaiTools will always be exceedingly simple to use. This package strives to never interrupt your flow or waste your battery. Of course, JaiTools will be continually updated as the language evolves.

If you have any problems, let me know! Please create an [issue](https://github.com/RobinWragg/JaiTools/issues/new).

## Usage

### Building Your Program

Choose *Build* from the *Tools* menu or hit ctrl+B/cmd+B to run the compiler on the current file, i.e. `jai current_file.jai`. Build errors and warnings will appear in your code, and you can jump to them by hitting F4 or choosing *Tools > Build Results > Next Result*.

### Autocomplete

JaiTools gathers completions from your open files. For the best experience, make sure you set any other autocompletion packages to ignore .jai files, otherwise you might receive duplicate/unhelpful completion suggestions. Other than that, no setup is required.

If you're autocompleting a procedure call, you can hit Tab to jump to the first parameter, hit Tab again to go to the next parameter and so on.

### Goto

You can use *Goto Reference* and *Goto Definition* from the *Goto* menu or with your keyboard shortcuts.

If you hover the mouse cursor over a procedure name, you can select from a list of all calls and definitions with that name.

*Goto Symbol* (ctrl+R/cmd+R) shows all the top-level symbols in the file including procedure parameters, so you can easily tell the difference between overloaded procedures. *Goto Symbol in Project* (shift+ctrl+R/shift+cmd+R) shows all top-level symbols in your project, but doesn't show procedure parameters due to Sublime Text 3's indexing limitations.



