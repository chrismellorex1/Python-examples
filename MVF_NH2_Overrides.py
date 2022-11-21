import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis


#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class MVF_NH2_Overrides:
    def __init__(self):
        pass

# End MAKE NO CHANGES HERE
#**********************************************************************
    # Make sure to indent methods inside the class statement.
    #----- WFO ONA MVF Overrides -----

    # It is helpful to put a debug statement at the beginning of each
    # method to help with trouble-shooting.
    #def _method(self):
        #self.debug_print("Debug: _method in MVF_NC_Overrides")

    # Example of Overriding a dictionary from TextRules
    #def phrase_descriptor_dict(self, tree, node):
        #dict = TextRules.TextRules.phrase_descriptor_dict(self, tree, node)
        #dict["PoP"] = "chance of"
        #return dict

# Taken from MVF.py
# Add "Locations" text at bottom of product
# F.Achorn 01/27/11
    def _postProcessProduct(self, fcst, argDict):
        self.debug_print("Debug: _postProcessProduct in MVF_NC_Overrides")
        fcst += "\n$$"
        fcst += "\n\n" + \
               "LOCATIONS...\n" + \
               "41010   28.9N 78.5W   E OF CAPE CANAVERAL, FL\n" + \
               "42003   26.0N 85.6W   W OF NAPLES, FL\n" + \
               "42001   25.9N 89.7W   S OF SOUTHWEST PASS, LA\n" + \
               "42002   26.1N 93.8W   E OF BROWNSVILLE, TX\n"
        self.setProgressPercentage(100)
        self.progressMessage(0, 100, self._displayName + " Complete")
        return fcst
