# ---------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without
# technical  support, and with no warranty, express or implied, as to
# its usefulness for any purpose.
#
# HighSeas_Definition.TextUtility
#
#  This file sets up all the Product Definition overrides for the
#  HSF formatter for a site.
#
# ---------------------------------------------------------------------
# TAFB Change Log
# ---------------------------------------------------------------------
VariableList = [
    (("Product Issuance", "productIssuance"), "0430 UTC", "radio",
    ["0430 UTC", "1030 UTC", "1630 UTC", "2230 UTC"]),

#     (("Forecaster Name", "forecasterName") , "99", "radio",
#     ["NELSON","STRIPLING","SCHAUER","CHRISTENSEN",
#      "LEWITSKY", "AL", "GR", "AGUIRRE", "DGS",
#      "MUNDELL", "COBB", "LANDSEA", "PAW",
#      "FORMOSA", "HUFFMAN", "MT"]),
                ]

Definition =  {
    "type": "smart",
    "displayName": "HSF_AT2_SWELL",
    "database": "Fcst",
    # Defines output location of finished product.
    "outputFile": "{prddir}/TEXT/HSF_AT2.txt",
    "debug": 0,
    "showZoneCombiner": 0,
    # Name of map background for creating Combinations
    #"mapNameForCombinations": "Marine_Zones",

    "lineLength": 65,
    ## Edit Areas: Create Combinations file with edit area combinations.
    "defaultEditAreas": [("GMZ040", "NW GULF INCLUDING STETSON BANK"),
                            ],
#Definition["editAreaSuffix"] = "_pt"

    "editAreaSuffix": None,
    # product identifiers
    "productName": "HIGH SEAS FORECAST", # product name
    "fullStationID": "KNHC",    # full station identifier (4letter)
    "wmoID": "FZNT02",          # WMO ID
    "pil": "HSFAT2",            # Product pil
    "areaName": "MIAMI FL",             # Name of state, such as "GEORGIA" -- optional
    "wfoCityState": "NATIONAL HURRICANE CENTER MIAMI FL",   # Location of WFO - city state

    "ccc": "MIA",               # AFOS node
    "tcmBasin": "AT",           # AT = Atlantic, EP = East Pacific, CP = Central Pacific

    "synopsisUGC": "",                # UGC code for synopsis
    "synopsisHeading": ".SYNOPSIS...",# Heading for synopsis

    "textdbPil": "MIAHSFAT2",       # Product ID for storing to AWIPS text database.
    "awipsWANPil": "KNHCHSFAT2",   # Product ID for transmitting to AWIPS WAN.

    "hazardSamplingThreshold": (0, 1),  #(%cov, #points)

    "fixedExpire": 1,       #ensure VTEC actions don't affect segment expiration time

    "periodCombining": 0,       # If 1, combine periods, if possible
    # Product-specific variables:
    # Set to one if you want a 6-hour evening period instead of
    # 18-hour period without lows
    "includeEveningPeriod": 0,
    "useAbbreviations": 1,

    # CCode flag - added for OPC 11/14/2017 CNJ
    "ccode": 0,             # If 1, produce ccode. If 0, don't produce ccode

    # Weather-related flags
    "hoursSChcEnds": 24,

    # Area Dictionary -- Descriptive information about zones
    "areaDictionary": "AreaDictionary",
    "useHolidays": 0,            # Set to 1 to use holidays in the time period labels
    # Language
    "language": "english",

    # Trouble-shooting items
    "passLimit": 20,             # Limit on passes allowed through
                                # Narrative Tree
    "trace": 0,                  # Set to 1 to turn on trace through
                                # Narrative Tree for trouble-shooting
    #"lowerCase": 1, #added this to test mixed case per T. Hansen 03/06/2016-JRL
    }
