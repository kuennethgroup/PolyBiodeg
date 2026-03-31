# PolyBiodeg 🧬 : A Polymer Biodegradability Prediction Simulator

## 🔍 About the Project

**PolyBiodeg** is an interactive web-based simulator designed to enable the real-time prediction of polymer environmental behavior. Unlike traditional toxicity screening, this tool focuses on predicting the **kinetic biodegradation percentage** of a polymer over time. By leveraging deep learning and transfer learning from molecular data, the application allows researchers to input polymer structures and visualize their degradation pathways.

The application deploys a **Frozen-Layer Fine-Tuned Deep Neural Network (DNN)**. This model was specifically adapted to capture the unique structural characteristics of polymers to provide accurate, time-dependent biodegradation forecasts.

---

## 🧬 Key Features

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
* **Sigmoid Kinetic Curve:** The results are visualized as a **sigmoid kinetic biodegradation curve**, providing an intuitive assessment of how a polymer breaks down over its environmental lifespan.
* **Threshold Monitoring:** The simulator includes a **60% "Ready Biodegradability" threshold** marker to align with international standards.

---

## 🔬 Methodology & Model Training

The predictive engine behind PolyBiodeg is the result of advanced deep learning strategies:

* **Frozen-Layer Transfer Learning:** To overcome the challenge of limited polymer data, the model was initialized with weights from a Deep Neural Network pre-trained on the large **Tox21 molecular dataset**.
* **Architecture:** The model consists of an input layer for 601 features, followed by hidden layers (dimensions [200, 729]) utilizing **LeakyReLU** activations, **Batch Normalization**, and **Dropout** for robust generalization.
* **Output Layer:** A final **Sigmoid activation** bounds the predictions between 0.0 and 1.0, representing 0% to 100% biodegradation.
* **Optimization:** **Optuna** was utilized for comprehensive hyperparameter tuning, ensuring maximum predictive performance and stability.

---

## 🔗 References & Further Reading

* **PolyBERT Publication:** Christopher Kuenneth, Rampi Ramprasad: *polyBERT: a chemical language model to enable fully machine-driven ultrafast polymer informatics.* Nature Communications (2023).
* **PSMILES Documentation:** [PSMILES - Fun with P🙂s strings](https://psmiles.readthedocs.io/en/latest/)
* **Standard Methods:** OECD 301B Guidelines for Testing of Chemicals.
* **Transfer Learning in Chemistry:** [Transfer Learning for Molecular Property Prediction](https://pubs.acs.org/doi/10.1021/acs.jcim.0c00375)

---


 


   

      
