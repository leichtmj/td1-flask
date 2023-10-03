import numpy as np
import tensorflow as tf
import cv2
from src.utils import download_model
# Model to Use
model_name = "ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8.tar.gz"

# Load model from path (it will download from url if not exists locally )
model_path, labels_path = download_model( model_name )
model = tf.saved_model.load( model_path )
# labels = read_label_map( labels_path )

def process_image( image_path ) :
    # Read image and preprocess
    img= cv2.imread( image_path )
    h, w, _= img.shape
    img = cv2.cvtColor( img , cv2.COLOR_BGR2RGB )
    input_tensor = np.expand_dims( img , 0)
    
    # Predict from model
    resp = model( input_tensor )
    
    # Get the output of the prediction
    # Iterate over boxes , class_index and score list
    for boxes, classes, scores in zip ( resp ['detection_boxes'].numpy() , 
                                         resp ['detection_classes'] , 
                                         resp ['detection_scores'].numpy() ) :
        for box, cls, score in zip ( boxes , classes , scores ) : # Iterate over sub values in list
            if score > 0.1: # We are using only detection with confidence of over 0. xx
                ymin = int( box [0] * h )
                xmin = int( box [1] * w )
                ymax = int( box [2] * h )
                xmax = int( box [3] * w )
                # write classname for bounding box
                #cv2. putText (img , labels [cls] , (xmin , ymin -10) , cv2. FONT_HERSHEY_SIMPLEX , 1 , (0 , 255 , 0) , 1)
            # Draw on image
            cv2.rectangle( img, ( xmin , ymin ), ( xmax , ymax ), (128, 0, 128), 2)
    # Convert back to bgr and save image
    cv2.imwrite( image_path , cv2.cvtColor( img , cv2.COLOR_RGB2BGR ) )