##
# This software was developed and / or modified by Raytheon Company,
# pursuant to Contract DG133W-05-CQ-1067 with the US Government.
#
# U.S. EXPORT CONTROLLED TECHNICAL DATA
# This software product contains export-restricted data whose
# export/transfer/disclosure is restricted by U.S. law. Dissemination
# to non-U.S. persons whether in the United States or abroad requires
# an export license or other authorization.
#
# Contractor Name:        Raytheon Company
# Contractor Address:     6825 Pine Street, Suite 340
#                         Mail Stop B8
#                         Omaha, NE 68106
#                         402.291.0100
#
# See the AWIPS II Master Rights File ("Master Rights File.pdf") for
# further licensing information.
##
# ---------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without
# technical  support, and with no warranty, express or implied, as to
# its usefulness for any purpose.
#
# MVF_ONA_001_Definition.TextUtility
#
#  This file sets up all the Product Definition overrides for the
#  MVF formatter for a site.
#
# History:
# F.Achorn/OPC  12/06/11    Migrated from AWIPS1
# ---------------------------------------------------------------------

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum content of this file is the following Definition statement

Definition = {}

# End MAKE NO CHANGES HERE
#**********************************************************************
#####################################################
# Override VariableList if desired
## Un-comment the following lines to include a Tropical Storm Winds Flag:
##VariableList = [
##         (("Forecaster Number", "forecasterNumber"), 99, "alphaNumeric"),
##         (("Tropical Storm", "tropicalStorm"), "no", "radio", ["NO", "YES"]),
##        ]

#----- WFO ONA MVF Definition -----
# Definition Statements must start in column 1.

# REQUIRED CONFIGURATION ITEMS
#Definition['displayName'] = None
Definition['displayName'] = None

Definition["defaultEditAreas"] = [
     ("K41010", "41010"),
     ("K42003", "42003"),
     ("K42001", "42001"),
     ("K42002", "42002")
     ]

# Header configuration items
#Definition["productName"] = "MARINE VERIFICATION FORECAST"  # name of product
Definition["fullStationID"] = "KNHC"  # full station identifier (4letter)
Definition["wmoID"] = "FXUS52"        # WMO ID
Definition["pil"] = "MVF007"          # product pil
Definition["zoneCode"] = "stZALL"     # Zone Code, such as "GAZ025-056"
Definition["stateName"] = "" # Name of state, such as "GEORGIA"
Definition["wfoCityState"] = "NATIONAL HURRICANE CENTER MIAMI FL" # Location of WFO - city state
Definition["textdbPil"] = "MIAMVF007"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KNHCMVF007"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "{prddir}/TEXT/MVF007.txt"

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
#Definition["debug"] = 1

# Testing for Lower Case Below
Definition["lowerCase"] = 1  #1 for lowerCase 0 for upperCase
