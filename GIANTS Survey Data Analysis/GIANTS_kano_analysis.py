import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# Set the font to serif globally
plt.rcParams["font.family"] = "sans-serif"

def get_feature_names():
    """Returns the list of feature names for Kano analysis."""
    return [
        "Heating System", "Air Conditioning", "Small Vehicle Cargo Capacity", 
        "Large Vehicle Cargo Capacity", "Tailorable", "ABS", 
        "Backing Up Alarm", "Headrests and Mirrors", "Crash Safety Features",
        "Passenger Capacity", "Doors", "Anti-theft", "Comfort Features", 
        "Comfort Features - Space", "Comfort Features - Acoustic",
        "Compact Size", "Vehicle Aesthetics", "General Swappable Batteries",
        "Self-Swappable Batteries", "Power Capacity", "Rapid Charging", 
        "Charging Infrastructure", "Battery Enclosure", "Solar Panels"
    ]

def prepare_kano_data(df):
    """Prepares the Kano-related columns from the DataFrame."""
    df_kano = df.iloc[:, 51:99]
    return df_kano

def apply_kano_scoring(df_kano, feature_names):
    """Applies Kano scoring to functional and dysfunctional responses."""
    
    # Scoring logic for functional and dysfunctional responses
    def score_functional(response):
        scoring = {"I dislike it": -2, "I can tolerate it": -1, "I am neutral": 0, "I expect it": 2, "I like it": 4}
        return scoring.get(response, 0)

    def score_dysfunctional(response):
        scoring = {"I like it": -2, "I expect it": -1, "I am neutral": 0, "I can tolerate it": 2, "I dislike it": 4}
        return scoring.get(response, 0)
    
    # Create a copy of df_kano to avoid working on a view
    df_kano = df_kano.copy()

    # Apply the scoring functions to the columns
    for i, feature_name in enumerate(feature_names):
        df_kano.loc[:, f'{feature_name}_functional_score'] = df_kano.iloc[:, 2*i].apply(score_functional)
        df_kano.loc[:, f'{feature_name}_dysfunctional_score'] = df_kano.iloc[:, 2*i + 1].apply(score_dysfunctional)
    
    return df_kano

def apply_kano_scoring_explicit(df_kano, kano_column_map):
    """Applies Kano scoring using explicit functional/dysfunctional column mapping."""
    def score_functional(response):
        scoring = {"I dislike it": -2, "I can tolerate it": -1, "I am neutral": 0, "I expect it": 2, "I like it": 4}
        return scoring.get(response, 0)

    def score_dysfunctional(response):
        scoring = {"I like it": -2, "I expect it": -1, "I am neutral": 0, "I can tolerate it": 2, "I dislike it": 4}
        return scoring.get(response, 0)

    df_kano = df_kano.copy()

    for feature_name, (func_col, dysfunc_col) in kano_column_map.items():
        df_kano[f"{feature_name}_functional_score"] = df_kano[func_col].apply(score_functional)
        df_kano[f"{feature_name}_dysfunctional_score"] = df_kano[dysfunc_col].apply(score_dysfunctional)

    return df_kano

def calculate_kano_averages(df_kano, feature_names):
    """Calculates the average functional and dysfunctional scores for each feature, including standard deviation."""
    average_functional_scores = []
    average_dysfunctional_scores = []
    functional_stddevs = []  # Standard deviations for functional
    dysfunctional_stddevs = []  # Standard deviations for dysfunctional

    for feature_name in feature_names:
        avg_func_score = df_kano[f'{feature_name}_functional_score'].mean()
        avg_dysfunc_score = df_kano[f'{feature_name}_dysfunctional_score'].mean()
        
        # Calculate standard deviations
        func_stddev = df_kano[f'{feature_name}_functional_score'].std()
        dysfunc_stddev = df_kano[f'{feature_name}_dysfunctional_score'].std()

        average_functional_scores.append(avg_func_score)
        average_dysfunctional_scores.append(avg_dysfunc_score)
        functional_stddevs.append(func_stddev)
        dysfunctional_stddevs.append(dysfunc_stddev)

    df_averages = pd.DataFrame({
        'Feature': feature_names, 
        'Average Functional Score': average_functional_scores, 
        'Average Dysfunctional Score': average_dysfunctional_scores,
        'Functional StdDev': functional_stddevs,  # Add functional standard deviation
        'Dysfunctional StdDev': dysfunctional_stddevs  # Add dysfunctional standard deviation
    })
    
    return df_averages

def plot_feature_means_with_std(df_averages):
    features = df_averages['Feature']
    functional_means = df_averages['Average Functional Score']
    dysfunctional_means = df_averages['Average Dysfunctional Score']
    functional_stddev = df_averages['Functional StdDev']
    dysfunctional_stddev = df_averages['Dysfunctional StdDev']
    
    x = np.arange(len(features))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(12, 10))

    # Add custom x-ticks
    ax.set_xticks(x)
    ax.set_xticklabels(features, rotation=90, fontsize=8)

    # Add gridlines
    ax.grid(True, linestyle='--', alpha=0.6)

    # Add a legend for functional/dysfunctional score interpretation
    ax.text(-1, -3.5, "Functional Scoring:\n-2: Dislike, -1: Tolerate, 0: Neutral, 2: Must-be, 4: Like", 
            fontsize=20, color='blue', ha='left', bbox=dict(facecolor='white', alpha=0.7))

    ax.text(-1, -4, "Dysfunctional Scoring:\n-2: Like, -1: Expect, 0: Neutral, 2: Tolerate, 4: Dislike", 
            fontsize=20, color='red', ha='left', bbox=dict(facecolor='white', alpha=0.7))

    # Add a legend
    ax.legend(loc='upper left', fontsize=12)

    # Add tight layout for better spacing
    plt.tight_layout()

    # Show the plot
    plt.show()

def plot_kano_results(df_averages, plot_title='Kano Model: Functional vs. Dysfunctional Scores'):
    """Plots Kano results using Plotly for interactive visualization, with standard deviation error bars."""
    fig = px.scatter(df_averages,
        x='Average Dysfunctional Score',
        y='Average Functional Score',
        text='Feature', 
        title=plot_title,
        #error_x='Dysfunctional StdDev',  # Add standard deviation for dysfunctional scores
        #error_y='Functional StdDev'  # Add standard deviation for functional scores
    )

    fig.update_layout(height=800, width=1400)  # Adjust height as needed
    


    # Custom axis labels
    dysfunctional_labels = ['Like', 'Must-be', 'Neutral', 'Tolerate', 'Dislike']
    functional_labels = ['Dislike', 'Tolerate', 'Neutral', 'Expect it', 'Like']

    fig.update_xaxes(
    tickvals=[-2, -1, 0, 2, 4],
    ticktext=dysfunctional_labels,
    title="Dysfunctional",
    tickfont=dict(size=18)  # Increased font size for x-axis labels
    )

    fig.update_yaxes(
    tickvals=[-2, -1, 0, 2, 4],
    ticktext=functional_labels,
    title="Functional",
    tickfont=dict(size=18)  # Increased font size for y-axis labels
    )
   

    fig.update_layout(
    xaxis_title=dict(
        text="Dysfunctional",
        font=dict(size=20)  # Adjust the size here
    ),
    yaxis_title=dict(
        text="Functional",
        font=dict(size=20)  # Adjust the size here
    )
    )
    
    fig.update_traces(textposition='bottom right', textfont=dict(size=14))

    # Add quadrant shapes and labels
    fig.add_shape(type="rect", x0=2, x1=4, y0=2, y1=4,
                  line=dict(color="LightSeaGreen"),
                  fillcolor="PaleTurquoise", opacity=0.3, layer="below")

    fig.add_shape(type="rect", x0=2, x1=4, y0=0, y1=2,
                  line=dict(color="LightCoral"),
                  fillcolor="LightSalmon", opacity=0.3, layer="below")

    fig.add_shape(type="rect", x0=0, x1=2, y0=2, y1=4,
                  line=dict(color="LightBlue"),
                  fillcolor="LightSteelBlue", opacity=0.3, layer="below")

    fig.add_shape(type="rect", x0=0, x1=2, y0=0, y1=2,
                  line=dict(color="Gray"),
                  fillcolor="LightGray", opacity=0.3, layer="below")

   # Quadrant annotations
    fig.add_annotation(
        text="One-dimensional",
        x=3,
        y=3.5,
        showarrow=False,
        font=dict(size=20, color="LightSeaGreen", family="Arial", weight="bold")
    )
    fig.add_annotation(
        text="Must-have",
        x=3,
        y=1,
        showarrow=False,
        font=dict(size=20, color="LightCoral", family="Arial", weight="bold")
    )
    fig.add_annotation(
        text="Attractive",
        x=1,
        y=3.5,
        showarrow=False,
        font=dict(size=20, color="Blue", family="Arial", weight="bold")
    )
    fig.add_annotation(
        text="Indifferent",
        x=1,
        y=1,
        showarrow=False,
        font=dict(size=20, color="Gray", family="Arial", weight="bold")
    )


    return fig

def plot_interactive_scatter_for_feature(df_kano, feature_name):
    # Extract the functional and dysfunctional scores for the specific feature
    functional_scores = df_kano[f'{feature_name}_functional_score']
    dysfunctional_scores = df_kano[f'{feature_name}_dysfunctional_score']

    # Create a scatter plot using Plotly
    fig = px.scatter(
        x=dysfunctional_scores, 
        y=functional_scores, 
        labels={"x": "Dysfunctional Score", "y": "Functional Score"},
        title=f'Functional vs. Dysfunctional Scores for {feature_name}'
    )

    # Customize axis ranges
    fig.update_xaxes(range=[-2, 4])
    fig.update_yaxes(range=[-2, 4])

    # Add quadrant shapes and labels
    fig.add_shape(type="rect", x0=2, x1=4, y0=2, y1=4,
                  line=dict(color="LightSeaGreen"),
                  fillcolor="PaleTurquoise", opacity=0.3, layer="below")

    fig.add_shape(type="rect", x0=2, x1=4, y0=0, y1=2,
                  line=dict(color="LightCoral"),
                  fillcolor="LightSalmon", opacity=0.3, layer="below")

    fig.add_shape(type="rect", x0=0, x1=2, y0=2, y1=4,
                  line=dict(color="LightBlue"),
                  fillcolor="LightSteelBlue", opacity=0.3, layer="below")

    fig.add_shape(type="rect", x0=0, x1=2, y0=0, y1=2,
                  line=dict(color="Gray"),
                  fillcolor="LightGray", opacity=0.3, layer="below")

    # Quadrant annotations
    fig.add_annotation(text="One-dimensional", x=3, y=3.5, showarrow=False, font=dict(size=16, color="LightSeaGreen"))
    fig.add_annotation(text="Must-have", x=3, y=1, showarrow=False, font=dict(size=16, color="LightCoral"))
    fig.add_annotation(text="Attractive", x=1, y=3.5, showarrow=False, font=dict(size=16, color="LightBlue"))
    fig.add_annotation(text="Indifferent", x=1, y=1, showarrow=False, font=dict(size=16, color="Gray"))

    return fig
  
def plot_kano_by_age_group(df, df_kano, feature_names):
    # Define the specific age groups we are interested in
    age_order = ['18-29', '30-44', '45-59', '60-78', '>78']

    # Filter out unwanted ages (e.g., singular ages, NaN)
    df_filtered = df[df['AGE'].isin(age_order)].copy()

    # List to store figures if needed later
    figures = []

    # Iterate through each specified age group
    for age_group in age_order:
        # Filter the original data for this age group
        df_age_group = df_filtered[df_filtered['AGE'] == age_group]
        
        # Filter the Kano data as well based on the indices of the filtered df
        df_kano_age_group = df_kano.loc[df_age_group.index]
        
        # Calculate the averages for this age group
        df_averages_age_group = calculate_kano_averages(df_kano_age_group, feature_names)
        
        # Plot the Kano results for this age group
        fig = plot_kano_results(df_averages_age_group, plot_title=f"Kano Analysis for Age Group {age_group}")
        
        # Optionally store the figure for later use
        figures.append(fig)

        fig.show()

      # Return all figures if needed for other operations
      
def plot_kano_with_leader_lines(df_averages, plot_title="Kano Analysis with Leader Lines"):
    import plotly.graph_objects as go

def plot_kano_results_new(df_averages, plot_title='Kano Model: Functional vs. Dysfunctional Scores'):
    feature_abbreviations = {
        "Passenger Capacity": "PCap", "Comfort Features - Space": "Space", "Air Conditioning": "AC",
        "Heating System": "Heat", "Crash Safety Features": "CSF", "ABS": "ABS", "Compact Size": "Size",
        "Small Vehicle Cargo Capacity": "Cargo-S", "Large Vehicle Cargo Capacity": "Cargo-L",
        "Power Capacity": "Power", "Rapid Charging": "RC", "General Swappable Batteries": "GSB",
        "Self-Swappable Batteries": "SSB", "Headrests and Mirrors": "H&M"
    }

    feature_categories = {
        "Comfort": ["Passenger Capacity", "Comfort Features - Space", "Compact Size"],
        "Safety": ["Crash Safety Features", "ABS", "Headrests and Mirrors"],
        "HVAC": ["Air Conditioning", "Heating System"],
        "Size": ["Small Vehicle Cargo Capacity", "Large Vehicle Cargo Capacity"],
        "Battery/Charging": ["Power Capacity", "Rapid Charging", "General Swappable Batteries", "Self-Swappable Batteries"]
    }

    category_colors = {
        "Comfort": "royalblue",
        "Safety": "firebrick",
        "HVAC": "forestgreen",
        "Size": "orange",
        "Battery/Charging": "darkviolet"
    }

    df_averages = df_averages.copy()
    df_averages['Abbreviation'] = df_averages['Feature'].map(feature_abbreviations)

    fig = go.Figure()

    for category, features in feature_categories.items():
        df_category = df_averages[df_averages['Feature'].isin(features)]
        fig.add_trace(go.Scatter(
            x=df_category['Average Dysfunctional Score'],
            y=df_category['Average Functional Score'],
            mode='markers+text',
            text=df_category['Abbreviation'],
            textposition='top center',
            marker=dict(size=12, color=category_colors[category]),
            name=category,
            showlegend=False
        ))

    fig.update_layout(
        height=800, width=1400, title=plot_title
    )

    fig.update_xaxes(
        tickvals=[-2, -1, 0, 2, 4],
        ticktext=["Like", "Must-be", "Neutral", "Tolerate", "Dislike"],
        title="Dysfunctional",
        tickfont=dict(size=18),
        title_font=dict(size=20)
    )
    fig.update_yaxes(
        tickvals=[-2, -1, 0, 2, 4],
        ticktext=["Dislike", "Tolerate", "Neutral", "Expect it", "Like"],
        title="Functional",
        tickfont=dict(size=18),
        title_font=dict(size=20)
    )

    # Quadrant backgrounds
    fig.add_shape(type="rect", x0=2, x1=4, y0=2, y1=4, fillcolor="PaleTurquoise", opacity=0.3, layer="below")
    fig.add_shape(type="rect", x0=2, x1=4, y0=0, y1=2, fillcolor="LightSalmon", opacity=0.3, layer="below")
    fig.add_shape(type="rect", x0=0, x1=2, y0=2, y1=4, fillcolor="LightSteelBlue", opacity=0.3, layer="below")
    fig.add_shape(type="rect", x0=0, x1=2, y0=0, y1=2, fillcolor="LightGray", opacity=0.3, layer="below")

    # Quadrant labels
    fig.add_annotation(text="One-dimensional", x=3, y=3.5, showarrow=False, font=dict(size=20, color="DarkCyan"))
    fig.add_annotation(text="Must-have", x=3, y=1, showarrow=False, font=dict(size=20, color="IndianRed"))
    fig.add_annotation(text="Attractive", x=1, y=3.5, showarrow=False, font=dict(size=20, color="RoyalBlue"))
    fig.add_annotation(text="Indifferent", x=1, y=1, showarrow=False, font=dict(size=20, color="DimGray"))

    # Custom legend annotation
    legend_text = "<b>Feature Category</b><br>"
    for category, features in feature_categories.items():
        color = category_colors[category]
        legend_text += f"<span style='color:{color}'>●</span> <b>{category}</b><br>"
        for feature in features:
            abbr = feature_abbreviations.get(feature, feature)
            legend_text += f"{abbr}: {feature}<br>"

    fig.add_annotation(
        text=legend_text,
        xref="paper", yref="paper",
        x=1.05, y=1,
        showarrow=False,
        align="left",
        font=dict(size=14),
        bgcolor="white", bordercolor="black", borderwidth=1
    )

    return fig
