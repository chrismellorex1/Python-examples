import string
import time
import re
import os
import types
import copy
import AbsTime
import TimeRange

import TextRules

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class FWF_MFL_Overrides:
    def __init__(self):
        pass

# End MAKE NO CHANGES HERE
#**********************************************************************
    # Make sure to indent methods inside the class statement.
    #----- WFO MFL FWF Overrides -----

    # It is helpful to put a debug statement at the beginning of each
    # method to help with trouble-shooting.
    #def _method(self):
        #self.debug_print("Debug: _method in FWF_SR_Overrides")

    # Example of Overriding a dictionary from TextRules
    #def phrase_descriptor_dict(self, tree, node):
        #dict = TextRules.TextRules.phrase_descriptor_dict(self, tree, node)
        #dict["PoP"] = "chance of"
        #return dict

    def _postProcessProduct(self, fcst, argDict):
        #Include any local string replacements here (CP 08/05/03)
        #fcst = string.upper(fcst)
        fcst = fcst.lower()
        fcst = re.sub(r'THUNDERSTORMS AND RAIN SHOWERS', r'SHOWERS AND THUNDERSTORMS', fcst)
        fcst = re.sub(r'THUNDERSTORMS AND SHOWERS', r'SHOWERS AND THUNDERSTORMS', fcst)
        fcst = re.sub(r'THUNDERSTORMS AND RAIN', r'RAIN AND THUNDERSTORMS', fcst)
        fcst = re.sub(r'RAIN SHOWERS AND THUNDERSTORMS', r'SHOWERS AND THUNDERSTORMS', fcst)
        fcst = re.sub(r'RAIN SHOWERS', r'SHOWERS', fcst)
        fcst = re.sub(r'RAIN\nSHOWERS', r'SHOWERS', fcst)

        #fcst = string.upper(fcst)
        fcst = fcst.lower()

        return fcst
