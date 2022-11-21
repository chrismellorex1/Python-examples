#!/usr/bin/env python
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
# ----------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
# Translator.py
# Class for Translator.
#
# Author: mathwig
# ----------------------------------------------------------------------------
import string

LanguageTables = {
    "english" : {},
    "french" : {
        "Expressions" : [
            ('nw gulf including stetson bank', 'le nord-ouest du golfe du mexique y compris la banque stetson'),
            ('n central gulf including flower garden banks marine sanctuary', 'LE GOLFE DU CENTRE-NORD DU MEXIQUE Y COMPRIS LE FLOWER GARDEN BANKS MARINE SANCTUARY'),
            ('ne gulf n of 25n e of 87w', 'LE GOLFE DU NORD-EST DU MEXIQUE AU NORD DE 25N A L-OUEST DE 87W'),
            ('w central gulf from 22n to 26n w of 94', 'LE GOLFE DU CENTRE-OUEST DE 22N A 26N A L-OUEST DE 94W'),
            ('central gulf from 22n to 26n between 87w and 94w', 'LE GOLFE CENTRAL DU MEXIQUE DE 22N A 26N ENTRE 87W ET 94W'),
            ('e gulf from 22n to 25n e of 87w including straits of florida', 'LE GOLFE ORIENTAL DU MEXICO DE 22N A 25N A L-EST DE 87W Y COMPRIS LE DETROIT DE FLORIDE'),
            ('sw gulf s of 22n w of 94w', 'LE DU SUD-OUEST DU GOLFE DE MEXIQUE AU SUD DE 22N A L-OUEST DE 94W'),
            ('e bay of campeche including campeche bank', 'LA BAIE EST DE CAMPECHE Y COMPRIS LA BANQUE CAMPECHE'),

            ('wind', 'vent'),
            ('knots', 'noeuds'),
            ('seas', 'mers'),
            ('feet', 'pieds'),
            ('scattered', 'disperse'),
            ('showers', 'pluie'),

            ('tonight', "Ce soir"),
            ('today', "Aujourd'hui"),
            ('night', "soir"),
            ('monday', "Lundi"),
            ('tuesday', "Mardi"),
            ('wednesday', "Mercredi"),
            ('thursday', "Jeudi"),
            ('friday', "Vendredi"),
            ('saturday', "Samedi"),
            ('sunday', "Dimanche",),

            ('mostly sunny', 'generalement ensoleille'),
            ('mostly clear', 'generalement degage'),
            ('mostly cloudy', 'generalement nuageux'),
            ('partly cloudy', 'partiellement nuageux'),
            ('sunny', 'ensoleille'),
            ('clear', 'ciel degage'),
            ('cloudy', 'nuageux'),
            ('high winds', 'vents forts'),
            ('light winds', 'vents faibles'),
            ('very windy', 'tres venteux'),
            ('probability of precipitation', 'probabilite de precipitations'),
            ('chance of precipitation', 'risque de precipitations'),
            ('areal coverage of precipitation', 'areal coverage de precipitations'),
            ('slight chance of', 'faible risque de'),
            ('chance of', 'risque de'),
            ('snow accumulation of', 'accumulation de neige de'),
            ('northeast winds at', 'vents du nord-est de'),
            ('northwest winds at', 'vents du nord-ouest de'),
            ('southest winds at', 'vents du sud-est de'),
            ('southwest winds at', 'vents du sud-ouest de'),
            ('east winds at', "vents de l'est de"),
            ('west winds at', "vents de l'ouest de"),
            ('north winds at', 'vents du nord de'),
            ('south winds at', 'vents du sud de'),
            ('northeast winds up', "vents du nord-est jusqu'"),
            ('northwest winds up', "vents du nord-ouest jusqu'"),
            ('southest winds up', "vents du sud-est jusqu'"),
            ('southwest winds up', "vents du sud-ouest jusqu'"),
            ('east winds up', "vents de l'est jusqu'"),
            ('west winds up', "vents de l'ouest jusqu'"),
            ('north winds up', "vents du nord jusqu'"),
            ('south winds up', "vents du sud jusqu'"),
            ('northeast', 'nord-est'),
            ('northwest', 'nord-ouest'),
            ('southeast', 'sud-est'),
            ('southwest', 'sud-ouest'),
            ('east', 'est'),
            ('west', 'ouest'),
            ('north', 'nord'),
            ('south', 'sud'),
            ('in the evening', 'au cours de la soiree'),
            ('in the night', 'au cours de la nuit'),
            ('in the morning', 'au cours de la matinee'),
            ('in the afternoon', "au cours de l'apres-midi"),
            ('through the evening', 'pret de la soiree'),
            ('through the night', 'pret de la nuit'),
            ('through the morning', 'pret de la matinee'),
            ('through the afternoon', "pret de l'apres-midi"),
            ('through', "pret"),
            ('overnight', 'pendant la nuit'),
            ('decreasing to', 'changeant a'),
            ('increasing to', 'augmentant a'),
            ('shifting to the', 'devenant du'),
            ('becoming', 'devenant'),
            ('much warmer', 'beaucoup plus chaud'),
            ('warmer', 'plus chaud'),
            ('cooler', 'plus frais'),
            ('sharply colder', 'beaucoup plus froid'),
            ('clearing later', 'se degageant plus tard'),
            ('becoming cloudy', 'devenant nuageux'),
            ('increasing cloudiness', 'augmentation de nuages'),
            ('decreasing cloudiness', 'diminution de nuages'),
            ('around', 'de pres de'),
            ('in the lower', 'dans les bas'),
            ('in the mid', 'dans les mi-'),
            ('in the upper', 'dans les hauts'),
            ('in the', 'dans les'),
            ('highs', 'maximums'),
            ('lows', 'minimums'),
            ('. high', '. maximum'),
            ('. low', '. minimum'),
            ('rising', 'montant'),
            ('falling', 'descendant'),
            ('high', 'eleve'),
            ('low', 'bas'),
            ('temperatures', 'temperaturas'),
            ('percent', 'pour cent'),
            ('inches', 'pouces'),
            ('inch', 'pouce'),
            (' to ', ' a '),
            (' at ', ' a '),
            (' and ', ' et '),
            ('mixed with', 'avec'),
            ('with', 'avec'),
            ('no swells', 'aucune houle'),
            ('swell', 'houle'),
            ('waves', 'mer'),
            ('less than', 'de moins de'),
            ('sky/weather...', 'CIEL/METEO.......'),
            ('lal...........', 'LAL..............'),
            ('temperature...', 'TEMPERATURE......'),
            ('humidity......', 'HUMIDITE.........'),
            ('wind - 20 ft..', 'VENT - 20 PIEDS..'),
            ('valleys...', 'VALLEES...'),
            ('ridges....', 'ARETES....'),
            ('haines index..', 'INDICE HAINES....'),
            ('smoke dispersal', 'DISPERSION DE FUMEE'),
            ('mixing height...', 'HAUTEUR DE MELANGE..'),
            ('transport wind..', 'VENT DE TRANSPORTATION..'),
            ('visibility', 'visibilite'),
            ('frequent lightning', 'foudre frequente'),
            ('gusty winds', 'vents brisques'),
            ('heavy rainfall', 'pluie abondante'),
            ('damaging winds', 'vents damageux'),
            ('small hail', 'petite grele'),
            ('large hail', 'grosse grele'),
            ('then', 'alors'),
            ],
        "Types" : [
            ('freezing rain', 'pluie verglacante', 'FS'),
            ('rain showers', 'averses de pluie', 'FP'),
            ('rain', 'pluie', 'FS'),
            ('freezing drizzle', 'bruine', 'FS'),
            ('drizzle', 'bruine', 'FS'),
            ('snow showers', 'averses de neige', 'FP'),
            ('snow', 'neige', 'FS'),
            ('dust', 'poussiere', 'FS'),
            ('fog', 'brouillard', 'MS'),
            ('haze', 'brume', 'FS'),
            ('hail', 'grele', 'FS'),
            ('sleet', 'verglas', 'MS'),
            ('smoke', 'fumee', 'FS'),
            ('thunderstorms', 'orages', 'MP'),
            ('volcanic ash', 'cendre volcanique', 'FS')
            ],
        "Intensities" :[
            ('very light', 'tres faible', 'tres faible', 'tres faible',
             'tres faibles'),
            ('light', 'faible', 'faibles', 'faible', 'faibles'),
            ('moderate', 'modere', 'moderes', 'moderee', 'moderees'),
            ('very heavy', 'tres abondant', 'tres abondants',
             'tres abondante', 'tres abondantes'),
            ('heavy', 'abondant', 'abondants', 'abondante', 'abondantes')
            ],
        "Coverages" : [
            ('isolated', 'isole', 'isoles', 'islolee', 'isolees'),
            ('widely scattered', 'largement disperse',
             'largement disperses',
              'largement dispersee', 'largement dispersees'),
            ('scattered', 'disperse', 'disperses', 'dispersee',
             'dispersees'),
            ('widespread', 'repandu', 'repandus', 'repanduee', 'repanduees'),
            ('occasional', 'passage', 'passages', 'passagee', 'passagees'),
            ('numerous', 'nombreux', 'nombreux', 'nombreuse', 'nombreuses')
            ],
        "Exceptions" : [
            ('likely', 'probable', 'probables', 'probable', 'probables')
            ],
        "CleanUp" :  [
            ('de a', "d'a"),
            ('mi- ', 'mi-'),
            ("jusqu' a", "jusqu'a")
            ]
        },
    "spanish" : {
        "Expressions" : [

            ('caribbean n of 18n w of 85w including yucatan basin', 'Caribe al N de 18N y O de 85O incluyendo la cuenca de Yucatan'),
            ('caribbean n of 20n e of 85w', 'Caribe al N de 20N y E de 85O'),
            ('Caribbean from 18N to 20N between 80W and 85W including Cayman Basin', 'Caribe de 18N a 20N entre 80O y 85O incluyendo la Cuenca de Cayman'),
            ('Caribbean from 18N to 20N between 76W and 80W', 'Caribe de 18N a 20N entre 76O y 80O'),
            ('Caribbean Approaches to the Windward Passage', 'Cercanias del Caribe hasta el Paso de los Vientos'),
            ('S of 18N W of 85W including Gulf of Honduras', 'S de 18N y O de 85O incluyendo el Golfo de Honduras'),
            ('Caribbean from 15N to 18N between 80W and 85W', 'Caribe de 15N a 18N de 80O a 85O'),
            ('Caribbean from 15N to 18N between 76W and 80W', 'Caribe de 15N a 18N de 76O a 80W' ),
            ('Caribbean from 15N to 18N between 72W and 76W', 'Caribe de 15N a 18N de 72O a 76O'),
            ('Caribbean N of 15N between 68W and 72W', 'Caaribe al N de 15N entre 68O y 72O'),
            ('Caribbean N of 15N between 64W and 68W', 'Caribe al N de 15N entre 64O y 68O'),
            ('Offshore Waters Leeward Islands', 'Aguas Costa Afuera de las Islas de Sotavento'),
            ('Tropical N Atlantic from 15N to 19N between 55W and 60W','Atlantico Tropical de 15N a 19N entre 55O y 60O'),
            ('W Central Caribbean from 11N to 15N W of 80W', 'Centro y Oeste del Caribe de 11N a 15N y O de 80O'),
            ('Caribbean from 11N to 15N between 72W and 76W', 'Caribe de 11N a 15N entre 72O y 76O'),
            ('Caribbean S of 15N between 68W and 72W', 'Caribe al S de 15N entre 68O y 72O'),
            ('Caribbean S of 15N between 64W and 68W', 'Caribe al S de 15N entre 64Oy 68O'),
            ('Offshore Waters Windward Islands including Trinidad and Tobago', 'Aguas costa Afuera de Islas de Barlovento incluyendo Trinidad y Tobago'),
            ('Tropical N Atlantic from 11N to 15N between 55W and 60W', 'Atlantico N Tropical de 11N a 15N entre 55O y 60O'),
            ('Tropical N Atlantic from 07N to 11N', 'Atlantico N Tropical de 07N a 11N'),
            ('SW Caribbean S of 11N W of 80W', 'SO del Caribe al S de 11N y O de 80O'),
            ('SW Caribbean S of 11N E of 80W including Approaches to Panama Canal', 'SO del Caribe a S de 11N y E de 80O incluyendo las cercanias al Canal de Panama'),
     
#             ('AMZ063', "Atlantic from 29N to 31N W of 77W"),
#             ('AMZ064', "Atlantic from 29N to 31N between 74W and 77W"),
#             ('AMZ065', "Atlantic from 29N to 31N between 70W and 74W"),
#             ('AMZ066', "Atlantic from 29N to 31N between 65W and 70W"),
#             ('AMZ067', "Atlantic from 29N to 31N between 60W and 65W"),
#             ('AMZ068', "Atlantic from 29N to 31N between 55W and 60W"),
#             ('AMZ069', "Atlantic from 27N to 29N W of 77W"),
#             ('AMZ070', "Atlantic from 27N to 29N between 74W and 77W"),
#             ('AMZ071', "Atlantic from 27N to 29N between 70W and 74W"),
#             ('AMZ072', "Atlantic from 27N to 29N between 65W and 70W"),
#             ('AMZ073', "Atlantic from 27N to 29N between 60W and 65W"),
#             ('AMZ074', "Atlantic from 27N to 29N between 55W and 60W"),
#             ('AMZ075', "Northern Bahamas from 24N to 27N"),
#             ('AMZ076', "Atlantic from 25N to 27N E of Bahamas to 70W"),
#             ('AMZ077', "Atlantic from 25N to 27N between 65W and 70W"),
#             ('AMZ078', "Atlantic from 25N to 27N between 60W and 65W"),
#             ('AMZ079', "Atlantic from 25N to 27N between 55W and 60W"),
#             ('AMZ080', "Central Bahamas from 22N to 24N including Cay Sal Bank"),
#             ('AMZ081', "Atlantic from 22N to 25N E of Bahamas to 70W"),
#             ('AMZ082', "Atlantic from 22N to 25N between 65W and 70W"),
#             ('AMZ083', "Atlantic from 22N to 25N between 60W and 65W"),
#             ('AMZ084', "Atlantic from 22N to 25N between 55W and 60W"),
#             ('AMZ085', "Atlantic S of 22N W of 70W including Approaches to the Windward Passage"),
#             ('AMZ086', "Atlantic S of 22N between 65W and 70W including Puerto Rico Trench"),
#             ('AMZ087', "Atlantic from 19N to 22N between 60W and 65W"),
#             ('AMZ088', "Atlantic from 19N to 22N between 55W and 60W"),
#             
            
            
            ('forecaster ', 'Pronosticador '),
            ('national hurricane center', 'Centro Nacional de Huracanes'),
            ('offshore forecast ', 'Pronostico para las Aguas Costa Afuera ' ),
            ('mostly sunny', 'mayormente soleado'),
            ('mostly clear', 'mayormente claro'),
            ('mostly cloudy', 'mayormente nublado'),
            ('partly cloudy', 'parcialmente nublado'),
            ('sunny', 'soleado'),
            ('clearing', 'despejandose'),
            ('clear', 'despejado'),
            ('later', 'mas tarde'),
            ('cloudy', 'nublado'),
            ('snow accumulation of', 'acumulacion de nieve'),
            ('probability of precipitation', 'probabilidad de lluvias'),
            ('chance of precipitation', 'probabilidad de lluvias'),
            ('areal coverage of precipitation', 'cobertura de lluvias'),
            ('slight chance of', 'leve probabilidad de'),
            ('chance of', 'probabilidad de'),

            ('in the night', 'en la noche'),
            ('during the night', 'durante la noche'),
            ('early', 'temprano'),
            ('in the morning', ' en la manana'), #1/8/18 fixed era
            ('in the late', 'tarde'),
            ('in the afternoon', 'en la tarde'),
            ('in the evening', 'temprano en la noche'),
            ('through the morning', 'durante la manana'),
            ('through the afternoon', 'durante la tarde'),
            ('through the evening', 'durante las primeras horas de la noche'),

            ('morning', 'manana'),
            ('afternoon', 'tarde'),

            ('overnight', 'durante la noche'),
            ('evening', 'en la noche'),
            ('evening', 'temprano en la noche'),
            ('decreasing to', 'disminuyendo a'),
            ('increasing to', 'aumentando a'),
            ('shifting to the', 'tornandose del'),
            ('becoming', 'tornandose'),
            ('then', 'luego'),
            ('followed by', 'seguido por'),
            ('much warmer', 'mucho mas caliente'),
            ('warmer', 'mas caliente'),
            ('sharply colder', 'marcadamente frio'),
            ('cooler', 'mas fresco'),
            ('clearing later', 'aclarando en la tarde'),
            ('becoming cloudy', 'llegando a ser nublado'),
            ('increasing cloudiness', 'nubosidad aumentando'),
            ('decreasing cloudiness', 'nubosidad disminuyendo'),
            ('high winds', 'vientos fuertes'),
            ('. highs', '. temperaturas maximas'),
            ('. lows', '. temperaturas minimas'),

            (' jan', ' Enero'),
            (' feb', ' Febrero'),
            (' mar ', ' Marzo '),
            (' apr', ' Abril'),
            (' may ', ' Mayo '),
            (' jun', ' Junio'),
            (' jul', ' Julio'),
            (' aug', ' Agosto'),
            (' sep', ' Septiembre'),
            (' oct', ' Octubre'),
            (' nov', ' Noviembre'),
            (' dec', ' Diciembre'),

            (' mon', ' Lunes'),
            (' tue', ' Martes'),
            (' wed', ' Miercoles'),
            (' thu ', 'Jueves'),
            (' fri', ' Viernes'),
            (' sat', ' Sabado'),
            (' sun', ' Domingo'),

            ('in north swell', 'en marejada del norte'),
			('in south swell', 'en marejada del sur'),
			('in east swell', 'en marejada del este'),
			('in west swell', 'en marejada del oeste'),

			('in northeast swell', 'en marejada del noroeste'),
			('in northwest swell', 'en marejada del noroeste'),
			('in southeast swell', 'en marejada del sureste'),
			('in southwest swell', 'en marejada del suroeste'),

			('in northwest to north swell', 'en marejada del noroeste a norte'),
			('in northeast to north swell', 'en marejada del noroeste a norte'),
			('in northeast to east swell', 'en marejada del noroeste a este'),
			('in north to northeast swell', 'en marejada del norte a noreste'),
			('in southwest to south swell', 'en marejada del suroeste a sur'),
			('in southwest to west swell', 'en marejada del suroeste a oeste'),
			('in southeast to south swell', 'en marejada del sureste a sur'),
			('in south to southwest swell', 'en marejada del sur a suroeste'),
			('in east to southeast swell', 'en marejada del este a sureste'),
			('in west to northwest swell', 'en marejada del oeste a noroeste'),

            #('gale conditions possible', 'condiciones de galerna posibles'),
            ('north to northeast winds', 'vientos del norte a noreste'),
            ('northeast to east winds', 'vientos del noreste a este'),
            ('northeast to north winds', 'vientos del noreste a norte'),
            ('north to northwest winds', 'vientos del norte a noroeste'),
            ('northwest to west winds', 'vientos del noroeste a oeste'),
            ('northwest to north winds', 'vientos del noroeste a norte'),
            ('south to southeast winds', 'vientos del sur a sureste'),
            ('southeast to south winds', 'vientos del sureste a sur'),
            ('south to southwest winds', 'vientos del sur a suroeste'),
            ('southwest to south winds', 'vientos del suroeste a sur'),
            ('east to northeast winds', 'vientos del este a noreste'),
            ('northeast to east winds', 'vientos del noreste a este'),
            ('east to southeast winds', 'vientos del este a sureste'),
            ('southeast to east winds', 'vientos del sureste a este'),
            ('west to northwest winds', 'vientos del oeste a noroeste'),
            ('northwest to west winds', 'vientos del noroeste a oeste'),
            ('west to southwest winds', 'vientos del oeste a suroeste'),
            ('southwest to west winds', 'vientos del suroeste a oeste'),

            ('northeast winds', 'vientos del noreste'),
            ('northwest winds', 'vientos del noroeste'),
            ('southeast winds', 'vientos del sureste'),
            ('southwest winds', 'vientos del suroeste'),
            ('east winds', 'vientos del este'),
            ('west winds', 'vientos del oeste'),
            ('north winds', 'vientos del norte'),
            ('south winds', 'vientos del sur'),
            ('northeast winds up', 'vientos del noreste hasta'),
            ('northwest winds up', 'vientos del noroeste hasta'),
            ('southest winds up', 'vientos del sureste hasta'),
            ('southwest winds up', 'vientos del suroeste hasta'),
            ('east winds up', 'vientos del este hasta'),
            ('west winds up', 'vientos del oeste hasta'),
            ('north winds up', 'vientos del norte hasta'),
            ('south winds up', 'vientos del sur hasta'),
            ('northeast', 'noreste'),
            ('northwest', 'noroeste'),
            ('southeast', 'sureste'),
            ('southwest', 'suroeste'),

            ('small craft exercise caution', 'precaucion a embarcaciones pequenas'),
            ('small craft advisory', 'advertencias a embarcaciones pequenas'),
            ('knots', 'nudos'),
            (' ft ', ' pies '),
            ('seas', 'oleaje de'),
            ('bay and inland waters', 'aguas tierra adentro y de las bahias'),
            ('inland waters', 'aguas tierra adentro'),
            ('a light chop', 'picadas ligeramente'),
            ('a moderate chop', 'picadas moderadamente'),
            ('rough', 'turbulentas'),
            ('very rough', 'bien turbulentas'),
            ('almost smooth', 'casi llanas'),
            ('smooth', 'llanas'),
            ('choppy', 'picadas'),
            ('extended forecast', 'pronostico extendido'),
            #('forecast for', 'pronostico de'),
            ('bay waters', 'aguas de la bahia'),
            ('lake waters', 'aguas del lago'),
            ('feet', 'pies'),
            ('foot', 'pie'),
            ('east', 'este'),
            ('west', 'oeste'),
            ('north', 'norte'),
            ('south', 'sur'),
            ('patchy dense fog', 'niebla densa esparcida'),
            ('areas of dense fog', 'areas de niebla densa'),
            ('widespread dense fog', 'niebla densa extensa'),
            ('patchy fog', 'niebla esparcida'),
            ('areas of fog', 'areas de niebla'),
            ('widespread fog', 'niebla extensa'),
            ('dense fog', 'niebla densa'),
            ('around', 'alrededor de'),
            ('in the lower to mid', 'en los bajos a medios'),
            ('in the mid to upper', 'en los medios a altos'),
            ('in the lower', 'en los bajos'),
            ('in the mid', 'en los medios'),
            ('in the upper', 'en los altos'),
            #('in the', 'en los'), #1/8/18 era commented out
            (' low ', 'bajo'),
            ('high', 'alto'),
            ('no swells', 'sin marejeda'),
            ('swell', 'marejeda'),
            ('waves', 'olas'),
            ('less than', 'menos de'),
            ('percent', 'por ciento'),
            #('inches', 'pulgadas'),
            #('inch', 'pulgada'),
            ('light winds', 'vientos ligeros'),
            ('very windy', 'muy ventoso'),
            ('windy', 'ventoso'),
            ('breezy', 'brisas'),
            ('and gusty', 'con rafagas mas altas'),
            ('...and ', '...y '),
            (' and ', ' y '),
            (' to ', ' a '),
            (' at ', ' en '),
            ('within', 'a'),
            (' for ', ' para '),
            ('building', 'incrementando'),
            ('of coast of nicaragua', 'de la costa de nicaragua'),
            (' with ', ' con '),
            ('mixed with', 'con'),
            ('sky/weather...', 'CIELO/TIEMPO.....'),
            ('lal...........', 'NAE..............'),
            ('temperature...', 'TEMPERATURA......'),
            ('humidity......', 'HUMEDAD........'),
            ('wind - 20 ft..', 'VIENTO - 20 FT..'),
            ('valleys...', 'VALLES...'),
            ('ridges....', 'CRESTAS....'),
            ('haines index..', 'INDICE DE HAINES....'),
            ('smoke dispersal', 'DISPERSION DE HUMO'),
            ('mixing height...', 'ALTURA DE MEZCLA..'),
            ('transport wind..', 'VIENTO TRANSPORTADOR..'),
            ('visibility', 'visibilidad'),
            ('frequent lightning', 'rayos frequentes'),
            ('gusty winds', 'rachas de viento'),
            ('heavy rainfall', 'lluvia intensa'),
            ('damaging winds', 'vientos perjudiciales'),
            ('small hail', 'granizo pequeno'),
            ('large hail', 'granizo grande'),
            ('sunday night', 'DOMINGO EN LA NOCHE'),
            ('monday night', 'LUNES EN LA NOCHE'),
            ('tuesday night', 'MARTES EN LA NOCHE'),
            ('wednesday night', 'MIERCOLES EN LA NOCHE'),
            ('thursday night', 'JUEVES EN LA NOCHE'),
            ('friday night', 'VIERNES EN LA NOCHE'),
            ('saturday night', 'SABADO EN LA NOCHE'),
            ('sunday', 'DOMINGO'),
            ('monday', 'LUNES'),
            ('tuesday', 'MARTES'),
            ('wednesday', 'MIERCOLES'),
            ('thursday', 'JUEVES'),
            ('friday', 'VIERNES'),
            ('saturday', 'SABADO'),
            ('tonight', 'ESTA NOCHE'),
            ('today', 'HOY'),
            ('this afternoon', 'ESTA TARDE'),
            ('overnight', 'DURANTE LA NOCHE'),
            ('scattered tstms', 'tormentas dispersas'),
            #('isolated tstms.','tormentas aisladas'),
            ('near the coast', 'cerca de la costa'),
            ('inland', 'tierra adentro'),
            ('winds', 'vientos'),
            ('wind', 'vientos'),
            ('or less', 'o menos'),
            ('isolated thunderstorms', 'tormentas aisladas'), #added 01/31/18
            ('isolated', 'aisladas'), #added 01/31/18
            ('late', 'tarde'), #1/8/18 era took space out at the beginning
            ('elsewhere', 'para el resto del area'),
            ('diminishing', 'disminuyendo'),
            ('subsiding', 'disminuyendo'), #1/8/18 era added
            ('shifting', 'tornandose')
            ],
        "Types" : [
            ('freezing rain', 'lluvia helada', 'FS'),
            ('rain showers', 'chubascos', 'MP'),
            ('showers', 'chubascos', 'MP'),
            ('freezing drizzle', 'llovizna helada', 'FS'),
            ('rain', 'lluvia', 'FS'),
            ('drizzle', 'llovizna', 'FS'),
            ('snow showers', 'chubascos de nieve', 'FS'),
            ('snow', 'nieve', 'FS'),
            ('fog', 'nieblas', 'MS'),
            ('dust', 'polvo', 'MS'),
            ('haze', 'neblina', 'FS'),
            ('hail', 'granizo', 'MS'),
            ('sleet', 'aguanieve', 'FS'),
            ('smoke', 'humo', 'MS'),
            ('thunderstorms', 'tormentas', 'MP'),
            ('volcanic ash', 'ceniza volcanica', 'FS')
            ],
        "Intensities" : [
            ('light', 'muy ligero', 'muy ligeros', 'muy ligera',
             'muy ligeras'),
            ('light', 'ligero', 'ligero', 'ligero', 'ligero'),
            ('moderate', 'moderado', 'moderado', 'moderado', 'moderado'),
            ('very heavy', 'muy intenso', 'muy intensos', 'muy intensa',
             'muy intensas'),
            ('heavy', 'intenso', 'intensos', 'intensa', 'intensas'),
            ('numerous', 'numeroso', 'numerosos', 'numerosa', 'numerosas')
            ],
        "Coverages" : [
            ('isolated', 'aislado', 'aisladas', 'aislada', 'aisladas'),
            ('widely scattered', 'extensamente disperso',
             'extensamente dispersos', 'extensamente dispersa',
             'extensamente dispersas'),
            ('scattered', 'disperso', 'dispersos', 'dispersa', 'dispersas'),
            ('occasional', 'ocasional', 'ocasionales', 'ocasional',
             'ocasionales'),
            ('widespread', 'muy difundido', 'muy difundidos',
             'muy difundida', 'muy difundidas')
            ],
        "Exceptions" :[
            ('likely', 'probable', 'probables', 'probable', 'probables')
            ],
       "CleanUp" :[ ]
        }
    }


# ValueDict :  This index and table contain subsitution values for the HTML
#   Template pages, FastWx.html and Table.html
Index = {
    "english": 1,
    "french" : 2,
    "spanish": 3
}

ValueDictTable = [
    ("Type", "Category", "Categorie", "Categoria"),
    ("Public", "Public", "Publiques", "Publico"),
    ("FireWeather", "FireWeather", "Previsions Feu", "Incendios-Tiempo"),
    ("Aviation", "Aviation", "Aviation", "Aviacion"),
    ("Marine", "Marine", "Marine", "Maritimo"),
    ("Language", "Language", "Langue", "Lenguaje"),
    ("Audio", "Audio", "Audio", "Audio"),
    ("Click", "CLICK", "CLIQUER", "HAGA CLIC"),
    ("ClickText", "on a location OR Select:",
     "sur une location ou Choisir",
     "en una localidad o Seleccionela"),
    ("CityTable", "Table of Cities", "Table de Villes", "Tabla de Ciudades"),
    ("CountyTable", "Table of Counties", "Table de Comtes",
      "Tabla de Condados "),
    ("issued", "Issued", "Emises", "Emitido"),
    ("Site", "Forecast Location: ", "Site de Previsions: ",
      "Area de Pronostico: "),
    ("English", "English", "Anglais", "Ingles"),
    ("Spanish", "Spanish", "Espagnol", "Espanol"),
    ("French", "French", "Francais", "Franceses")
    ]

# General Expressions: Time, Column headings, Web page
Expression = [
    ("Tonight", "Ce soir", "Esta Noche"),
    ('Today', "Aujourd'hui", "Hoy"),
    ('Night', "soir", "Noche"),
    ('Monday', "Lundi", "Lunes"),
    ('Tuesday', "Mardi", "Martes"),
    ('Wednesday', "Mercredi", "Miercoles"),
    ('Thursday', "Jeudi", "Jueves"),
    ('Friday', "Vendredi", "Viernes"),
    ('Saturday', "Samedi", "Sabado"),
    ('Sunday', "Dimanche", "Domingo"),
#COMMENTED OUT 8/30/22
#     ("TONIGHT", "CE SOIR", "ESTA NOCHE"),
#     ('TODAY', "AUJOURD'HUI", "HOY"),
#     ('NIGHT', "SOIR", "NOCHE"),
#     ('MONDAY', "LUNDI", "LUNES"),
#     ('TUESDAY', "MARDI", "MARTES"),
#     ('WEDNESDAY', "MERCREDI", "MIERCOLES"),
#     ('THURSDAY', "JEUDI", "JUEVES"),
#     ('FRIDAY', "VENDREDI", "VIERNES"),
#     ('SATURDAY', "SAMEDI", "SABADO"),
#     ('SUNDAY', "DIMANCHE", "DOMINGO"),

#     ('Jan', "Jan", "Enero"),
#     ('Feb', "Fev", "Febrero"),
#     ('Mar', "Mar", "Marzo"),
#     ('Apr',"Avr","Abril"),
#     ('May',"Mai","Mayo"),
#     ('Jun',"Juin","Junio"),
#     ('Jul',"Juil","Julio"),
#     ('Aug',"Aout", "Agosto"),
#     ('Sep',"Sep","Septiembre"),
#     ('Oct',"Oct","Octubre"),
#     ('Nov',"Nov","Noviembre"),
#     ('Dec',"Dec","Diciembre"),
    ('Sky', 'Ciel', 'Cielo'),
    ('Wind (mph)', 'Vent (mph)', 'Viento (mph)'),
    ('Max Temp', 'Temp Max', 'Temp Max'),
    ('Min Temp', 'Temp Min', 'Temp Min'),
    ('Precip', 'Precip', 'Lluvias'),
    ('Wind (kt)', 'Vent (kt)', 'Viento (kt)'),
    ('Waves (ft)', 'Vagues (pd)', 'Ondas (ft)'),
    ('Swells (ft)', 'Houles (ft)', 'Swells (ft)'),
    ('LAL', 'LAL', 'LAL'),
    ('RelHum(%)', 'HumRel(%)', 'RelHum(%)'),
    ('MaxT', 'TMax', 'TMax',),
    ('MinT', 'TMin', 'TMin'),
    ('FreeWind(mph)', 'VentLibre(mph)', 'VientoLibre(mph)'),
    ('Haines', 'Haines', 'Haines'),
    ('TransWind(mph)', 'VentTrans(mph)', 'VientoTrans(mph)'),
    ('MixHgt(ft agl)', 'ElevMelang(ft agl)', 'AltuMezcl(ft agl)'),
    ('City', 'Ville', 'Ciudad'),
    ('County', 'Comte', 'Condado'),
    ('Nowcast', 'Previsions Courantes', 'Pronostico Sobre Tiempo'),
    ('Short Term Forecast', 'Previsions Court Terme',\
      'Pronostico a Corto Plazo'),
    ('Extended Forecast', 'Previsions Long Terme', 'Pronostico a Largo Plazo'),
    ('Spot Forecast', 'Previsions Spot', 'Pronostico de punto'),
    ('Outlook', 'Perspective', 'Panorama'),
    ('Marine Nowcast', 'Previsions Marines Courantes',
      'Pronostico de Tiempo Maritimo'),
    ('Coastal Marine Forecast', 'Coastal Marine Forecast',
      'Pronostico Maritimo Costero'),
    ('Terminal Aerodrome Forecast', "Previsions a l'Aerodrome",
      'Pronostico Para Terminal Aerodromo'),
    ('Latitude', 'Latitude', 'Latitud'),
    ('Longitude', 'Longitude', 'Longitud'),
    ('Area', 'Aire', 'Area'),
    ('Cities', 'Villes', 'Ciudades'),
    ('Counties', 'Comtes', 'Condados'),
    ('in the morning', 'du matin', 'por la manana'),
    ('in the afternoon', "de l'apres-midi", "por la tarde"),
    ('in the evening', 'du soir', "por la tarde"),
    ('during the night', 'pendant la nuit', 'durante la noche'),
    ('followed by', 'suivi par', 'seguido por'),
    ('overnight', 'pendant la nuit', 'durante la noche'),
    ]

class Translator:
    def __init__(self, language, parent=None):

        self._language = language
        self._langDict = LanguageTables[language]

    # Function translating a forecast
    def getForecast(self, forecast):
        lwForecast = forecast.lower()

        # Convert forecast using translation tuples
        transForecast = self._translateExpForecast(lwForecast)

        # Convert the exceptions
        exceptForecast = self._translateExceptions(transForecast)

        # Convert forecast using type and intensity tuples
        transForecast = self._translateTypeForecast(exceptForecast)

        # Clean up the translated forecast
        cleanTransForecast = self._cleanUp(transForecast)

        # Capitalize the beginning of sentences
        self.capTransForecast = self._capital(cleanTransForecast)

        #fcst = self.capTransForecast

        #fcst = self.endline(fcst, linelength=65)

        return self.capTransForecast
        #return fcst

### added to attempt to fix line wrap - 08/10/15 CNJ
    def endline(self, phrase, linelength=65, breakStr=[" ", "..."]):
        "Insert endlines into phrase"

        # Break into sub-phrases separated by \n
        subPhrases = phrase.split("\n")

        # Break each sub-phrase into lines
        str = ""
        for subPhrase in subPhrases:
            if not subPhrase:
                str += "\n"
            else:
                str += self.linebreak(subPhrase, linelength, breakStr)
        return str

    def linebreak(self, phrase, linelength, breakStr=[' ', '...'],
                  forceBreakStr=[" ", "/"]):
        # Break phrase into lines of the given linelength
        # Prevents a line break on a number.
        # If no breakStr is found for a given linelength of characters,
        # force a break on the rightmost forceBreakStr.
        text = ''
        start = 0
        end = start + linelength
        subPhrase = phrase[start:end]
        while len(subPhrase) == linelength:
            maxIndex, breakChars = self.findRightMost(subPhrase, breakStr)
            if maxIndex == -1:
                # Didn't find any breakStr; line is too long.
                # Find the rightmost force break string, if possible.
                forceIndex, breakChars = self.findRightMost(subPhrase, forceBreakStr)
                if forceIndex == 0:
                    # space in first position: will be skipped.
                    pass
                elif forceIndex > 0:
                    subPhrase = subPhrase[0:forceIndex]
                    text = '%s%s\n' % (text, subPhrase)
                    start += forceIndex
                else:
                    # no forcebreak spot, either.
                    # break at linelength.
                    text = '%s%s\n' % (text, subPhrase)
                    start += linelength
            elif maxIndex == 0:
                pass # space in first position: will be skipped
            else:
                text = '%s%s\n' % (text, subPhrase[:maxIndex])
                start += maxIndex
            if breakChars == " ":
                # Skip the space
                start +=1
            end = start + linelength
            subPhrase = phrase[start:end]
        if subPhrase:
            return '%s%s\n' % (text, subPhrase)
        else:
            # It's possible for subPhrase to be [] coming out of the while
            # loop. In that case, we just need to return text.
            return text

    def findRightMost(self, text, breakStr=[" "], nonNumeric=1):
        # Return the index of the right most break string characters
        # and the break characters that were found.
        # If nonNumeric, then make sure the index does not refer to
        # a numeric character.
        # If the break characters are a space, the index indicate
        # the character prior to the space.
        maxIndex = -1
        maxChars = ''
        for breakChars in breakStr:
            index = text.rfind(breakChars)
            done = False
            while index > 0 and not done:
                # Check for a numeric at end of line
                if nonNumeric and breakChars == " " and text[index-1].isdigit():
                    # Try to find the next right most break char
                    index = text.rfind(breakChars, 0, index-1)
                    continue
                done = True
            if index > maxIndex:
                maxIndex = index
                maxChars = breakChars
        if maxIndex == -1:
            return maxIndex, maxChars
        if maxChars == ' ':
            index = maxIndex
        else:
            # We want to keep the breakChars, which are assumed not to end
            # with a number
            index = maxIndex + len(maxChars)
        return index, maxChars
### end of section added 8/10/15 CNJ

    # Function converting appropriate letters of a string to capital letters
    def _capital(self, str):

        if not str:
            return str

        # Find all the periods
        index = []

        for i in range(0, len(str)-1):
            if str[i] == "." and str[i+1] == " ":
                index.append(i+2)
            elif str[i] == "." and str[i+1] == ".":
                index.append(i+2)

        # Always capitalize the first letter
        capitalStr = str[0].upper()

        # Capitalize the letters following the periods and a space
        for i in range(1, len(str)):
            if i in index:
                capitalStr += str[i].upper()
            else:
                capitalStr += str[i]

        return capitalStr


    # Function translating a forecast using the translation expression tuples
    def _translateExpForecast(self, lwForecast):

        for expr, transExpr in self._langDict['Expressions']:
#print(expr, transExpr)
            lwForecast = lwForecast.replace(expr, transExpr)

        return lwForecast

    # Function translating a forecast using the translation type and
    # intensity tuples
    def _translateTypeForecast(self, lwForecast):

        # translate combination of type, intensity, and coverage
        for ttuple in self._langDict['Types']:
            for ituple in self._langDict['Intensities']:
                for ctuple in self._langDict['Coverages']:
                    origEx = ctuple[0] + ' ' + ituple[0] + ' ' + ttuple[0]
                    transEx = ''
                    if ttuple[2] == 'MS':
                        transEx = ttuple[1] + ' ' + ituple[1] + ' ' + ctuple[1]
                    elif ttuple[2] == 'MP':
                        transEx = ttuple[1] + ' ' + ituple[2] + ' ' + ctuple[2]
                    elif ttuple[2] == 'FS':
                        transEx = ttuple[1] + ' ' + ituple[3] + ' ' + ctuple[3]
                    elif ttuple[2] == 'FP':
                        transEx = ttuple[1] + ' ' + ituple[4] + ' ' + ctuple[4]
                    lwForecast = lwForecast.replace(origEx, transEx)

        # translate combination of type and intensity (no coverage)
        for ttuple in self._langDict['Types']:
            for ituple in self._langDict['Intensities']:
                origEx = ituple[0] + ' ' + ttuple[0]
                transEx = ''
                if ttuple[2] == 'MS':
                    transEx = ttuple[1] + ' ' + ituple[1]
                elif ttuple[2] == 'MP':
                  transEx = ttuple[1] + ' ' + ituple[2]
                elif ttuple[2] == 'FS':
                  transEx = ttuple[1] + ' ' + ituple[3]
                elif ttuple[2] == 'FP':
                  transEx = ttuple[1] + ' ' + ituple[4]
                lwForecast = lwForecast.replace(origEx, transEx)

        # translate combination of type and coverage (no intensity)
        for ttuple in self._langDict['Types']:
            for ctuple in self._langDict['Coverages']:
                origEx = ctuple[0] + ' ' + ttuple[0]
                transEx = ''
                if ttuple[2] == 'MS':
                    transEx = ttuple[1] + ' ' + ctuple[1]
                elif ttuple[2] == 'MP':
                  transEx = ttuple[1] + ' ' + ctuple[2]
                elif ttuple[2] == 'FS':
                  transEx = ttuple[1] + ' ' + ctuple[3]
                elif ttuple[2] == 'FP':
                  transEx = ttuple[1] + ' ' + ctuple[4]
                lwForecast = lwForecast.replace(origEx, transEx)

        # translate type (no coverage and no intensity)
        for ttuple in self._langDict['Types']:
            lwForecast = lwForecast.replace(ttuple[0], ttuple[1])

        return lwForecast

    # Convert the exceptions
    def _translateExceptions(self, transForecast):
        for ttuple in self._langDict['Types']:
            for etuple in self._langDict['Exceptions']:
                origEx = ttuple[0] + ' ' + etuple[0]
                transEx = ''
                if ttuple[2] == 'MS':
                  transEx = ttuple[0] + ' ' + etuple[1]
                elif ttuple[2] == 'MP':
                  transEx = ttuple[0] + ' ' + etuple[2]
                elif ttuple[2] == 'FS':
                  transEx = ttuple[0] + ' ' + etuple[3]
                elif ttuple[2] == 'FP':
                  transEx = ttuple[0] + ' ' + etuple[4]
                transForecast = transForecast.replace(origEx, transEx)
        return transForecast

    # Function cleaning up the translated forecast
    def _cleanUp(self, lwForecast):

        for expr, transExpr in self._langDict['CleanUp']:
            lwForecast = lwForecast.replace(expr, transExpr)

        return lwForecast

    def getExpression(self, phrase):
        "Translate the phrase"

        if self._language == "english":
            return phrase
        index = Index[self._language] - 1
        for expr in Expression:
            phrase = phrase.replace(expr[0], expr[index])
        return phrase


if __name__ == '__main__':

    forecastList = [
    "High winds in the afternoon. Partly cloudy. Very heavy rain showers likely. Snow accumulation of 1 inch. Lows in the mid 30s. East winds at 75 mph. Probability of precipitation 65 percent.",
    "Mostly sunny. Widespread heavy volcanic ash. Snow accumulation of 1 to 20 inches. Highs around 120. Probability of precipitation 99 percent.",
    "High winds. Partly cloudy. Slight chance of very heavy rain showers. Snow accumulation of 1 inch. Lows in the mid 30s. East winds at 75 mph. Probability of precipitation 1 percent. Southwest winds up to 15 mph.",
    "SKY/WEATHER...Mostly cloudy with scattered rain showers and thunderstorms\nLAL...........3-4\nTEMPERATURE...Lows in the mid 30s\nHUMIDITY......70 pct\nWIND - 20 FT..Northwest to Southeast in the evening\n    VALLEYS...\n    RIDGES....\nHAINES INDEX..4 low\nSMOKE DISPERSAL:\n MIXING HEIGHT...Decreasing to 500-1,000 ft agl\n TRANSPORT WIND..Northeast to southeast 3-8 mph",
    "High winds. Decreasing cloudiness. Widely scattered light sleet. Snow accumulation of 1 to 50 inches. Low 0. Northwest winds at 90 to 100 mph becoming southwest at 80 to 90 mph. Probability of precipitation 110 percent." ]

    for forecast in forecastList:
        #transForecast = Translator('french')
        transForecast = Translator('spanish')
        #transForecast = self.endline(transForecast, linelength=65)
        print(' ')
        print('Original Forecast')
        print(forecast)
        print(' ')
        print('Translated Forecast')
        print(transForecast.getForecast(forecast))
