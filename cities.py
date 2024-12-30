import pandas as pd

def add_city():
    shows = pd.read_excel('Output/shows.xlsx')
    locations = pd.read_excel('Input/locations.xlsx')

    shows2=pd.merge(shows,locations, left_on='location', right_on='location', how='left')
    shows2.to_excel('Output/shows.xlsx', sheet_name='data', index=False)
    print(f"Data saved to {'Output/shows.xlsx'}")

# Run script
if __name__ == "__main__":
    add_city()