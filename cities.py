import pandas as pd
from datetime import datetime


def transform_date_to_future(date_str):
    # Map month names to numbers
    months = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }
    
    # Split the input string into day and month
    day, month_name = date_str.split(' de ')
    month = months[month_name.lower()]  # Get the numeric month
    
    # Get today's date
    today = datetime.today()
    
    # Create a datetime object for the parsed date in the current year
    parsed_date = datetime.strptime(f"{day}/{month}/{today.year}", "%d/%m/%Y")
    
    # If the parsed date is in the past, move it to the next year
    if parsed_date < today:
        parsed_date = parsed_date.replace(year=today.year + 1)
    
    # Format the result as dd/mm/yyyy
    return parsed_date.strftime("%d/%m/%Y")

def add_date():

    shows = pd.read_excel('Output/shows.xlsx')
    shows['date2'] = shows.apply(transform_date_to_future,shows['date'],axis=1)
    shows.to_excel('Output/shows.xlsx', sheet_name='data', index=False)

    print(f"Data saved to {'Output/shows.xlsx'}")

def add_city():
    shows = pd.read_excel('Output/shows.xlsx')
    locations = pd.read_excel('Input/locations.xlsx')

    shows2=pd.merge(shows,locations, left_on='location', right_on='location', how='left')
    shows2.to_excel('Output/shows.xlsx', sheet_name='data', index=False)
    print(f"Data saved to {'Output/shows.xlsx'}")


# Run script
if __name__ == "__main__":
    #add_city()
    add_date()
    # Example usage
