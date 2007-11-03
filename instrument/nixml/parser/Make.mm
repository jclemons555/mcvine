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
PACKAGE = nixml/parser

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	AbstractNode.py \
	Block.py \
	Cylinder.py \
	Copy.py \
	Detector.py \
	DetectorArray.py \
	DetectorPack.py \
	DetectorSystem.py \
	Document.py \
	Guide.py \
	HollowCylinder.py \
	Instrument.py \
	InstrumentGeometer.py \
	LocalGeometer.py \
	Moderator.py \
	Monitor.py \
	Pixel.py \
	RectTube.py \
	Register.py \
	Sample.py \
	Shape.py \
	__init__.py \

include doxygen/default.def

export:: export-package-python-modules 

# version
# $Id: Make.mm 1205 2006-11-15 16:23:10Z linjiao $

# End of file
