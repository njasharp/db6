import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Check if the CSV file exists
if os.path.exists('game_type.csv'):
    # Load data from the CSV file
    data = pd.read_csv('game_type.csv')
    
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        body {background-color: #212121;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)




    # Streamlit app
    st.title("Game Cultural Fit Analysis")
    
    # Sidebar for selecting quadrant
    quadrant = st.sidebar.selectbox("Select Quadrant", df["Quadrant"].unique())
    
    st.sidebar.markdown("### Select Games to Display")

    # Get unique games for the current quadrant
    unique_games = df[df["Quadrant"] == quadrant]["Game"].unique()

    # Create a dictionary to store the state of each checkbox
    games_to_display = {}

    # Create a checkbox for each game
    for game in unique_games:
        games_to_display[game] = st.sidebar.checkbox(game, value=True)

    # Filter the dataframe based on selected games
    selected_games = [game for game, selected in games_to_display.items() if selected]
    filtered_df = df[df["Game"].isin(selected_games)]

    # Sidebar for selecting columns to display
    st.sidebar.markdown("### Select Columns to Display")

    # Get all columns from the dataframe
    all_columns = df.columns.tolist()

    # Create a dictionary to store the state of each checkbox
    columns_to_display = {}

    # Create a checkbox for each column
    for column in all_columns:
        columns_to_display[column] = st.sidebar.checkbox(column, value=True)

    # Create a list of selected columns
    selected_columns = [column for column, selected in columns_to_display.items() if selected]

    # Use selected_columns for further processing or display
    filtered_df = df[selected_columns]




    # Sidebar for selecting chart type
    st.sidebar.markdown("### Select Chart Type")
    chart_type = st.sidebar.selectbox(
        "Chart Type", 
        ["Pie Chart", "Bar Chart", "Line Chart"],
        index=0  # This sets "Pie Chart" as the default
    )
    
    # Filter data based on selected quadrant and games
    filtered_data = df[df["Quadrant"] == quadrant]
    filtered_data = filtered_data[filtered_data["Game"].isin(selected_games)]

    # Apply column selection
    filtered_data = filtered_data[selected_columns]

    # Display table
    st.write(f"### Games in {quadrant} Quadrant")
    st.dataframe(filtered_data.reset_index(drop=True))

    # Display charts
    st.write("### Charts for Selected Games and Columns")

    for column in selected_columns:
        if column in filtered_data.columns and filtered_data[column].nunique() > 1:
            st.write(f"#### {column} Distribution")
            column_counts = filtered_data[column].value_counts()
            
            if chart_type == "Bar Chart":
                st.bar_chart(column_counts)
            elif chart_type == "Line Chart":
                st.line_chart(column_counts)
            elif chart_type == "Pie Chart":
                fig, ax = plt.subplots()
                ax.pie(column_counts, labels=column_counts.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.pyplot(fig)

    # Sidebar for selecting column to map area for bottom chart
    st.sidebar.markdown("### Select Column for Overall Distribution Chart")
    overall_column = st.sidebar.selectbox(
        "Overall Column", 
        df.columns.tolist()
    )
    
    # Display overall bar charts for the selected column in the full dataset
    st.write("### Overall Chart for Selected Column in Full Dataset")
    
  
    if overall_column:
        if df[overall_column].dtype == 'object' and df[overall_column].nunique() > 1:
            st.write(f"#### {overall_column} Distribution in Full Dataset")
            column_counts = df[overall_column].value_counts()
            st.bar_chart(column_counts)
        else:
            st.write(f"No sufficient categorical data available for {overall_column}.")

    st.header("Game Cultural Fit Matrix")
    st.image("picgt.PNG")
    st.info("built by dw v1.2 6-27-24")
else:
    st.error("The file 'game_type.csv' was not found.")


