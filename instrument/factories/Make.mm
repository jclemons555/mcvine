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
PACKAGE = factories


BUILD_DIRS = \
    ARCS \

RECURSE_DIRS = $(BUILD_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	__init__.py	 \
	ARCSBootstrap.py \
	ARCSDetPackCSVParser.py\
	FakeInstrument.py	\
	Instrument_CylindricalDetectorSystem.py \
	LPSDFactory.py \
	LrmecsBootstrap.py \
	LrmecsDataFileParser.py \
	PharosBootstrap.py \
	PharosDetCSVParser.py\
	PseudoSingleton.py\
	units.py \
	_journal.py \


export:: export-package-python-modules

# version
# $Id$

# End of file
