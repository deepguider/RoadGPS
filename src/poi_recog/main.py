import _init_paths
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGE = True

from timeit import default_timer as timer
from keras_yolo3.yolo import YOLO
from logos import detect_logo, match_logo, detect_logo_demo
#from similarity import load_brands_compute_cutoffs
from utils import load_extractor_model, load_features, model_flavor_from_name, parse_input

sim_threshold = 0.95
output_txt = 'out.txt'


def test(filename, timestamp):
    """
    Test function: runs pipeline for a small set of input images and input
    brands.
    """
    yolo = YOLO(**{"model_path": './model/keras_yolo3/model_data/yolo_weights_logos.h5',
                "anchors_path": './model/keras_yolo3/model_data/yolo_anchors.txt',
                "classes_path": './data/preprocessed/classes.txt',
                "score" : 0.05,
                "gpu_num" : 1,
                "model_image_size" : (416, 416),
                })
    save_img_logo, save_img_match = True, True
    
    test_dir = os.path.join(os.path.dirname(__file__), 'data/test')

    # get Inception/VGG16 model and flavor from filename
    model_name, flavor = model_flavor_from_name(filename)
    ## load pre-processed features database
    features, brand_map, input_shape = load_features(filename)

    ## load inception model
    model, preprocess_input, input_shape = load_extractor_model(model_name, flavor)
    my_preprocess = lambda x: preprocess_input(utils.pad_image(x, input_shape))
     
    images = [ p for p in os.listdir(os.path.join(test_dir, 'input/'))] #if p.endswith('.jpg')]
    images_path = [ os.path.join(test_dir, 'input/', p) for p in images]

    start = timer()
    times_list = []
    img_size_list = []
    candidate_len_list = []
    for i, img_path in enumerate(images_path):
        outtxt = img_path

        ## find candidate logos in image
        prediction, image = detect_logo(yolo, img_path, save_img = True,
                                          save_img_path = test_dir, postfix='_logo')

        ## match candidate logos to input
        #outtxt, times = match_logo(image, prediction, (model, my_preprocess),
        #        outtxt, (feat_input, sim_cutoff, bins, cdf_list, input_labels),
        #        save_img = save_img_match, save_img_path=test_dir, timing=True)

        img_size_list.append(np.sqrt(np.prod(image.size)))
        candidate_len_list.append(len(prediction))
        #times_list.append(times)

    end = timer()
    print('Processed {} images in {:.1f}sec - {:.1f}FPS'.format(
            len(images_path), end-start, len(images_path)/(end-start)
           )) 
    print(f'Timestamp : {timestamp}')


def initialize(filename):
    
    yolo = YOLO(**{"model_path": './model/keras_yolo3/model_data/yolo_weights_logos.h5',
                "anchors_path": './model/keras_yolo3/model_data/yolo_anchors.txt',
                "classes_path": './data/preprocessed/classes.txt',
                "score" : 0.05,
                "gpu_num" : 1,
                "model_image_size" : (416, 416),
                })
    
    return yolo


if __name__ == '__main__':
    timestamp = 123.456
    filename = './model/inception_logo_features_200_trunc2.hdf5'
    #test(filename, timestamp)
    model = initialize(filename)
    pred, timestamp = detect_logo_demo(model, './data/test/input/test_starbucks.png', timestamp)
    print(pred)
    print(timestamp)
    '''
    image = cv2.imread('./data/test/input/test_starbucks.png')
    pred, timestamp = detect_logo_demo('./data/test/input/test_starbucks.png', timestamp)
    print(pred, timestamp)
    '''
