import pandas as pd
from rdkit import Chem
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score, mean_absolute_error
import pickle
from typing import List


def calc_rdkitfp(smiles_list: List[str]) -> pd.DataFrame:
    rdkitfp_feat = []
    bitI_rdkit = {}
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        fp_rdkit = Chem.RDKFingerprint(mol, bitInfo=bitI_rdkit)
        rdkitfp_feat.append(fp_rdkit.ToList())
    rdkitfp_feat = pd.DataFrame(rdkitfp_feat)
    return rdkitfp_feat


def train(
    csv_path="data/delaney-rdkitfp.csv",
    model_path="data/model.pkl",
    scaler_path="data/scaler.pkl",
    alpha=0.1,
):
    df = pd.read_csv(csv_path)
    y = df["logS"]
    X = calc_rdkitfp(df["smiles"].values.tolist())
    sc = StandardScaler()
    X_std = sc.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_std, y)

    model = Lasso(alpha=alpha)
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    mae_train = mean_absolute_error(y_train, y_train_pred)
    mae_test = mean_absolute_error(y_test, y_test_pred)

    r2_train = r2_score(y_train, y_train_pred)
    r2_test = r2_score(y_test, y_test_pred)
    print(f"R2(train): {r2_train}, R2(test): {r2_test}")
    print(f"MAE(train): {mae_train}, MAE(test): {mae_test}")

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    with open(scaler_path, "wb") as f:
        pickle.dump(sc, f)


def predict_logS(
    smiles_list,
    model_path="src/streamlit_starter_kit/data/model.pkl",
    scaler_path="src/streamlit_starter_kit/data/scaler.pkl",
):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    X = calc_rdkitfp(smiles_list)
    X_std = scaler.transform(X)
    y_pred = model.predict(X_std)
    return y_pred


# train()
# smiles_list = ["CCO", "CCN", "CCOCC", "CCNCC"]
# logS = predict_logS(smiles_list)
