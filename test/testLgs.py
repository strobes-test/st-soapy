from soapy import confParse, LGS
import aotools
import unittest
import numpy
import os
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../conf/")

class TestLgs(unittest.TestCase):

    def testa_initLgs(self):

        config = confParse.loadSoapyConfig(os.path.join(CONFIG_PATH, "sh_8x8_lgs-uplink.yaml"))

        mask = aotools.circle(config.sim.pupilSize/2., config.sim.simSize)

        lgs = LGS.LGS(config.wfss[1], config)


    def testb_initGeoLgs(self):
        config = confParse.loadSoapyConfig(os.path.join(CONFIG_PATH, "sh_8x8_lgs-uplink.yaml"))
        config.wfss[1].lgs.propagationMode = "Geometric"

        mask = aotools.circle(config.sim.pupilSize/2., config.sim.simSize)

        lgs = LGS.LGS_Geometric(config.wfss[1], config)

    def testc_geoLgsPsf(self):
        config = confParse.loadSoapyConfig(os.path.join(CONFIG_PATH, "sh_8x8_lgs-uplink.yaml"))

        mask = aotools.circle(config.sim.pupilSize/2., config.sim.simSize)
        config.wfss[1].lgs.propagationMode = "Geometric"
        lgs = LGS.LGS_Geometric(config.wfss[1], config)
        psf = lgs.getLgsPsf(
                   numpy.zeros((config.atmos.scrnNo, config.sim.simSize, config.sim.simSize)))

    def testd_initPhysLgs(self):
        config = confParse.loadSoapyConfig(os.path.join(CONFIG_PATH, "sh_8x8_lgs-uplink.yaml"))
        config.wfss[1].lgs.propagationMode = "Physical"

        mask = aotools.circle(config.sim.pupilSize/2., config.sim.simSize)

        lgs = LGS.LGS_Physical(config.wfss[1], config)

    def teste_physLgsPsf(self):
        config = confParse.loadSoapyConfig(os.path.join(CONFIG_PATH, "sh_8x8_lgs-uplink.yaml"))

        config.wfss[1].lgs.propagationMode = "Physical"
        mask = aotools.circle(config.sim.pupilSize/2., config.sim.simSize)

        lgs = LGS.LGS_Physical(config.wfss[1], config, nOutPxls=10)
        psf = lgs.getLgsPsf(
                numpy.zeros((config.atmos.scrnNo, config.sim.simSize, config.sim.simSize)))

if __name__=="__main__":
    unittest.main()
