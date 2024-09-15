import pandas as pd
from sklearn.preprocessing import OneHotEncoder

from GIANTS_personas_classification import classify_market, classify_income, classify_user_type, classify_age, classify_mode_of_transport, classify_city

def load_data(file_path):
    # Load the dataset
    df = pd.read_excel(file_path)
    return df

def preprocess_data(df):
    # Rename columns for clarity
    df = df.rename(columns={
        '2. Age': 'AGE',
        '3. Country': 'COUNTRY',
        '1. Gender': 'GENDER',
        '4. City (*If you are completing this survey as a fleet operator, public authority, etc. the primary city of your operations / city you represent)': 'CITY',
        '9.  Estimated annual household (family) income in 2023 in Euros (€/EUR)? (Link to EU Currency Converter)': 'INCOME',
        '14. What is your primary mode (most used for daily trips) of transportation? ': 'PRIMARY TRANSPORT MODE',
    })
    print(list(df.columns))
    # Apply classification functions to the key features
    df['Market'] = df['COUNTRY'].apply(classify_market)
    df['INCOME'] = df['INCOME'].apply(classify_income)
    df['USER TYPE'] = df['USER TYPE'].apply(classify_user_type)
    df['AGE'] = df['AGE'].apply(classify_age)
    df['CITY TYPE'] = df['CITY'].apply(classify_city)

    # Convert 'PRIMARY TRANSPORT MODE' to string and handle missing values
    df['PRIMARY TRANSPORT MODE'] = df['PRIMARY TRANSPORT MODE'].astype(str).fillna('Unknown')

    # Now apply the classification function
    df['PRIMARY TRANSPORT MODE'] = df['PRIMARY TRANSPORT MODE'].apply(classify_mode_of_transport)
    
    
    # Define the categorical columns for encoding
    categorical_columns = ['AGE', 'INCOME', 'PRIMARY TRANSPORT MODE', 'Market', 'CITY TYPE']
    
    # Apply OneHotEncoder
    encoder = OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False)
    encoded_data = encoder.fit_transform(df[categorical_columns])
    
    # Create DataFrame with encoded data
    df_encoded = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_columns))
    
    return df_encoded

    
