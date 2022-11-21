# ---------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without
# technical  support, and with no warranty, express or implied, as to
# its usefulness for any purpose.
#
# CWF_WT_Definition.TextUtility
#
#  This file sets up all the Product Definition overrides for the
#  CWF_Pacific formatter for a site.
#
# ---------------------------------------------------------------------

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum content of this file is the following Definition statement

Definition = {}

# End MAKE NO CHANGES HERE
#**********************************************************************
#####################################################
# Override VariableList if desired
#

#----- WFO EKA CWF_Pacific Definition -----
# Definition Statements must start in column 1.
# REQUIRED CONFIGURATION ITEMS
Definition['displayName'] = "EKA_Formatters_CWF" #Experimental_WaveTerm"
#Definition['displayName'] = ""#"CWFPacific"

Definition["defaultEditAreas"] = "Combinations_CWF_EKA"
Definition["mapNameForCombinations"] = "Marine_Zones_EKA" # Map background for creating Combinations

# Header configuration items
Definition["productName"] = "COASTAL WATERS FORECAST"  # name of product
Definition["fullStationID"] = "KEKA"  # full station identifier (4letter)
Definition["wmoID"] = "FZUS56"        # WMO ID
Definition["pil"] = "CWFEKA"          # product pil
Definition["areaName"] = "CALIFORNIA"  # Name of state, such as "GEORGIA"
Definition["wfoCityState"] = "EUREKA CA"  # Location of WFO - city st
Definition["textdbPil"] = "SFOWRKEKA"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KEKACWFEKA"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "/data/local/Text/wrkeka.txt"

# OPTIONAL CONFIGURATION ITEMS
#Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
#Definition["debug"] = 1

#Automatic Functions
#Definition["autoSend"] = 1   #set to 1 to automatically transmit product
#Definition["autoSendAddress"] = "000"   #transmission address
Definition["autoStore"] = 0   #set to 1 to store product in textDB
Definition["autoWrite"] = 1   #set to 1 to write product to file

Definition["staticIssuanceTimes"] = 1

Definition["periodCombining"] = 1     # If 1, do period combining
Definition["includeEveningPeriod"] = 0 # If 1, include Evening Period
#Definition["useAbbreviations"] = 0     # If 1, use marine abbreviations

# Weather-related flags
#Definition["hoursSChcEnds"] = 48

Definition["areaDictionary"] = "AreaDictionary"     # For product headers
#Definition["language"] = "english"
#Definition["lineLength"] = 66
#Definition["useHolidays"] = 1

# Trouble-shooting items
#Definition["passLimit"] = 20       # Limit on passes allowed through Narrative Tree
#Definition["trace"] = 1            # Set to 1 to turn on trace through
                                   # Narrative Tree for trouble-shooting

################################################################################
#
#    APPEND THIS FILE TO YOUR CWF_Pacific_XXX_Definition.TextUtility File
#    in the SITE directory:
#    AWIPS -  /awips/GFESuite/primary/data/databases/SITE/TEXT/TextUtility/CWF_FPPacific_FPPQR_FPDefinition.TextUtility
#    RPP -    ~/release/data/databases/SITE/TEXT/TextUtility/CWF_FPPacific_FPPQR_FPDefinition.TextUtility
#
#################################################################################
#
#    #<16.f> - WRS >>>>>>
#    RECOMMENDED SETTINGS FOR BASELINE OPTIONAL SETTINGS
#    WESTERN REGIONAL CWF_Pacific FORMATTER
#    If you don't like these change or delete to meet your requirements
#    IFPS WR Definition Overrides Version 1 for 16.f by WRS 09/15/2004
#
#################################################################################

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
#Definition["debug"] = 1

#Automatic Functions
#Definition["autoSend"] = 1   #set to 1 to automatically transmit product
#Definition["autoSendAddress"] = "000"   #transmission address
# Set to automatically store the product in the AWIPS database (but not transmit)
#Definition["autoStore"] = 1   #set to 1 to store product in textDB
#Definition["autoWrite"] = 1   #set to 1 to write product to file

#
# Period combining doesn't seem to work for the CWF
#Definition["periodCombining"] = 1#0     # If 1, do period combining
#Definition["includeEveningPeriod"] = 1 # If 1, include Evening Period
#Definition["useAbbreviations"] = 1     # If 1, use marine abbreviations

# ADDED 03/13/05 so the Humboldt Bay Bar (PZZ410) would not show up on
# map of zones in the Formatter Launcher.

Definition['subDomainUGCs'] = ["PZZ450", "PZZ455", "PZZ470", "PZZ475"]

# Weather-related flags
Definition["periodSChcEnds"] = 5

Definition["language"] = "english"
Definition["lineLength"] = 64
Definition["useHolidays"] = 0

# Trouble-shooting items
#Definition["passLimit"] = 20       # Limit on passes allowed through Narrative Tree
#Definition["trace"] = 1            # Set to 1 to turn on trace through
                                   # Narrative Tree for trouble-shooting

#################################################################################
#
#    #<16.f> - WRS >>>>>>
#    NON BASELINE DEFINITIONS NEEDED FOR WESTERN REGIONAL CWF_Pacific FORMATTER
#    You must Edit these definitions below to fit your office
#    IFPS WR Definition Overrides Version 16.f by WRS 09/15/2004
#
#################################################################################

# Definition of the area covered by you CWF which will appear at the
# top of the CWF
# example: Definition["CWFAreaLabel"]  = "COASTAL WATERS FROM CAPE SHOALWATER WASHINGTON TO FLORENCE OREGON\nAND WESTWARD 60 NM\n\n"

Definition["CWFAreaLabel"]  = "PT ST GEORGE TO PT ARENA AND OUT 60 NM\n\n" \
                              #"THIS IS AN AUTOMATED AREA FORECAST GENERATED FROM THE NATIONAL\n" \
                              #"WEATHER SERVICE DIGITAL FORECAST DATABASE. TO PROVIDE FEEDBACK ON\n" \
                              #"THIS PRODUCT PLEASE COMPLETE OUR SURVEY LOCATED AT\n" \
                              #"HTTP://WWW.NWS.NOAA.GOV/SURVEY/NWS-SURVEY.PHP?CODE=WR-ACWF\n\n"

# "previousProductID" specifies the AWIPS key for the previous version of
# the CWF to use in getting the previous synopsis, previous bar forecasts
# and/or previous forecast segments
# example: Definition["previousProductID"]  = "PDXCWFPQR"

Definition["previousProductID"]  = "SFOCWDEKA"#"SFOCWFEKA"

# "synopsisHeading defines the heading for your CWF synopsis (or "None" if you don't want a previous synopsis"
# example: Definition["synopsisHeading"]  = "SYNOPSIS FOR SOUTHERN WASHINGTON AND NORTHERN OREGON COAST..."

Definition["synopsisHeading"]  = ".SYNOPSIS FOR NORTHERN CALIFORNIA WATERS..."

# "synopsisUGC" is the UGC FIPS code for your synopsis
# example: Definition["synopsisUGC"]  = "PZZ200"

Definition["synopsisUGC"]  = "PZZ400"

# If you do a river bar forecast supply the barzone and barname deffinitions
# and uncomment the following section...otherwise return None
# example:
# Definition["riverBarForecast_dict"] = {
#    "barzone": "PZZ210",
#    "barname": "COLUMBIA RIVER BAR FORECAST"
#    }

Definition["barZoneUGC"] = None#["PZZ410"]

# If running the GFE/IFPServer on AWIPS you can ignore the following section, but
# if you are running GFE/IFPServer on an RPP or non PX1 system you need this.
#
# "awipsTEXTDBhost" and "awipsTEXTDBuser" defines the host name and login user name to use to
# access the AWIPS text database from a non baseline (non AWIPS e.g. RPP BOX)
# version of the IFP Server.  If not specified, the default workstation for
# remote access is "lx1" and the default login user is "awipsusr".
# This method uses "secure shell" (ssh) to login to AWIPS, therefore you need
# to set up the passwordless login feature of ssh on your AWIPS before this will work
#    1.    On your host non-AWIPS GFE server computer go to the following
#        directory:
#                cd ~/.ssh
#    2.    Look for the files "id_dsa" and "id_dsa.pub".  If they exist
#        skip to step 4.
#    3.    If the "id_dsa" and "id_dsa.pub" files do not exist run the
#        following command to generate the key files:
#                ssh-keygen -t dsa
#        Use the default filenames, and no passkey.
#    4.    Copy the contents of the file "id_dsa.pub" (644), to the $HOME/.ssh directory on
#        the host machine into the "autohrized_keys2" (640) file (e.g. lx1 in the
#        /awips/fxa/awipsusr/.ssh/authorized_keys2)
#    5.    Now you need to set up the known_hosts file.  To do this at an
#        xterm window "ssh host -l username" where host is your host name
#               (e.g. lx1) and username is the username you are logging into (e.g.
#        awipsusr).
#    6.    The system will prompt you to add the key to the known
#        hosts. Answer yes.  Then exit and do the ssh command again.  If
#        you did everything correctly you should now be able to log in
#        without supplying a password.

# If you did the above correctly you should now be able to login to the specified
# AWIPS workstation and the specified user without entering a password using the
# command "ssh hose -l username".  Try it to make sure it works...you should
# not have to supply a password.
# Try commenting these out
#Definition["awipsTEXTDBhost"] = "lx1"
#Definition["awipsTEXTDBuser"] = "awipsusr"

Definition["attributionLine"] = "visit us at www.weather.gov/eureka"


########### END Regional CWF_Pacific Definitions Section######################
