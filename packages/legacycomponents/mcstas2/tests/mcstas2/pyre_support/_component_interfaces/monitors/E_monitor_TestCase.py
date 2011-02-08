#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


skip = False
standalone = True


import unittestX as unittest
import journal


from mcni.pyre_support.MpiApplication import usempi
outputdir = 'out-E_monitor_TestCase'


class TestCase(unittest.TestCase):

    def test1(self):
        # remove the output directory
        if os.path.exists(outputdir):
            shutil.rmtree(outputdir)
        
        # build the command to ru
        cmd = ['python E_monitor_TestCase_app.py']
        if usempi:
            cmd.append('--mpirun.nodes=2')
        cmd = ' '.join(cmd)

        # run command
        if os.system(cmd):
            raise RuntimeError, "%s failed" % cmd

        # checks
        import time
        ctime = time.time()

        #check output directory exists
        self.assert_( os.path.exists( outputdir ) )
        
        # make sure that the final histogram is identical to the 
        # sum of all the final histograms in different nodes
        # NOT IMPLEMENTED YET
        return
    
    pass  # end of TestCase


import os, shutil


def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )


def main():
    #debug.activate()
    #journal.debug("CompositeNeutronScatterer_Impl").activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id$"

# End of file 
