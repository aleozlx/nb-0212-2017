from __future__ import print_function
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import os, argparse, sys
import multiprocessing
import numpy as np

DATA = lambda p: os.path.join('../datafiles', p)
images = list()
depth = list()

for root, dirs, files in os.walk(DATA('zed-subset')):
    for name in files:
        if os.path.splitext(name)[1] in ['.jpeg']:
            fname = os.path.join(root, name)
            if 'depth' in name:
                depth.append(fname)
            else:
                images.append(fname)

def _task_slic((fname, numSegments, output_path)):
    try:
        im = img_as_float(io.imread(fname))
        #segments = slic(im, n_segments = numSegments, sigma = 5)
        #np.save(os.path.join(output_path, os.path.basename(fname)), segments, allow_pickle=False)
        return (fname, 'SUCCESS')
    except Exception as e:
        return (fname, e)

def gen_slic(fnames, numSegments, output_path):
    """Run SLIC on a batch of images and store the segmentations in a directory"""
    print('Output path', output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    pool = multiprocessing.Pool(2)
    for fname, status in pool.imap_unordered(_task_slic, [(fname,numSegments,output_path) for fname in fnames], chunksize=5):
        if status == 'SUCCESS': print('SLIC', fname)
        else: print('ERR', fname, status)
    pool.close()
        
gen_slic(images, 200, os.path.join(DATA('zed-subset'), 'SLIC200'))