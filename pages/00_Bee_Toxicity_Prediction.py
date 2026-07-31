import pickle
import pandas as pd
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw

from utils import extract_lipinski_and_other_descriptors_from_txt
from constants import LABELS, COLUMNS, POSSIBLE_NULL_COLUMNS, SINGLE_UNIQUE_VALUE_COLUMNS


# Require user authentication
if not st.user.is_logged_in:
    st.error("Please log in to access the app.")
    st.stop()


@st.cache_resource
def load_model(model_path):
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)

    return model


CLASSIFICATION_MODEL = "BM_unscaled_unbalanced"
IMPUTER = "imputer_model"
OHE_MODEL = "onehot_encoder.pkl"



st.title("Bee Toxicity Classification")

st.subheader("Enter Chemical Structure")

smiles = st.text_input(
    "SMILES string",
    placeholder="Enter a SMILES string, for example: C[N+]1(C)CCCCC1.[Cl-]",
    help="Enter one SMILES string describing the chemical structure.",
)

if smiles.strip():

    # Select pesticide type
    pesticide_type = st.selectbox(
        "Select the pesticide type",
        ("Herbicide", "Fungicide", "Insecticide", "Other"),
        index=None,
        placeholder="Select pesticide type..."
    )


    # Select PPDB level
    ppdb_level = st.selectbox(
        "PPDB Level",
        ("0", "1", "2"),
        index=None,
        placeholder="Select PPDB level..."
    )



    # Select toxicity type
    toxicity_type = st.selectbox(
        "Toxicity Type",
        ("Contact", "Oral", "Other"),
        index=None,
        placeholder="Select toxicity type..."
    )




    if st.button("Predict Toxicity"):

        if pesticide_type is None or ppdb_level is None or toxicity_type is None:
            st.warning("Please complete all selections.")

        else:

            try:
                # Validate the SMILES and create the descriptor dataframe
                molecule, descriptor_df = extract_lipinski_and_other_descriptors_from_txt(
                    smiles.strip()
                )
            except ValueError:
                st.error("Invalid SMILES string. Please check the structure and try again.")
                st.stop()
            
            canonical_smiles = Chem.MolToSmiles(molecule)
            st.code(canonical_smiles, language="text")
            molecule_image = Draw.MolToImage(molecule)

            st.success("✅ SMILES file uploaded and validated successfully.")
            st.markdown("#### 🧪 Detected SMILES")
            st.image(
                molecule_image,
                caption="Molecular Structure",
                width=350
            )

            
            # Impute the null values
            imputer = load_model(IMPUTER)
            descriptor_df[POSSIBLE_NULL_COLUMNS] = imputer.transform(descriptor_df[POSSIBLE_NULL_COLUMNS])

            # Drop columns with a single unique value
            descriptor_df_cleaned = descriptor_df.drop(columns=SINGLE_UNIQUE_VALUE_COLUMNS+["SMILES"])
        

            input_data = {
                "herbicide": int(pesticide_type == "Herbicide"),
                "fungicide": int(pesticide_type == "Fungicide"),
                "insecticide": int(pesticide_type == "Insecticide"),
                "other_agrochemical": int(pesticide_type == "Other"),
                "ppdb_level": int(ppdb_level)
            }

            input_df = pd.DataFrame([input_data],columns=COLUMNS)


            # OHE the categorical data and attach
            onehot_encoder = load_model(OHE_MODEL)
            encoded_data = onehot_encoder.transform([[toxicity_type]])
            encoded_df = pd.DataFrame(encoded_data, columns=onehot_encoder.get_feature_names_out(['toxicity_type']), index=input_df.index)
            final_df = pd.concat([input_df, descriptor_df_cleaned, encoded_df], axis=1)


            X_test = final_df.copy()

            with st.spinner("Predicting bee toxicity... 🐝"):
                classification_model = load_model(CLASSIFICATION_MODEL)
                y_pred = classification_model.predict(X_test)
                predicted_class = y_pred[0]

            st.toast("Processing Completed ✅")

            if predicted_class == 0:
                st.success(f"{LABELS.get(predicted_class)}")
            else:
                st.error(f"{LABELS.get(predicted_class)}")

else:
    st.info("Enter a SMILES string to get started.")
