import pandas as pd

from GIANTS_personas_classification import (classify_market, classify_income, classify_user_type, classify_age, classify_mode_of_transport, classify_city, 
                                            classify_education, classify_gender, classify_trip_purpose, classify_family_size,
)


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
        '8. How many people  / family members live in your household? (for safety related questions) [Adults (18 and older)]': 'ADULTS',
        '8. How many people  / family members live in your household? (for safety related questions) [Kids (6-17)]': 'KIDS',
        '8. How many people  / family members live in your household? (for safety related questions) [Toddlers (1-5)]': 'TODDLERS',
        '8. How many people  / family members live in your household? (for safety related questions) [Infants (younger than 1)]': 'INFANTS',
        # Adding the vehicle features renaming
        '55. How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Additional Heating]': 'Additional Heating',
        '55. How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Air Conditioning]': 'Air Conditioning',
        '55. How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Cargo / Passenger capacity]': 'Cargo Capacity',
        '55. How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Price]': 'Price',
        '55. How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Tailorable (vehicle modifications made by the user) changes in seating and cargo space]': 'Tailorability',
        '55. How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Doors]': 'Doors',
        '55. How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Charging Infrastructure]': 'Charging Infrastructure',
        '55. How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Safety Features (in general)]': 'Safety Features General',
        '55. How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Vehicle Aesthetics and Design]': 'Aesthetics and Design',
        '56.  How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Price]': 'Price 2',
        '56.  How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Safety features (in general)]': 'Safety Features General 2',
        '56.  How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Anti-theft features]': 'Anti-Theft Features',
        '56.  How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Range (cover longer distances without charging)]': 'Range',
        '56.  How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Rapid charging]': 'Rapid Charging',
        '56.  How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Swappable batteries for charging (lighter, ability to self-swap)]': 'Swappable Batteries',
        '56.  How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Comfort features - Space (legroom and headspace)]': 'Comfort Space',
        '56.  How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Comfort Features – Acoustic (shield from noise)]': 'Acoustic Comfort',
        '56.  How important do you rank the following features (1 = Not Important, 9 = Extremely Important) [Solar panels]': 'Solar Panels',
        '57.  How important do you rank the following safety features (1 = Not Important, 9 = Extremely Important) [Anti-Lock Braking Systems (ABS)]': 'ABS',
        '57.  How important do you rank the following safety features (1 = Not Important, 9 = Extremely Important) [Driving in reverse / Backing up alarm]': 'Reverse Alarm',
        '57.  How important do you rank the following safety features (1 = Not Important, 9 = Extremely Important) [Headrests]': 'Headrests',
        '57.  How important do you rank the following safety features (1 = Not Important, 9 = Extremely Important) [Side/rear-view mirrors]': 'Mirrors',
        '57.  How important do you rank the following safety features (1 = Not Important, 9 = Extremely Important) [Airbags]': 'Airbags',
        '57.  How important do you rank the following safety features (1 = Not Important, 9 = Extremely Important) [Crumple zones]': 'Crumple Zones',
        '57.  How important do you rank the following safety features (1 = Not Important, 9 = Extremely Important) [Collapsable steering column]': 'Collapsible Steering Column'
    })
    
    

    
    # Print the column names of the DataFrame as a list
    print(list(df.columns))

    # Convert family size columns to numeric (convert non-numeric to NaN and then fill with 0)
    family_columns = ['ADULTS', 'KIDS', 'TODDLERS', 'INFANTS']
    df[family_columns] = df[family_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

    # Calculate total family members
    df['total_family_members'] = (
        df['ADULTS'] + df['KIDS'] + df['TODDLERS'] + df['INFANTS']
    )
    # Apply classification functions
    df['age'] = df['AGE'].apply(classify_age)
    df['market'] = df['COUNTRY'].apply(classify_market)
    df['gender'] = df['GENDER'].apply(classify_gender)
    df['city_type'] = df['CITY'].apply(classify_city)
    df['user_type'] = df['USER TYPE'].apply(classify_user_type)
    df['education'] = df['EDUCATION'].apply(classify_education)
    df['income'] = df['INCOME'].apply(classify_income)
    df['mode'] = df['PRIMARY TRANSPORT MODE'].apply(classify_mode_of_transport)
    df['purpose'] = df['PURPOSE'].apply(classify_trip_purpose)
    df['family_size_category'] = df['total_family_members'].apply(classify_family_size)

    print(df['family_size_category'].unique())
    return df
    
