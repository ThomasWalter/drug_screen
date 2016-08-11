import numpy as np
import pdb
import cPickle as pickle

from optparse import OptionParser
import os, sys

import scipy.io.arff as arff
import collections
import re

import operator as op

import shutil

# from CellCognition
class WriterBase(object):

    FLOAT_DIGITS = 8

    def __init__(self, strFilename, lstFeatureNames, dctClassLabels):
        self.oFile = file(strFilename, "w")
        self.lstFeatureNames = lstFeatureNames
        self.dctClassLabels = dctClassLabels

    def close(self):
        self.oFile.close()

    @classmethod
    def buildLineStatic(cls, strClassName, lstObjectFeatures, dctClassLabels):
        raise NotImplementedError("This is an abstract method!")

    def buildLine(self, strClassName, lstObjectFeatures):
        return self.buildLineStatic(strClassName, lstObjectFeatures,
                                    self.dctClassLabels)

    def writeLine(self, strLine=""):
        self.oFile.write(strLine+"\n")

    def writeLineList(self, lstLine):
        for strLine in lstLine:
            self.writeLine(strLine)

    def writeObjectFeatureData(self, strClassName, lstObjectFeatureData):
        self.writeLine(self.buildLine(strClassName, lstObjectFeatureData))

    def writeAllFeatureData(self, feature_data):
        for class_name in feature_data:
            for sample_features in feature_data[class_name]:
                self.writeObjectFeatureData(class_name, sample_features)

    @classmethod
    def _convert(cls, f):
        return "%%.%de" %cls.FLOAT_DIGITS %f


# from cellcognition
class ArffWriter(WriterBase):

    def __init__(self, strFilename, lstFeatureNames, dctClassLabels,
                 dctHexColors=None, hasZeroInsert=False):
        super(ArffWriter, self).__init__(strFilename, lstFeatureNames,
                                         dctClassLabels)
        self.writeLine("@RELATION CecogClassifier")
        self.writeLine()
        for strFeatureName in self.lstFeatureNames:
            self.writeLine("@ATTRIBUTE %s NUMERIC" % strFeatureName)

        lstClassNames = self.dctClassLabels.keys()
        # sort names by labels
        lstClassNames.sort(key = lambda n: self.dctClassLabels[n])
        self.writeLine("@ATTRIBUTE class {%s}" %
                       ",".join(["'%s'" % x
                                 for x in lstClassNames])
                       )
        self.writeLine()
        self.writeLine("%%CLASS-LABELS {%s}" %
                       ",".join(["%s" % self.dctClassLabels[x]
                                 for x in lstClassNames])
                       )
        if dctHexColors is not None:
            self.writeLine("%%CLASS-COLORS {%s}" %
                           ",".join(["%s" % dctHexColors[x]
                                     for x in lstClassNames])
                           )
        self.writeLine()

        self.writeLine('%%HAS-ZERO-INSERTED-IN-FEATURE-VECTOR %d' %
                       (1 if hasZeroInsert else 0))
        self.writeLine()

        self.writeLine("@DATA")

    @classmethod
    def buildLineStatic(cls, strClassName, lstObjectFeatures, dctClassLabels):
        strLine = ",".join(map(cls._convert, lstObjectFeatures) +
                           ["'%s'" % strClassName]
                           )
        return strLine

    def close(self):
        self.writeLine()
        super(ArffWriter, self).close()


class ClassifierMerger(object):
    def __init__(self, c1, c2, output_path):
        self.c1_folder = os.path.abspath(os.path.expanduser(c1))
        self.c2_folder = os.path.abspath(os.path.expanduser(c2))
        self.output_path = os.path.abspath(os.path.expanduser(output_path))
        return

    def get_labels_and_colors(self, filename):
        fp = open(os.path.join(self.c2_folder, 'data', 'features.arff'), 'r')
        temp = fp.readlines()
        fp.close()

        class_labels = None
        class_colors = None
        
        for line in temp:
            if line.rfind('CLASS-LABELS') >= 0:
                regex = re.compile('.*?\{(?P<labels>.*?)\}.*?')
                res = regex.search(line)
                if res is None:
                    raise ValueError('A problem has occurred while parsing the arff file. No matching of labels is possible')
                class_labels = [int(x) for x in res.groupdict()['labels'].split(',')]

            if line.rfind('CLASS-COLORS') >= 0:
                regex = re.compile('.*?\{(?P<labels>.*?)\}.*?')
                res = regex.search(line)
                if res is None:
                    raise ValueError('A problem has occurred while parsing the arff file. No matching of labels is possible')
                class_colors = res.groupdict()['labels'].split(',')
        
        if class_labels is None:
            raise ValueError("information on class labels was not found in %s." % filename)

        if class_colors is None:
            raise ValueError("information on class colors was not found in %s." % filename)

        return class_labels, class_colors
    
    def __call__(self, copy=False):
        c1_data, c1_meta = arff.loadarff(os.path.join(self.c1_folder, 'data', 'features.arff'))
        c2_data, c2_meta = arff.loadarff(os.path.join(self.c2_folder, 'data', 'features.arff'))
        c1_labels, c1_colors = self.get_labels_and_colors(os.path.join(self.c1_folder, 'data', 'features.arff'))
        c2_labels, c2_colors = self.get_labels_and_colors(os.path.join(self.c2_folder, 'data', 'features.arff'))

        X1 = np.array([x.tolist()[:-1] for x in c1_data])
        X2 = np.array([x.tolist()[:-1] for x in c2_data])

        y1 = [x[-1] for x in c1_data]
        y2 = [x[-1] for x in c2_data]
        y = y1 + y2
        
        # first reduce the features to a compatible set 
        if collections.Counter(c1_meta.names()) != collections.Counter(c2_meta.names()):
            compatible_features = filter(lambda x: x in c2_meta.names()[:-1], c1_meta.names()[:-1])

            c1_indices = [c1_meta.names().index(feat) for feat in compatible_features]
            c2_indices = [c2_meta.names().index(feat) for feat in compatible_features]
            
            X1_mod = X1[:,c1_indices]
            X2_mod = X2[:,c2_indices]
            X = np.vstack([X1_mod, X2_mod])
        else:
            compatible_features = c2_meta.names()[:-1]
            joint_data = np.vstack([X1, X2])
            #joint_data = c1_data.tolist() + c2_data.tolist()

        
        # make output folder and features file. 
        out_folder = os.path.join(self.output_path, 'data')
        if not os.path.exists(out_folder) :
            os.makedirs(out_folder)
        filename = os.path.join(out_folder, 'features.arff')

        # get class names
        c1_classnames = [x[1:-1] for x in c1_meta._attributes['class'][-1]] #c1_meta._attributes #[x[1:-1] for x in c1_meta._attributes]
        c2_classnames = [x[1:-1] for x in c2_meta._attributes['class'][-1]] #c2_meta._attributes #[x[1:-1] for x in c2_meta._attributes]
        c1_dctClassLabels = dict(zip(c1_classnames, c1_labels))
        c2_dctClassLabels = dict(zip(c2_classnames, c2_labels))
        c1_dctColors = dict(zip(c1_classnames, c1_colors))
        c2_dctColors = dict(zip(c2_classnames, c2_colors))

        # get class labels (to build the dict)
        dctClassLabels = {}
        all_classes = list(set(c1_dctClassLabels.keys() + c2_dctClassLabels.keys()))
        for cl in all_classes:
            if cl in c1_dctClassLabels:
                label = c1_dctClassLabels[cl]
                if cl in c2_dctClassLabels and label != c2_dctClassLabels[cl]:                        
                    raise ValueError('Label mismatch in the two arff files. Fix the label assignment.')
            else:
                label = c2_dctClassLabels[cl]
            dctClassLabels[cl] = label
            
        # get class colors (to build the dict)
        dctHexColors = {}
        for cl in all_classes:
            if cl in c1_dctColors:
                color = c1_dctColors[cl]
                if cl in c2_dctColors and color != c2_dctColors[cl]:                        
                    raise ValueError('Color mismatch in the two arff files. Fix the label assignment.')
            else:
                color = c2_dctColors[cl]
            dctHexColors[cl] = color

        # initialization of the ArffWriter
        writer = ArffWriter(filename, compatible_features, dctClassLabels=dctClassLabels,
                            dctHexColors=dctHexColors)

        all_feature_data = dict(zip(all_classes,[[] for cl in all_classes]))
        for i in range(X.shape[0]):
            class_name = y[i][1:-1]
            feature_vec = X[i]
            all_feature_data[class_name].append(feature_vec)

        writer.writeAllFeatureData(all_feature_data)

        writer.close()

        print 'arff file written.'
        
        # export class_definition
        filename = os.path.join(self.output_path, 'class_definition.txt')
        fp = open(filename, 'w')
        temp = zip(all_classes, [dctClassLabels[x] for x in all_classes], [dctHexColors[x] for x in all_classes])
        temp.sort(key=op.itemgetter(1))
        for x in temp:
            fp.write('\t'.join([str(y) for y in x]) + '\n')
        fp.close()
        print 'class definition written.'

        if copy:
            # concatenate the sample files
            fp = open(os.path.join(self.c1_folder, 'data', 'features.samples.txt'), 'r')
            samples = fp.readlines()
            fp.close()
            fp = open(os.path.join(self.c2_folder, 'data', 'features.samples.txt'), 'r')
            samples += fp.readlines()
            fp.close()
            samples.sort()
            fp = open(os.path.join(self.output_path, 'data', 'features.samples.txt'), 'w')
            for line in samples:
                fp.write(line)
            fp.close()
        
            # copy
            folder = os.path.join(self.output_path, 'controls')
            if not os.path.exists(folder):
                os.makedirs(folder)
            shutil.copy(os.path.join(self.c1_folder, 'controls', "*.*"), folder)
            shutil.copy(os.path.join(self.c2_folder, 'controls', "*.*"), folder)
    
            folder = os.path.join(self.output_path, 'samples')
            if not os.path.exists(folder):
                os.makedirs(folder)
            for s_folder in [self.c1_folder, self.c2_folder]:
                sub_folders = os.listdir(s_folder)
                for sf in sub_folders:
                    nf = os.path.join(folder, sf)
                    if not os.path.exists(nf):
                        os.makedirs(nf)
                    shutil.copy(os.path.join(s_folder, sf, '*.*'), nf)
                    
        return
    
    def compatibility_check(self):
        c1_data, c1_meta = arff.loadarff(os.path.join(self.c1_folder, 'data', 'features.arff'))
        c2_data, c2_meta = arff.loadarff(os.path.join(self.c1_folder, 'data', 'features.arff'))

        testres = {}
        
        # check features
        if collections.Counter(c1_meta.names()) == collections.Counter(c2_meta.names()):
            testres['features'] = True
        else:
            testres['features'] = False

        # check classes
        classes_c1 = list(set([x[-1] for x in c1_data]))
        classes_c2 = list(set([x[-1] for x in c1_data]))
        if collections.Counter(classes_c1) == collections.Counter(classes_c2):
            testres['classes'] = True
        else:
            testres['classes'] = False

        print 'Compatibility report:'
        print 'features: ', testres[features]
        print 'classes: ', testres['classes']
        
        return testres
    
    

if __name__ ==  "__main__":

    description =\
'''
%prog - convert all color images into nifti color images. 
'''

    parser = OptionParser(usage="usage: %prog [options]",
                         description=description)
    parser.add_option("-a", "--classifier_a_folder", dest="classifier_a_folder",
                      help="Folder of classifier A to be merged.")
    parser.add_option("-b", "--classifier_b_folder", dest="classifier_b_folder",
                      help="Folder of classifier B to be merged.")
    
    parser.add_option("-o", "--output_folder", dest="output_folder",
                      help="Output folder")

    (options, args) = parser.parse_args()

    if (options.classifier_a_folder is None or options.classifier_b_folder is None):
        parser.error("The two classifiers must be given (two folders, each corresponding to one classifier).")

    c1 = options.classifier_a_folder
    c2 = options.classifier_b_folder

    output_folder = options.output_folder
    if (output_folder is None):
        output_folder = os.path.join(c1, '..', 'joint_classifier')

    cm = ClassifierMerger(c1, c2, output_folder)
    cm(copy=False)
    print 'DONE!'
