import streamlit as st
import pandas as pd
import numpy as np
from ml import predict_logS
from streamlit_ketcher import st_ketcher
import rpy2.robjects as ro
from rpy2.robjects import default_converter, conversion, pandas2ri
from database import init_db, get_db
from models import Prediction

st.set_page_config(layout="wide")
st.title("Streamlit with R Integration Demo")

# Rのサンプルコード実行セクション
st.header("Rによるデータ分析例")
if st.button("Rでヒストグラムを生成"):
    np.random.seed(42)
    data = np.random.normal(0, 1, 1000)
    df = pd.DataFrame({"value": data})

    with conversion.localconverter(default_converter + pandas2ri.converter):
        r_df = conversion.py2rpy(df)
        r_code = """
        function(dataframe) {
            hist_data <- hist(dataframe$value, plot=FALSE)
            list(
                breaks = hist_data$breaks,
                counts = hist_data$counts
            )
        }
        """

        r_func = ro.r(r_code)
        result = r_func(r_df)
        breaks = list(result["breaks"])
        counts = list(result["counts"])

    hist_data = pd.DataFrame({"breaks": breaks[:-1], "counts": counts})
    st.bar_chart(hist_data.set_index("breaks"))

# Initialize database
init_db()

st.set_page_config(layout="wide")

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
