import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
"""
@Project: Maman15

@Description: In the course "Data Analysis in Python",
I was required to submit this assignment –  based on Units 13 and 14 of the course.
The assignment is divided into three main phases:
    1. Data refinement and preparation.
    2. Data analysis.
    3. Data presentation.
    
On a personal note, I would like to thank the course team.
You helped me become more confident in my programming in the Python language:)    

@Author: Maya_Katan
@Semester: 2025a
"""

#Data refinement and preparation phase
"""
Section 1: Loads asteroid data from a CSV file into a Pandas DataFrame.

Args:
    filename (str): CSV file path.

Returns:
    pandas.DataFrame or None: DataFrame if successful, None if an error occurs.

Raises:
    FileNotFoundError: File not found.
    pd.errors.EmptyDataError: File is empty.
    pd.errors.ParserError: Invalid CSV format.
    Exception: Any unexpected error.

Notes:
    - The CSV must be properly formatted.
    - Errors are printed to the console.

Example:
    data = NASADataProcessor.load_data("nasa.csv")
"""

def load_data(filename):
    try:
        df = pd.read_csv(filename)
        return df  #Return the DataFrame if successful
    except FileNotFoundError:  #Handle missing file error
        print("Error: The file was not found.")
    except pd.errors.EmptyDataError:  #Handle empty file error
        print("Error: The file is empty.")
    except pd.errors.ParserError:  #Handle parsing errors
        print("Error: Failed to parse the file. Please check its format.")
    except Exception as unexpected:  #Catch any other unexpected errors
        print(f"Error: An unexpected error occurred - {unexpected}")

    return None  #Return None if an error occurred

"""
    Section 2: Filters the DataFrame to include only asteroids with a Close Approach Date from the year 2000 onwards.

    Args:
        df (pandas.DataFrame): The original DataFrame containing asteroid data.

    Returns:
        pandas.DataFrame: A filtered DataFrame with only asteroids from the year 2000 and later.

    Notes:
        - Assumes the column "Close Approach Date" exists and is in a recognizable date format.
        - Converts the column to datetime format for accurate filtering.
        - If the column is missing, an error message is displayed, and the original DataFrame is returned.

    Example:
        filtered_df = mask_data(nasa_file)
"""
def mask_data(df):
    if "Close Approach Date" not in df.columns:
        print("Error: The column 'Close Approach Date' is missing.")
        return df

    df["Close Approach Date"] = pd.to_datetime(df["Close Approach Date"], errors="coerce")
    filtered_df = df[df["Close Approach Date"].dt.year >= 2000]

    return filtered_df

"""
    Section 3: Cleans the DataFrame by removing specific columns and returns dataset details.

    Args:
        df (pandas.DataFrame): The original DataFrame containing asteroid data.

    Returns:
        tuple: A tuple containing:
            - int: Number of rows in the DataFrame.
            - int: Number of columns after removing specified ones.
            - list: List of remaining column names.

    Notes:
        - Removes the columns: "Orbiting Body", "Neo Reference ID", and "Equinox".
        - If any of these columns are missing, the function continues without error.

    Example:
        num_rows, num_cols, column_names = data_details(filtered_nasa_file)
"""
def data_details(df):
    columns_to_remove = ["Orbiting Body", "Neo Reference ID", "Equinox"] #Columns to be removed
    df_cleaned = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors="ignore")

    num_rows = df_cleaned.shape[0] #Get the number of rows
    num_cols = df_cleaned.shape[1] #Get the number of columns
    column_names = list(df_cleaned.columns) # Get the list of remaining column names

    return num_rows, num_cols, column_names #Return a tuple with dataset details

#Data analysis phase
"""
    Section 4: Finds the asteroid with the maximum absolute magnitude value.

    Args:
        df (pandas.DataFrame): DataFrame containing asteroid data with "Name" and "Absolute Magnitude" columns.

    Returns:
        tuple: (asteroid_name, max_value) where:
            - asteroid_name (str): Name of the asteroid with the highest absolute magnitude.
            - max_value (numeric): The maximum absolute magnitude value.
"""
def max_absolute_magnitude(df):
    max_value = df["Absolute Magnitude"].max()  #Find the highest absolute magnitude value
    asteroid_name = df.loc[df["Absolute Magnitude"] == max_value, "Name"].iloc[0]  # Get the corresponding asteroid name
    return asteroid_name, max_value  #Return the result as a tuple


"""
    Section 5: Finds the asteroid that is closest to Earth based on its miss distance in kilometers.

    Args:
        df (pandas.DataFrame): DataFrame containing asteroid data with "Name" and "Miss Dist.(kilometers)" columns.

    Returns:
        str: The name of the asteroid that is closest to Earth.
"""
def closest_to_earth(df):
    min_distance = df["Miss Dist.(kilometers)"].min() #Find the minimum miss distance value
    #Get the name of the asteroid corresponding to the minimum miss distance
    asteroid_name = df.loc[df["Miss Dist.(kilometers)"] == min_distance, "Name"].iloc[0]
    return asteroid_name


"""
    Section 6: Counts the number of asteroids for each Orbit ID and returns a dictionary.

    Args:
        df (pandas.DataFrame): DataFrame containing asteroid data with the "Orbit ID" column.

    Returns:
        dict: A dictionary where each key is an Orbit ID and the value is the count of asteroids in that orbit.
"""
def common_orbit(df):
    orbit_counts = df["Orbit ID"].value_counts().to_dict()  #Count occurrences of each Orbit ID and convert to dictionary
    return orbit_counts

"""
    Section 7: Counts the number of asteroids whose maximum estimated diameter ("Est Dia in KM(max)")
    is above the average maximum diameter among all asteroids in the DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame containing asteroid data with "Est Dia in KM(max)" column.

    Returns:
        int: Count of asteroids with a maximum estimated diameter above the average.
"""
def min_max_diameter(df):
    avg_diameter = df["Est Dia in KM(max)"].mean()  #Calculate the average maximum diameter
    count_above_avg = df[df["Est Dia in KM(max)"] > avg_diameter].shape[0]  #Count rows with diameter above average
    return count_above_avg

#Data presentation phase
"""
    Section 8: Displays a histogram of the number of asteroids according to their average diameter in km.
    
    The average diameter for each asteroid is computed as the mean of the minimum and maximum 
    estimated diameters in kilometers:
        average = (Est Dia in KM(min) + Est Dia in KM(max)) / 2
    
    Args:
        df (pandas.DataFrame): DataFrame containing asteroid data.
            (Note: This DataFrame is expected to have the columns 
             "Est Dia in KM(min)" and "Est Dia in KM(max)". 
             If these columns are absent, adjust the column names accordingly.)
    
    The histogram is plotted using 100 contiguous bins.
"""
def plt_hist_diameter(df):
    # Check that the required columns exist
    if "Est Dia in KM(min)" not in df.columns or "Est Dia in KM(max)" not in df.columns:
        print("Error: Required diameter columns not found in the DataFrame.")
        return

    # Compute the average diameter for each asteroid
    avg_diameter = (df["Est Dia in KM(min)"] + df["Est Dia in KM(max)"]) / 2
    avg_diameter = avg_diameter.dropna()  # Remove any missing values

    plt.figure(figsize=(10, 6))  # Create a new figure with dimensions 10x6 inches
    plt.hist(avg_diameter, bins=100, color='blue', edgecolor='black')
    plt.title("Distribution of Average diameter size ")
    plt.xlabel("Average Value")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


"""
 Section 9: Displays a histogram of the number of asteroids based on their Minimum Orbit Intersection.

 The histogram uses 10 contiguous bins spanning from the minimum to the maximum 
 value of the 'Minimum Orbit Intersection' column.

 Args:
     df (pandas.DataFrame): DataFrame containing asteroid data with the 
"""
def plt_hist_common_orbit(df):
    orbit_intersections = df["Minimum Orbit Intersection"].dropna()
    min_val = orbit_intersections.min() #Determine the minimum values for the range of the histogram
    max_val = orbit_intersections.max() #Determine the maximum values for the range of the histogram
    plt.figure(figsize=(10, 6)) #Create a new figure

    #Plot the histogram with 10 bins over the specified range, set colors and add a label
    plt.hist(orbit_intersections, bins=10, range=(min_val, max_val),
             color='blue', edgecolor='black')

    #Set the title and labels for the axes
    plt.title("Distribution of Asteroids by Minimum Orbit intersection")
    plt.xlabel("Min orbit intersection")
    plt.ylabel("Number of Asteroids")

    #Display the legend and add gridlines
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout() #Adjusts the layout so that all plot elements
    plt.show()  #Renders and displays the final plot in a window or inline


"""
    Section 10: Displays a pie chart showing the percentage of hazardous and non-hazardous asteroids 
    based on the 'Hazardous' column in the DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame containing asteroid data with a 'Hazardous' column 
                               (expected to be boolean or numeric with 1 for hazardous and 0 for non-hazardous).
"""
def plt_pie_hazard(df):
    counts = df["Hazardous"].value_counts() #Counts how many times each value appears in the 'Hazardous' column
    if True in counts.index or False in counts.index:
        hazardous_count = counts.get(True, 0)   #If booleans are used, get the count for True (hazardous)
        non_hazardous_count = counts.get(False, 0)  #Get the count for False (non-hazardous)
    else:
        hazardous_count = counts.get(1, 0)  #Assume 1 represents hazardous and get its count
        non_hazardous_count = counts.get(0, 0)  #Assume 0 represents non-hazardous and get its count

    labels = ["True", "False"]
    sizes = [hazardous_count, non_hazardous_count] #Create a list with the counts for each category
    explode = (0.1, 0)  #Explode the hazardous slice for emphasis

    plt.figure(figsize=(8, 8)) # Create a new figure
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, explode=explode, colors=["lightblue", "pink"])
    plt.title("Percentage of Hazardous and Non-Hazardous Asteroids")
    plt.legend(labels, loc="best") #Add a legend with the labels, placed in the best location automatically
    plt.tight_layout()
    plt.show()

"""
    Section 11: Displays a scatter plot with a simple linear regression line to examine the linear relationship 
    between an asteroid's miss distance from Earth (in kilometers) and its speed (in Miles per hour).

    Args:
        df (pandas.DataFrame): DataFrame containing asteroid data with the columns 
                               "Miss Dist.(kilometers)" and "Miles per hour".

    Returns:
        None

    My answer:
        Based on the regression analysis presented on the page,
        it appears that there is no strong linear correlation between the miss distance and the asteroid's speed.
        I believe the the result might vary depending on different dataset values.
"""
def plt_linear_motion_magnitude(df):
    #Remove rows with missing values in the relevant columns
    df_clean = df[["Miss Dist.(kilometers)", "Miles per hour"]].dropna()
    x = df_clean["Miss Dist.(kilometers)"]
    y = df_clean["Miles per hour"]

    slope, intercept = np.polyfit(x, y, 1) #Compute the linear regression coefficients
    y_fit = slope * x + intercept #Compute the fitted y values for the regression line

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='blue', alpha=0.6, label='Data Points')  # Plot the actual data points
    plt.plot(x, y_fit, color='red', label='Regression line')  # Plot the regression line
    plt.title("Linear Regression: Absolute Magnitude vs Miles per hour")
    plt.xlabel("Absolute Magnitude")
    plt.ylabel("Miles per hour")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
