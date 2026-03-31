import streamlit as st
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import plotly.graph_objects as go
from sentence_transformers import SentenceTransformer
from psmiles import PolymerSmiles as PS
from streamlit_ketcher import st_ketcher
from rdkit import Chem
import config

# --- 1. DNN Architecture ---
class BiodegradationDNN(nn.Module):
    def __init__(self, input_dim=601, layers_dims=[200, 729], dropout_rates=[0.2, 0.2]):
        super(BiodegradationDNN, self).__init__()
        layers = []
        current_dim = input_dim
        for h_dim, drop_rate in zip(layers_dims, dropout_rates):
            layers.append(nn.Linear(current_dim, h_dim))
            layers.append(nn.LeakyReLU()) 
            layers.append(nn.BatchNorm1d(h_dim))
            layers.append(nn.Dropout(drop_rate))
            current_dim = h_dim
        self.network = nn.Sequential(*layers)
        self.output_layer = nn.Linear(current_dim, 1)
        self.sigmoid = nn.Sigmoid() 

    def forward(self, x):
        features = self.network(x)
        out = self.output_layer(features)
        return self.sigmoid(out)
    # Try this ONLY if your training labels were 0-100

# --- 2. Resource Loading with Resilient Fallback ---
@st.cache_resource
def load_resources():
    device = torch.device("cpu")
    
    # Try the two most likely public mirrors for PolyBERT
    bert_model = None
    # 'anshu-6211' is a known public mirror for the kuelumbus weights
    for model_id in ["anshu-6211/polybert-transformer", "sentence-transformers/all-MiniLM-L6-v2"]:
        try:
            bert_model = SentenceTransformer(model_id)
            break
        except Exception:
            continue
            
    if bert_model is None:
        return None, None, device

    model = BiodegradationDNN()
    try:
        model.load_state_dict(torch.load(config.get_model_path(), map_location=device))
        model.eval()
    except Exception as e:
        st.error(f"Error loading Final_Polymer_Transfer_Model.pt: {e}")
        return bert_model, None, device
        
    return bert_model, model, device

# --- 3. UI Setup ---
st.set_page_config(page_title="Polymer Biodegradation Predictor", layout="wide")
st.title("🧬 Polymer Biodegradation Predictor")

bert_model, predictor, device = load_resources()

if bert_model is None:
    st.error("🚨 Critical Error: Could not reach HuggingFace to load the PolyBERT transformer. Please check your internet connection or firewall.")
    st.stop()

# --- 4. Main Simulator Interface ---
st.sidebar.header("⏱️ Simulation Settings")
selected_days = st.sidebar.multiselect(
    "Predict specific days:",
    options=list(range(1, 102)),
    default=[28, 60, 101]
)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Draw Your Polymer & Visualize Structures")
    smiles_input = st.text_input("PSMILES String", "[*]CC(C)CC[*]")
    drawn_smiles = st_ketcher(smiles_input)
    final_smiles = drawn_smiles if drawn_smiles else smiles_input

with col2:
    if final_smiles and predictor:
        try:
            # Canonicalize
            ps = PS(final_smiles)
            canon_smiles = str(ps.canonicalize)
            
            # Step 2: Generate 600D Fingerprint
            fp = bert_model.encode([canon_smiles])[0]
            
            # If fallback model (384D) is used, pad it to 600D for the DNN
            if len(fp) < 600:
                fp = np.pad(fp, (0, 600 - len(fp)), 'constant')

            
            # Step 3: Run Simulation (1-101 Days)
            days_axis = np.arange(1, 102)
            curve_preds = []

            with torch.no_grad():
                for d in days_axis:
                    # 1. Combine 600D Fingerprint + 1D Time (Total 601 features)
                    input_vec = torch.tensor(np.append(fp, d)).float().unsqueeze(0).to(device)
                    
                    # 2. Get decimal prediction (0.0 to 1.0) from the Sigmoid layer
                    raw_pred = predictor(input_vec).item() 
                    
                    # 3. Scale to percentage for display (e.g., 0.97 -> 97.0)
                    curve_preds.append(raw_pred * 100)
            
            # # Step 3: Run Simulation (1-101 Days)
            # days_axis = np.arange(1, 102)
            # curve_preds = []
            # # with torch.no_grad():
            # #     for d in days_axis:
            # #         # Input = 600D FP + 1D Time
            # #         input_vec = torch.tensor(np.append(fp, d)).float().unsqueeze(0).to(device)
            # #         curve_preds.append(predictor(input_vec).item() * 100)
            # # Updated Code
            # with torch.no_grad():
            #         for d in days_axis:
            #             input_vec = torch.tensor(np.append(fp, d)).float().unsqueeze(0).to(device)
            #             # If 0.96 means 96%, we just display the raw model output as a percentage
            #             raw_pred = predictor(input_vec).item() 
            #             curve_preds.append(raw_pred * 100)  

            # # Display Selected Day Metrics
            # st.subheader("2. Prediction Results")
            # if selected_days:
            #     data = {"Day": selected_days, "Biodegradation (%)": [f"{curve_preds[d-1]:.2f}%" for d in selected_days]}
            #     st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)
            #2. Prediction Results with Increased Font Size ---
            st.subheader("2. Prediction Results")

            if selected_days:
                # Prepare the data based on your specific days
                data = {
                    "Day": selected_days, 
                    "Biodegradation (%)": [f"{curve_preds[d-1]:.2f}%" for d in selected_days]
                }
                df_results = pd.DataFrame(data)

                # Add CSS to target the table font specifically
                st.markdown(
                    """
                    <style>
                    /* This targets all table cells and headers in the app */
                    table {
                        font-size: 22px !important;
                    }
                    th {
                        font-size: 24px !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Use st.table instead of st.dataframe for easier CSS styling
                st.table(df_results)
            # Step 6: Visualise Sigmoid Kinetic Curve
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=days_axis, y=curve_preds, mode='lines', line=dict(color='#00CC96', width=4)))
            
            if selected_days:
                fig.add_trace(go.Scatter(
                    x=selected_days, y=[curve_preds[d-1] for d in selected_days],
                    mode='markers', marker=dict(color='red', size=10), name="Selected Points"
                ))

            fig.update_layout(
                title="Step 3: Kinetic Biodegradation Curve",
                xaxis_title="Time (Days)",
                yaxis_title="Biodegradation (%)",
                template="plotly_white",
                yaxis=dict(range=[0, 105])
            )
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Processing Error: {e}")
    elif not predictor:
        st.warning("Prediction model not found in /models folder.")