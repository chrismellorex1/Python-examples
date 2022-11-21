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
# MIM_ONA_Definition.TextUtility
#
#  This file sets up all the Product Definition overrides for the
#  MIM formatter for a site.
#
# History:
# F.Achorn/OPC    02/10/14    Added new zones (but commented out still).
# ---------------------------------------------------------------------

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum content of this file is the following Definition statement
#HideTool = 1
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

#----- WFO ONA MIM Definition -----
# Definition Statements must start in column 1.

# REQUIRED CONFIGURATION ITEMS
#Definition['displayName'] = None

VariableList = []
#         (("Include Previous Discussion?", "includePrevDisc") , "Yes - for reference - your name only", "radio",
#             ["Yes - update - both forecaster names","Yes - for reference - your name only"]),
#         ]

#Definition['displayName'] = "MIM_NEW"
Definition['displayName'] = "None"

#old zones
Definition["defaultEditAreas"] = [
            #Gulf of Mexico
            ('GMZ011', "NW GULF INCLUDING STETSON BANK"),
            ('GMZ013', "N CENTRAL GULF INCLUDING FLOWER GARDEN BANKS MARINE SANCTUARY"),
            ('GMZ015', "NE GULF N OF 25N E OF 87W"),
            ('GMZ017', "W CENTRAL GULF FROM 22N TO 26N W OF 94W"),
            ('GMZ019', "CENTRAL GULF FROM 22N TO 26N BETWEEN 87W AND 94W"),
            ('GMZ021', "E GULF FROM 22N TO 25N E OF 87W INCLUDING STRAITS OF FLORIDA"),
            ('GMZ023', "SW GULF S OF 22N W OF 94W"),
            ('GMZ025', "E BAY OF CAMPECHE INCLUDING CAMPECHE BANK"),
            #Caribbean Sea and Tropical N Atlc
            ('AMZ011', "CARIBBEAN N OF 18N W OF 85W INCLUDING YUCATAN BASIN"),
            ('AMZ013', "CARIBBEAN N OF 18N BETWEEN 76W AND 85W INCLUDING CAYMAN BASIN"),
            ('AMZ015', "CARIBBEAN APPROACHES TO THE WINDWARD PASSAGE"),
            ('AMZ017', "GULF OF HONDURAS"),
            ('AMZ019', "CARIBBEAN FROM 15N TO 18N BETWEEN 80W AND 85W"),
            ('AMZ021', "CARIBBEAN FROM 15N TO 18N BETWEEN 72W AND 80W"),
            ('AMZ023', "CARIBBEAN N OF 15N BETWEEN 64W AND 72W"),
            ('AMZ025', "OFFSHORE WATERS LEEWARD ISLANDS"),
            ('AMZ027', "TROPICAL N ATLANTIC FROM 15N TO 19N BETWEEN 55W AND 60W"),
            ('AMZ029', "W CENTRAL CARIBBEAN FROM 11N TO 15N W OF 80W"),
            ('AMZ031', "CARIBBEAN FROM 11N TO 15N BETWEEN 72W AND 80W INCLUDING COLOMBIA BASIN"),
            ('AMZ033', "CARIBBEAN S OF 15N BETWEEN 64W AND 72W INCLUDING VENEZUELA BASIN"),
            ('AMZ035', "OFFSHORE WATERS WINDWARD ISLANDS INCLUDING TRINIDAD AND TOBAGO"),
            ('AMZ037', "TROPICAL N ATLANTIC FROM 07N TO 15N BETWEEN 55W AND 65W"),
            ('AMZ039', "SW CARIBBEAN S OF 11N INCLUDING APPROACHES TO PANAMA CANAL"),
            #SW N Atlc
            ('AMZ111', "ATLANTIC FROM 27N TO 31N W OF 77W"),
            ('AMZ113', "ATLANTIC FROM 27N TO 31N BETWEEN 70W AND 77W"),
            ('AMZ115', "ATLANTIC FROM 27N TO 31N BETWEEN 65W AND 70W"),
            ('AMZ117', "BAHAMAS INCLUDING CAY SAL BANK"),
            ('AMZ119', "ATLANTIC FROM 22N TO 27N E OF BAHAMAS TO 70W"),
            ('AMZ121', "ATLANTIC FROM 22N TO 27N BETWEEN 65W AND 70W"),
            ('AMZ123', "ATLANTIC S OF 22N W OF 70W INCLUDING APPROACHES TO THE WINDWARD PASSAGE"),
            ('AMZ125', "ATLANTIC S OF 22N BETWEEN 65W AND 70W INCLUDING PUERTO RICO TRENCH"),
            ('AMZ127', "ATLANTIC FROM 19N TO 22N BETWEEN 55W AND 65W"),
#             ('PMZ011', "Gulf of Maine"),
#             ('PMZ013', "Georges Bank"),
#             ('PMZ015', "South of New England"),
#             ('PMZ017', "Hudson Canyon to Baltimore Canyon"),
#             ('PMZ019', "Baltimore Canyon to Hague Line" ),
#             ('PMZ021', "Baltimore Canyon to Hatteras Canyon" ),
#             ('PMZ023', "Hatteras Canyon to Cape Fear" ),
#             ('PMZ025', "Cape Fear to 31N" )
            ]
#new zones
# Definition["defaultEditAreas"] = [
#             #NT1
#             ('ANZ800', "Gulf of Maine"),
#             ('ANZ805', "Georges Bank east of 68W"),
#             ('ANZ900', "Georges Bank west of 68W"),
#             ('ANZ810', "South of New England"),
#             ('ANZ815', "South of Long Island"),
#             #NT2
#             ('ANZ820', "Hudson Canyon to Baltimore Canyon"),
#             ('ANZ915', "Hudson Canyon to the Great South Channel"),
#             ('ANZ920', "Baltimore Canyon to the Great South Channel" ),
#             ('ANZ905', "The Great South Channel to the Hague Line" ),
#             ('ANZ910', "East of the Great South Channel and south of 39N" ),
#             ('ANZ825', "Inner Waters from Baltimore Canyon to Cape Charles Light" ),
#             ('ANZ828', "Inner Waters from Cape Charles Light to Currituck Beach Light" ),
#             ('ANZ925', "Outer Waters from Baltimore Canyon to Hatteras Canyon" ),
#             ('ANZ830', "Inner Waters from Currituck Beach Light to Cape Hatteras" ),
#             ('ANZ833', "Inner Waters from Cape Hatteras to Cape Fear" ),
#             ('ANZ930', "Outer Waters from Hatteras Canyon to Cape Fear" ),
#             ('ANZ835', "Inner Waters from Cape Fear to 31N" ),
#             ('ANZ935', "Outer Waters from Cape Fear to 31N" ),
#             ]
# Header configuration items
Definition["fullStationID"] = "KNHC"  # full station identifier (4letter)
Definition["wmoID"] = "AGXX40"        # WMO ID
Definition["pil"] = "MIMATS"          # product pil
Definition["areaName"] = ""#THE GULF OF MEXICO...CARIBBEAN\nSEA AND TROPICAL N ATLANTIC...AND SW N ATLANTIC" # Name of area
Definition["longProductDesc"] = "NORTH ATLANTIC OCEAN W OF 50W FROM 30N TO 50N." # long product name for heading
Definition["textdbPil"] = "MIAMIMATS"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KNHCMIMATS"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "{prddir}/TEXT/MIAMIMATS.txt"
Definition["signature"] = "National Hurricane Center."

Definition["lineLength"] = 65

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
Definition["debug"] = 0
# Need to add a product header in the middle of the warnings?
# Add the areaLabel that the following header precedes
#old zones
Definition["zoneWarningHeaders"] = {
            "NW GULF INCLUDING STETSON BANK": "GULF OF MEXICO",
            "CARIBBEAN N OF 18N W OF 85W INCLUDING YUCATAN BASIN": "CARIBBEAN SEA AND TROPICAL N ATLANTIC FROM 07N TO 19N BETWEEN\n55W AND 64W",
            "ATLANTIC FROM 27N TO 31N W OF 77W": "SW N ATLANTIC INCLUDING THE BAHAMAS"
            }

Definition["synopsisHeading"] = ".SYNOPSIS..."# Heading for synopsis
            #"Gulf of Maine": "NT1 NEW ENGLAND WATERS",
            #"Hudson Canyon to Baltimore Canyon": "NT2 MID ATLC WATERS"}
#new zones - no change
# Definition["zoneWarningHeaders"] = {
#             "Gulf of Maine": "NT1 NEW ENGLAND WATERS",
#             "Hudson Canyon to Baltimore Canyon": "NT2 MID ATLC WATERS"}
Definition ["hideTool"] = 1
