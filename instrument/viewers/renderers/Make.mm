
PROJECT = instrument
PACKAGE = viewers/renderers


# directory structure

BUILD_DIRS = \
	vtk

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
	Renderer.py \
	__init__.py \

EXPORT_BINS = \


export:: export-package-python-modules export-binaries

# version
# $Id: Make.mm 4 2006-01-10 08:44:13Z linjiao $
