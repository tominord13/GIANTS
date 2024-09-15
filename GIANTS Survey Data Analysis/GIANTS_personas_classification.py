import pandas as pd

#Classification of Gender
def classify_gender(gender):
    if pd.isna(gender):
        return 'Unknown Gender'
    elif gender == 'Male':
        return 'Male'
    elif gender == 'Female':
        return 'Female'
    elif gender == 'Non-Binary':
        return 'Non-Binary'
    else:
        return 'Other Gendered Person'
    
#Classification of Market based on Country
# List of advanced market countries

advanced_market_countries = [
        'United States', 'Canada', 'United Kingdom', 'Germany', 'France',
        'Japan', 'Australia', 'Netherlands', 'Sweden', 'Switzerland', 
        'Austria', 'Belgium', 'Finland', 'Denmark', 'Norway', 'Singapore',
        'New Zealand', 'South Korea', 'Ireland', 'Italy', 'Spain', 'Malta',
        'Portugal', 'Greece', 'Luxembourg', 'Czech Republic', 'Poland',
        'Hungary', 'Slovakia', 'Slovenia', 'Estonia', 'Latvia', 'Lithuania',
        'Iceland', 'Cyprus', 'Hong Kong', 'Taiwan', 'Israel', 'United Arab Emirates'
    ]

emerging_market_countries = [
        'India', 'China', 'Brazil', 'South Africa', 'Russia', 'Philippines',
        'Thailand', 'Indonesia', 'Malaysia', 'Turkey', 'Mexico', 
        'Argentina', 'Vietnam', 'Nigeria', 'Kenya', 'Egypt', 'Peru',
        'Bangladesh', 'Pakistan', 'Cambodia', 'Nepal', 'Romania', 'Bulgaria',
        'Croatia', 'Serbia', 'Chile', 'Colombia', 'Kazakhstan', 'Ukraine',
        'Morocco', 'Saudi Arabia', 'Qatar', 'Oman', 'Kuwait', 'Bahrain',
        'Sri Lanka', 'Uzbekistan', 'Azerbaijan', 'Jordan', 'Lebanon',
        'Algeria', 'Tunisia', 'Ecuador', 'Bolivia', 'Paraguay', 'Uruguay',
        'Georgia', 'Armenia', 'Bosnia and Herzegovina', 'North Macedonia',
        'Montenegro', 'Botswana', 'Zambia', 'Ghana', 'Laos'
    ]
def classify_market(country):
    
    if country in advanced_market_countries:
        return 'Advanced Market'
    elif country in emerging_market_countries:
        return 'Emerging Market'
    else:
        return 'Unknown Market'



# Classification of Urban/Suburban/Rural based on Cities
# List of urban cities
urban_cities = [
    'Brussels', 'Birkirkara', 'Qormi', 'Graz', 'Nanterre - Ile de France', 
    'AMIENS', 'Amsterdam', 'Breda', 'Eindhoven', 'Amstelveen', 'Leuven',
    'Malmö', 'Gothenburg', 'Osteraker, Stockholm', 'Berlin', 'Bonn',
    'Lisbon', 'Phoenix', 'Raleigh', 'Madrid', 'London', 'Brisbane',
    'Rotterdam', 'Porto', 'Zurich', 'Vienna', 'Prague', 'CAPE TOWN',
    'München', 'Paris', 'Helsinki', 'Bangkok', 'Santa Rosa', 
    'Quezon City', 'Manila', 'Issy-les-Moulineaux', 'Penang', 'Kuala Lumpur',
    'Hoorn', 'Almere', 'Haarlem', 'Long Beach, CA', 'Bern CH3007',
    'Lübeck', 'Antwerp', 'Cachan', 'České Budějovice', 'Métropole Rouen Normandie',
    'Kharagpur', 'Mladá Boleslav', 'CLAMART', 'Velizy Villacoublay',
    'Guernsey', 'Chaville', 'Saint Quentin en Yvelines', 'Issy-les-moulineaux 92130',
    # Add more urban cities here as needed
]

# List of suburban cities
suburban_cities = [
    'Kungsbacka', 'Fleet operator, urban and peri urban set ups',
    'San Juan Capistrano, Ca', 'Naperville IL', 'Maarssenbroek', 
    'Moka', 'Saint Paul, Minnesota', 'Rochdale', 'Rabat', 'South Harting, Petersfield',
    'Billingham.Cleveland', 'Perth', 'Hamilton', 'Edinburgh', 'Saint Remy Les Chevreuse',
    'Vanves', 'Viroflay', 'Zebbug', 'Zabbar', 'Zittau', 'Vorchten',
    'Gent', 'Antony', 'Reinsberg', 'Mittweida', 'Floriana',
    'Kidderminster Rural', 'Santa Rosa', 'Trencin', 'Haarlem',
    'Gorkha', 'Saint Remy Les Chevreuse', 'Chevreuse', 'Penang',
    # Add more suburban cities here as needed
]

# List of rural cities
rural_cities = [
    'Kiruna', 'Ciro', 'Plauen', 'Portimão', 'Boekelo', 'SIX FOURS LES PLAGES', 
    'Góis', 'Torrox Costa', 'Witzenhausen', 'Kralendijk Bonaire', 'St Paul\'s Bay', 
    'The Villages, Florida', 'Hilversum', 'Springfield, MO', 'Maintal', 'Kiili', 
    'Heeswijk-Dinther', 'Phnom Penh', 'Udon Thani', 'Rostock', 'sintruiden',
    'Maribor', 'Hope Town, Elbow Cay, Abaco', 'Kingman', 'Rabat', 
    'Aveiro', 'Torino', 'Pasig City', 'Vienna', 'Crymych', 'Birkirkara', 'Qormi',
    'Hamrun', 'Sto. Tomas Batangas', 'Kaufbeuren', 'Viterbo', 'Velizy Villacoublay',
    'Dolany', 'Bělá pod Pradědem', 'Carmona City', 'Vientiane', 'Parañaque', 
    # Add more rural cities here as needed
]

# Helper function to classify respondents by City Type
def classify_city(city):
    if city in urban_cities:
        return 'Urban'
    elif city in suburban_cities:
        return 'Suburban'
    elif city in rural_cities:
        return 'Rural'
    else:
        return 'Unknown'


def classify_user_type(user_type):
    # Convert user_type to string and handle missing or null values
    if pd.isna(user_type):
        return 'Other'
    
    # Convert user_type to string, strip whitespace, and standardize format
    user_type = str(user_type).strip().lower()

    # Classify based on match with known types
    if 'private individual' in user_type or 'user' in user_type:
        return 'Private User'
    elif 'public authority' in user_type or 'government' in user_type:
        return 'Public Authority'
    elif 'fleet operator' in user_type or 'fleet' in user_type:
        return 'Fleet Operator'
    elif 'oem' in user_type or 'manufacturer' in user_type or 'engineering' in user_type:
        return 'Manufacturer/OEM'
    elif 'university' in user_type or 'research' in user_type:
        return 'Research/University'
    elif 'nonprofit' in user_type or 'private non-profit' in user_type:
        return 'Nonprofit'
    else:
        return 'Other'



#Classification of Age
def classify_age(age_range):
    if pd.isna(age_range):
        return 'Unknown Aged '
    elif age_range == '18-29':
        return 'Young '
    elif age_range in ['30-44', '45-59']:
        return 'Middle-Aged '
    elif age_range in ['60-78', '>78']:
        return 'Old '
    else:
        return 'Unknown Aged '
    
# Classification of Education Level
def classify_education(education):
    if education == 'Elementary school':
        return 'Elementary School'
    elif education == 'High school':
        return 'High School'
    elif education == 'Bachelor':
        return 'Bachelor'
    elif education == 'Master':
        return 'Master'
    elif education == 'PhD':
        return 'PhD'
    elif education == 'None':
        return 'No Formal Education'
    else:
        return 'Other'


def classify_income(income):
    # Convert income to string and handle missing or null values
    if pd.isna(income):
        return 'Unknown Income'
    
    # Convert income to string, strip whitespace, and standardize format
    income = str(income).strip()

    # Classify based on exact match with known ranges
    if income in ["0 - 2,500€", "2,500 - 5,000€", "5,000 - 10,000€", "10,000 - 25,000€"]:
        return 'Lower Income'
    elif income in ["25,000 - 40,000€", "40,000 - 75,000€"]:
        return 'Middle Income'
    elif income in ["75,000 - 125,000€", ">125,000€"]:
        return 'Upper Income'
    else:
        return 'Unknown Income'  # Default to 'Unknown Income' for unrecognized formats




#Classification of Vehicle Type
def classify_mode_of_transport(mode):
    # Convert to string and handle missing values
    mode = str(mode).strip().lower() if pd.notnull(mode) else "unknown"
    
    # Classify into specific vehicle types or categories
    if mode == "sedan (traditional passenger car)":
        return "Sedan"
    elif mode == "suv / truck":
        return "SUV/Truck"
    elif mode == "motorcycle / scooter":
        return "Motorcycle/Scooter"
    elif mode == "cargo bicycle":
        return "Cargo Bicycle"
    elif mode == "bicycle":
        return "Bicycle"
    elif mode == "walking":
        return "Walking"
    elif "public transportation" in mode:
        return "Public Transportation"
    elif mode == "e-scooter":
        return "E-Scooter"
    elif "lev" in mode or "renault twizy" in mode:
        return "Light Electric Vehicle"
    elif mode == "taxi":
        return "Taxi"
    else:
        return "Other"

def classify_trip_purpose(purpose):
    """Classifies the trip purposes for the primary mode of transport based on multiple choice answers."""
    
    # Ensure input is handled properly for missing or invalid data
    if pd.isnull(purpose):
        return "unknown"
    
    purpose = purpose.strip().lower()  # Ensure the response is standardized
    
    # Map multiple-choice responses to broader categories
    if purpose in ["commuting to work", "commuting to school"]:
        return "commuting"
    elif purpose in ["leisure activities", "recreation", "going to the gym", "entertainment"]:
        return "leisure"
    elif purpose in ["grocery shopping", "shopping for goods"]:
        return "shopping"
    elif purpose in ["running errands", "appointments", "personal business"]:
        return "errands"
    elif purpose in ["visiting friends", "visiting family", "social events"]:
        return "social/visiting"
    else:
        return "other"  # Catch-all for any other category



