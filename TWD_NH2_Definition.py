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

VariableList = [
       # (("Issuance Time", "includePrevDisc") , "Yes - for reference - your name only", "radio",
       #     ["0430 UTC","1030 UTC", "1630 UTC", "2230 UTC"]),
        #(("Product Issuance", "Z"), "0000Z", "radio",
        # ["0405 UTC","1005 UTC", "1605 UTC", "2205 UTC"]),
       # (("Product Issuance", "productIssuance"), "205 AM", "radio",
       #  ["205 AM", "805 AM", "205 PM", "805 PM"]),
        (("Include Previous Discussion?", "includePrevDisc"), "Yes - for reference - your name only", "radio",
            ["Yes - for reference - your name only"]),
        ]

Definition['displayName'] = "TWD_Atlantic"
#old zones
Definition["defaultEditAreas"] = [
            #E PACIFIC WITHIN 250 NM OF MEXICO
            #('GMZ011', "")
            ('GMZ040', "")
            ]

# Header configuration items
Definition["fullStationID"] = "KNHC"  # full station identifier (4letter)
Definition["wmoID"] = "AXNT20"        # WMO ID
Definition["pil"] = "TWDAT"          # product pil
Definition["areaName"] = ""#THE GULF OF MEXICO...CARIBBEAN\nSEA AND TROPICAL N ATLANTIC...AND SW N ATLANTIC" # Name of area
Definition["longProductDesc"] = "NORTH ATLANTIC OCEAN W OF 50W FROM 30N TO 50N." # long product name for heading
Definition["textdbPil"] = "MIATWDAT"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KNHCTWDAT"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "{prddir}/TEXT/MIATWDAT.txt"
Definition["signature"] = ""
Definition["includeEveningPeriod"] = 1

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
#Definition["debug"] = 1
# Need to add a product header in the middle of the warnings?
# Add the areaLabel that the following header precedes
#old zones
Definition["zoneWarningHeaders"] = {
            #"US MEXICO BORDER TO PUNTA EUGENIA": "E PACIFIC WITHIN 250 NM OF MEXICO",
            #"GUATEMALA AND EL SALVADOR": "E PACIFIC WITHIN 250 NM OF CENTRAL AMERICA...COLOMBIA...AND ECUADOR",
            }
