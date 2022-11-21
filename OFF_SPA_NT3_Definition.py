Definition = {}

Definition['displayName'] = "SPA_NT3"

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
    ('AMZ040', "Caribbean N of 18N W of 85W including Yucatan Basin"),
    ('AMZ041', "NW Caribbean N of 20N E of 85W"),
    ('AMZ042', "Caribbean from 18N to 20N between 80W and 85W including Cayman Basin"),
    ('AMZ043', "Caribbean from 18N to 20N between 76W and 80W"),
    ('AMZ044', "Caribbean Approaches to the Windward Passage"),
    ('AMZ045', "S of 18N W of 85W including Gulf of Honduras"),
    ('AMZ046', "Caribbean from 15N to 18N between 80W and 85W"),
    ('AMZ047', "Caribbean from 15N to 18N between 76W and 80W"),
    ('AMZ048', "Caribbean from 15N to 18N between 72W and 76W"),
    ('AMZ049', "Caribbean N of 15N between 68W and 72W"),
    ('AMZ050', "Caribbean N of 15N between 64W and 68W"),
    ('AMZ051', "Offshore Waters Leeward Islands"),
    ('AMZ052', "Tropical N Atlantic from 15N to 19N between 55W and 60W"),
    ('AMZ053', "W Central Caribbean from 11N to 15N W of 80W"),
    ('AMZ054', "Caribbean from 11N to 15N between 76W and 80W"),
    ('AMZ055', "Caribbean from 11N to 15N between 72W and 76W"),
    ('AMZ056', "Caribbean S of 15N between 68W and 72W"),
    ('AMZ057', "Caribbean S of 15N between 64W and 68W"),
    ('AMZ058', "Offshore Waters Windward Islands including Trinidad and Tobago"),
    ('AMZ059', "Tropical N Atlantic from 11N to 15N between 55W and 60W"),
    ('AMZ062', "Tropical N Atlantic from 07N to 11N"),
    ('AMZ060', "SW Caribbean S of 11N W of 80W"),
    ('AMZ061', "SW Caribbean S of 11N E of 80W including Approaches to Panama Canal"),
     
    ('AMZ063', "Atlantic from 29N to 31N W of 77W"),
    ('AMZ064', "Atlantic from 29N to 31N between 74W and 77W"),
    ('AMZ065', "Atlantic from 29N to 31N between 70W and 74W"),
    ('AMZ066', "Atlantic from 29N to 31N between 65W and 70W"),
    ('AMZ067', "Atlantic from 29N to 31N between 60W and 65W"),
    ('AMZ068', "Atlantic from 29N to 31N between 55W and 60W"),
    ('AMZ069', "Atlantic from 27N to 29N W of 77W"),
    ('AMZ070', "Atlantic from 27N to 29N between 74W and 77W"),
    ('AMZ071', "Atlantic from 27N to 29N between 70W and 74W"),
    ('AMZ072', "Atlantic from 27N to 29N between 65W and 70W"),
    ('AMZ073', "Atlantic from 27N to 29N between 60W and 65W"),
    ('AMZ074', "Atlantic from 27N to 29N between 55W and 60W"),
    ('AMZ075', "Northern Bahamas from 24N to 27N"),
    ('AMZ076', "Atlantic from 25N to 27N E of Bahamas to 70W"),
    ('AMZ077', "Atlantic from 25N to 27N between 65W and 70W"),
    ('AMZ078', "Atlantic from 25N to 27N between 60W and 65W"),
    ('AMZ079', "Atlantic from 25N to 27N between 55W and 60W"),
    ('AMZ080', "Central Bahamas from 22N to 24N including Cay Sal Bank"),
    ('AMZ081', "Atlantic from 22N to 25N E of Bahamas to 70W"),
    ('AMZ082', "Atlantic from 22N to 25N between 65W and 70W"),
    ('AMZ083', "Atlantic from 22N to 25N between 60W and 65W"),
    ('AMZ084', "Atlantic from 22N to 25N between 55W and 60W"),
    ('AMZ085', "Atlantic S of 22N W of 70W including Approaches to the Windward Passage"),
    ('AMZ086', "Atlantic S of 22N between 65W and 70W including Puerto Rico Trench"),
    ('AMZ087', "Atlantic from 19N to 22N between 60W and 65W"),
    ('AMZ088', "Atlantic from 19N to 22N between 55W and 60W"),
            ]
    
    
    
    
    
    
#     ('SPA011', "EL CARIBE AL N DE 18N Y O DE 85O INCLUYENDO LA CUENCA DE YUCATAN"),
#     ('SPA013', "EL CARIBE AL N DE 18N ENTRE 76O Y 85O INCLUYENDO LA CUENCA DE CAYMAN"),
#     ('SPA015', "EL CARIBE ACERCANDOSE AL PASO DE LOS VIENTOS"),
#     ('SPA017', "GOLFO DE HONDURAS"),
#     ('SPA019', "EL CARIBE DESDE 15N A 18N ENTRE 80O Y 85O"),
#     ('SPA021', "EL CARIBE DESDE 15N A 18N ENTRE 72O Y 80O"),
#     ('SPA023', "EL CARIBE AL N DE 15N ENTRE 64O AND 72O"),
#     ('SPA025', "AGUAS COSTA AFUERA ISLAS DE SOTAVENTO"),
#     ('SPA027', "ATLANTICO NORTE TROPICAL DESDE 15N A 19N ENTRE 55O AND 60O"),
#     ('SPA029', "EL CENTRO Y OESTE DEL CARIBE DESDE 11N HASTA 15N O DE 80O"),
#     ('SPA031', "EL CARIBE DESDE 11N A 15N ENTRE 72O AND 80O INCLUYENDO LA CUENCA DE COLOMBIA"),
#     ('SPA033', "EL CARIBE AL S DE 15N ENTRE 64O Y 72O INCLUYENDO LA CUENCA DE VENEZUELA"),
#     ('SPA035', "AGUAS COSTA AFUERA DE LAS ISLAS DE SOTAVENTO INCLUYENDO TRINIDAD Y TOBAGO"),
#     ('SPA037', "ATLANTICO NORTE TROPICAL DESDE 7N A 15N ENTRE 55O Y 65O"),
#     ('SPA039', "SUROESTE DEL CARIBE S DE 11N INCLUYENDO LAS CERCANIAS AL CANAL DE PANAMA"),
#     ('SPA111', "ATLANTICO DESDE 27N A 31N O DE 77O"),
#     ('SPA113', "ATLANTICO DESDE 27N A 31N ENTRE 70O A 77O"),
#     ('SPA115', "ATLANTICO DESDE 27N TO 31N ENTRE 65O Y 70O"),
#     ('SPA117', "BAHAMAS INCLUYENDO EL BANCO DE CAY SAL"),
#     ('SPA119', "ATLANTICO DESDE 22N A 27N AL E DE LAS BAHAMAS HASTA 70W"),
#     ('SPA121', "ATLANTICO DESDE 22N A 27N ENTRE 65O Y 70O"),
#     ('SPA123', "ATLANTICO AL S DE 22N O DE 70O INCLUYENDO LAS CERCANIAS AL PASO DE LOS VIENTOS"),
#     ('SPA125', "ATLANTICO AL S DE 22N ENTRE 65O Y 70O INCLUYENDO LA TRENCHA DE PUERTO RICO"),
#     ('SPA127', "ATLANTICO DESDE 19N A 22N ENTRE 55O Y 65O"),
#                 ]

Definition["mapNameForCombinations"] = "Offshore_Marine_Zones" # Map background for creating Combinations

# Header configuration items
#Definition["productName"] = "COASTAL WATERS FORECAST"  # name of product
Definition["fullStationID"] = "KNHC"  # full station identifier (4letter)
Definition["wmoID"] = "TEST05"        # WMO ID
Definition["pil"] = "SPANT3"          # product pil
Definition["areaName"] = " EL SUROESTE\n" + \
                         "DEL ATLANTICO NORTE Y TROPICAL Y PARA EL CARIBE"
                         #"PARA EL MAR CARIBE"  # Name of state, such as "GEORGIA"
Definition["wfoCityState"] = "CENTRO NACIONAL DE HURACANES MIAMI FL"  # Location of WFO - city st
Definition["textdbPil"] = "MIASPANT3"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KNHCSPANT3"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "{prddir}/TEXT/SPANT3.txt"

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
Definition["debug"] = 0
#Definition["editAreaSuffix"] = "_pt"

Definition["lineLength"] = 65   #Product line length
Definition["hazardSamplingThreshold"] = (0, 1)  #(%cov, #points)

Definition["periodCombining"] = 0     # If 1, do period combining
Definition["includeEveningPeriod"] = 0  # If 1, include Evening Period
Definition["useAbbreviations"] = 0      # If 1, use marine abbreviations

# Weather-related flags
#Definition["hoursSChcEnds"] = 24

#Definition["areaDictionary"] = "AreaDictionary"     # For product headers
Definition["language"] = "spanish"
#Definition["useHolidays"] = 1
Definition['lowerCase'] = 1
# Trouble-shooting items
#Definition["passLimit"] = 20             # Limit on passes allowed through Narrative Tree
#Definition["trace"] = 1                  # Set to 1 to turn on trace through
                                         # Narrative Tree for trouble-shootin

# Required for BASE OFF!
#  synopsisUGC      UGC code for Synopsis
Definition["synopsisUGC"] = "AMZ001"    # UGC code for synopsis
Definition["synopsisHeading"] = ".SYNOPSIS..."# Heading for synopsis
Definition["productName"] = "PRONOSTICO PARA LAS AGUAS COSTA AFUERA"  # name of product ADDED 2/7/18 ERA

#Definition["synopsis2UGC"] = "AMZ101"    # UGC code for 2nd synopsis
#Definition["synopsis2Heading"] = ".SYNOPSIS..."# Heading for 2nd synopsis
