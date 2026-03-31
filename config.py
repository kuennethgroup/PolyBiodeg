import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
DATA_DIR = os.path.join(BASE_DIR, "data")
MOL_DATA_PATH = os.path.join(DATA_DIR, "Mol_DNN_cleaned.csv")
POL_DATA_PATH = os.path.join(DATA_DIR, "POL_DNN_data.csv")

# Model paths
MODEL_DIR = os.path.join(BASE_DIR, "models")
POLYMER_MODEL_PATH = os.path.join(MODEL_DIR, "Final_Polymer_Transfer_Model.pt")

def get_mol_data():
    return MOL_DATA_PATH

def get_pol_data():
    return POL_DATA_PATH

# Added for compatibility to stop the AttributeError
def get_data_path():
    return POL_DATA_PATH

def get_model_path():
    return POLYMER_MODEL_PATH