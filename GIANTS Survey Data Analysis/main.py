
import pandas as pd
import matplotlib.pyplot as plt
plt.ion()  # Interactive mode on
# Importing necessary modules and functions from your files
from GIANTS_data_load_and_preprocessing import load_data, preprocess_data
from GIANTS_personas_classification import classify_persona, apply_persona_classification
from GIANTS_kano_analysis import get_feature_names, prepare_kano_data, apply_kano_scoring, calculate_kano_averages, plot_kano_results, plot_kano_by_age_group
from GIANTS_survey_demographics import plot_age_distribution, plot_market_distribution, plot_income_distribution, plot_user_type_distribution

# Load data
def main():

    show_plots = True  # Set to False if you don't want to display the figures
    # Step 1: Load the data
    file_path = "C:/Users/TomiNordi2m/OneDrive - i2m Unternehmensentwicklung GmbH/Documents/Python/GIANTS Survey Data Analysis/2024.08.08 GIANTS project_ Survey Response Data.xlsx"
    df = load_data(file_path)
    
    
    # Step 2: Preprocess the data
    df = preprocess_data(df)

    # Step 3: Prepare Kano data
    df_kano = prepare_kano_data(df)

    # Step 4: Get feature names for Kano analysis
    feature_names = get_feature_names()

    # Step 5: Apply Kano scoring
    df_kano = apply_kano_scoring(df_kano, feature_names)

    # Step 6: Calculate Kano averages
    df_averages = calculate_kano_averages(df_kano, feature_names)

    # Step 7: Plot Kano results (set show_plot to False if you don't want immediate display)
    plot_kano_results(df_averages, show_plot=show_plots)

    # Step 8: Plot Kano analysis for each age group (set show_plot to False to avoid showing)
    plot_kano_by_age_group(df, df_kano, feature_names, show_plot=show_plots)

    
    # Step 9: Plot the market distribution
    plot_market_distribution(df, show_plot = show_plots)

    # Plot income distribution
    plot_income_distribution(df, show_plot = show_plots)

    # Plot age distribution
    plot_age_distribution(df, show_plot = show_plots)

    #Plot user type distribution
    plot_user_type_distribution(df, show_plot = show_plots)
    

    df = apply_persona_classification(df)
    
    # Print the first few rows to check the classified personas
    print(df[['Persona']].head())

    plt.show(block=True)
if __name__ == "__main__":
    main()

