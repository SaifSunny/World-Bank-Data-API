import os
import pandas as pd
from flask import Blueprint, request, jsonify, json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functions import GetData

current_directory = os.path.dirname(os.path.abspath(__file__))


report_files = {
    "AgricultureAndRuralDevelopment": 'AgricultureAndRuralDevelopment.csv',
    "AidEffectiveness": 'AidEffectiveness.csv',
    "ClimateChange": 'ClimateChange.csv',
    "EconomyAndGrowth": 'EconomyAndGrowth.csv',
    "Education": 'Education.csv',
    "EnergyAndMining": 'EnergyAndMining.csv',
    "Environment": 'Environment.csv',
    "ExternalDebt": 'ExternalDebt.csv',
    "FinancialSector": 'FinancialSector.csv',
    "Gender": 'Gender.csv',
    "Health": 'Health.csv',
    "Infrastructure": 'Infrastructure.csv',
    "Poverty": 'Poverty.csv',
    "PrivateSector": 'PrivateSector.csv',
    "PublicSector": 'PublicSector.csv',
    "ScienceAndTechnology": 'ScienceAndTechnology.csv',
    "SocialDevelopment": 'SocialDevelopment.csv',
    "SocialProtectionAndLabor": 'SocialProtectionAndLabor.csv',
    "Trade": 'Trade.csv',
    "UrbanDevelopment": 'UrbanDevelopment.csv',
}

code_ranges_to_files = {
    (1, 42): 'AgricultureAndRuralDevelopment.csv',
    (43, 116): 'AidEffectiveness.csv',
    (117, 192): 'ClimateChange.csv',
    (193, 446): 'EconomyAndGrowth.csv',
    (447, 608): 'Education.csv',
    (609, 658): 'EnergyAndMining.csv',
    (659, 799): 'Environment.csv',
    (800, 860): 'ExternalDebt.csv',
    (861, 936): 'FinancialSector.csv',
    (937, 1092): 'Gender.csv',
    (1093, 1346): 'Health.csv',
    (1347, 1393): 'Infrastructure.csv',
    (1394, 1422): 'Poverty.csv',
    (1423, 1593): 'PrivateSector.csv',
    (1594, 1736): 'PublicSector.csv',
    (1737, 1746): 'ScienceAndTechnology.csv',
    (1747, 1780): 'SocialDevelopment.csv',
    (1781, 1891): 'SocialProtectionAndLabor.csv',
    (1892, 2040): 'Trade.csv',
    (2041, 2059): 'UrbanDevelopment.csv',
}

wb_blueprint = Blueprint('wb_blueprint', __name__)

# Country Codes
@wb_blueprint.route('/CountryCodes', methods=['GET'])
def AllCountryCode():

    csv_file_path = os.path.join(current_directory, 'data', 'region_data.csv')  

    try:
        df = pd.read_csv(csv_file_path, encoding='latin1')
        df = df.dropna(subset=['Region'])

        country_data = dict(zip(df['Country Code'], df['CountryName']))

        return jsonify(country_data)
    
    except FileNotFoundError:
        return jsonify({'message': 'CSV File Not Found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Region Codes
@wb_blueprint.route('/RegionCodes', methods=['GET'])
def AllRegionCode():
    csv_file_path = os.path.join(current_directory, 'data', 'region_data.csv')  

    try:
        # Load data from CSV file into a DataFrame with 'latin1' encoding
        df = pd.read_csv(csv_file_path, encoding='latin1')

        # Filter rows where 'Region' is null
        df_null_region = df[df['Region'].isnull()]

        # Create a dictionary with CountryCode as keys and CountryName as values
        region_data = dict(zip(df_null_region['Country Code'], df_null_region['CountryName']))

        return jsonify(region_data)
    except FileNotFoundError:
        return jsonify({'message': 'CSV File Not Found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@wb_blueprint.route('/IndicatorCodes', methods=['GET'])
def get_unique_indicator_list():

    csv_file_path = os.path.join(current_directory, 'data', 'indicators_list.csv')

    try:
       
        df = pd.read_csv(csv_file_path, encoding='latin1')
        df = df.rename(columns={"Indicator_id": "IndicatorId", "IndicatorName": "IndicatorName", "category": "Category"})

        indicator_data = {}
        for _, row in df.iterrows():
            category_name = f"{row['Category']}"
            indicator_data.setdefault(category_name, {})[f"{row['IndicatorId']}"] = row['IndicatorName']

        return jsonify(indicator_data)

    except FileNotFoundError:
        return jsonify({'message': 'CSV File Not Found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@wb_blueprint.route('/ReportCodes', methods=['GET'])
def get_unique_report_list():

    return {
    "WBRE-01": 'AgricultureAndRuralDevelopment',
    "WBRE-02": 'AidEffectiveness',
    "WBRE-03": 'ClimateChange',
    "WBRE-04": 'EconomyAndGrowth',
    "WBRE-05": 'Education',
    "WBRE-06": 'EnergyAndMining',
    "WBRE-07": 'Environment',
    "WBRE-08": 'ExternalDebt',
    "WBRE-09": 'FinancialSector',
    "WBRE-10": 'Gender',
    "WBRE-11": 'Health',
    "WBRE-12": 'Infrastructure',
    "WBRE-13": 'Poverty',
    "WBRE-14": 'PrivateSector',
    "WBRE-15": 'PublicSector',
    "WBRE-16": 'ScienceAndTechnology',
    "WBRE-17": 'SocialDevelopment',
    "WBRE-18": 'SocialProtectionAndLabor',
    "WBRE-19": 'Trade',
    "WBRE-20": 'UrbanDevelopment',
}
 

@wb_blueprint.route('/IndicatorData', methods=['GET'])
def IndicatorData():
    try:
        country = request.args.get('country')
        indicator = request.args.get('indicator')

        # Extract the code value from the indicator
        code = indicator.split('-')[1]

        file_name = None
        for code_range, file in code_ranges_to_files.items():
            if code_range[0] <= int(code) <= code_range[1]:
                file_name = file
                break

        if file_name is None:
            return jsonify({'message': 'Invalid code'}), 400

        csv_file_path = os.path.join(current_directory, 'data', file_name)
        df = pd.read_csv(csv_file_path, encoding='latin1')

        indicator_name = GetData.get_indicator_name_by_code(indicator)

        filtered_data = df[(df['Country Code'] == country) & (df['Indicator Name'] == indicator_name)]
        
        # Convert filtered data to a dictionary directly
        result_data = filtered_data.to_dict(orient='records')[0] if not filtered_data.empty else {}

        country_data = GetData.get_country_data_by_code(country)

        # Organize data into a dictionary
        response_data = {
                'Country': country_data,
                indicator_name: result_data
        }

        return jsonify(response_data)

    except FileNotFoundError:
        return jsonify({'message': 'CSV File Not Found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
 
@wb_blueprint.route('/ReportData', methods=['GET'])
def ReportData():
    try:
        country = request.args.get('country')
        report_code = request.args.get('report')

        # Mapping report code to file name
        report_file_mapping = {
            "WBRE-01": 'AgricultureAndRuralDevelopment.csv',
            "WBRE-02": 'AidEffectiveness.csv',
            "WBRE-03": 'ClimateChange.csv',
            "WBRE-04": 'EconomyAndGrowth.csv',
            "WBRE-05": 'Education.csv',
            "WBRE-06": 'EnergyAndMining.csv',
            "WBRE-07": 'Environment.csv',
            "WBRE-08": 'ExternalDebt.csv',
            "WBRE-09": 'FinancialSector.csv',
            "WBRE-10": 'Gender.csv',
            "WBRE-11": 'Health.csv',
            "WBRE-12": 'Infrastructure.csv',
            "WBRE-13": 'Poverty.csv',
            "WBRE-14": 'PrivateSector.csv',
            "WBRE-15": 'PublicSector.csv',
            "WBRE-16": 'ScienceAndTechnology.csv',
            "WBRE-17": 'SocialDevelopment.csv',
            "WBRE-18": 'SocialProtectionAndLabor.csv',
            "WBRE-19": 'Trade.csv',
            "WBRE-20": 'UrbanDevelopment.csv',
        }

        # Check if the report code is valid
        if report_code not in report_file_mapping:
            return jsonify({'message': 'Invalid report code'}), 400

        # Retrieve file name based on the report code
        file_name = report_file_mapping[report_code]

        # Construct the file path
        csv_file_path = os.path.join(current_directory, 'data', file_name)

        # Read CSV file using pandas
        df = pd.read_csv(csv_file_path)

        # Filter data for the specified country
        filtered_data = df[df['Country Code'] == country]

        # Get country data
        country_data = GetData.get_country_data_by_code(country)

        # Convert filtered data to a dictionary
        result_data = {file_name[:-4]: {}}

        for _, row in filtered_data.iterrows():
            indicator_name = row['Indicator Name']
            del row['Country Code']
            del row['Indicator Name']
            result_data[file_name[:-4]][indicator_name] = row.to_dict()

        return jsonify({'Country': country_data, 'Reports': result_data})

    except FileNotFoundError:
        return jsonify({'message': 'CSV File Not Found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



    

@wb_blueprint.route('/CountryFullReport', methods=['POST'])
def country_full_report():
    data = request.get_json()

    # Extracting values from the request body
    country_code = data["country_code"]
    start_year = int(data["start_year"])
    end_year = int(data["end_year"])
    reports = data["Reports"]

    # Validate the years
    if start_year == end_year:
        return jsonify({"error": "Start Year and End Year cannot be the same."})

    if end_year < start_year:
        return jsonify({"error": "End Year cannot be smaller than Start Year."})

    if start_year > 2022 or end_year > 2022 or start_year < 1960 or end_year < 1960:
        return jsonify({"error": "Data is available only for the range 1960 to 2022."})

    result_data = {}

    # Iterate over the reports
    for report_key, report_enabled in reports.items():
        if report_enabled:
            report_data = GetData.retrieve_data_for_report(report_key, country_code, start_year, end_year)
            result_data[report_key] = report_data

    country_data = GetData.get_country_data_by_code(country_code)

    # Include country data in the response
    result_data['Country'] = country_data

    return jsonify(result_data)



@wb_blueprint.route('/MultipleIndicatorData', methods=['POST'])
def getIndicatorData():
    try:
        data = request.get_json()

        country = data["country_code"]
        start_year = int(data["start_year"])
        end_year = int(data["end_year"])
        indicators = data["Indicators"]


        # Validate the years
        if start_year == end_year:
            return jsonify({"error": "Start Year and End Year cannot be the same."})

        if end_year < start_year:
            return jsonify({"error": "End Year cannot be smaller than Start Year."})

        if start_year > 2022 or end_year > 2022 or start_year < 1960 or end_year < 1960:
            return jsonify({"error": "Data is available only for the range 1960 to 2022."})
        
        
        response_data = {'Country': GetData.get_country_data_by_code(country)}

        for indicator in indicators:
            # Extract the code value from the indicator
            code = indicator.split('-')[1]

            file_name = None
            for code_range, file in code_ranges_to_files.items():
                if code_range[0] <= int(code) <= code_range[1]:
                    file_name = file
                    break

            if file_name is None:
                return jsonify({'message': f'Invalid code for indicator: {indicator}'}), 400

            csv_file_path = os.path.join(current_directory, 'data', file_name)
            df = pd.read_csv(csv_file_path, encoding='latin1')

            indicator_name = GetData.get_indicator_name_by_code(indicator)

            # Filter data for the specified country code, indicator name, and years
            filtered_data = df[(df['Country Code'] == country) & (df['Indicator Name'] == indicator_name)]
            
            # Extract columns for the specified years
            year_columns = [str(year) for year in range(start_year, end_year + 1)]
            selected_columns = year_columns
            filtered_data = filtered_data[selected_columns]

            result_data = filtered_data.to_dict(orient='records')

            response_data[indicator_name] = result_data

        return jsonify(response_data)

    except FileNotFoundError:
        return jsonify({'message': 'CSV File Not Found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



    