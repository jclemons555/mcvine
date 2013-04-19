# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = instrument
PACKAGE = factories/SEQUOIA

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	BootstrapBase.py\
	Bootstrap_mantid_idf.py\
	__init__.py	\
	packSize.py 	\
	tubePositions.py\


export:: export-package-python-modules

# version
# $Id: Make.mm 1255 2007-09-29 02:45:09Z linjiao $

# End of file
