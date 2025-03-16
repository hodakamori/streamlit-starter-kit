import streamlit as st
import pandas as pd
from ml import predict_logS
from streamlit_ketcher import st_ketcher
from database import init_db, get_db
from models import Prediction

# Initialize database
init_db()

st.set_page_config(layout="wide")
st.title("Chemical Solubility Prediction")

# Prediction section
st.header("Make Prediction")
molecule = st.text_input("Molecule", "CCO")
smiles = st_ketcher(molecule)
logS = predict_logS([smiles])
st.write(f"Predicted logS: {logS[0]}")

# Save prediction button
if st.button("Save Prediction to Database"):
    with get_db() as db:
        # Convert numpy.float64 to Python float
        logs_value = float(logS[0])
        prediction = Prediction(smiles=smiles, logs_pred=logs_value)
        db.add(prediction)
        db.commit()
        st.success("Prediction saved successfully!")

# Display recent predictions
st.header("Recent Predictions")
with get_db() as db:
    recent_predictions = (
        db.query(Prediction).order_by(Prediction.created_at.desc()).limit(5).all()
    )

    if recent_predictions:
        predictions_data = {
            "SMILES": [p.smiles for p in recent_predictions],
            "Predicted logS": [p.logs_pred for p in recent_predictions],
            "Timestamp": [p.created_at for p in recent_predictions],
        }
        st.dataframe(pd.DataFrame(predictions_data))
