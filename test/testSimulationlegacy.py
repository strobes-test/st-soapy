import unittest

import soapy

import numpy
from astropy.io import fits

import os
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../conf/")

soapy.logger.setLoggingLevel(3)

RESULTS = {
        "8x8": 0.5,
        "8x8_open": 0.5,
        "8x8_offAxis": 0.22,
        "8x8_zernike": 0.36,
        "8x8_lgs"    : 0.4,
        "8x8_phys": 0.53,
        "8x8_lgsuplink":0.35,
        }


class TestSimpleSCAO(unittest.TestCase):

    def testOnAxis(self):
        sim = soapy.Sim(os.path.join(CONFIG_PATH, "sh_8x8.yaml"))
        sim.config.wfss[0].type = "ShackHartmannLegacy"
        sim.config.sim.simName = None
        sim.config.sim.logfile = None
        sim.config.sim.nIters = 100
        sim.config.wfss[0].GSPosition=(0,0)

        sim.aoinit()

        sim.makeIMat(forceNew=True)

        sim.aoloop()

        #Check results are ok
        assert numpy.allclose(sim.longStrehl[0,-1], RESULTS["8x8"], atol=0.2)

    def testPhysProp(self):
        sim = soapy.Sim(os.path.join(CONFIG_PATH, "sh_8x8.yaml"))
        sim.config.wfss[0].type = "ShackHartmannLegacy"

        sim.config.sim.simName = None
        sim.config.sim.logfile = None
        sim.config.sim.nIters = 100
        sim.config.wfss[0].GSPosition=(0,0)
        sim.config.wfss[0].propagationMode="Physical"

        sim.aoinit()

        sim.makeIMat(forceNew=True)

        sim.aoloop()

        #Check results are ok
        assert numpy.allclose(sim.longStrehl[0,-1], RESULTS["8x8_phys"], atol=0.2)

    def testOffAxis(self):
        sim = soapy.Sim(os.path.join(CONFIG_PATH, "sh_8x8.yaml"))
        sim.config.wfss[0].type = "ShackHartmannLegacy"

        sim.config.sim.simName = None
        sim.config.sim.logfile = None
        sim.config.sim.nIters = 100
        sim.config.wfss[0].GSPosition = (20,0)

        sim.aoinit()

        sim.makeIMat(forceNew=True)

        sim.aoloop()

        #Check results are ok
        assert numpy.allclose(
                sim.longStrehl[0,-1], RESULTS["8x8_offAxis"], atol=0.2)


    def testZernikeDM(self):
        sim = soapy.Sim(os.path.join(CONFIG_PATH, "sh_8x8.yaml"))
        sim.config.wfss[0].type = "ShackHartmannLegacy"

        sim.config.sim.simName = None
        sim.config.sim.logfile = None
        sim.config.sim.nIters = 100
        sim.config.wfss[0].GSPosition = (0,0)

        sim.config.sim.nDM = 1
        sim.config.dms[0].type = "Zernike"
        sim.config.dms[0].nxActuators = 45
        sim.config.dms[0].svdConditioning = 0.01
        sim.config.dms[0].iMatValue = 100

        sim.aoinit()

        sim.makeIMat(forceNew=True)

        sim.aoloop()

        #Check results are ok
        assert numpy.allclose(
                sim.longStrehl[0,-1], RESULTS["8x8_zernike"], atol=0.2)


    def testCone(self):

        sim = soapy.Sim(os.path.join(CONFIG_PATH, "sh_8x8_lgs.yaml"))
        sim.config.wfss[0].type = "ShackHartmannLegacy"
        sim.config.wfss[1].type = "ShackHartmannLegacy"

        sim.config.sim.simName= None
        sim.config.sim.logfile = None
        sim.config.sim.nIters = 100

        sim.aoinit()
        print("WFS TYPE: {}".format(sim.wfss[0]))
        sim.makeIMat(forceNew=True)

        sim.aoloop()

        #Check results are ok
        assert numpy.allclose(
                sim.longStrehl[0,-1], RESULTS["8x8_lgs"], atol=0.2)

    def testOpenLoop(self):
        sim = soapy.Sim(os.path.join(CONFIG_PATH, "sh_8x8_openloop.yaml"))
        sim.config.wfss[0].type = "ShackHartmannLegacy"

        sim.config.sim.simName = None
        sim.config.sim.logfile = None
        sim.config.sim.nIters = 100
        sim.config.wfss[0].GSPosition=(0,0)

        for i in range(sim.config.sim.nDM):
            sim.config.dms[i].closed = False

        sim.aoinit()

        sim.makeIMat(forceNew=True)

        sim.aoloop()

        #Check results are ok
        assert numpy.allclose(sim.longStrehl[0,-1], RESULTS["8x8_open"], atol=0.2)

    def testLgsUplink_phys(self):
        sim = soapy.Sim(os.path.join(CONFIG_PATH, "sh_8x8_lgs-uplink.yaml"))
        sim.config.wfss[0].type = "ShackHartmannLegacy"
        sim.config.wfss[1].type = "ShackHartmannLegacy"

        sim.config.sim.simName = None
        sim.config.sim.logfile = None
        sim.config.sim.nIters = 100
        sim.config.wfss[0].GSPosition = (0, 0)
        sim.config.wfss[1].GSPosition = (0, 0)
        sim.config.wfss[1].lgs.propagationMode = "Physical"
        sim.aoinit()

        sim.makeIMat(forceNew=True)

        sim.aoloop()

        #Check results are ok
        assert numpy.allclose(sim.longStrehl[0,-1], RESULTS["8x8_lgsuplink"], atol=0.2)

    def testLgsUplink_geo(self):
        sim = soapy.Sim(os.path.join(CONFIG_PATH, "sh_8x8_lgs-uplink.yaml"))
        sim.config.wfss[0].type = "ShackHartmannLegacy"
        sim.config.wfss[1].type = "ShackHartmannLegacy"

        sim.config.sim.simName = None
        sim.config.sim.logfile = None
        sim.config.sim.nIters = 100
        sim.config.wfss[0].GSPosition = (0, 0)
        sim.config.wfss[1].GSPosition = (0, 0)
        sim.config.wfss[1].lgs.propagationMode = "Geometric"
        sim.aoinit()

        sim.makeIMat(forceNew=True)

        sim.aoloop()

        #Check results are ok
        assert numpy.allclose(sim.longStrehl[0,-1], RESULTS["8x8_lgsuplink"], atol=0.2)

if __name__ == '__main__':
    unittest.main()
