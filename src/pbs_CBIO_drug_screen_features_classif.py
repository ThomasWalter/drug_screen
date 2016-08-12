
# to start this script:
# cd /g/software/linux/pack/cellcognition-1.2.4/SRC/cecog_git/pysrc/scripts/EMBL/cluster
# for example:
# python-2.7 pbs_script_generation.py -b <settings_filename>
# python-2.7 pbs_script_generation.py -b ../settings_files/chromosome_condensation/pbs_chromosome_condensation_settings.py
# python-2.7 pbs_script_generation.py -b ../settings_files/lamin/pbs_laminb_settings.py


path_command = """setenv PATH /cbio/donnees/nvaroquaux/.local/bin:${PATH}
setenv LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/cbio/donnees/nvaroquaux/.local/lib
setenv LIBRARY_PATH /cbio/donnees/nvaroquaux/.local/lib
setenv PYTHONPATH /cbio/donnees/aschoenauer/software/lib/python2.7/site-packages
setenv DRMAA_LIBRARY_PATH /opt/gridengine/lib/lx26-amd64/libdrmaa.so
"""

# data directories
baseInDir = '/share/data40T/aschoenauer/drug_screen/data'
baseOutDir = '/share/data40T/aschoenauer/drug_screen/results'

# settings for scripts
baseScriptDir = '/cbio/donnees/aschoenauer/data/drug_screen/scripts'
scriptPrefix = 'DS_features_classif'

# settingsfile
settingsFilename = '/cbio/donnees/aschoenauer/projects/drug_screen/settings/drug_screen_features_classif.conf'

# plates=None means that all plates found in baseInDir are going to be processed.
# plates = None NON!!

#A CHANGER
plates = None

#['LT0104_04--ex2006_07_07--sp2005_08_16--tt17--c4',
# 'LT0104_14--ex2006_11_22--sp2005_08_16--tt19--c4',
# 'LT0104_20--ex2007_10_24--sp2005_08_16--tt17--c4',
# 'LT0104_31--ex2005_08_26--sp2005_08_16--tt18--c5',
# 'LT0105_04--ex2006_02_03--sp2005_08_22--tt17--c3',
# 'LT0105_07--ex2006_03_17--sp2005_08_22-tt17--c3',
# 'LT0105_20--ex2006_07_05--sp2005_08_22--tt17--c4',
# 'LT0105_27--ex2005_09_16--sp2005_08_22--tt17--c5',
# 'LT0106_02--ex2005_12_07--sp2005_08_22--tt17--c3',
# 'LT0106_06--ex2006_12_13--sp2005_08_22--tt18--c4',
# 'LT0106_10--ex2005_09_16--sp2005_08_22--tt17--c4',
# 'LT0106_43--ex2005_09_07--sp2005_08_22--tt17--c5',
# 'LT0107_02--ex2005_12_14--sp2005_08_23--tt163--c5',
# 'LT0107_17--ex2005_09_16--sp2005_08_23--tt17--c5',
# 'LT0107_18--ex2005_09_21--sp2005_08_23--tt17--c5',
# 'LT0108_01--ex2006_03_15--sp2005_08_23--tt17--c5',
# 'LT0108_02--ex2006_12_13--sp2005_08_23--tt18--c4',
# 'LT0108_25--ex2005_09_16--sp2005_08_23--tt17--c4',
# 'LT0108_47--ex2005_09_07--sp2005_08_23--tt17--c5',
# 'LT0109_13--ex2006_07_07--sp2005_08_24--tt17--c5',
# 'LT0109_38--ex2005_09_21--sp2005_08_24--tt17--c5',
# 'LT0109_45--ex2005_09_14--sp2005_08_24--tt173--c4',
# 'LT0110_01--ex2006_03_15--sp2005_08_25--tt17--c3',
# 'LT0110_07--ex2005_09_07--sp2005_08_25--tt17--c5',
# 'LT0110_09--ex2005_09_09--sp2005_08_25--tt17--c5',
# 'LT0111_08--ex2007_10_24--sp2005_08_25--tt17--c4',
# 'LT0111_27--ex2005_10_05--sp2005_08_25--tt193--c4',
# 'LT0111_44--ex2005_09_09--sp2005_08_25--tt17--c5',
# 'LT0112_01--ex2006_03_15--sp2005_09_12--tt17--c3',
# 'LT0112_35--ex2005_09_28--sp2005_09_12--tt17--c3',
# 'LT0112_36--ex2005_09_23--sp2005_09_12--tt163--c4',
# 'LT0113_01--ex2006_03_17--sp2005_08_29--tt17--c3',
# 'LT0113_15--ex2005_09_07--sp2005_08_29--tt17--c5',
# 'LT0113_18--ex2005_09_09--sp2005_08_29--tt17--c5',
# 'LT0114_31--ex2005_10_07--sp2005_08_30-tt17--c5',
# 'LT0114_34--ex2005_09_14--sp2005_08_30--tt173--c4',
# 'LT0114_59--ex2006_11_17--sp2006_11_06--tt17--c4',
# 'LT0114_62--ex2006_11_17--sp2006_11_06--tt17--c5',
# 'LT0115_01--ex2006_03_17--sp2005_08_30--tt17--c3',
# 'LT0115_21--ex2005_09_14--sp2005_08_30--tt17--c5',
# 'LT0115_23--ex2005_09_21--sp2005_08_30--tt17--c4',
# 'LT0116_01--ex2006_03_17--sp2005_09_01--tt17--c5',
# 'LT0116_43--ex2005_09_09--sp2005_09_01--tt17--c5',
# 'LT0116_47--ex2005_09_16--sp2005_09_01--tt17--c5',
# 'LT0117_05--ex2006_02_01--sp2005_09_01--tt17--c3',
# 'LT0117_06--ex2006_02_03--sp2005_09_01--tt17--c3',
# 'LT0117_15--ex2005_09_21--sp2005_09_01--tt17--c5',
# 'LT0117_18--ex2005_09_28--sp2005_09_01--tt17--c5',
# 'LT0118_01--ex2006_01_18--sp2005_09_05--tt17--c3',
# 'LT0118_23--ex2005_09_14--sp2005_09_05--tt17--c5',
# 'LT0118_26--ex2005_09_28--sp2005_09_05--tt17--c5',
# 'LT0119_07--ex2006_12_08--sp2005_09_05--tt18--c5',
# 'LT0119_13--ex2005_09_14--sp2005_09_05--tt17--c5',
# 'LT0119_14--ex2005_09_21--sp2005_09_05--tt17--c5',
# 'LT0120_06--ex2005_10_19--sp2005_09_06--tt17--c4',
# 'LT0120_07--ex2005_09_28--sp2005_09_06--tt17--c5',
# 'LT0120_09--ex2006_03_22--sp2005_09_06--tt173--c3',
# 'LT0121_09--ex2006_06_14--sp2005_09_06--tt17--c5',
# 'LT0121_37--ex2005_09_23--sp2005_09_06--tt163--c4',
# 'LT0121_41--ex2005_09_21--sp2005_09_06--tt17--c4',
# 'LT0122_04--ex2005_12_07--sp2005_09_08--tt17--c4',
# 'LT0122_11--ex2006_07_26--sp2005_09_08--tt17--c4',
# 'LT0122_38--ex2006_11_29--sp2005_09_08--tt18--c4',
# 'LT0122_51--ex2007_01_17--sp2006_12_21--tt18--c4',
# 'LT0122_55--ex2007_01_19--sp2006_12_21--tt19--c4',
# 'LT0123_13--ex2006_07_07--sp2005_09_08--tt17--c4',
# 'LT0123_29--ex2005_10_05--sp2005_09_08--tt193--c4',
# 'LT0123_32--ex2005_09_23--sp2005_09_08--tt17--c5',
# 'LT0124_06--ex2005_09_28--sp2005_09_13--tt173--c4',
# 'LT0124_08--ex2006_03_22--sp2005_09_13--tt173--c3',
# 'LT0124_19--ex2006_07_12--sp2005_09_13--tt17--c3',
# 'LT0125_02--ex2005_10_26--sp2005_09_13--tt173--c3',
# 'LT0125_03--ex2005_10_26--sp2005_09_13--tt173--c4',
# 'LT0125_41--ex2005_09_28--sp2005_09_13--tt173--c4',
# 'LT0126_01--ex2006_03_22--sp2005_09_15--tt173--c5',
# 'LT0126_31--ex2005_09_30--sp2005_09_15--tt17--c5',
# 'LT0126_38--ex2005_09_28--sp2005_09_15--tt17--c3',
# 'LT0127_01--ex2006_03_22--sp2005_09_15--tt173--c5',
# 'LT0127_33--ex2005_09_28--sp2005_09_15--tt173--c4',
# 'LT0127_43--ex2005_09_23--sp2005_09_15--tt17--c5',
# 'LT0128_01--ex2005_10_26--sp2005_09_19--tt173--c3',
# 'LT0128_07--ex2006_01_18--sp2005_09_19--tt17--c5',
# 'LT0128_08--ex2006_12_08--sp2005_09_19--tt18--c5',
# 'LT0128_16--ex2005_09_30--sp2005_09_19--tt17--c4',
# 'LT0129_37--ex2005_09_28--sp2005_09_19--tt173--c4',
# 'LT0129_50--ex2005_08_31--sp2006_08_23--tt17--c3',
# 'LT0129_52--ex2006_08_30--sp2006_08_23--tt20--c4',
# 'LT0130_01--ex2005_11_23--sp2005_09_26--tt17--c5',
# 'LT0130_02--ex2005_10_19--sp2005_09_26--tt17--c3',
# 'LT0130_41--ex2005_10_12--sp2005_09_26--tt17--c4',
# 'LT0131_01--ex2006_03_22--sp2005_09_20--tt173--c3',
# 'LT0131_42--ex2005_09_30--sp2005_09_20--tt17--c5',
# 'LT0131_47--ex2005_09_28--sp2005_09_20--tt17--c5',
# 'LT0132_02--ex2005_12_07--sp2005_09_22--tt17--c5',
# 'LT0132_04--ex2005_10_19--sp2005_09_22-tt17--c3',
# 'LT0132_06--ex2005_10_19--sp2005_09_22--tt17--c4',
# 'LT0132_31--ex2005_09_30--sp2005_09_22--tt173--c3',
# 'LT0133_01--ex2006_03_22--sp2005_09_22--tt173--c3',
# 'LT0133_19--ex2005_09_30--sp2005_09_22--tt173--c3',
# 'LT0133_38--ex2005_10_07--sp2005_09_22--tt17--c5']
#
#['LT0134_01--ex2005_10_19--sp2005_10_11--tt17--c3',
# 'LT0134_03--ex2005_10_21--sp2005_10_11--tt17--c5',
# 'LT0134_06--ex2005_12_07--sp2005_10_11--tt17--c4',
# 'LT0134_07--ex2005_12_14--sp2005_10_11--tt163--c5',
# 'LT0135_02--ex2005_11_23--sp2005_09_27--tt17--c3',
# 'LT0135_47--ex2005_10_12--sp2005_09_27--tt17--c4',
# 'LT0135_48--ex2005_10_12--sp2005_09_27--tt17--c5',
# 'LT0136_21--ex2007_10_24--sp2005_09_30--tt17--c4',
# 'LT0136_44--ex2005_10_12--sp2005_09_30--tt17--c5',
# 'LT0136_45--ex2005_10_12--sp2005_09_30--tt17--c4',
# 'LT0137_01--ex2005_11_23--sp2005_10_04--tt17--c3',
# 'LT0137_03--ex2006_02_01--sp2005_10_04--tt17--c5',
# 'LT0137_05--ex2005_10_19--sp2005_10_04--tt17--c5',
# 'LT0137_44--ex2005_10_12--sp2005_10_04--tt17--c5',
# 'LT0138_01--ex2005_10_19--sp2005_10_04--tt17--c3',
# 'LT0138_02--ex2005_11_18--sp2005_10_04--tt173--c4',
# 'LT0138_03--ex2005_10_19--sp2005_10_04--tt17--c4',
# 'LT0138_04--ex2005_11_23--sp2005_10_04--tt17--c4',
# 'LT0138_46--ex2005_10_12--sp2005_10_04--tt17--c4',
# 'LT0139_01--ex2005_10_19--sp2005_10_06--tt17--c5',
# 'LT0139_07--ex2006_01_18--sp2005_10_06--tt17--c5',
# 'LT0139_08--ex2006_07_07--sp2005_10_06--tt17--c5',
# 'LT0140_05--ex2006_03_22--sp2005_10_10--tt173--c5',
# 'LT0140_06--ex2005_10_26--sp2005_10_10--tt173--c3',
# 'LT0140_10--ex2005_10_21--sp2005_10_10--tt17--c3',
# 'LT0141_02--ex2005_10_21--sp2005_10_10--tt17--c5',
# 'LT0141_03--ex2005_10_26--sp2005_10_10--tt173--c4',
# 'LT0141_04--ex2006_03_22--sp2005_10_10--tt173--c5',
# 'LT0142_01--ex2005_10_21--sp2005_10_11--tt17--c4',
# 'LT0142_03--ex2005_10_26--sp2005_10_11--tt173--c4',
# 'LT0142_06--ex2006_03_24--sp2005_10_11--tt17--c3',
# 'LT0143_01--ex2005_10_21--sp2005_10_13--tt17--c3',
# 'LT0143_02--ex2005_10_21--sp2005_10_13--tt17--c4',
# 'LT0143_05--ex2006_03_24--sp2005_10_13-tt17--c3',
# 'LT0144_01--ex2005_10_26--sp2005_10_13--tt173--c5',
# 'LT0144_02--ex2005_11_11--sp2005_10_13--tt173--c3',
# 'LT0144_04--ex2006_02_01--sp2005_10_13--tt17--c5',
# 'LT0145_01--ex2005_10_26--sp2005_10_14--tt173--c5',
# 'LT0145_02--ex2006_03_24--sp2005_10_14--tt17--c3',
# 'LT0145_04--ex2005_11_11--sp2005_10_14--tt173--c5',
# 'LT0146_02--ex2005_10_26--sp2005_10_14--tt173--c3',
# 'LT0146_04--ex2005_11_11--sp2005_10_14--tt173--c4',
# 'LT0146_06--ex2006_03_24--sp2005_10_14--tt17--c5',
# 'LT0147_01--ex2005_11_16--sp2005_10_17--tt17--c3',
# 'LT0147_02--ex2005_12_14--sp2005_10_17--tt163--c5',
# 'LT0147_03--ex2005_11_11--sp2005_10_17--tt173--c4',
# 'LT0148_01--ex2005_11_16--sp2005_10_17--tt17--c5',
# 'LT0148_02--ex2005_11_18--sp2005_10_17--tt173--c5',
# 'LT0148_11--ex2005_11_11--sp2005_10_17--tt173--c5',
# 'LT0148_37--ex2007_02_09--sp2005_10_17--tt183--c5']
#
#
#['LT0148_40--ex2007_02_09--sp2005_10_18--tt17--c4',
# 'LT0149_01--ex2005_11_11--sp2005_10_18--tt173--c3',
# 'LT0149_03--ex2005_12_07--sp2005_10_18--tt17--c5',
# 'LT0149_05--ex2006_02_01--sp2005_10_18--tt17--c5',
# 'LT0150_02--ex2005_11_18--sp2005_10_18--tt173--c3',
# 'LT0150_04--ex2005_11_18--sp2005_10_18--tt173--c5',
# 'LT0150_05--ex2006_01_20--sp2005_10_18--tt19--c4',
# 'LT0151_06--ex2005_12_07--sp2005_09_20--tt17--c3',
# 'LT0151_08--ex2005_12_09--sp2005_09_20--tt17--c5',
# 'LT0151_09--ex2006_01_20--sp2005_09_10--tt19--c3',
# 'LT0152_04--ex2005_12_02--sp2005_09_20--tt17--c4',
# 'LT0152_05--ex2006_01_20--sp2005_09_20--tt19--c3',
# 'LT0152_18--ex2005_11_18--sp2005_09_20--tt173--c3',
# 'LT0153_01--ex2005_11_16--sp2005_10_24--tt17--c5',
# 'LT0153_06--ex2005_11_11--sp2005_10_24--tt173--c4',
# 'LT0153_08--ex2006_03_24--sp2005_10_23--tt17--c5',
# 'LT0154_02--ex2005_11_23--sp2005_10_24--tt17--c3',
# 'LT0154_03--ex2005_12_07--sp2005_10_24--tt17--c5',
# 'LT0154_04--ex2005_11_11--sp2005_10_24--tt173--c3',
# 'LT0155_03--ex2006_01_20--sp2005_10_25--tt19--c3',
# 'LT0155_05--ex2005_12_09--sp2005_10_25--tt17--c3',
######## 'LT0155_08--ex2007_07_11--sp2005_10_25--tt19--c4',
# 'LT0156_07--ex2005_12_07--sp2005_10_25--tt17--c5',
# 'LT0156_08--ex2005_12_09--sp2005_10_25--tt17--c3',
# 'LT0156_09--ex2006_01_18--sp2005_10_25--tt17--c5',
# 'LT0157_04--ex2006_01_20--sp2005_10_27--tt17--c5',
# 'LT0157_05--ex2006_01_18--sp2005_10_27--tt17--c3',
# 'LT0157_07--ex2006_03_24--sp2005_10_17-tt17--c5',
# 'LT0158_01--ex2005_11_16--sp2005_10_27--tt17--c3',
# 'LT0158_03--ex2005_11_23--sp2005_10_27--tt17--c3',
# 'LT0158_05--ex2006_01_18--sp2005_10_27--tt17--c3',
# 'LT0159_17--ex2006_01_20--sp2006_01_10--tt17--c5',
# 'LT0159_49--ex2006_01_18--sp2006_01_10--tt17--c5',
# 'LT0159_50--ex2006_02_01--sp2006_01_10--tt17--c5',
# 'LT0170_01--ex2006_09_27--sp2006_09_13--tt17--c3',
# 'LT0170_07--ex2006_09_27--sp2006_09_13--tt17--c5',
# 'LT0170_08--ex2006_09_27--sp2006_09_13--tt17--c5',
# 'LT0170_09--ex2006_09_27--sp2006_09_13--tt17--c3',
# 'LT0601_01--ex2007_01_17--sp2007_01_10-tt18--c4',
# 'LT0601_03--ex2007_01_24--sp2007_01_09--tt18--c5',
# 'LT0601_04--ex2007_01_19--sp2007_01_10-tt19--c4',
# 'LT0601_05--ex2007_01_19--sp2007_01_10-tt19--c5',
# 'LT0602_01--ex2007_01_17--sp2007_01_10--tt18--c4',
# 'LT0602_04--ex2007_01_19--sp2007_01_10--tt19--c4',
# 'LT0602_05--ex2007_01_19--sp2007_01_10--tt19--c5',
# 'LT0602_06--ex2007_01_24--sp2007_01_10--tt18--c5',
# 'LT0603_03--ex2007_01_17--sp2007_01_10--tt18--c4',
# 'LT0603_04--ex2007_01_19--sp2007_01_10--tt19--c5',
# 'LT0603_05--ex2007_01_19--sp2007_01_10--tt19--c4',
# 'LT0603_06--ex2007_01_24--sp2007_01_11--tt18--c5']
          
#dans cette plaque il y a 119 puits donc si on a dix films/job on aura 12 jobs
batchScriptDirectory = '/cbio/donnees/aschoenauer/software/bin'
pythonBinary = 'python'
batchScript = 'cecog_batch.py'

# PBS settings (cluster, walltime, log folders)
#pbsArrayEnvVar = 'PBS_ARRAY_INDEX'
pbsArrayEnvVar = 'SGE_TASK_ID'
jobArrayOption = 't'
clusterName = None

pbsOutDir = '/cbio/donnees/aschoenauer/PBS/OUT'
pbsErrDir = '/cbio/donnees/aschoenauer/PBS/ERR'
pbsMail = 'alice.schoenauer_sebag@mines-paristech.fr'

hours = 10
minutes = 0
ncpus = 1
mem = 2
#NB DE FILMS/JOB
jobSize = 1
omit_processed_positions = False

additional_flags = ["create_no_images","minimal_effort"]

additional_attributes = {
                         }

rendering = {}

#rendering = {
#             'primary_contours':
#             {'Primary': {'raw': ('#FFFFFF', 1.0),
#                          'contours': {'primary': ('#FF0000', 1, True)}
#                          }
#             },
#             'secondary_contours':
#             {'Secondary': {'raw': ('#FFFFFF', 1.0),
#                            'contours': {'propagate': ('#FF0000', 1, True)}
#                            }
#             }
#             }

rendering_class = {}
#rendering_class = {'primary_classification':
#                   {
#                    'Primary': {'raw': ('#FFFFFF', 1.0),
#                                'contours': [('primary', 'class_label', 1, False),
#                                             ('primary', '#000000', 1, False)]},
##                    'Secondary': {'raw': ('#00FF00', 1.0),
##                                  'contours': [('propagate', 'class_label', 1, False),
##                                               ('propagate', '#000000', 1, False)]}
#                    },
#                    'secondary_classification':
#                    {
#                     'Secondary': {'raw': ('#FFFFFF', 1.0),
#                                   'contours': [('propagate', 'class_label', 1, False),
#                                                ('propagate', '#000000', 1, False)]}
#                     }
#                    }

#primary_graph = '/g/mitocheck/Thomas/data/Moritz_analysis_cecog/cecog_settings/graph_primary.txt'
#secondary_graph = '/g/mitocheck/Thomas/data/Moritz_analysis_cecog/cecog_settings/graph_secondary.txt'
#filename_to_r = '/g/software/bin/R-2.13.0'

primary_graph = None
secondary_graph = None
filename_to_r = None

#primary_classification_envpath = '/g/mitocheck/Thomas/data/Moritz_analysis_cecog/cecog_classifiers/23092011_H2B-LB1_TRFX_H2B'
#secondary_classification_envpath = '/g/mitocheck/Thomas/data/Moritz_analysis_cecog/cecog_classifiers/111222_H2B_TRFX_LB1'
primary_classification_envpath = None
secondary_classification_envpath = None

#filename_to_r = '/Users/twalter/software/R/R.framework/Versions/2.13/Resources/bin/R'
#primary_graph = '/Users/twalter/data/Moritz_cecog/cecog_settings/graph_primary.txt'
#secondary_graph = '/Users/twalter/data/Moritz_cecog/cecog_settings/graph_secondary.txt'

# example: overlay the primary results to the two-channel image.
# primary channel in red, secondary channel in green.
# The secondary segmentation is propagate
#rendering_class = {'primary_classification':
#                   {'Primary': {'raw': ('#FF0000', 1.0),
#                                'contours': [('primary', 'class_label', 1, False)]},
#                    'Secondary': {'raw': ('#00FF00', 1.0),
#                                  'propagate': [('propagate', 'class_label', 1, False)]}
#                    }
#                   }

# folders to be generated
lstFolders = [pbsOutDir, pbsErrDir, baseScriptDir, baseOutDir]


