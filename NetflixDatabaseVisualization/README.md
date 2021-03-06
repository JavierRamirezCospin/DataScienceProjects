# Netflix Data Visualization

The main objective of this project is to visualize data of the netflix streaming service database. 
The database includes all tv shows and movies offered in the streaming service as of 2021.
Data was separated by year of release, with each category holding up to 10 different years.
Data visualization includes: movies vs tv shows proportion, top countries of origin, top years of release and top categories for each category.
Data obtained from: https://www.kaggle.com/shivamb/netflix-shows

## 1. Requirements
 
The following libraries are required:

- Numpy >= 1.19.5
- Pandas >= 1.3.0
- Matplotlib >= 3.4.2
- Seaborn >= 0.11.2
- Dash >= 2.1.0

## 2. Files Description

- **NetflixData.csv:** Contains raw data from the netflix database.
- **NetflixDataAnalysis.ipynb:** Contains netflix raw data cleaning and transformation process, as well as the exploratory data analysis.
- **NetflixCleanData.csv:** Contains clean data for visualization program.
- **NetflixDashboard.py:** Main program for interactive Dashboard. Data can be visualized by range of order of release and by default runs on the local port: 8050.
