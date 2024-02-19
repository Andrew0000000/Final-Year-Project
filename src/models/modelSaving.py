import os
import pickle

def save_model(model, filename):
    # directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # full path for the model file
    models_dir = os.path.join(current_dir, 'trained_models', filename)
    
    # save model
    with open(models_dir, 'wb') as file:
        pickle.dump(model, file)