Definition =  {
        "type": "smart",
        "displayName": "VOBRA_NT3",
        "database": "Fcst",
        # Defines output location of finished product.
        "outputFile": "{prddir}/TEXT/OFFN20.txt",
        "debug": 0,
        # Name of map background for creating Combinations
        "showZoneCombiner": 0, # 1 to cause zone combiner to display
        "mapNameForCombinations": "Offshore_Marine_Zones",

        "lineLength": 65,
        ## Edit Areas: Create Combinations file with edit area combinations.
        "defaultEditAreas": [
              ('VOBRA05', "NW CARIBBEAN W OF 85W"),
              ('VOBRA06', "CARIBBEAN N OF 15N BETWEEN 72W AND 85W"),
              ('VOBRA07', "CARIBBEAN FROM 11N TO 15N W OF 85W"),
              ('VOBRA08', "SW CARIBBEAN S OF 11N"),
              ('VOBRA09', "CARIBBEAN BETWEEN 64W AND 72W"),
              ('VOBRA10', "OFFSHORE LEEWARD ISLANDS AND ADJACENT ATLC WATERS FROM 15N TO 19N W OF 55W"),
              ('VOBRA11', "OFFSHORE WINDWARD ISLANDS AND ADJACENT ATLC WATERS FROM 07N TO 15N W OF 55W"),
              ('VOBRA12', "ATLC WATERS FROM 27N TO 31N W OF 77W"),
              ('VOBRA13', "ATLC WATERS FROM 27N TO 31N BETWEEN 65W AND 77W"),
              ('VOBRA14', "BAHAMAS N OF 22N"),
              ('VOBRA15', "ATLC WATERS FROM 22N TO 27N BETWEEN 65W AND THE BAHAMAS"),
              ('VOBRA16', "ATLC WATERS S 0F 22N W OF 65W"),
              ('VOBRA17', "ATLC WATERS FROM 19N TO 22N BETWEEN 55W AND 65W"),
              ],
        "editAreaSuffix": None,
        # product identifiers
        "productName": "Marine Weather HF Voice Broadcast", # product name
        "fullStationID": "KNHC",    # full station identifier (4letter)
        "wmoID": "FZNT31",          # WMO ID
        "pil": "OFFN20",            # Product pil
        "areaName": "",             # Name of state, such as "GEORGIA" -- optional
        "wfoCityState": "Miami, FL",   # Location of WFO - city state


        "synopsisUGC": "AMZ001",                # UGC code for synopsis
        "synopsisHeading": ".SYNOPSIS...",# Heading for synopsis
        "synopsis2UGC": "AMZ101",                # UGC code for synopsis 2
        "synopsis2Heading": ".SYNOPSIS...",# Heading for synopsis

        "textdbPil": "MIAOFFN20",       # Product ID for storing to AWIPS text database.
        "awipsWANPil": "KNHCOFFN20",   # Product ID for transmitting to AWIPS WAN.

        "hazardSamplingThreshold": (0, 1),  #(%cov, #points)

        "fixedExpire": 1,       #ensure VTEC actions don't affect segment expiration time

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
#         "prevProdPIL": "MIAOFFN20",
#         "updatePeriodIndex": 0,
#         "includeCombine": 0,

        }
