import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Age distribution
def plot_age_distribution(df):
    # Define the logical order for age groups
    age_order = ['18-29', '30-44', '45-59', '60-78', '>78']

    # Convert the 'AGE' column to a categorical type with the defined order
    df['AGE'] = pd.Categorical(df['AGE'], categories=age_order, ordered=True)

    # Age distribution in logical order
    age_distribution = df['AGE'].value_counts().sort_index()
    print(age_distribution)

    # Visualize the age distribution
    plt.figure(figsize=(8,6))
    age_distribution.plot(kind='bar', color='skyblue')
    plt.title('Age Distribution')
    plt.xlabel('Age Group')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

# Market distribution
def plot_market_distribution(df):
    
    # Market distribution in logical order
    market_distribution = df['Market'].value_counts()
    print("Market distribution:\n", market_distribution)

    # Plot market distribution
    plt.figure(figsize=(8,6))
    market_distribution.plot(kind='bar', color='lightgreen')
    plt.title('Market Distribution (Advanced vs. Emerging)')
    plt.xlabel('Market Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()
    

    return plt  # Ensure the figure is returned for further use

def plot_income_distribution(df):
    # Define the logical order for income categories
    income_order = ['Lower Income', 'Middle Income', 'Upper Income']

    # Convert the 'INCOME' column to a categorical type with the defined order
    df['INCOME'] = pd.Categorical(df['INCOME'], categories=income_order, ordered=True)

    # Check if 'INCOME' column is processed and has valid values
    print(df['INCOME'].value_counts(dropna=False))

    # Income distribution in logical order
    income_distribution = df['INCOME'].value_counts().sort_index()

    print("Income distribution:\n", income_distribution)  # Debugging output

    # Visualize the income distribution
    plt.figure(figsize=(8,6))
    income_distribution.plot(kind='bar', color='orange')
    plt.title('Income Distribution')
    plt.xlabel('Income Category')
    plt.ylabel('Count')
    plt.xticks(rotation=45)

# User Type distribution
def plot_user_type_distribution(df):
    # Define the logical order for user types
    user_type_order = ['Private User', 'Fleet Operator', 'Manufacturer/OEM', 'Public Authority', 'Research/University', 'Nonprofit', 'Other']

    # Convert the 'User Category' column to a categorical type with the defined order
    df['USER TYPE'] = pd.Categorical(df['USER TYPE'], categories=user_type_order, ordered=True)

    # User Type distribution in logical order
    user_type_distribution = df['USER TYPE'].value_counts().sort_index()
    print(user_type_distribution)

    # Visualize the user type distribution
    plt.figure(figsize=(8,6))
    user_type_distribution.plot(kind='bar', color='purple')
    plt.title('User Type Distribution')
    plt.xlabel('User Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

   
