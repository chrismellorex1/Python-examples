Definition = {}

Definition['displayName'] = "SPA_NT4"

VariableList = [
        #(copy.deepcopy(CWF.TextProduct.VariableList)),
        (("Include Tropical?", "includeTropical"), "No", "radio", ["Yes", "No"]),
        #(("Forecaster Name", "forecasterName") , "99", "radio",
        # ["NELSON","STRIPLING","SCHAUER","CHRISTENSEN",
        #  "LEWITSKY", "AL", "GR", "AGUIRRE", "DGS",
        #  "MUNDELL", "COBB", "LANDSEA", "CAB", "PAW",
        #  "FORMOSA", "HUFFMAN", "MT", "NAR"]),
        #(("Period Combining?","pdCombo"), "No", "radio", ["Yes","No"]),
        ((("Keep Previous Text After Period",
                      "updatePeriodIndex"), "No old text",
                      "radio", ["No old text", "Refresh headlines only",
                                1, 2, 3, 4, 5]))
        ]

# VariableList = [
#         #(copy.deepcopy(CWF.TextProduct.VariableList)),
#         (("Include Tropical?", "includeTropical") , "No", "radio", ["Yes","No"]),
#         #(("Forecaster Name", "forecasterName") , "99", "radio",
#         # ["NELSON","STRIPLING","SCHAUER","CHRISTENSEN",
#         #  "LEWITSKY", "AL", "GR", "AGUIRRE", "DGS",
#         #  "MUNDELL", "COBB", "LANDSEA", "CAB", "PAW",
#         #  "FORMOSA", "HUFFMAN", "MT", "NAR"]),
#         #(("Period Combining?","pdCombo"), "No", "radio", ["Yes","No"]),
#         ((("Keep Previous Text After Period (Selecting zero\nwill keep all old text but will refresh headlines)",
#                       "updatePeriodIndex"), "No old text",
#                       "radio", ["No old text",0,1,2,3,4,5,6,7,8]))
#         ]

Definition["showZoneCombiner"] = 0 # 1 to cause zone combiner to display
#Definition["defaultEditAreas"] = "Combinations_OFF_ONA_NT1"
Definition["defaultEditAreas"] = [
    ('GMZ040', "NO del Golfo incluyendo el Stetson Bank"),
    ('GMZ041', "SW Louisiana Offshore Waters including Flower Garden Banks Marine Sanctuary"),
    ('GMZ056', "N Central Gulf N of 26N between 87W and 91W"),
    ('GMZ057', "NE Gulf N of 26N E of 87W"),
    ('GMZ058', "W Central Gulf from 22N to 26N W of 94W"),
    ('GMZ045', "W Central Gulf from 22N to 26N between 91W and 94W"),
    ('GMZ046', "Central Gulf from 22Nto 26N between 87W and 91W"),
    ('GMZ047', "E Gulf from 22N to 26N E of 87W  Including Straits of Florida"),
    ('GMZ048', "SW Gulf S of 22N W of 94W"),
    ('GMZ049', "Central Bay of Campeche S of 22N between 92W and 94W"),
    ('GMZ050', "E Bay of Campeche S of 22N between 87W and 92W"),
            ]



# Definition["defaultEditAreas"] = [
#     ('SPG011', "NW GULF INCLUDING STETSON BANK"),
#     ('SPG013', "N CENTRAL GULF INCLUDING FLOWER GARDEN BANKS MARINE SANCTUARY"),
#     ('SPG015', "NE GULF N OF 25N E OF 87W"),
#     ('SPG017', "W CENTRAL GULF FROM 22N TO 26N W OF 94W"),
#     ('SPG019', "CENTRAL GULF FROM 22N TO 26N BETWEEN 87W AND 94W"),
#     ('SPG021', "E GULF FROM 22N TO 25N E OF 87W INCLUDING STRAITS OF FLORIDA"),
#     ('SPG023', "SW GULF S OF 22N W OF 94W"),
#     ('SPG025', "E BAY OF CAMPECHE INCLUDING CAMPECHE BANK"),
#             ]

Definition["mapNameForCombinations"] = "Offshore_Marine_Zones" # Map background for creating Combinations

# Header configuration items
#Definition["productName"] = "COASTAL WATERS FORECAST"  # name of product
Definition["fullStationID"] = "KNHC"  # full station identifier (4letter)
Definition["wmoID"] = "TEST04"        # WMO ID
Definition["pil"] = "SPANT4"          # product pil
Definition["areaName"] = "EL GOLFO DE MEXICO"  # Name of state, such as "GEORGIA"
Definition["wfoCityState"] = "CENTRO NACIONAL DE HURACANES MIAMI FL"  # Location of WFO - city st
Definition["textdbPil"] = "MIASPANT4"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KNHCSPANT4"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "{prddir}/TEXT/SPANT4.txt"

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
Definition["debug"] = 0
#Definition["editAreaSuffix"] = "_pt"

Definition["lineLength"] = 65   #Product line length
Definition["hazardSamplingThreshold"] = (0, 1)  #(%cov, #points)

Definition["periodCombining"] = 0     # If 1, do period combining
Definition["includeEveningPeriod"] = 0  # If 1, include Evening Period
Definition["useAbbreviations"] = 0      # If 1, use marine abbreviations
#Definition['lowerCase'] = 0
# Weather-related flags
#Definition["hoursSChcEnds"] = 24

#Definition["areaDictionary"] = "AreaDictionary"     # For product headers
Definition["language"] = "spanish"
#Definition["useHolidays"] = 1
Definition["lowercase"] = 1
# Trouble-shooting items
#Definition["passLimit"] = 20             # Limit on passes allowed through Narrative Tree
#Definition["trace"] = 1                  # Set to 1 to turn on trace through
                                         # Narrative Tree for trouble-shootin


# Required for BASE OFF!
#  synopsisUGC      UGC code for Synopsis
Definition["synopsisUGC"] = "GMZ001"    # UGC code for synopsis
Definition["synopsisHeading"] = ".SYNOPSIS..."# Heading for synopsis

Definition["productName"] = "PRONOSTICO PARA LAS AGUAS COSTA AFUERA"  # name of product ADDED 2/7/18 ERA
