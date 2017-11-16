#!/usr/bin/env bash

DATA_DIR=~/bin/data/
BREW_LIST=${DATA_DIR}brew-list.txt
CASK_LIST=${DATA_DIR}cask-list.txt
PIP3_LIST=${DATA_DIR}pip3-list.txt
GEM_LIST=${DATA_DIR}gem-list.txt
APP_LIST=${DATA_DIR}app-list.txt

function app_list {
	BASE_DIR=$1
	ls -d $BASE_DIR/*.app | sed '/^.*\//s///'
}

function git_list {
	TAB="	"
	GROUP=$1
	pushd .
	cd $GROUP
	#For-list of all folders
	#  if [[ -d $SUB_FOLDER/.git ]]
	#    cd $SUB_FOLDER
	R_ORIGIN=$(git config --get remote.origin.url)
	#  echo "$GROUP$TAB$SUB_FOLDER$TAB$R_ORIGIN"
}

NAME=${0##*/}
NAME=${NAME%.*}
echo "${NAME}: diff installed packages for brew, cask, pip3, gem and app"
echo ""

if [[ "$2" == "store" ]] ; then
	case $1 in
		brew) echo "Updating '${BREW_LIST}'"; brew list > ${BREW_LIST};;
		cask) echo "Updating '${CASK_LIST}'"; brew cask list > ${CASK_LIST};;
		pip3) echo "Updating '${PIP3_LIST}'"; pip3 list --format=columns > ${PIP3_LIST};;
		gem) echo "Updating '${GEM_LIST}'"; gem list --local > ${GEM_LIST};;
		app) echo "Updating '${APP_LIST}'"; app_list /Applications > ${APP_LIST};;
		*) echo "⚠️ Please specify option for store ($1 found): brew, cask, pip3, gem or app"; exit 1;;
	esac
	echo "Done updating"
	exit 0
fi

function list_header {
	echo "Local setup ($1)                                              Stored setup ('pm-diff $1 store' to update)"
	echo "-------------------------------------------------------------------------------------------------------------"
}

case $1 in
	brew) list_header "$1"; brew list | diff --side-by-side --suppress-common-lines - ${BREW_LIST};;
	cask) list_header "$1"; brew cask list | diff --side-by-side --suppress-common-lines - ${CASK_LIST};;
	pip3) list_header "$1"; pip3 list --format=columns | diff --side-by-side --suppress-common-lines - ${PIP3_LIST};;
	gem) list_header "$1"; gem list --local | diff --side-by-side --suppress-common-lines - ${GEM_LIST};;
	app) list_header "$1"; app_list /Applications | diff --side-by-side --suppress-common-lines - ${APP_LIST};;
	*) echo "⚠️ Unknown parameter ($1 unrecognized as package manager)"
esac
