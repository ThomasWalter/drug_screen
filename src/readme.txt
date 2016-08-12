DRUG SCREEN:
in order to generate the scripts that can be launched on the cluster, just do:
python Cecog_script_generation_drug_screen.py -b pbs_drug_screen_features_classif_August2016.py

--> all settings are in the settings file (self-explanatory)

MITOCHECK: 

to start missing : 
python Cecog_script_generation.py -b ../pbs_mitocheck_missing.py -p ../../../missing.pickle

to start everything
python Cecog_script_generation.py -b ../pbs_mitocheck_full.py
