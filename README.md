# Dash_surname_Data_Visualization


<img width="1511" alt="DASH_FRANCE_SURNAME" src="https://github.com/user-attachments/assets/1c8a7a38-3e47-403e-950a-9fc9d96241c1">

## Steps to Use the Application

- **Step 1**: Enter a first name of your choice.
  
- **Step 2**: Select a gender (Man or Woman).

- **Step 3**: Choose the date range that suits your needs.

- **Step 4**: Analyze the graph displaying the quantity of the chosen first name.

- **Step 5**: Navigate the map of France to visualize the distribution of the first name by department.




________________________________________________________________________________________________________________




## Project Overview

This project is a data visualization application developed using Dash, a web framework for building interactive web applications in Python. The application allows users to analyze the distribution of first names across different departments in France, providing insights based on user-defined parameters.


### Features

- **Interactive User Input**: 
  - Users can enter a first name to filter the dataset.
  - Gender selection is available to narrow down the results to either "Man" or "Woman".
  - A date range slider enables users to specify the relevant years for analysis.
  - A dropdown menu allows selection of specific departments.


- **Data Visualization**:
  - The application generates a line chart that displays the quantity of the chosen first name over the specified date range.
  - A choropleth map visualizes the distribution of the selected first name across different departments in France, allowing users to see geographic trends.


### Data Processing

- The dataset is pre-processed to include the following steps:
  - Column renaming for clarity (e.g., 'sexe' to 'Sexe', 'preusuel' to 'Prenom').
  - Gender labels are mapped to user-friendly names ("Man" and "Woman").
  - Leading zeros are added to department numbers for consistent formatting.
  - Case-insensitive comparison for first names is achieved by creating a lowercase version of the 'Prenom' column.


### Technologies Used

- **Python**: The core programming language for the application.
- **Dash**: Framework for building the interactive web application.
- **Pandas**: Library for data manipulation and analysis.
- **Plotly Express**: Library for creating interactive visualizations.


### How to Run the Application

1. Ensure you have Python installed on your system.
2. Install the required packages by running:
   ```bash
   pip install dash pandas plotly

3. Clone the repository and navigate to the project directory.
4. Run the application using
   ```bash
    python appstyles_JENNYFER_WAN.py

5. Open your web browser and navigate to http://127.0.0.1:8051 to view the application.


### Conclusion
This application serves as a powerful tool for analyzing first name trends in France, combining user-friendly interfaces with rich data visualizations. It can be further enhanced with additional features such as user authentication, export options, and more comprehensive datasets.
