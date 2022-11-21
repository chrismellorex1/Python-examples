# ----------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
# HighSeas_AT2_Overrides
#
# Author:
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

import SWELL_HighSeas_AT2
import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis

import ForecastNarrative
import UserInfo

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class SWELL_HighSeas_AT2_Overrides:
    def __init__(self):
       pass

# End MAKE NO CHANGES HERE
#**********************************************************************

#**********************************************************************
# REQUIRED OVERRIDES
# _Text2 is set to the basin description string
#
#     def _Text2(self):
#         return "ATLANTIC FROM 07N TO 31N W OF 35W INCLUDING CARIBBEAN SEA AND\n" + \
#                "GULF OF MEXICO\n\n"

# End REQUIRED OVERRIDES
#**********************************************************************

    def __init__(self):
       TextRules.TextRules.__init__(self)
       SampleAnalysis.SampleAnalysis.__init__(self)
