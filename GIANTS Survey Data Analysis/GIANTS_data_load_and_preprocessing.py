import pandas as pd
from sklearn.preprocessing import OneHotEncoder

from GIANTS_personas_classification import classify_market, classify_income, classify_user_type, classify_age, classify_mode_of_transport, classify_city, classify_education, classify_gender, classify_trip_purpose

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
        '6. You are completing this survey as: (*You will be directed to focused survey questions.)': 'USER TYPE',
        '7. What is the nearest equivalent to your highest obtained educational degree?': 'EDUCATION',
        '9.  Estimated annual household (family) income in 2023 in Euros (€/EUR)? (Link to EU Currency Converter)': 'INCOME',
        '14. What is your primary mode (most used for daily trips) of transportation? ': 'PRIMARY TRANSPORT MODE',
        '16. How do you generally use your primary mode of transportation? (Multiple answers allowed.)': 'PURPOSE',
    })
    
    # Print the column names of the DataFrame as a list
    print(list(df.columns))

    df['age'] = df['AGE'].apply(classify_age)
    df['market'] = df['COUNTRY'].apply(classify_market)
    df['gender'] = df['GENDER'].apply(classify_gender)
    df['city_type'] = df['CITY'].apply(classify_city)
    df['user_type'] = df['USER TYPE'].apply(classify_user_type)
    df['education'] = df['EDUCATION'].apply(classify_education)
    df['income'] = df['INCOME'].apply(classify_income)
    df['mode'] = df['PRIMARY TRANSPORT MODE'].apply(classify_mode_of_transport)
    df['purpose'] = df['PURPOSE'].apply(classify_trip_purpose)

    
    return df

    
