# python3
#
# Author: Pavlos Sermpezis
# Institute of Computer Science, Foundation for Research and Technology - Hellas (FORTH), Greece
#
# E-mail: sermpezis@ics.forth.gr
#
#
# example for catchment inference, see related paper:
# 	[1] Pavlos Sermpezis and Vasileios Kotronis. “Inferring Catchment in Internet Routing”, ACM SIGMETRICS, 2019.
#


#from bgp_simulator_anycast_coloring import *
from measurement_selection_methods import *
import json


CAIDA_DATASET = './CAIDA AS-graph/20190401.as-rel2.txt'
NB_ANYCASTERS = 2
SHORTEST_PATH = True
# list of ASes with RIPE Atlas prob
RIPE_ATLAS = [57344, 262145, 8194, 3, 4, 262149, 57350, 327687, 196616, 24586, 16395, 57356, 36866, 50628, 40975, 16, 49169, 13094, 40981, 12657, 16409, 57370, 27, 8220, 196638, 393249, 8226, 24611, 49188, 57381, 41000, 39602, 196655, 41008, 8241, 29462, 52, 202078, 12297, 8248, 199348, 41018, 8251, 24638, 57407, 41026, 262212, 39010, 327750, 49223, 41034, 24651, 57422, 12301, 204880, 31416, 88, 196697, 8283, 92, 8285, 196705, 49254, 24679, 104, 196714, 42343, 8301, 8302, 39613, 32881, 24691, 6846, 327799, 49272, 327805, 196734, 8319, 39616, 41090, 196740, 327813, 8326, 41095, 8328, 137, 8331, 327821, 8334, 41103, 20504, 8339, 24725, 8346, 9583, 156, 8218, 158, 57503, 25374, 57507, 50629, 8359, 12316, 8362, 8364, 8365, 174, 24751, 8369, 327859, 202077, 24757, 8374, 42560, 49337, 131258, 24764, 49342, 24768, 41153, 204994, 8391, 29467, 8393, 196810, 8395, 41164, 262178, 16591, 8400, 209, 8402, 196819, 41176, 217, 8412, 49375, 8416, 57571, 4134, 8422, 8426, 8427, 237, 8430, 196847, 8437, 205046, 8439, 49402, 24827, 8445, 8447, 49409, 262197, 8452, 327941, 42369, 196874, 16652, 7203, 8462, 36909, 24848, 196881, 8466, 24851, 8468, 8473, 196890, 16668, 8477, 286, 57631, 8240, 292, 8489, 57642, 24875, 8492, 24877, 49455, 393522, 8501, 49463, 33080, 24889, 196922, 33083, 8508, 24893, 24895, 49472, 8515, 8517, 57670, 24904, 33097, 8522, 2, 49485, 328014, 56304, 8529, 43747, 24916, 196949, 41302, 24921, 205147, 8540, 24634, 49505, 59, 8551, 196969, 57707, 24940, 43930, 8559, 8560, 2792, 131442, 33139, 8564, 45118, 41334, 24951, 378, 24955, 24956, 24958, 17813, 24961, 57734, 20545, 8586, 24971, 61506, 8591, 8595, 41364, 42393, 49560, 197019, 16796, 197021, 33182, 49567, 24992, 328098, 42395, 8612, 8262, 8615, 25002, 16814, 41391, 205235, 49588, 41397, 197046, 262583, 8632, 23201, 49594, 25019, 8636, 41405, 8639, 49601, 37386, 20555, 49604, 49605, 8648, 200780, 16842, 41419, 262605, 25038, 197071, 41424, 57809, 33234, 197075, 8660, 8661, 197078, 41435, 49628, 205277, 25054, 49232, 25058, 8676, 25061, 41446, 197095, 8680, 16876, 8685, 16881, 25074, 57843, 20565, 513, 25091, 8708, 25094, 49673, 57866, 197133, 25106, 197140, 8726, 41495, 5459, 198064, 546, 262691, 25124, 8741, 553, 557, 57902, 25135, 8758, 49719, 25145, 8763, 8764, 199434, 8767, 577, 8771, 25156, 9021, 8778, 8779, 41549, 41552, 33361, 41554, 33363, 8788, 41557, 197207, 31117, 41562, 25180, 8749, 25182, 28773, 197216, 197219, 49767, 25192, 57961, 49770, 57963, 393837, 8816, 41585, 8818, 49779, 8820, 8821, 8823, 49784, 49788, 41599, 41601, 25220, 39702, 8839, 49800, 25229, 49808, 42303, 25234, 49813, 199449, 58820, 58010, 8859, 49821, 131743, 25248, 41275, 8866, 33445, 679, 680, 681, 49835, 19229, 17072, 8881, 41653, 41655, 25273, 8890, 701, 58046, 49855, 8896, 705, 41668, 12406, 197318, 8903, 33480, 49866, 25291, 41676, 41678, 719, 205521, 41682, 25299, 197335, 41690, 41691, 25310, 58079, 8928, 49893, 8934, 49896, 8937, 206845, 41709, 41710, 57469, 25428, 205555, 49909, 760, 8953, 41722, 41723, 766, 41727, 262913, 35627, 41733, 25353, 45186, 41745, 786, 49941, 790, 44217, 197405, 8990, 8991, 49952, 803, 25381, 25384, 812, 197422, 9008, 205617, 25394, 205619, 33588, 41781, 49974, 327817, 41785, 49981, 25406, 8211, 9026, 135055, 262981, 9031, 25417, 197451, 9036, 46562, 9038, 199480, 852, 200846, 25431, 9050, 197467, 50661, 25441, 50020, 17253, 9063, 197480, 60220, 5607, 9070, 41841, 41843, 25460, 394102, 206313, 50042, 42038, 33660, 9085, 41854, 58239, 25472, 205697, 9092, 25478, 50056, 31400, 25486, 9103, 41872, 9105, 41876, 41878, 38220, 197529, 25500, 205726, 9119, 9121, 50083, 197540, 9125, 7753, 25512, 25513, 25515, 25518, 9135, 25521, 58291, 9143, 9145, 24582, 58299, 197564, 50113, 25538, 58308, 9158, 25543, 197580, 9166, 9167, 41937, 24739, 394197, 58328, 327844, 197595, 9182, 197602, 41955, 9188, 41957, 60241, 17385, 33771, 9198, 9199, 197227, 45224, 50163, 50166, 9208, 50170, 9211, 33788, 17408, 33796, 25607, 50188, 58381, 41998, 394255, 42000, 50195, 25620, 196782, 42009, 17435, 58396, 9245, 33823, 33824, 58405, 20657, 199516, 33835, 33837, 50222, 9268, 9269, 197686, 17465, 19429, 51319, 263228, 197696, 132162, 205891, 25668, 28854, 50247, 17480, 197708, 1101, 1103, 33873, 9299, 1109, 9304, 1113, 50266, 17501, 9310, 1120, 197729, 17506, 1124, 33894, 17511, 58473, 197738, 58475, 42093, 17518, 1136, 9329, 205938, 17523, 1140, 42102, 132215, 33915, 9340, 50304, 33924, 26134, 9351, 42120, 205961, 50316, 58511, 17552, 50324, 132245, 9367, 132255, 9378, 42148, 60273, 50345, 132268, 42160, 24776, 11123, 1205, 206006, 197815, 33980, 1213, 33983, 33984, 12491, 33988, 1221, 33991, 42184, 42189, 60280, 1237, 17622, 9431, 50392, 1241, 8399, 1246, 1249, 34019, 49964, 1257, 17645, 206062, 1133, 206066, 1267, 9464, 1273, 197882, 42235, 58620, 1280, 197889, 197892, 58629, 17670, 197895, 34056, 1289, 17676, 50446, 50448, 50449, 54054, 50457, 9498, 1307, 9500, 9318, 9503, 34080, 34081, 9506, 50467, 43910, 17705, 206122, 34093, 39816, 206130, 17721, 42298, 31960, 9534, 8228, 224, 17732, 42310, 34119, 42313, 9546, 34123, 197965, 45345, 42322, 17747, 197975, 42334, 206013, 206177, 50530, 24806, 50535, 34154, 197996, 50543, 42355, 198004, 50550, 203815, 1403, 50558, 60309, 34177, 9605, 198024, 28908, 47784, 206221, 9617, 42387, 50581, 50583, 50585, 239, 9733, 60314, 17823, 42401, 50595, 17828, 50597, 43966, 42409, 198060, 65516, 39837, 34224, 34225, 20723, 198068, 203817, 206268, 42431, 34244, 34245, 34248, 198089, 42442, 34251, 52130, 206288, 43939, 28000, 42455, 59789, 43940, 42459, 250, 394719, 35239, 34279, 42473, 206314, 48039, 26094, 49405, 34288, 50673, 17907, 18004, 42490, 50685, 206339, 58885, 28929, 17931, 17934, 198161, 37150, 42518, 198167, 34968, 198171, 17948, 42525, 8781, 132079, 34347, 42541, 263728, 134067, 42548, 42549, 17974, 26167, 132664, 9785, 42557, 9790, 198208, 6830, 34372, 34373, 49420, 42571, 17996, 9808, 263762, 42579, 50772, 41230, 34393, 263771, 9821, 50783, 9824, 26210, 42596, 9829, 198247, 198249, 34410, 37153, 42610, 20755, 1653, 34409, 50810, 22122, 200981, 50825, 34442, 394893, 42337, 9872, 42642, 34456, 42652, 41242, 34471, 9897, 50858, 42668, 1712, 42673, 42676, 198325, 18103, 50873, 42682, 42685, 198335, 198336, 42689, 1734, 4385, 18121, 9930, 42615, 1741, 18126, 42707, 206548, 206549, 34156, 34524, 206557, 1759, 59105, 198370, 1764, 34533, 18150, 50919, 394989, 50926, 20776, 34549, 59128, 206594, 9988, 1797, 34568, 34569, 50956, 50957, 206610, 10003, 198420, 18199, 18200, 26793, 10010, 34587, 10013, 18209, 18210, 198435, 57365, 43996, 34602, 1835, 1836, 198651, 34606, 42800, 196687, 198452, 198455, 1850, 134111, 51004, 1853, 34622, 34624, 31712, 42819, 132933, 198471, 51018, 57656, 26451, 133453, 61984, 1880, 42841, 51038, 1887, 1680, 34659, 34660, 12611, 10091, 51052, 1901, 10094, 42863, 198512, 51057, 10098, 1909, 39617, 1916, 206718, 34687, 34688, 51074, 34695, 198537, 1930, 51083, 51088, 34705, 51090, 10131, 51093, 1942, 13977, 49711, 48111, 30362, 42910, 10143, 198561, 1955, 8518, 198570, 1967, 26546, 34743, 51130, 133051, 51132, 34749, 200561, 20811, 34758, 34760, 42953, 34762, 34764, 42961, 133075, 198612, 10197, 60409, 42968, 42970, 34779, 51164, 34781, 51167, 10208, 2018, 18403, 51172, 42981, 34790, 22927, 51184, 26610, 18419, 18420, 44030, 26615, 16724, 27647, 198653, 34814, 12629, 198657, 10242, 26627, 133124, 51207, 198668, 51214, 198672, 18451, 59414, 196745, 51225, 395291, 50864, 206886, 59432, 57692, 34863, 18480, 59441, 59444, 43061, 56329, 43065, 2107, 2108, 2109, 2110, 51263, 51265, 198722, 2116, 198725, 198726, 2119, 43081, 198731, 59469, 10318, 59472, 8547, 18516, 43097, 18106, 34911, 26721, 198754, 34916, 59494, 51309, 43118, 42077, 59507, 34934, 43127, 198781, 27669, 59521, 49515, 34948, 43142, 34497, 395400, 10381, 34960, 51349, 2200, 34970, 34971, 201072, 198818, 43171, 207013, 8677, 20849, 34984, 59561, 18119, 8562, 51375, 12508, 26803, 133301, 43192, 35003, 207036, 43197, 35006, 20853, 51395, 43205, 198854, 51401, 51402, 207051, 133324, 51405, 200836, 198864, 2259, 198869, 133334, 51417, 201709, 207071, 59617, 43234, 57723, 35046, 18663, 10474, 59627, 10481, 198901, 35063, 34516, 35067, 43260, 198357, 35076, 59659, 51468, 59665, 198930, 35094, 43289, 51483, 59676, 207134, 395559, 59689, 395570, 26932, 35125, 59702, 198967, 43320, 43321, 35130, 198971, 20810, 43326, 198977, 20875, 35140, 35141, 395592, 198985, 10570, 43341, 59729, 48089, 35158, 59737, 18779, 51551, 29072, 35171, 43366, 59752, 51561, 19517, 60478, 43382, 43384, 18809, 133498, 10620, 52455, 16175, 59780, 18822, 43402, 12902, 43406, 59791, 43408, 59793, 43413, 207254, 12697, 35226, 35227, 37453, 133536, 35236, 2470, 198385, 199081, 35244, 43437, 24989, 43442, 59827, 2485, 3356, 35258, 43451, 199101, 199103, 264640, 2497, 35266, 35267, 2500, 35271, 133579, 2510, 51664, 2514, 201123, 2516, 51669, 2518, 2519, 199128, 51675, 2527, 2529, 199139, 395748, 43494, 43495, 51690, 199150, 35314, 2547, 2549, 199159, 35320, 10745, 35323, 35328, 51718, 29100, 43531, 199181, 59919, 51728, 35348, 17, 12361, 35352, 2586, 49583, 2588, 133661, 20912, 43554, 43557, 35366, 35368, 35369, 2602, 2603, 10796, 43566, 2607, 2609, 35378, 2611, 2613, 2614, 51773, 43583, 35393, 59970, 199236, 51782, 51784, 35401, 51786, 12727, 199246, 27747, 10838, 199256, 43611, 43612, 4538, 51806, 43700, 264806, 51815, 35432, 49596, 198418, 60015, 199283, 35444, 133749, 60022, 133752, 199289, 199291, 34187, 2686, 35456, 10881, 199298, 60036, 43656, 198423, 43660, 199309, 60049, 43667, 43668, 51862, 199319, 51865, 2818, 27759, 199324, 27294, 51871, 35489, 29551, 19108, 133797, 133802, 199339, 50973, 35505, 51892, 51896, 43709, 35518, 60095, 199361, 51906, 43720, 35530, 34594, 51918, 60111, 35539, 35540, 43733, 206186, 19165, 51935, 19171, 27364, 43751, 51944, 43754, 35566, 35567, 10993, 35573, 35574, 197076, 60156, 60157, 199422, 35584, 60162, 60163, 57814, 11014, 35593, 51978, 206637, 35600, 199441, 51989, 43801, 60187, 35612, 35613, 35615, 2848, 197083, 2852, 2854, 2856, 2857, 11051, 2860, 43824, 43826, 8670, 19255, 35640, 34612, 199484, 52030, 11071, 396097, 28738, 199493, 133959, 43848, 3212, 8674, 52048, 35665, 43859, 2907, 60252, 52063, 60256, 27792, 2914, 199524, 43880, 35559, 52080, 49640, 35699, 60277, 52088, 199547, 52092, 52094, 60288, 43905, 48926, 60294, 60295, 199562, 56837, 60304, 199571, 43925, 35734, 199578, 60316, 396190, 60319, 11170, 60323, 199588, 134053, 43942, 393713, 15516, 35754, 4657, 35761, 199603, 43956, 395089, 60351, 35776, 7738, 42927, 60362, 52173, 199631, 43984, 52177, 37199, 29834, 35804, 35805, 60382, 35807, 11232, 199652, 199846, 35815, 35816, 23719, 199662, 199664, 35826, 131583, 35832, 35833, 197119, 11260, 60414, 60415, 44034, 35843, 52228, 52233, 44045, 199853, 27665, 44050, 27668, 44053, 11290, 27678, 199712, 44066, 44068, 43203, 6758, 205479, 27699, 44084, 11318, 27828, 3130, 52285, 19518, 199743, 44096, 44097, 16333, 199748, 134220, 27725, 12813, 60497, 27733, 11351, 52314, 44124, 52323, 201419, 43478, 41023, 27754, 27755, 44141, 44143, 60531, 52344, 27771, 44156, 199805, 44158, 27775, 44160, 199811, 3208, 3209, 52362, 52286, 11404, 3213, 52366, 3215, 3216, 35985, 3221, 44185, 3226, 60574, 19653, 3233, 11426, 11427, 7366, 3238, 3242, 3243, 3244, 3245, 3246, 44208, 3249, 3927, 49613, 199860, 134325, 3255, 3257, 3274, 59253, 3265, 27843, 3268, 3269, 49697, 44234, 1200, 3277, 19662, 52431, 52432, 44244, 11478, 396503, 41508, 27866, 3292, 22394, 44257, 11492, 3301, 205515, 3303, 27882, 27883, 3308, 27887, 3314, 3320, 3323, 29571, 29226, 3326, 3327, 3329, 3330, 3331, 3333, 28753, 3335, 111, 134413, 25133, 48344, 44306, 3352, 27929, 559, 199964, 11550, 3359, 61215, 60706, 199971, 11556, 3367, 60713, 27947, 60721, 36149, 199993, 200001, 49718, 44365, 27983, 200023, 60764, 200031, 44384, 44385, 29243, 200037, 49724, 44395, 10130, 28017, 200050, 28024, 3449, 3450, 25151, 48362, 15735, 44417, 60651, 60804, 3462, 44424, 60810, 200077, 44431, 11664, 42905, 21060, 3491, 28073, 62023, 60846, 200114, 49763, 60852, 201290, 38158, 19905, 28099, 28104, 44489, 44491, 60876, 200142, 60879, 60664, 52694, 44507, 3549, 200161, 28130, 200163, 33362, 200174, 28146, 30633, 265721, 60924, 36351, 11776, 60932, 44549, 199937, 60940, 3597, 44558, 3599, 3605, 44567, 60955, 44574, 20001, 11814, 11815, 134697, 205406, 11830, 60983, 134715, 28220, 49452, 11845, 36423, 61006, 25187, 7438, 37668, 20057, 44634, 27919, 44637, 44641, 61029, 265830, 59324, 29287, 11888, 48403, 61044, 198709, 36483, 15945, 8208, 44684, 20115, 3737, 3741, 61094, 28329, 28330, 61102, 8819, 61111, 44735, 44746, 44750, 41589, 61138, 7459, 50591, 37497, 206350, 61156, 61157, 44776, 44327, 20207, 198611, 44788, 61174, 34772, 8311, 61189, 61194, 3851, 3855, 12628, 42252, 61211, 29317, 12066, 200490, 42973, 262792, 36955, 12083, 37513, 7477, 15133, 44869, 200519, 20299, 34786, 36692, 200533, 15673, 61272, 34788, 200539, 266082, 135014, 61287, 200555, 12143, 61296, 12145, 44914, 200567, 36731, 135036, 20355, 28548, 201367, 61327, 12177, 44946, 4761, 28573, 204101, 38896, 61349, 37532, 44973, 53166, 34803, 4771, 23881, 198644, 12222, 135106, 62113, 51191, 45005, 197029, 60749, 21155, 37649, 45014, 61399, 61400, 135132, 131749, 45025, 200675, 45031, 25255, 45037, 135150, 12271, 197288, 12276, 12969, 20473, 135162, 61438, 45055, 12290, 36867, 36868, 20485, 20488, 28681, 36874, 28683, 28685, 12302, 12303, 48472, 43782, 12307, 12310, 12312, 264196, 36890, 20507, 61468, 12319, 200736, 12322, 12324, 36902, 36903, 20523, 28716, 12333, 40285, 12337, 36914, 21171, 28725, 4150, 12346, 12348, 12350, 197301, 12353, 200770, 12355, 12357, 28742, 24689, 12360, 36937, 45131, 28748, 200781, 196815, 20559, 20561, 36947, 4181, 12374, 28760, 20569, 15663, 53339, 135260, 12381, 28768, 12389, 12390, 12392, 12395, 45164, 20590, 8893, 12400, 28788, 702, 36982, 28792, 22548, 12991, 12414, 44604, 45184, 20609, 12418, 200043, 36996, 36997, 12423, 37002, 200844, 20621, 12430, 60781, 20625, 20626, 45204, 20631, 20634, 200862, 28831, 135328, 20647, 28840, 37037, 4270, 20655, 28849, 28851, 12470, 29385, 28857, 28859, 37054, 12479, 12480, 49867, 20676, 37061, 12486, 13004, 28875, 28876, 20686, 45773, 12496, 37074, 45267, 28885, 28886, 28889, 28890, 28891, 37084, 12513, 37090, 22512, 12519, 20712, 28905, 28907, 37100, 28909, 205523, 28917, 135600, 37693, 200953, 12539, 51155, 12543, 12545, 37123, 200964, 20741, 37126, 12552, 56611, 20746, 12556, 20750, 48155, 200979, 12565, 135448, 12570, 12571, 20764, 45786, 20766, 12576, 20769, 12578, 21211, 20773, 25242, 28968, 135465, 12586, 45355, 28972, 20783, 12594, 201011, 37172, 12597, 201014, 20794, 41695, 12605, 20798, 37183, 41696, 37187, 45382, 12617, 12618, 29003, 12620, 37197, 29007, 29009, 4434, 62179, 37204, 20821, 29014, 53591, 12637, 21221, 10299, 29032, 6849, 53610, 20845, 30781, 20848, 41704, 20852, 18494, 12662, 4474, 59455, 20860, 45437, 29056, 12676, 201094, 198721, 4844, 29066, 29067, 12684, 12687, 20880, 45458, 29076, 21230, 20889, 4508, 8879, 133189, 37281, 45475, 20900, 12709, 37286, 20904, 12714, 37292, 20910, 4528, 59890, 20915, 45494, 135607, 29114, 12731, 20926, 29119, 201155, 29124, 12741, 45510, 201163, 29134, 201169, 12754, 28067, 29140, 12757, 20955, 20956, 12767, 2128, 37346, 12772, 20965, 12775, 12778, 12779, 4589, 199284, 29170, 202012, 12793, 20986, 201213, 4608, 20612, 61958, 4616, 29194, 15975, 12812, 21250, 45582, 12816, 29208, 45595, 21021, 37406, 45600, 12833, 12835, 4647, 21032, 21034, 12843, 37422, 12847, 12849, 62007, 7604, 50168, 12859, 29244, 45629, 29247, 53824, 201283, 29252, 12871, 62024, 12874, 12876, 4685, 12880, 37457, 45650, 12883, 200924, 21079, 62040, 12579, 37468, 29278, 4704, 12897, 37474, 29286, 45671, 4713, 12906, 62059, 12912, 26617, 37492, 201333, 25509, 37495, 29305, 62078, 25365, 12929, 29314, 4739, 8982, 21127, 29321, 21131, 37517, 62094, 37519, 37520, 62099, 37524, 201366, 25369, 4760, 62105, 4764, 45725, 4766, 37537, 35731, 12963, 4773, 37542, 4775, 21161, 21162, 29355, 62125, 4787, 4788, 21173, 21175, 37560, 201402, 4796, 62141, 12990, 21183, 12993, 4802, 4804, 12998, 13000, 4809, 37578, 21195, 4812, 13005, 201422, 13009, 201201, 29396, 28110, 62167, 201508, 4826, 11727, 29404, 8997, 21217, 13026, 21219, 4837, 13030, 37608, 22652, 37611, 13036, 201453, 29422, 21232, 13041, 37618, 21235, 13045, 13046, 41079, 21246, 47232, 29442, 37640, 62217, 45838, 21263, 267024, 62225, 201494, 21274, 201499, 37663, 201505, 21282, 200155, 13092, 37670, 9009, 13097, 62250, 62251, 29484, 13101, 37680, 50901, 21299, 37684, 13110, 29492, 4922, 62267, 21309, 13121, 62275, 13124, 13127, 29512, 37705, 62282, 41783, 37708, 29518, 328049, 197659, 45906, 136019, 201557, 21334, 29527, 136028, 54115, 13156, 45926, 21351, 35549, 45935, 201587, 201588, 21365, 45942, 31263, 29562, 8271, 201603, 13188, 13189, 13193, 13194, 29580, 21390, 62352, 62353, 29587, 21396, 62276, 17625, 62365, 29599, 29600, 21412, 29605, 54182, 201641, 8351, 62383, 13237, 21430, 45177, 29624, 13246, 29632, 13249, 16073, 197745, 21446, 26785, 21453, 62416, 29649, 62418, 201686, 29655, 13272, 29084, 21472, 5089, 21476, 201701, 29670, 13287, 62290, 29680, 28812, 62455, 21497, 13306, 29691, 21500, 21502, 29695, 48453, 13319, 21513, 855, 4808, 15874, 13331, 52000, 9051, 13354, 201773, 39642, 21556, 21570, 50017, 52748, 201806, 35000, 29540, 201822, 62310, 38001, 54390, 41833, 38009, 35007, 201852, 9067, 201860, 21637, 38026, 36375, 201868, 59587, 25454, 13167, 201887, 13476, 201898, 38064, 13489, 25459, 197495, 41913, 13178, 13238, 46309, 201958, 25468, 29933, 51411, 41096, 5377, 5378, 5379, 5384, 5385, 5387, 5390, 5391, 5394, 21379, 5396, 5397, 5400, 38170, 5404, 62341, 5408, 5409, 5410, 5413, 46375, 5416, 5419, 5421, 202032, 38195, 5430, 21385, 5432, 202042, 5435, 21826, 42699, 8092, 30028, 51426, 46416, 38227, 30036, 38229, 203687, 13657, 5466, 5467, 5468, 15930, 5470, 59622, 5479, 13672, 202089, 5483, 202094, 5488, 5491, 46454, 5503, 5505, 49284, 5518, 13728, 5538, 5539, 9116, 38315, 136620, 202164, 53923, 5547, 5563, 21949, 5567, 58273, 5578, 13771, 5580, 202194, 5588, 21413, 136672, 5602, 5603, 202214, 202215, 5610, 5617, 202228, 12735, 202236, 9735, 62380, 5645, 198228, 46609, 5650, 55555, 5661, 22047, 38442, 29104, 54841, 5692, 25376, 6412, 54858, 41911, 5713, 54869, 5719, 30298, 46685, 55569, 25532, 5738, 5739, 30325, 51430, 63112, 5769, 18196, 25540, 5786, 8376, 38565, 38566, 35100, 22192, 22200, 38592, 22211, 30404, 30407, 17356, 24183, 14043, 202463, 14051, 38629, 38635, 14061, 14080, 38657, 63242, 136972, 206420, 25560, 22300, 21466, 47408, 200915, 14117, 46887, 202540, 4128, 207156, 55101, 38719, 22342, 21473, 26935, 33762, 22355, 38740, 63318, 17380, 13285, 47420, 202605, 31037, 44691, 38778, 202625, 202632, 38794, 38796, 49847, 30607, 38800, 8657, 59715, 30619, 59395, 202657, 29555, 6057, 6058, 30640, 43847, 6067, 137144, 22458, 327814, 6079, 49534, 13303, 2381, 197624, 14291, 31054, 46073, 202716, 38880, 30689, 38883, 25596, 6124, 6128, 59125, 63479, 21503, 30722, 6147, 43350, 47116, 30737, 30740, 30741, 30742, 30746, 22561, 38949, 38952, 37577, 30764, 57763, 30766, 47165, 48821, 30784, 47169, 30786, 30793, 38987, 30798, 30813, 55391, 55392, 33808, 14434, 39020, 47215, 47217, 42003, 30836, 39029, 133481, 202872, 47227, 30844, 55423, 30848, 30851, 47236, 47237, 55430, 49037, 202895, 55441, 202898, 34580, 39063, 12426, 22684, 39069, 30880, 39074, 33819, 30886, 47271, 30889, 29125, 6315, 30892, 39087, 52039, 39093, 6327, 14522, 197317, 202940, 39102, 47297, 39107, 22727, 47304, 30923, 30925, 39120, 47313, 39122, 22742, 6360, 39138, 6373, 51580, 44451, 39150, 39151, 55536, 39153, 30962, 22773, 47350, 48768, 30971, 30972, 41887, 6400, 39169, 17451, 30982, 6407, 55561, 39179, 30988, 39184, 47377, 14615, 14618, 63771, 63774, 203043, 31012, 39205, 31017, 133232, 31019, 47407, 39216, 31027, 31034, 16095, 31036, 6461, 31042, 197437, 47438, 31055, 39250, 47447, 39257, 47451, 39260, 44134, 203102, 39263, 39264, 13037, 31076, 31078, 6503, 39273, 6510, 55666, 31103, 47490, 55685, 39302, 6535, 63882, 31115, 196621, 39309, 39310, 197985, 31122, 31124, 39318, 58436, 31133, 39326, 132165, 14754, 47524, 47526, 47527, 6568, 132167, 31148, 50473, 39351, 47544, 47548, 31167, 31169, 11131, 31138, 39375, 203228, 14813, 23007, 39392, 48503, 39396, 55785, 59815, 39405, 31214, 1312, 31221, 14840, 23033, 47610, 6661, 47623, 31240, 31241, 31242, 39435, 31246, 31250, 14868, 6677, 58457, 39449, 31259, 55836, 47645, 7941, 203296, 39458, 31270, 31272, 6697, 55850, 6701, 33885, 55863, 6713, 14907, 47678, 47680, 203329, 47682, 47683, 6724, 2486, 6730, 6734, 6736, 39505, 47698, 6739, 55895, 31323, 64095, 6752, 6753, 39522, 14949, 31334, 7590, 31337, 23148, 29413, 31349, 39542, 39544, 35263, 31357, 39555, 6789, 18881, 39560, 31370, 47755, 14988, 6799, 23184, 6802, 203412, 6805, 39578, 12502, 50288, 31394, 6821, 6823, 203432, 6829, 15022, 47794, 39603, 39605, 39608, 39611, 203453, 15038, 6848, 203457, 197750, 47814, 6855, 23242, 6866, 6867, 39636, 39637, 6871, 47834, 6876, 56030, 39647, 6881, 6882, 39651, 31461, 6886, 56040, 50300, 6893, 56046, 15088, 6898, 31477, 56055, 6905, 6908, 59861, 33920, 15108, 31493, 39686, 47889, 39699, 31510, 39704, 56089, 31514, 6939, 39709, 39713, 56099, 47913, 47914, 6621, 31543, 39737, 64314, 47583, 31549, 31200, 31554, 23366, 203593, 39756, 39759, 39761, 42514, 47956, 50620, 203615, 203618, 47973, 203623, 31592, 48956, 7018, 39790, 31604, 7029, 7034, 23419, 39857, 201877, 39811, 61421, 39815, 56200, 34878, 64396, 31633, 203670, 7065, 31642, 64413, 39839, 20694, 31655, 31658, 15275, 64429, 56241, 39863, 15290, 64444, 39869, 31679, 7106, 39875, 15301, 39878, 48072, 31692, 31693, 39886, 50348, 7122, 31705, 31708, 64478, 39904, 39906, 23523, 203752, 31721, 56300, 31725, 31727, 48112, 39923, 39925, 39927, 31736, 39931, 27833, 43520, 15366, 15368, 48137, 15370, 48139, 15372, 13032, 15377, 50894, 56339, 203797, 8613, 48152, 48154, 56347, 15389, 48159, 48161, 61275, 56357, 48166, 15399, 15401, 51523, 48173, 15415, 56377, 15426, 6667, 48200, 15435, 7247, 15440, 56402, 56403, 204010, 15450, 15451, 40029, 15456, 48230, 23655, 3943, 56430, 15471, 56433, 15474, 45797, 15480, 203898, 48252, 43541, 15488, 56449, 200738, 15493, 7303, 56456, 15497, 15502, 15510, 31257, 56472, 48284, 15517, 56478, 48288, 48293, 48294, 15527, 203944, 48299, 15533, 15535, 203953, 15542, 15544, 15547, 8053, 203969, 56515, 15557, 58075, 35361, 23752, 50710, 61303, 23756, 7377, 39912, 24796, 56534, 15576, 203993, 15582, 23780, 15589, 56550, 23783, 31976, 15594, 15595, 15598, 15600, 15605, 56566, 43561, 7418, 48379, 51754, 15614, 40191, 35371, 15623, 15626, 56588, 15630, 56595, 204052, 204053, 9433, 6703, 48417, 58587, 15657, 15659, 23855, 43571, 23860, 15669, 48438, 48441, 56635, 204092, 48446, 18997, 56641, 15683, 15685, 56647, 15689, 31287, 48460, 15695, 56656, 23889, 7506, 9443, 198290, 7511, 15704, 262394, 7514, 44943, 204125, 204126, 48481, 32098, 15716, 56679, 2495, 15725, 203201, 15734, 204151, 4851, 7545, 59967, 15743, 6720, 15747, 23944, 15754, 23947, 48526, 23951, 7570, 15763, 7575, 56728, 15772, 15774, 23969, 56740, 15782, 49052, 7594, 19016, 7602, 15796, 15798, 15802, 15808, 15815, 15817, 204234, 34421, 56783, 24016, 15826, 29169, 15830, 56791, 7642, 15835, 15836, 15844, 41135, 47697, 264787, 32244, 204279, 48265, 15870, 7679, 48642, 59990, 15879, 48648, 7690, 39511, 201986, 48659, 44974, 15895, 24088, 48670, 7712, 7713, 48679, 48683, 48685, 7727, 40497, 15924, 24122, 15934, 15935, 15941, 15943, 48712, 32329, 56910, 56911, 40528, 15955, 21774, 15962, 21775, 15964, 15965, 15969, 32354, 56933, 7782, 24167, 10352, 32363, 32365, 15982, 24176, 15987, 48756, 15991, 204408, 24192, 16004, 56969, 44994, 328145, 16019, 24213, 16030, 48803, 48804, 24233, 29449, 198847, 42695, 32437, 32440, 51828, 25887, 32448, 24257, 16066, 131755, 57033, 197922, 48846, 48847, 48848, 16082, 16086, 24282, 48863, 16097, 57069, 7922, 45011, 204585, 24309, 57079, 57084, 16125, 60032, 24323, 48901, 35457, 16141, 48917, 48918, 16154, 57118, 57119, 16160, 16347, 42289, 12252, 48943, 48945, 16178, 57142, 7992, 16185, 48954, 16188, 16191, 57154, 48964, 16200, 16202, 48971, 48972, 24398, 24399, 202040, 40788, 16218, 39567, 34106, 57187, 8036, 34108, 16234, 8047, 8048, 49009, 49010, 16243, 16245, 16246, 47764, 8059, 57214, 49024, 57218, 57219, 49029, 8728, 16364, 57227, 49036, 32653, 57231, 16276, 16281, 32666, 42005, 8094, 24482, 49059, 8100, 57254, 49063, 16296, 2716, 16298, 50503, 16300, 16302, 49071, 50505, 43679, 16316, 58698, 57279, 49088, 16322, 43317, 51873, 24521, 24523, 49100, 57293, 50463, 16342, 8151, 35733, 16345, 49115, 45050, 49120, 16353, 49125, 24550, 8167, 196948, 39007, 32748, 24560, 57329, 204786, 197971, 49140, 204796, 8190, 24823]
sample_size_RIPE_ATLAS = 1000
NB_RANDOM_SAMPLES = 5
random_budget = 10
budget = 10

print('Loading topology...')
Topo = BGPtopology()
Topo.load_topology_from_csv(CAIDA_DATASET)
list_of_ASNs = Topo.get_all_nodes_ASNs()
anycasters = random.sample(list_of_ASNs, NB_ANYCASTERS)
	

prefix = 0
for AS in anycasters:
	Topo.add_prefix(AS, prefix)


print('Creating Rgraph...')
G = create_Rgraph_from_Topo(Topo, prefix, shortest_path_preference=SHORTEST_PATH)
print(G.get_nb_of_nodes())
print('--- removing leaves ---')
G.remove_all_leaves()
print(G.get_nb_of_nodes())

print('Probabilistic coloring...')
G.set_probabilistic_coloring(anycasters)

initial_color = copy.deepcopy(G.colors)#G.colors.copy()


print('Start measurements...')
nodes_with_color = G.get_list_of_nodes(with_color=True)
nodes_with_certain_color = G.get_list_of_nodes(with_certain_color=True)

nodes_to_measure = set(nodes_with_color)-set(nodes_with_certain_color)
print('Nodes to measure: {}'.format(len(nodes_to_measure)))
print('Nb of RIPE Atlas probes {}'.format(len(RIPE_ATLAS)))
nodes_to_measure = nodes_to_measure.intersection(set(RIPE_ATLAS))
if len(nodes_to_measure) > sample_size_RIPE_ATLAS:
	nodes_to_measure = random.sample(copy.deepcopy(nodes_to_measure),sample_size_RIPE_ATLAS)
print('Nodes to measure: {}'.format(len(nodes_to_measure)))
time.sleep(3)

RND_nodes = []
RND_eff = []
for i in range(NB_RANDOM_SAMPLES):
	# select randomly measurements:
	(nodes, eff) = random_measurements(G, list(nodes_to_measure), random_budget, lazy_probabilities_threshold=0, lazy_state_space_sampling=20)
	RND_nodes.append( nodes )
	RND_eff.append( eff )
	G.colors = copy.deepcopy(initial_color)
# select greedily measurements (i.e., Algorithm 6 from [1]):
(GRD_nodes, GRD_eff) = greedy_measurements(G, list(nodes_to_measure), budget, lazy_evaluations=True, lazy_state_space_sampling=20)
G.colors = copy.deepcopy(initial_color)


# Print the data
DATA = {'nb_nodes_w_color': len(nodes_with_color), 'RND_nodes': RND_nodes, 'RND_eff': RND_eff, 'GRD_nodes': GRD_nodes, 'GRD_eff': GRD_eff}
print(DATA)