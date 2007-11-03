
PROJECT = instrument
PACKAGE = viewers/renderers/vtk


# directory structure

BUILD_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS)

#--------------------------------------------------------------------------
#
all: export
	BLD_ACTION="all" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

export::
	BLD_ACTION="export" $(MM) recurse

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	__init__.py \
	Base.py \
	McStasConvention.py \
	mcstasRotation.py \
	RedConvention.py \
	SimuRedConvention.py \


EXPORT_BINS = \


export:: export-package-python-modules export-binaries

# version
# $Id: Make.mm 9 2006-04-18 08:05:40Z jiao $
