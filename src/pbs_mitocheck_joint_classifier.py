
# to start this script:
# cd /g/software/linux/pack/cellcognition-1.2.4/SRC/cecog_git/pysrc/scripts/EMBL/cluster
# for example:
# python-2.7 pbs_script_generation.py -b <settings_filename>
# python-2.7 pbs_script_generation.py -b ../settings_files/chromosome_condensation/pbs_chromosome_condensation_settings.py
# python-2.7 pbs_script_generation.py -b ../settings_files/lamin/pbs_laminb_settings.py


path_command = """setenv PATH /share/apps/user_apps/QT5/bin:/cbio/donnees/nvaroquaux/.local/bin:/cbio/donnees/twalter/software/bin:/share/apps/libxslt-1.1.28/bin:/share/apps/libxml2-2.9.2/bin:${PATH}
setenv LD_LIBRARY_PATH /share/apps/user_apps/QT5/lib:/cbio/donnees/nvaroquaux/.local/lib:/cbio/donnees/twalter/software/lib:/cbio/donnees/twalter/software/lib64/R/lib:/share/apps/user_apps/smil_0.8.1/lib/Smil:/share/apps/libxml2-2.9.2/lib:/share/apps/libxslt-1.1.28/lib:${LD_LIBRARY_PATH}
setenv LIBRARY_PATH /share/apps/user_apps/QT5/lib:/cbio/donnees/nvaroquaux/.local/lib:/cbio/donnees/twalter/software/lib:/cbio/donnees/twalter/software/lib64/R/lib:/share/apps/user_apps/smil_0.8.1/lib/Smil:/share/apps/libxml2-2.9.2/lib:/share/apps/libxslt-1.1.28/lib
setenv PYTHONPATH /cbio/donnees/twalter/cecog_install/lib/python2.7/site-packages:/cbio/donnees/twalter/cecog_dependencies/cellh5/pysrc:/share/apps/user_apps/smil_0.8.1/lib/Smil
setenv DRMAA_LIBRARY_PATH /opt/gridengine/lib/lx26-amd64/libdrmaa.so
"""

# data directories
baseInDir = '/share/data20T/mitocheck/compressed_data'
baseOutDir = '/share/data40T/aschoenauer/drug_screen/results_August_2016/mito_joint_classifier'

# settings for scripts
baseScriptDir = '/cbio/donnees/twalter/src/drug_screen/scripts/mito_joint'
scriptPrefix = 'mitojoint'

# settingsfile
#settingsFilename = '/cbio/donnees/aschoenauer/projects/drug_screen/settings/drug_screen_features_classif.conf'
settingsFilename = '/cbio/donnees/twalter/src/drug_screen/cecog_settings/mito_settings_dynseg_combined_classifier_cluster.conf'

plates = None

batchScriptDirectory = '/cbio/donnees/twalter/cecog_install/bin'
pythonBinary = 'python'
batchScript = 'cecog_batch.py'

# PBS settings (cluster, walltime, log folders)
pbsArrayEnvVar = 'SGE_TASK_ID'
jobArrayOption = 't'
clusterName = None

pbsOutDir = '/cbio/donnees/twalter/PBS/OUT'
pbsErrDir = '/cbio/donnees/twalter/PBS/ERR'
pbsMail = 'Thomas.Walter@mines-paristech.fr'

hours = 10
minutes = 0
ncpus = 1
mem = 2
#NB DE FILMS/JOB
jobSize = 8
omit_processed_positions = False

#additional_flags = ["create_no_images","minimal_effort"]
additional_flags = ["create_no_images"]

additional_attributes = {
                         }

rendering = {}

rendering_class = {}

primary_graph = None
secondary_graph = None
filename_to_r = None

primary_classification_envpath = None
secondary_classification_envpath = None

# folders to be generated
lstFolders = [pbsOutDir, pbsErrDir, baseScriptDir, baseOutDir]


