# PolyBiodeg : A Polymer Biodegradability Prediction Webapp

## 🔍 About the Project

**PolyBiodeg** is an interactive web-based simulator designed to enable the real-time prediction of polymer environmental behavior. Unlike traditional toxicity screening, this tool focuses on predicting the **kinetic biodegradation percentage** of a polymer over time. By leveraging deep learning and transfer learning from molecular data, the application allows researchers to input polymer structures and visualize their degradation pathways.

The application deploys a **Frozen-Layer Fine-Tuned Deep Neural Network (DNN)**. This model was specifically adapted to capture the unique structural characteristics of polymers to provide accurate, time-dependent biodegradation forecasts.

---

## 🧬 Methodology & Model Training

### 🚀 **Input & Visualization**
* **Flexible Structure Input:** Users can construct polymer structures visually using an integrated **Ketcher** molecular editor or by manually entering **PSMILES** strings.
* **PSMILES Standard:** Structures must use the `[*]` notation to represent connection points for the repeating unit.
* **Automated Canonicalization:** The system automatically processes and canonicalizes the input structure to ensure a standardized chemical representation.

### 🧠 **Model Inference Pipeline**
* **High-Dimensional Fingerprinting:** The processed polymer structure is converted into a **600-dimensional PolyBERT fingerprint**, capturing complex chemical features.
* **Kinetic Prediction:** Using the trained DNN, the application predicts the biodegradation percentage as a function of time, ranging from **Day 1 to Day 101**.
* **Feature Integration:** The model takes a 601-dimensional input vector consisting of the 600D PolyBERT fingerprint plus a 1D time variable (day).

### 📈 **Interactive Simulation**
* **Multi-Day Analysis:** Users can select specific timeframes or multiple individual days to compare predicted biodegradation percentages.
* **Kinetic Curve:** The results are visualized as a **kinetic biodegradation curve**, providing an intuitive assessment of how a polymer breaks down over its environmental lifespan.
* **Threshold Monitoring:** The simulator includes a **60% "Ready Biodegradability" threshold** marker to align with international standards.

---

## 🔬 Methodology & Model Training

The predictive engine behind PolyBiodeg is the result of advanced deep learning strategies:

* **Frozen-Layer Transfer Learning:** To overcome the challenge of limited polymer data, the model was initialized with weights from a Deep Neural Network pre-trained on the large **Tox21 molecular dataset**.
* **Architecture:** The model consists of an input layer for 601 features, followed by hidden layers activations, **Batch Normalization**, and **Dropout** for robust generalization.
* **Optimization:** **Optuna** was utilized for comprehensive hyperparameter tuning, ensuring maximum predictive performance and stability.

---

## 🔗 References & Further Reading

* **PolyBERT Publication:** Christopher Kuenneth, Rampi Ramprasad: *polyBERT: a chemical language model to enable fully machine-driven ultrafast polymer informatics.* Nature Communications (2023).
* **PSMILES Documentation:** [PSMILES - Fun with P🙂s strings](https://psmiles.readthedocs.io/en/latest/)
* **Standard Methods:** OECD 301B Guidelines for Testing of Chemicals.
* **Transfer Learning in Chemistry:** [Transfer Learning for Molecular Property Prediction](https://pubs.acs.org/doi/10.1021/acs.jcim.0c00375)

---

## 📁 Repository Structure and File Descriptions

This repository is organized to separate the core interactive web application from the experimental model training notebooks. 

* **`PolyBiodeg.py`**: The main Python script that runs the Streamlit interactive web application. It handles the user interface, takes SMILES inputs, and generates the biodegradation kinetic curves.
* **`config.py`**: Contains the configuration settings, global variables, and path definitions required by the main application.
* **`requirements.txt`**: A list of all Python dependencies and exact library versions required to run the code (e.g., `numpy`, `streamlit`, `torch`).
* **`Dockerfile`**: Instructions for containerizing the application. This ensures the app runs consistently across any operating system without manual environment setup.
* **`README.md`**: This documentation file.
* **`data/`**: Directory containing the datasets used by the application.
  * `POL_DNN_data.csv`: The primary dataset containing polymer SMILES strings and their encoded features used by the web app for inference.
* **`models/`**: Directory containing the saved weights of the trained predictive models.
  * `Final_Polymer_Transfer_Model.pt`: The final, fine-tuned PyTorch model weights used by the web application to make real-time predictions.
* **`model_training_notebooks/`**: Directory containing the Jupyter notebooks and research files used during the thesis to train and evaluate the models (includes subfolders for Autogluon, Base DNN, and Few-Shot learning experiments).

---

## ⚙️ Installation Instructions

You can run this project locally using standard Python tools, or you can run it using Docker for a fully isolated environment.

### Option 1: Local Installation (via pip)
1. Ensure you have Python 3.10+ installed on your system.
2. Clone this repository and navigate to the root directory:
   ```bash
   git clone [https://github.com/kuennethgroup/PolyBiodeg.git](https://github.com/kuennethgroup/PolyBiodeg.git)
   cd PolyBiodeg
3. Create a virtual environment (Recommended):
  ```bash
   python -m venv venv
   source venv/bin/activate
4. Install dependencies:
   ```bash
   pip install -r requirements.txt

### Option 2: Installation via Docker
If you have Docker installed, you do not need to install Python or any dependencies locally.

1. Clone the Repository
   ```bash
   git clone [https://github.com/kuennethgroup/PolyBiodeg.git](https://github.com/kuennethgroup/PolyBiodeg.git)
   cd PolyBiodeg
2. Build the Docker image:
    ```bash
   docker build -t polybiodeg-app 

### Option 3: Running Instructions
1. Running Locally (Option 1)
   If you installed the project using the local pip method, ensure your virtual environment is activated, then run the following command from the root directory:
   ```bash
   streamlit run PolyBiodeg.py

# 🧪 Polymer Biodegradation Prediction using DNN + Transfer Learning

This project implements a **three-stage transfer learning pipeline** to predict polymer biodegradation using knowledge learned from small organic molecules.

---

## ⚙️ 1. Data Preprocessing & Input Engineering

- Organic Molecule Biodegradation data: 1700 Organic molecule data points \cite{Huang2022}:  https://pubs.acs.org/doi/10.1021/acs.est.2c01764
https://drive.google.com/file/d/1epl1Kskq8Nua8U1f-XNlBXQ6qhSD_cXo/view?usp=drive_link
- Polymer experimental biodegradation data: 80 experimental polymer data points \cite{Lin2025} : https://orcid.org/0000-0002-5683-5117
https://drive.google.com/file/d/1epl1Kskq8Nua8U1f-XNlBXQ6qhSD_cXo/view?usp=drive_link
- For data preprocesiing steps please follow the Suuporting information documents: /home/sunil/am2/PolyBiodeg_Ready/Supporting information/AM_Structral Clustering and reevalutaion of Tranfer learnig Mehod_Biodegradabilty.pdf

- **Molecular Fingerprints (600D):**
  - Polymer repeat units converted into fingerprint vectors (RDKit / custom encoding).
  
- **Time Feature (1D):**
  - Biodegradation is time-dependent → added `Days` as input.

- **Final Input:**

- **Noble Split (Critical):**
- 80% → Training + CV (64 polymers)
- 20% → Noble Test Set (16 polymers, completely unseen)

---

## 🚀 2. Training Approaches

### 🔹 Approach 1: Zero-Shot Learning
**Concept:** Direct transfer without training

- Load pre-trained molecular DNN (~1700 molecules)
- No weight updates
- Evaluate directly on polymer data


### 🔹 Approach 2: Full Fine-Tuning
**Concept:** Total adaptation to polymer domain

- Initialize with molecular weights
- Unfreeze ALL layers
- Optuna (1000 trials) for hyperparameter tuning
- 5-Fold Cross Validation

---

### 🔹 Approach 3: Frozen-Layer Few-Shot Learning (Best)
**Concept:** Preserve chemistry + adapt to polymers

- Freeze early layers (feature extraction)
- Train only deeper layers
- Low learning rate (~1e-4)

---

## 📊 3. Evaluation Strategy

### 🔹 Internal Validation (5-Fold CV)
- Metrics:
- R²
- RMSE
- MAE
- Mean ± Std ensures stability

---

### 🔹 External Validation (Noble Test Set)
- 16 completely unseen polymers
- True real-world performance

---

### 🔹 Kinetic Validation
- Generated 28-day biodegradation curves
- Checked for:
- Sigmoid shape
- OECD 60% threshold crossing

---

## 📁 Project Structure
AM2_Poly_biodegradability_Cluster/
│
├── Data/
├── Data_preprocessing_mol/
├── Data_preprocessing_polymer/
├── DNN_Models/
│ ├── Mol_DNN_Model/
│ ├── Polymeronly_Model/
│ ├── Fewshot_DNN_Model/
│ ├── Zeroshot_Model/
│ └── Data_Cleaned_MOL_DNN_Model/
 


   

      
