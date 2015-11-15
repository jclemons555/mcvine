# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = instrument
PACKAGE = applications/InstrumentEditor

PROJ_TIDY += *.log
PROJ_CLEAN =

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
#

EXPORT_PYTHON_MODULES = \
	AddItemDialog.py \
	ChildrenTable.py \
	LowerPanel.py \
	MainFrame.py \
	MainPanel.py \
	MainWinApp.py \
	ShapeTreePanel.py \
	ShapeTree2GuiTree.py \
	TreeNotebook.py \
	TreePanel.py \
	UpperPanel.py \
	ViewNotebook.py \
	VtkPanel.py \
	__init__.py \



EXPORT_BINS = \
	InstrumentEditor.py \



export:: export-binaries release-binaries export-package-python-modules 



# version
# $Id: Make.mm 925 2006-05-22 06:45:13Z jiao $

# End of file
