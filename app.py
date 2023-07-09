from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import base64
import os
import io
from io import StringIO


app = Flask(__name__)

# Read the CSV files
data_sheet1 = pd.read_csv('data/sheet1.csv')
print("Reading sheet1.csv...")
print(data_sheet1.columns)
data_sheet2 = pd.read_csv('data/sheet3.csv')
#data_sheet2.columns = data_sheet2.columns.str.replace("[^a-zA-Z0-9]", "")
#data_sheet2 = data_sheet2.rename(columns=lambda x: x.strip().replace("'", ""))
print("Reading sheet2.csv...")
print(data_sheet2.columns)



# Home page
@app.route('/')
def home():
    return render_template('home.html', visualization=create_visualization())

# Interactive dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    selected_country = None
    selected_year = None

    if request.method == 'POST':
        selected_country = request.form.get('country')
        selected_year = request.form.get('year')

    return render_template('dashboard.html', visualization=create_dashboard_visualization(selected_country, selected_year), countries=get_countries(), years=get_years())

#create visualization for the home page
def create_visualization():
    countries = ['Belarus', 'Bosnia & Herzegovina', 'Chile', 'China', 'Croatia', 'Estonia', 'Hungary', 'Kuwait',
                 'Latvia', 'Lithuania', 'Montenegro', 'North Macedonia', 'Romania', 'Serbia', 'Slovak Republic',
                 'Türkiye', 'Uruguay', 'Costa Rica', 'United Arab Emirates']
    
    years = ['2000', '2007', '2014', '2022']
    
    # Filter the data for the specified countries and years
    filtered_data = data_sheet1[data_sheet1['Country'].isin(countries)][['Country'] + years]
    
    # Replace missing data points ('<5' or '—') with NaN
    filtered_data.replace(['<5', '—'], float('nan'), inplace=True)
    
    # Convert the rank columns to numeric
    for year in years:
        filtered_data[year] = pd.to_numeric(filtered_data[year], errors='coerce')
    
    plt.figure(figsize=(10, 6))
    
    # Plot the trend for each country
    for country in countries:
        country_data = filtered_data[filtered_data['Country'] == country]
        plt.plot(years, country_data.values.flatten()[1:], marker='o', label=country)
    
    plt.xlabel('Year')
    plt.ylabel('GHI Rank')
    plt.title('Trend of Global Hunger Index Ranks')
    plt.legend(loc='upper right')
    
    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data_bytes = buffer.getvalue()
    buffer.close()
    
    # Convert the bytes to a base64-encoded string
    plot_data_str = base64.b64encode(plot_data_bytes).decode('utf-8')

    # Generate the HTML code to display the plot
    html_code = f'<img src="data:image/png;base64,{plot_data_str}">'
    
    return html_code





def create_dashboard_visualization(country, year):
    # Read the dataset
    data_sheet2 = pd.read_csv('data/sheet3.csv')

    column_name = year
    print(f"Selected column name: {column_name}")
    print(f"Available columns in dataset: {data_sheet2.columns}")

    if column_name not in data_sheet2.columns:
        print("Column name not found in dataset")
        return "Column name not found in dataset"

    filtered_data = data_sheet2.loc[(data_sheet2["Country"] == country) & (data_sheet2[column_name].notnull())]
    print(f"Filtered data: {filtered_data}")

    # Convert the columns to numeric type
    filtered_data[column_name] = pd.to_numeric(filtered_data[column_name])
    filtered_data["2014 12-16"] = pd.to_numeric(filtered_data["2014 12-16"])

    # Calculate absolute change since 2014
    filtered_data["Absolute change since 2014"] = filtered_data[column_name] - filtered_data["2014 12-16"]

    # Convert wide-form data to long-form data
    df = filtered_data.melt(id_vars=["Country"], value_vars=[column_name, "Absolute change since 2014"], var_name="Year", value_name="GHI Index")

    fig = px.scatter(df, x="Year", y="GHI Index", hover_data=['Country'], color='Country')
    fig.update_layout(
    title="Global GHI Index Change Over Years (2014)",
    xaxis_title='Year',
    yaxis_title='GHI Index',
    width=720,  # Set the plot width
    height=600,  # Set the plot height
    showlegend=True,  # Show the legend
    )
    fig.update_traces(mode='lines+markers', line={'dash': 'solid'})  # Add lines connecting the markers
    visualization = fig.to_html(full_html=False)

    return visualization


def get_countries():
    data_sheet2 = pd.read_csv('data/sheet3.csv')  # Read the dataset
    return data_sheet2['Country'].unique()

def get_years():
    data_sheet2 = pd.read_csv('data/sheet3.csv')  # Read the dataset
    return data_sheet2.columns[1:-2].tolist()

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard_post():
    if request.method == 'POST':
        country = request.form['country']
        year = request.form['year']
        visualization = create_dashboard_visualization(country, year)
    else:
        visualization = ""

    countries = get_countries()
    years = get_years()

    return render_template('dashboard.html', countries=countries, years=years, visualization=visualization)





if __name__ == '__main__':
    app.run(debug=True)
   