import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis



# Define Regional overrides of Product Definition settings and
# default values of additional Regional Definition settings
#  ( This Definition section must be before the Class definition)

#***** THIS NEXT LINE IS REQUIRED *****
Definition = {}

#####################################################
# Override VariableList if desired
#
#VariableList = []
#
# NC Definitions:
# Definition statements must start in column 1

### Regional settings of baseline options: ###

#Definition["displayName"] = "FWS_NC"

### New Regional Definitions not in the baseline ###

# END NC definitions
############################################################

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the above Definition = {} line
# plus following class definition and the __init__ method with only
# the "pass" line in it.

class FWS_NC_Overrides:
    """Class NNN_FILETYPE - Version: IFPS"""

    def __init__(self):
        pass

# End MAKE NO CHANGES HERE
#**********************************************************************
    # Add methods here making sure to indent inside the class statement
    # NC FWS Overrides ------------------------

    # It is helpful to put a debug statement at the beginning of each
    # method to help with trouble-shooting.
    #def _method(self):
        #self.debug_print("Debug: _method in FWS_NC_Overrides")
