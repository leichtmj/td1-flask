import os, gdown
base_url = "http://download.tensorflow.org/models/object_detection/tf2/20200711/"
label_coco_url = "https://filesender.renater.fr/download.php?token=da7f1433-967c-4ff5-9213-deae261a6fab&archive_format=undefined&files_ids=29658162"

def download_model( model_name ) :
    """ Download model from TensorFlow .org if not exists extract and return
        path to model """
    url = f"{ base_url }{ model_name }" # Model URL
    model_path = f"models/{ model_name }" # Model zip path
    model_dir = model_path.replace(".tar.gz", "") # Model directory path
    label_path = None
    if not os.path.exists(model_dir) :
        # If not exists download model and extract
        gdown.cached_download(url , model_path , postprocess = gdown.extractall)
        # remove the zip file
        os.remove(model_path)
    
    # If 'coco' is in the model_name , download the labels
    if 'coco' in model_name :
        label_path = "models/mscoco_label_map.pbtxt"
        if not os.path.exists(label_path) :
            gdown.download(label_coco_url , label_path)
    if label_path is not None :
        return (os.path.join(model_dir , "saved_model") , label_path)
    else :
        return (os.path.join(model_dir , "saved_model") , 'No labels path available for this model.')