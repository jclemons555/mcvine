#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin   
#                      California Institute of Technology
#                      (C)   2007    All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from AbstractNode import AbstractNode, debug


class Phonon_CoherentInelastic_PolyXtal_Kernel(AbstractNode):


    tag = "Phonon_CoherentInelastic_PolyXtal_Kernel"
    

    def elementFactory( self, **kwds ):
        Ei = self._parse( kwds['Ei'] )
        max_omega = self._parse( kwds['max-omega'] )
        max_Q = self._parse( kwds['max-Q'] )
        nMCsteps_to_calc_RARV = int( kwds['nMCsteps_to_calc_RARV'] )
        
        from mccomponents.sample.phonon \
             import coherentinelastic_polyxtal_kernel as f
        return f(
            None,
            Ei, max_omega, max_Q, nMCsteps_to_calc_RARV)


    def onDispersion(self, dispersion):
        self.element.dispersion = dispersion
        return


    onPeriodicDispersion = onDispersion

    pass # end of Phonon_CoherentInelastic_PolyXtal_Kernel


from HomogeneousScatterer import HomogeneousScatterer
HomogeneousScatterer.onPhonon_CoherentInelastic_PolyXtal_Kernel = HomogeneousScatterer.onKernel


# version
__id__ = "$Id$"

# End of file 