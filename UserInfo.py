# ----------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
# UserInfo.py
#
# getForecasterName
#  Return the forecaster name that should be added to the end of the product
#
# Author: fachorn
#
# History:
# F.Achorn/OPC    03/08/13    initial creation
# F.Achorn/OPC    09/24/13    modify to get the debug level correctly from argDict
# ----------------------------------------------------------------------------

import TextRules
import SampleAnalysis
import time
import string

import os

class UserInfo(TextRules.TextRules, SampleAnalysis.SampleAnalysis):
    def __init__(self):
        TextRules.TextRules.__init__(self)
        SampleAnalysis.SampleAnalysis.__init__(self)

#    # Include your utility methods here
#    def p_myMethod(self):
#        return 10

    def forecasterDict(self):
        self.debug_print("Debug: forecasterDict in UserInfo")
        return {
            "chris.landsea": "Landsea",
            "andrew.levine": "AL",
            "scott.stripling": "Stripling",
            "eric.christensen": "Christensen",
            "jeffrey.lewitsky": "Lewitsky",
            "jorge.aguirre-echevarria": "Aguirre",
            "gladys.rubio": "GR",
            #"dmundell": "Mundell",
            #"cmcelroy": "CAM",
            "nelsie.ramos": "Ramos",
            #"brad.reinhart": "Reinhart",
            "evelyn.rivera": "ERA",
            "mformosa": "Formosa",
            "michael.tichacek": "MT",
            "maria.torres": "Torres",
            "amanda.reinhart": "AKR",
            "andrew.latto": "Latto",
            "sstewart": "Stewart",
            "pmanougi": "Manougian",
            "stephen.konarik": "KONARIK",
            "andrew.hagen": "Hagen",
            }

    def _getForecasterName(self, argDict):
        # get the debug level from the argDict, if available
        try:
            self._debug = argDict["debug"]
        except:
            self._debug = 1
        self.debug_print("Debug: _getForecasterName in UserInfo")
        userName = os.environ["USER"]
        if userName in self.forecasterDict():
            forecaster = self.forecasterDict()[userName]
        else:
            forecaster = "NATIONAL HURRICANE CENTER"
        self.debug_print("Forecaster = " + forecaster)
        return forecaster
