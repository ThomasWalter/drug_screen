import skimage
import skimage.io
import numpy as np
import pdb
import cPickle as pickle

from optparse import OptionParser
import os, sys

def rename_all_images(in_folder, out_folder, what_to_replace, by_what):
    res = {}
    for dirpath, dirnames, filenames in os.walk(in_folder):
        for filename in filter(lambda x: os.path.splitext(x)[-1] in ['.tif', '.tiff', '.png'], filenames):
            full_filename = os.path.join(dirpath, filename)
            new_filename = full_filename.replace(in_folder, out_folder).replace(what_to_replace, by_what)
            os.rename(full_filename, new_filename)
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
    parser.add_option("-a", "--a_string", dest="a_string",
                      help="String which is to be replaced")
    parser.add_option("-b", "--b_string", dest="b_string",
                      help="String which is to be replaced")

    (options, args) = parser.parse_args()

    if (options.input_folder is None or options.a_string is None or options.b_string is None):
        parser.error("incorrect number of arguments: input folder must be given.")

    inpath = options.input_folder
    outpath = options.output_folder
    if outpath is None:
        outpath = inpath
    what_to_be_replaced = options.a_string
    by_what = options.b_string

    rename_all_images(inpath, outpath, what_to_be_replaced, by_what)
    
    
    
