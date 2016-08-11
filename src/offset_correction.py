import skimage
import skimage.io
import numpy as np
import pdb
import cPickle as pickle

from optparse import OptionParser
import os, sys


class OffsetCorrector(object):
    def __init__(self, in_folder, out_folder=None):
        self.in_folder = self.get_full_name(in_folder)
        if out_folder is None:
            self.out_folder = self.get_full_name(self.in_folder)
            self.overwrite = True
        else:
            self.out_folder = self.get_full_name(out_folder)            
        
        return

    def get_full_name(self, folder):
        res = os.path.abspath(os.path.expanduser(folder))
        return res
    
    def correct_single_image(self, img):

        imout = img - np.percentile(img, 5)
        
        #minval = img.min()
        #pdb.set_trace()
        #imout = img - minval
        imout[imout < 0] = 0
        res = imout.astype(np.dtype('uint16'))
        
        return res

    def correct_single_image_filename(self, filename):

        full_filename = self.get_full_name(filename)
        img = skimage.io.imread(full_filename)
        imout = self.correct_single_image(img)

        if full_filename.rfind(self.in_folder) < 0:
            raise ValueError('file is not found in input folder.')

        new_filename = full_filename.replace(self.in_folder, self.out_folder)
        new_folder = os.path.dirname(new_filename)
        if not os.path.isdir(new_folder):
            os.makedirs(new_folder)
            print 'making %s' % new_folder
            
        skimage.io.imsave(new_filename, imout)
        
        return imout.min(), imout.max()
    
    def correct_all_images(self):
        res = {}
        for dirpath, dirnames, filenames in os.walk(self.in_folder):
            for filename in filter(lambda x: os.path.splitext(x)[-1] in ['.tif', '.tiff', '.png'], filenames):
                #print os.path.join(dirpath, filename)
                full_filename = os.path.join(dirpath, filename)
                lt = full_filename[full_filename.rfind('LT0'):(full_filename.rfind('LT0')+len('LT0900_01'))]
                well = full_filename[full_filename.rfind('W00'):(full_filename.rfind('W00')+len('W00037'))]
                res[(lt, well)] = self.correct_single_image_filename(os.path.join(dirpath, filename))
                #res[(lt, well)] = (0.0, 1000*np.random.rand())
        fp = open(os.path.join(self.out_folder, 'minmaxDistribution.pickle'), 'w')
        pickle.dump(res, fp)
        fp.close()

        print 'processed %i movies' % len(res)
        print 'total max: %i' % max([res[x][1] for x in res.keys()])

        labteks = list(set([x[0] for x in res.keys()]))
        for lt in labteks:
            keys = filter(lambda x: x[0] == lt, res.keys())
            print 'max for %s: %i' % (lt, max([res[x][1] for x in keys]))

        return

    
if __name__ ==  "__main__":

    description =\
'''
%prog - convert all color images into nifti color images. 
'''

    parser = OptionParser(usage="usage: %prog [options]",
                         description=description)
    parser.add_option("-i", "--input_folder", dest="input_folder",
                      help="Input folder")
    parser.add_option("-o", "--output_folder", dest="output_folder",
                      help="Output folder")

    (options, args) = parser.parse_args()

    if (options.input_folder is None):
        parser.error("incorrect number of arguments: input folder must be given.")

    inpath = options.input_folder
    outpath = options.output_folder
    oc = OffsetCorrector(inpath, outpath)
    oc.correct_all_images()

