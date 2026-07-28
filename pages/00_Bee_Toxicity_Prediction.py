import pickle
import pandas as pd
import streamlit as st

from utils import extract_lipinski_and_other_descriptors_from_txt


# Require user authentication
# if not st.user.is_logged_in:
#     st.error("Please log in to access the app.")
#     st.stop()


@st.cache_resource
def load_model(model_path):
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)

    return model




CLASSIFICATION_MODEL = "BM_unscaled_unbalanced"
IMPUTER = "imputer_model"
OHE_MODEL = "onehot_encoder.pkl"



LABELS = {0: "Non-Toxic", 1: "Toxic"}

COLUMNS = ["herbicide", "fungicide", "insecticide", "other_agrochemical", "ppdb_level"]
POSSIBLE_NULL_COLUMNS = ['MaxPartialCharge', 'MinPartialCharge', 'MaxAbsPartialCharge', 'MinAbsPartialCharge', 'BCUT2D_MWHI', 'BCUT2D_MWLOW', 'BCUT2D_CHGHI', 'BCUT2D_CHGLO', 'BCUT2D_LOGPHI', 'BCUT2D_LOGPLOW', 'BCUT2D_MRHI', 'BCUT2D_MRLOW']
SINGLE_UNIQUE_VALUE_COLUMNS = ['SMR_VSA8', 'SlogP_VSA9', 'fr_HOCCN', 'fr_azide', 'fr_azo', 'fr_barbitur', 'fr_benzodiazepine', 'fr_diazo', 'fr_dihydropyridine', 'fr_isocyan', 'fr_isothiocyan', 'fr_lactam', 'fr_nitroso']


st.title("Bee Toxicity Classification")

st.subheader("Upload Gene Features")

uploaded_file = st.file_uploader(
    "Upload SMILES text file",
    type=["txt"],
    accept_multiple_files=False,
)

if uploaded_file is not None:

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

            # Read the SMILES string from the text file
            smiles = uploaded_file.getvalue().decode("utf-8").strip()
            st.info(smiles)

            # Create the description dataframe
            descriptor_df = extract_lipinski_and_other_descriptors_from_txt(smiles)
            st.toast("SMILES Processed")
            
            # Impute the null values
            imputer = load_model(IMPUTER)
            descriptor_df[POSSIBLE_NULL_COLUMNS] = imputer.transform(descriptor_df[POSSIBLE_NULL_COLUMNS])
            st.toast("Null Values Imputed")

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
            st.toast("Final Dataframe Created")

            st.dataframe(final_df)

            X_test = final_df.copy()

            classification_model = load_model(CLASSIFICATION_MODEL)
            y_pred = classification_model.predict(X_test)
            predicted_class = y_pred[0]
            st.toast("Processing Completed")
            
            if y_pred == 0:
                st.success(f"{LABELS.get(predicted_class)}")
            else:
                st.warning(f"{LABELS.get(predicted_class)}")
                















else:
    st.info("Upload SMILES text file to get started.")
