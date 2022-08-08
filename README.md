# apt-world

Python program that parses /var/lib/dpkg/status (and/or any other needed files) and displays a list of packages explicitly installed by the user (the equivalent of Gentoo selected set).

Takes an optional command line argument:

--default or no argument: uses aptitude to identify installed packages

--aptmark: uses apt-mark to identify installed packages

Targets Ubuntu 18.04 and uses the manifest file for Ubuntu 18.04 to identify packages installed as part of the initial install of the operating system.

User intalled packages are determined by removing packages listed in the manifest file from the list of installed packages.
