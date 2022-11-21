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
        (("Include Previous FACA?", "includePrevDisc"), "Yes", "radio",
            ["Yes"]),
        ]

Definition['displayName'] = "AVIATION_FACA"
#old zones
Definition["defaultEditAreas"] = [
            #E PACIFIC WITHIN 250 NM OF MEXICO
            ('GMZ011', ""),
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
Definition["fullStationID"] = "KKCI"  # full station identifier (4letter)
Definition["wmoID"] = "FACA20"        # WMO ID
Definition["pil"] = "OFAMKC"          # product pil
Definition["areaName"] = ""#THE GULF OF MEXICO...CARIBBEAN\nSEA AND TROPICAL N ATLANTIC...AND SW N ATLANTIC" # Name of area
Definition["longProductDesc"] = "NORTH ATLANTIC OCEAN W OF 50W FROM 30N TO 50N." # long product name for heading
Definition["textdbPil"] = "MKCOFAMKC"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KKCIOFAMKC"   # Product ID for transmitting to AWIPS WAN.
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
