#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                   (C) Copyright 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


__doc__ = """
provides a model geometer that can be used to create tests

  - NAME: FakeGeometer
  - PURPOSE: provides a model geometer that can be used to create tests
  - DESCRIPTION: This module combined with FakeInstrument and FakeMeasurement
  provides a base for creating test for reduction procedures.
  - RELATED: instrument.factories.FakeInstrument, measurement.FakeMeasurement
  - TODOs:
"""


from instrument.geometers.AbstractInstrumentGeometer \
     import AbstractInstrumentGeometer as _Base



class Geometer(_Base):

    KEY_scatteringAngle = "scatteringAngle"
    KEY_distanceToSample = "distanceToSample"


    def __init__(self):
        self._registry = {}
        return


    def register(self, element, scatteringAngle, distanceToSample):
        self._registry[element] = {
            self.KEY_scatteringAngle: scatteringAngle,
            self.KEY_distanceToSample: distanceToSample
            }
        return


    def scatteringAngle(self, element):
        return self._registry[element][self.KEY_scatteringAngle]


    def distanceToSample(self, element):
        return self._registry[element][self.KEY_distanceToSample]


    def position(self, element): return None


    def psi(self, pixel): return 0.0


    pass # end of Geometer


# version
__id__ = "$Id$"

# End of file 
