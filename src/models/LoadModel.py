import pickle

def load_model(filename):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    return model