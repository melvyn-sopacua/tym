#!/bin/sh
# vim: ts=4 sw=4 noet tw=78 fo=croqn nobackup
# Small setup script to initialize a virtual environment and install it's
# dependencies.
SKIP_VENV=${SKIP_VENV:-"no"}

if [ ${SKIP_VENV} != "yes" ]
then
	[ ! -d .venv ] && python3 -m venv .venv 
	. .venv/bin/activate
fi
echo "Upgrading pip (if necessary)"
pip install -U pip
echo "Installing package requirements"
pip install -r requirements.txt

deactivate
echo ""
echo "Run source .venv/bin/activate to activate the virtual environment"
echo ""
