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
    
    # Streamlit app
    st.title("Game Cultural Fit Analysis")
    
    # Sidebar for selecting quadrant
    quadrant = st.sidebar.selectbox("Select Quadrant", df["Quadrant"].unique())
    
    # Sidebar for selecting games to display
    st.sidebar.markdown("### Select Games to Display")
    games_to_display = st.sidebar.multiselect(
        "Games", 
        df[df["Quadrant"] == quadrant]["Game"].unique(), 
        default=df[df["Quadrant"] == quadrant]["Game"].unique()
    )
    
    # Sidebar for selecting columns to display
    st.sidebar.markdown("### Select Columns to Display")
    columns_to_display = st.sidebar.multiselect(
        "Columns", 
        df.columns.tolist(), 
        default=df.columns.tolist()
    )
    
    # Sidebar for selecting chart type
    st.sidebar.markdown("### Select Chart Type")
    chart_type = st.sidebar.selectbox(
        "Chart Type", 
        ["Bar Chart", "Line Chart", "Pie Chart"]
    )
    
    # Filter data based on selected quadrant and games
    filtered_data = df[(df["Quadrant"] == quadrant) & (df["Game"].isin(games_to_display))][columns_to_display]
    
    # Display table
    st.write(f"### Games in {quadrant} Quadrant")
    st.dataframe(filtered_data.reset_index(drop=True))
    
    # Display charts
    st.write("### Charts for Selected Games and Columns")

    for column in columns_to_display:
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

else:
    st.error("The file 'game_type.csv' was not found.")
    st.info("built by dw")