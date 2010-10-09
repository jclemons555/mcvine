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


class Phonon_CoherentInelastic_SingleXtal_Kernel(AbstractNode):


    tag = "Phonon_CoherentInelastic_SingleXtal_Kernel"
    

    def elementFactory( self, **kwds ):
        from mccomponents.sample.phonon \
             import coherentinelastic_singlextal_kernel as f
        return f(None)


    def onDispersion(self, dispersion):
        self.element.dispersion = dispersion
        return


    onPeriodicDispersion = onDispersion

    pass # end of Phonon_CoherentInelastic_SingleXtal_Kernel


from HomogeneousScatterer import HomogeneousScatterer
HomogeneousScatterer.onPhonon_CoherentInelastic_SingleXtal_Kernel = HomogeneousScatterer.onKernel


# version
__id__ = "$Id$"

# End of file 