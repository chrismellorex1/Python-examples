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
        (("Include Previous Discussion?", "includePrevDisc"), "Yes - for reference - your name only", "radio",
            ["Yes - for reference - your name only"]),
        ]

Definition['displayName'] = "TWD_PacificEMERGENCY"
#old zones
Definition["defaultEditAreas"] = [
            #E PACIFIC WITHIN 250 NM OF MEXICO
            ('AMZ040', ""), #3/31/22 era
            #('AMZ011', ""),
            #('PMZ013', "PUNTA EUGENIA TO CABO SAN LAZARO"),
            #('PMZ015', "CABO SAN LAZARO TO CABO SAN LUCAS"),
            #('PMZ017', "NORTHERN GULF OF CALIFORNIA"),
            #('PMZ019', "CENTRAL GULF OF CALIFORNIA"),
            #('PMZ019', "SOUTHERN GULF OF CALIFORNIA"),
            #('PMZ021', "ENTRANCE TO THE GULF OF CALIFORNIA INCLUDING CABO CORRIENTES"),
            #('PMZ023', "MEXICO - MICHOACHAN AND GUERRERO"),
            #('PMZ025', "MEXICO - OAXACA AND CHIAPAS INCLUDING THE GULF OF TEHUANTEPEC"),
            #E PACIFIC WITHIN 250 NM OF CENTRAL AMERICA...COLOMBIA...AND ECUADOR
            #('PMZ111', "GUATEMALA AND EL SALVADOR"),
            #('PMZ113', "EL SALVADOR TO NORTH COSTA RICA INCLUDING THE GULFS OF FONSECA AND PAPAGAYO"),
            #('PMZ115', "NORTH COSTA RICA TO WEST PANAMA"),
            #('PMZ117', "EAST PANAMA AND COLOMBIA INCLUDING GULF OF PANAMA"),
            #('PMZ119', "ECUADOR INCLUDING GULF OF GUAYAQUIL"),
            ]

# Header configuration items
Definition["fullStationID"] = "KNHC"  # full station identifier (4letter)
Definition["wmoID"] = "AXPZ20"        # WMO ID
Definition["pil"] = "TWDEP"          # product pil
Definition["areaName"] = ""#THE GULF OF MEXICO...CARIBBEAN\nSEA AND TROPICAL N ATLANTIC...AND SW N ATLANTIC" # Name of area
Definition["longProductDesc"] = "NORTH ATLANTIC OCEAN W OF 50W FROM 30N TO 50N." # long product name for heading
Definition["textdbPil"] = "MIATWDEP"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KNHCTWDEP"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "{prddir}/TEXT/MIATWDEP.txt"
Definition["signature"] = ""
Definition["includeEveningPeriod"] = 1
Definition['lowerCase'] = 1
Definition['autoStore'] = 0

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
