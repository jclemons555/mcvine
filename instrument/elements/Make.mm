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
PACKAGE = elements

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	AbstractAttributeContainer.py\
	Attribute.py \
	AttributeContainer.py\
	Copy.py \
	Detector.py \
	DetectorPack.py \
	DetectorArray.py \
	DetectorSystem.py \
	DetectorVisitor.py \
	Element.py  \
	ElementContainer.py \
	GuidGenerator.py \
	GuidRegistry.py \
	Guide.py \
	IdGenerator.py \
	Instrument.py	   \
	Moderator.py  \
	Monitor.py  \
	Pixel.py \
	Sample.py \
	Visitor.py \
	__init__.py \
	_journal.py \
	elementTypes.py \
	units.py \


export:: export-package-python-modules

# version
# $Id$

# End of file
