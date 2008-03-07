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

PROJECT = mccomponents
PACKAGE = sample/phonon

BUILD_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	AbstractDOS.py \
	__init__.py \
	CoherentInelastic_PolyXtal_Kernel.py \
	DWFromDOS.py \
	LinearlyInterpolatedDispersion_3D.py \
	LinearlyInterpolatedDOS.py \
	NdArray.py \


export:: export-package-python-modules 


# version
# $Id: Make.mm 1234 2007-09-18 18:32:56Z linjiao $

# End of file
