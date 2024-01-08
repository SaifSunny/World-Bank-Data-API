import os
import pandas as pd

current_directory = os.path.dirname(os.path.abspath(__file__))
def read_csv_file(file_name):
    # Read the CSV file into a DataFrame
    file_path = os.path.join(current_directory, 'data', file_name)
    return pd.read_csv(file_path, encoding='latin1')

class GetData:
    def get_indicator_name_by_code(indicator_code):

        indicators_csv_file_path = os.path.join(current_directory, 'data', 'indicators_list.csv')
        
        try:
            df_indicators = pd.read_csv(indicators_csv_file_path, encoding='latin1')
            indicator_row = df_indicators[df_indicators['Indicator_id'] == indicator_code]
            
            return indicator_row.iloc[0]['IndicatorName'] if not indicator_row.empty else f"Unknown Indicator {indicator_code}"
        
        except FileNotFoundError:
            return f"Indicator CSV File Not Found"
        

    def get_country_data_by_code(country_code):
        region_data_csv_file_path = os.path.join(current_directory, 'data', 'region_data.csv')

        try:
            # Load data from the 'region_data.csv' file into a DataFrame with 'latin1' encoding
            df = pd.read_csv(region_data_csv_file_path, encoding='latin1')

            # Filter data based on the provided country code
            country_data = df[df['Country Code'] == country_code]

            # Convert the filtered data to a dictionary directly
            result_data = country_data.to_dict(orient='records')[0] if not country_data.empty else {}

            return result_data

        except FileNotFoundError:
            return {'error': 'CSV File Not Found'}
        except Exception as e:
            return {'error': str(e)}

        
        
    def retrieve_data_for_report(report_name, country_code, start_year, end_year):
        file_path = os.path.join(current_directory, 'data', f'{report_name}.csv')

        # Read the CSV file using pandas
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            return f"CSV file not found: {file_path}"

        # Filter data for the specified country code and years
        filtered_data = df[(df['Country Code'] == country_code)]
        
        # Extract columns for the specified years and include "Indicator Name"
        year_columns = [str(year) for year in range(start_year, end_year + 1)]
        selected_columns = ['Country Code', 'Indicator Name'] + year_columns
        filtered_data = filtered_data[selected_columns]

        # Convert the DataFrame to a dictionary with the desired structure
        report_data = {}

        for _, row in filtered_data.iterrows():
            indicator_name = row['Indicator Name']
            del row['Indicator Name']
            del row['Country Code']
            report_data[indicator_name] = row.to_dict()

        return report_data












    