import pickle
import os

def load_model(filename):
    # directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # full path for the model file
    models_dir = os.path.join(current_dir, 'trained_models', filename)
    
    # load model
    with open(models_dir, 'rb') as file:
        model = pickle.load(file)
    return model