import pandas as pd
import numpy as np

def generate_static_webpage(df, output_file):
    """
    Generates a static HTML webpage from a DataFrame containing comedy show information,
    grouped by date, with a filter to select artists.

    Parameters:
        df (pd.DataFrame): DataFrame with columns ['Date', 'Artist', 'Location', 'Time', 'Price', 'URL'].
        output_file (str): Name of the output HTML file.
    """
    # HTML template
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comedy Shows in My City</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 10px;
        }
        .container {
            max-width: 1200px;
            margin: 20px auto;
            padding: 0 15px;
        }
        .filter {
            margin-bottom: 20px;
            text-align: center;
        }
        .filter select {
            padding: 10px;
            font-size: 16px;
        }
        .date-section {
            margin-bottom: 30px;
        }
        .date-section h2 {
            background-color: #333;
            color: white;
            padding: 10px;
            border-radius: 5px;
        }
        .event-list {
            list-style-type: none;
            padding: 0;
        }
        .event-item {
            background-color: white;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .event-item h3 {
            margin: 0;
            color: #333;
        }
        .event-item h3 a {
            text-decoration: none;
            color: #007BFF;
        }
        .event-item h3 a:hover {
            text-decoration: underline;
        }
        .event-item p {
            margin: 5px 0;
        }
        .event-item .price {
            font-weight: bold;
            color: green;
        }
    </style>
    <script>
        function filterEvents() {
            const artist = document.getElementById('artistFilter').value.toLowerCase();
            const events = document.querySelectorAll('.event-item');

            events.forEach(event => {
                const artistName = event.getAttribute('data-artist').toLowerCase();
                if (artist === "all" || artistName.includes(artist)) {
                    event.style.display = "block";
                } else {
                    event.style.display = "none";
                }
            });

            // Hide empty date sections
            const dateSections = document.querySelectorAll('.date-section');
            dateSections.forEach(section => {
                const visibleEvents = section.querySelectorAll('.event-item[style="display: block;"]');
                section.style.display = visibleEvents.length > 0 ? "block" : "none";
            });
        }
    </script>
</head>
<body>

<header>
    <h1>Comedy Shows in My City</h1>
    <p>Find upcoming comedy shows in your city.</p>
</header>

<div class="container">
    <div class="filter">
        <label for="artistFilter">Filter by Artist:</label>
        <select id="artistFilter" onchange="filterEvents()">
            <option value="all">All</option>
            {filter_options}
        </select>
    </div>
    {content}
</div>

</body>
</html>"""

    # Generate filter options
    artists = df['artist'].unique()
    filter_options = "\n".join([f"<option value=\"{artist}\">{artist}</option>" for artist in artists])

    # Group events by date
    grouped = df.groupby('date')

    # Generate the HTML for each date and its events
    content_html = ""
    for date, group in grouped:
        content_html += f"""
        <div class="date-section">
            <h2>{date}</h2>
            <ul class="event-list">
        """
        for _, row in group.iterrows():
            price_display = row['price'] if pd.notna(row['price']) else "N/A"
            content_html += f"""
            <li class="event-item" data-artist="{row['artist']}">
                <h3><a href="{row['url']}" target="_blank">{row['artist']}</a></h3>
                <p><strong>Location:</strong> {row['location']}</p>
                <p><strong>Time:</strong> {row['time']}</p>
                <p><strong>Price:</strong> <span class="price">{price_display}</span></p>
            </li>
            """
        content_html += "</ul></div>"

    # Combine the template with the content
    final_html = html_template.replace("{filter_options}", filter_options).replace("{content}", content_html)

    # Write the HTML to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Static webpage generated: {output_file}")


def add_city():
    shows = pd.read_excel('Output/shows.xlsx')
    locations = pd.read_excel('Input/locations.xlsx')

    shows2=pd.merge(shows,locations, left_on='Courses', right_on='Courses', how='left')
    shows2.to_excel('Output/shows.xlsx', sheet_name='data', index=False)
    print(f"Data saved to {'Output/shows.xlsx'}")

input_file = "output/shows.xlsx"  # Replace with your Excel file name
output_file = "docs/index.html"

df = pd.read_excel(input_file)
df["price"] = np.nan

generate_static_webpage(df,output_file)