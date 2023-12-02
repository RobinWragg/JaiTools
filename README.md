# JaiTools

Syntax highlighting, autocompletion, and Goto Symbol/Anything/Definition for the Jai language in Sublime Text. Thank you to GreenLightning for their contributions.

## Usage

### Autocomplete

JaiTools indexes your open files for completions. For the best experience, make sure you set your other autocompletion packages to ignore .jai files, otherwise you might receive duplicate/unhelpful completion suggestions. Other than that, no setup is required.

Begin typing a procedure call to view the matching symbols in your project. Type more to narrow down the list, or use the arrow keys to pick the right procedure. Hit Tab to complete it and jump to its parameter, hit Tab again to jump to the second parameter, etc.

### Goto

Goto Symbol (ctrl+R/cmd+R) shows all the top-level symbols in the file including procedure parameters, so you can easily tell the difference between multiple overloaded procedures. Goto Symbol in Project (shift+ctrl+R/shift+cmd+R) shows all top-level symbols in your project, but doesn't show procedure parameters (yet).


