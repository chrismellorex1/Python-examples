Definition =  {
        "type": "smart",
        "displayName": "VOBRA_NT4",
        "database": "Fcst",
        # Defines output location of finished product.
        "outputFile": "{prddir}/TEXT/OFFN21.txt",
        "debug": 0,
        # Name of map background for creating Combinations
        "showZoneCombiner": 0, # 1 to cause zone combiner to display
        "mapNameForCombinations": "Offshore_Marine_Zones",

        "lineLength": 65,
        ## Edit Areas: Create Combinations file with edit area combinations.
        "defaultEditAreas": [
            ('VOBRA01', "GULF OF MEXICO N OF 26N W OF 87W"),
            ('VOBRA02', "GULF OF MEXICO FROM 22N TO 26N W OF 87W"),
            ('VOBRA03', "SW GULF OF MEXICO S OF 22N W OF 87W"),
            ('VOBRA04', "GULF OF MEXICO E OF 87W")
              ],
        "editAreaSuffix": None,
        # product identifiers
        "productName": "Marine Weather HF Voice Broadcast", # product name
        "fullStationID": "KNHC",    # full station identifier (4letter)
        "wmoID": "FZNT32",          # WMO ID
        "pil": "OFFN21",            # Product pil
        "areaName": "",             # Name of state, such as "GEORGIA" -- optional
        "wfoCityState": "Miami, FL",   # Location of WFO - city state


        "synopsisUGC": "GMZ001",                # UGC code for synopsis
        "synopsisHeading": ".SYNOPSIS...",# Heading for synopsis
#        "synopsis2UGC": "AMZ088",                # UGC code for synopsis 2
#        "synopsis2Heading": ".SYNOPSIS...",# Heading for synopsis

        "textdbPil": "MIAOFFN21",       # Product ID for storing to AWIPS text database.
        "awipsWANPil": "KNHCOFFN21",   # Product ID for transmitting to AWIPS WAN.

        "hazardSamplingThreshold": (0, 1),  #(%cov, #points)

        #"fixedExpire": 1,       #ensure VTEC actions don't affect segment expiration time

        "periodCombining": 1,       # If 1, combine periods, if possible
        # Product-specific variables:
        # Set to one if you want a 6-hour evening period instead of
        # 18-hour period without lows
        "includeEveningPeriod": 0,
        "useAbbreviations": 1,

        # Weather-related flags
        #"hoursSChcEnds": 24,

        # Area Dictionary -- Descriptive information about zones
        "areaDictionary": "AreaDictionary",
        #"useHolidays": 0,            # Set to 1 to use holidays in the time period labels
        # Language
        "language": "english",

        # Trouble-shooting items
        #"passLimit": 20,             # Limit on passes allowed through
                                     # Narrative Tree
        #"trace": 0,                  # Set to 1 to turn on trace through
                                     # Narrative Tree for trouble-shooting

        # Settings to insert text from previous Product.
        "prevProdPIL": "MIAOFFN21",
        "updatePeriodIndex": 0,
        "includeCombine": 0,

        }
