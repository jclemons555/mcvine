# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = instrument
PACKAGE = geometers

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES =    \
	AbstractGeometer.py \
	AbstractGlobalGeometer.py \
	AbstractInstrumentGeometer.py \
	ARCSGeometer.py \
	CoordinateSystem.py \
	FakeGeometer.py \
	Geometer.py \
	GlobalGeometer.py \
	InstrumentGeometer.py \
	LocationRegistry.py \
	PositionalInfo.py \
	__init__.py \
	_journal.py \
	angle.py \
	mcstasRotations.py \
	rotateVector.py \
	units.py \
	utils.py \


export:: export-package-python-modules

# version
# $Id$

# End of file
