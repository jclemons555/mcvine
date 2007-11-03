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


# this Make.mm requires non-standard config package that includes 
#  config/make/std-docs.def

PROJECT = instrument
#PACKAGE = instrument


# directory structure

BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)


PROJ_CLEAN =

#--------------------------------------------------------------------------
#

all: 
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

docs:: package-documentation-html-index
	BLD_ACTION="docs" $(MM) recurse


include std-docs.def


# version
# $Id: Make.mm 1213 2006-11-18 16:17:08Z linjiao $

# End of file
