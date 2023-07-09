# Python_Flask_App_Interactive_Dashboard

# Global Hunger Index Dashboard

This project is an interactive dashboard that visualizes the Global Hunger Index (GHI) data. It allows users to explore and analyze GHI scores for different countries over time.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)

## Features

- Home Page:
  - Displays a scatter plot of GHI scores by 2022 GHI Rank.
  - Provides an interactive visualization of GHI scores for different countries.
- Interactive Dashboard:
  - Allows users to select a country and a year to view the GHI index change over time.
  - Displays a line graph showing the trend of GHI ranks for the selected country.

## Installation

1. Clone the repository:

git clone https://github.com/your-username/global-hunger-index-dashboard.git


2. Navigate to the project directory:

cd global-hunger-index-dashboard


3. Install the required dependencies:

pip install -r requirements.txt


## Usage

1. Start the Flask application:

python app.py


2. Open a web browser and visit [http://localhost:5000](http://localhost:5000).

## Data

The project uses two CSV datasets:

1. `sheet1.csv`: Contains GHI scores by rank for different countries.
2. `sheet2.csv`: Contains detailed GHI data for different countries over time.

Please make sure to update the datasets with the latest information if needed.

## Technologies

- Python
- Flask
- Pandas
- Plotly

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
