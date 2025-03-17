import streamlit as st
import pandas as pd
import numpy as np
from ml import predict_logS
from streamlit_ketcher import st_ketcher
import rpy2.robjects as ro
from rpy2.robjects import default_converter, conversion, pandas2ri

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

st.header("分子構造入力")

# uploaded_file = st.file_uploader("Choose a CSV file")
# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)
#     df["logS(pred)"] = predict_logS(df[" SMILES"].values.tolist())
#     st.write(df)

molecule = st.text_input("Molecule", "CCO")
smiles = st_ketcher(molecule)
logS = predict_logS([smiles])
st.write(f"logS: {logS[0]}")
