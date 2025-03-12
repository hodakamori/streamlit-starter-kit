import streamlit as st
import pandas as pd
from ml import predict_logS
from streamlit_ketcher import st_ketcher


st.set_page_config(layout="wide")
st.title("Hello demoapp")

# uploaded_file = st.file_uploader("Choose a CSV file")
# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)
#     df["logS(pred)"] = predict_logS(df[" SMILES"].values.tolist())
#     st.write(df)

molecule = st.text_input("Molecule", "CCO")
smiles = st_ketcher(molecule)
logS = predict_logS([smiles])
st.write(f"logS: {logS[0]}")
