Installed Packages Manager
==========================

`ipm` is intended to manage which packages you have installed on which computers. You have a unified interface to:

* List all installed packages on your computer
* Inspect and diff stored configurations between computers
* Install packages you have on other computers but are missing on your current computer

Supported package managers:

* brew
* cask
* pip
* pip3
* gem
* git (repositories)
* app (Applications)

Computer configuration are stored in text-files (ini-style) a configurable folder, so they can be synced with Dropbox, git or another way.


pm-diff
-------

`pm-diff` is the previous ad-hoc implementation of this idea.


Data structures
---------------

The data-files should be human readable and edittable, so I don't spend to much time implementing features which are more easily been done inside a text editor.

The base config is stored in the well-known location `~/.ipmconfig`:

	[ipm]
	data_dir=~/Dropbox/ipm
	
	[brew]
	[cask]
	[pip]
	[pip3]
	[gem]

	[git]
	location=~/prj/BitBucket
	location=~/prj/GitHub

	[app]
	location=/Applications
	location=/Applications/Utilities
	location=~/Applications

The file for installed brew packages on computer `iMac` is `~/Dropbox/ipm/iMac/brew.txt` (this file is only updated by the iMac):

	[brew]
	archey	1.6.0	new
	cowsay	3.04	hide
	fortune	9708	new

Package identifier, version and label are stored. When storing the current configuration of a computer, the label *new* is added. The label *hide* can be used to not see the package again but leave it installed (dependencies or other reasons). Other labels can be used to group applications.

The `git`-file could look like this `~/Dropbox/ipm/iMac/git.txt`:

	[git ~/prj/BitBucket]
	[git ~/prj/GitHub]
	https://github.com/doekman/ipm.git	ipm	new
	git@github.com:doekman/til.git	til	new


Commands
--------

* ipm list <package-manager> [--label <label>]
* ipm store <package-manager>
* ipm diff <package-manager>
* ipm computers
* ipm install <package-manager>

The plan is to create a plug-in mechanism for package manager support; a package-provider.

Not all package-providers have to implement all commands. For example, the `app`-provider can list packages, but not install them (you can do that with App Store, cask, or manual installation).


