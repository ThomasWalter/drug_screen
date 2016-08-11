
import os, sys

#FILENAME = os.path.join(os.getcwd(), os.path.dirname(__file__), 'drug_screen_training_set.txt')
#print FILENAME

BASE_FOLDER = os.path.dirname(os.path.realpath(__file__))
FILENAME = os.path.join(BASE_FOLDER, 'drug_screen_training_set.txt')
DATA_FOLDER = os.path.join(BASE_FOLDER, 'data')
REMOTE_FOLDER = '/cbio/donnees/twalter/exchange/drug_screen'

#print __file__

def read_positions():
    fp = open(FILENAME, 'r')
    temp = fp.readlines()
    fp.close()
    positions = [line.strip('\n').split('\t') for line in temp]
    return positions

def copy_positions(positions):
    for lt, pos in positions:
        lt_folder = os.path.join(DATA_FOLDER, lt)
        if not os.path.isdir(lt_folder):
            print 'make %s' % lt_folder
            os.makedirs(lt_folder)
        remote_folder = os.path.join(REMOTE_FOLDER, lt, 'W%s' % pos)
        cmd = 'scp -r twalter@cbio.ensmp.fr:%s %s' % (remote_folder, lt_folder)

        if os.path.isdir(os.path.join(lt_folder, 'W%s' % pos)):
            print 'skipping %s %s' % (lt, pos)
            continue
        
        try:
            print cmd
            os.system(cmd)
        except:
            continue
        
pos = read_positions()
copy_positions(pos)

