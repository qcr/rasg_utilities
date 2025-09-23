# Research Engineering Facility: Robotics and Autonomous Systems Group Utilities

This repository is a collection of utilities which are useful for automating tedious tasks.

The utilities have been categorised according broadly according to their functional area to make searching for tools of interest a little easier.

## Contributing

The initial contribution is entirely made up of shell scripts for bash. However contributions in other lanuages are also acceptable provided they are properly packaged for their respective languages, where they are not simply single script files with main functions invokable from the command line.

As an example, if you wish to add a Python script with a main, simply add it to the existing folder structure along-side the other scripts.

If you wish to add a Python script along with its dependencies, ensure the project has been packaged correctly such that it can be installed with `pip`. Then add the complete package into the appropriate category.

### Contribution Etiquette

**Do not contribute directly to main!**

Please make a branch for your contribution off the `main` branch named as in the following:

`<username>/<what_it_is_you_are_making>`

Once the contribution is ready, make a pull request into `main` so that another member of REF RAS-G can approve the changes.

**Do not upload any editor files into this repository.**

Ensure that files that you have made or have made significant changes to have a header which includes the names of all authors, the date in yyyy-MM-dd format, and the version number.

## "Installing" a Utility

This can be accomplished for a single user on a given Linux system by adding the script to that user's `~/.local/bin` path. The script can be copied there if you wish to ensure that updating the repository will not automatically update the script, or the script may be linked as in the following example.

```
$ ln -s /path/to/rasg_utilities/deployment/apply_license.py ~/.local/bin/apply-license
```
