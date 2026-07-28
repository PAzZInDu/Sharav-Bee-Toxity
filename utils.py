import numpy as np
import pandas as pd

from rdkit import Chem
from rdkit.Chem import Descriptors


def extract_lipinski_and_other_descriptors_from_txt(smiles):
    """
    Calculate RDKit descriptors.

    Parameters
    ----------
    file_path : str
        smiles 
        
    Returns
    -------
    pandas.DataFrame
        A one-row DataFrame containing the SMILES string and its descriptors.
    """

    molecule = Chem.MolFromSmiles(smiles)

    if molecule is None:
        raise ValueError(f"Invalid SMILES string: {smiles}")

    descriptor_data = {
        "SMILES": smiles
    }

    for descriptor_name, descriptor_function in Descriptors._descList:
        try:
            descriptor_data[descriptor_name] = (
                descriptor_function(molecule)
            )
        except Exception as error:
            print(
                f"Could not calculate {descriptor_name}: {error}"
            )
            descriptor_data[descriptor_name] = np.nan

    return pd.DataFrame([descriptor_data])