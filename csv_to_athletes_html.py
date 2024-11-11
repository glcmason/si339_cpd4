import csv
import glob
import os


def process_athlete_data(file_path):

   # Extracting athlete stats by year
   records = []

   # Extracting athlete races
   races = []           

   athlete_name = ""
   athlete_id = ""
   comments = ""

   with open(file_path, newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      data = list(reader)

      athlete_name = data[0][0]
      athlete_id = data[1][0]
      print(f"The athlete id for {athlete_name} is {athlete_id}")

      for row in data[5:-1]:
         if row[2]:
            records.append({"year": row[2], "sr": row[3]})
         else:
            races.append({
               "finish": row[1],
               "time": row[3],
               "meet": row[5],
               "url": row[6],
               "comments": row[7]
            })

   return {
      "name": athlete_name,
      "athlete_id": athlete_id,
      "season_records": records,
      "race_results": races,
      "comments": comments
   }    

def gen_athlete_page(data, outfile):
   # template 
   # Start building the HTML structure
   html_content = f'''<!DOCTYPE html>
   <html lang="en">
   <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <!-- Get your own FontAwesome ID -->
       <script src="https://kit.fontawesome.com/48d9c551f8.js" crossorigin="anonymous"></script>


      <link rel = "stylesheet" href = "../css/reset.css">
      <link rel="stylesheet" href="dist/css/lightbox.css">
      <link rel = "stylesheet" href = "../css/style.css">
      

      <title>{data["name"]}</title>
   </head>
   <body>
   <a href = "#main">Skip to Main Content</a>
   <nav>
     <ul>
        <li><a href="../index.html">Home Page</a></li>
        <li><a href="../mens.html">Men's Team</a></li>
        <li><a href="../womens.html">Women's Team</a></li>
     </ul>
   </nav>
   <header>
      <!--Athlete would input headshot-->
       <h1>{data["name"]}</h1>

    <a href = "../images/profiles/{data["athlete_id"]}.jpg" data-lightbox = "athlete" target = "_blank">
      <img src="../images/profiles/{data["athlete_id"]}.jpg" alt="Athlete headshot" width="200"> 
    </a>

   </header>
   <main id = "main">
      <section id= "athlete-sr-table">
         <h2>Athlete's Seasonal Records (SR) per Year</h2>
            <table>
                  <thead>
                     <tr>
                        <th> Year </th>
                        <th> Season Record (SR)</th>
                     </tr>
                  </thead>
                  <tbody>
                  '''
   
   for sr in data["season_records"]:
      sr_row = f'''
                     <tr>
                        <td>{sr["year"]}</td>
                        <td>{sr["sr"]}</td>
                     </tr>                  
               '''
      html_content += sr_row

   html_content += '''                   
                </tbody>
                  </table>
                     </section>

                        <h2>Race Results</h2>

                        <section id="athlete-result-table">
                           

                           <table id="athlete-table">
                              <thead>
                                 <tr>
                                    <th>Race</th>
                                    <th>Athlete Time</th>
                                    <th>Athlete Place</th>
                                    <th>Race Comments</th>
                                 </tr>
                              </thead>

                              <tbody>
                  '''

   # add each race as a row into the race table 
   for race in data["race_results"]:
      race_row = f'''
                                 <tr class="result-row">
                                    <td>
                                       <a href="{race["url"]}">{race["meet"]}</a>
                                    </td>
                                    <td>{race["time"]}</td>
                                    <td>{race["finish"]}</td>
                                     <td>{race["comments"]}</td>
                                 </tr>
      '''
      html_content += race_row

   html_content += '''
                              </tbody>

                        </table>
                     </section>
                     <section id = "gallery">
                     <h2>Gallery</h2>
                      </section>
                     </main>
                     <footer>
                     <p>
                     Skyline High School<br>
                     <address>
                     2552 North Maple Road<br>
                     Ann Arbor, MI 48103<br><br>

                     <a href = "https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
                    

                     </footer>
                      <script src="dist/js/lightbox-plus-jquery.js"></script>
 <script>
        lightbox.option({
            'resizeDuration': 200,
            'positionFromTop': 250,
        })
    </script>
    <script>
        document.querySelectorAll('img').forEach(img => {
        img.onerror = function() {
            this.onerror = null; // Prevents infinite loop if default image missing
            this.src = 'path/to/default.jpg';
            this.alt = ""
        };
        });

    </script>
               </body>
         </html>
   '''

   with open(outfile, 'w') as output:
      output.write(html_content)

def gen_womens_team_page(folder_path, outfile):
    # Find all HTML files for athletes in the women's team folder
    html_files = glob.glob(os.path.join(folder_path, '*.html'))
    # Get just the file names (without the folder path) for display
    athlete_pages = [os.path.basename(file) for file in html_files]
    
    # Start building the HTML structure for the women's team page
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://kit.fontawesome.com/48d9c551f8.js" crossorigin="anonymous"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Women's Team - Skyline Cross Country</title>
    <link rel="stylesheet" href="css/reset.css">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
<a href="#main">Skip to Main Content</a>
<nav>
    <ul>
        <li><a href="index.html">Home Page</a></li>
        <li><a href="mens.html">Men's Team</a></li>
        <li><a href="womens.html">Women's Team</a></li>
    </ul>
</nav>
<header>
    <h1>Skyline High School Women's Cross Country Team</h1>
</header>
<main id="main">
    <section id="team-members">
        <h2>Women's Team Roster</h2>
        <ul>
    '''
    
    # Add each athlete as a list item with a clickable link to their profile page
    for page in athlete_pages:
        athlete_name = page.replace(".html", "").replace("_", " ").title()  # Format name from file name
        link = f'<li><a href="{folder_path}/{page}">{athlete_name}</a></li>'
        html_content += link
    
    # Close the HTML tags
    html_content += '''
        </ul>
    </section>
</main>
<footer>
    <p>Skyline High School<br>
    <address>
        2552 North Maple Road<br>
        Ann Arbor, MI 48103
    </address><br>
    <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
</footer>
</body>
</html>
    '''
    
    # Write the HTML content to the output file
    with open(outfile, 'w') as output:
        output.write(html_content)

import os
import glob

def gen_mens_team_page(folder_path, outfile):
    # Find all HTML files for athletes in the men's team folder
    html_files = glob.glob(os.path.join(folder_path, '*.html'))
    athlete_pages = [os.path.basename(file) for file in html_files]

    # Start building the HTML structure for the men's team page
    html_content = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <script src="https://kit.fontawesome.com/48d9c551f8.js" crossorigin="anonymous"></script>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Men's Team - Skyline Cross Country</title>
        <link rel="stylesheet" href="css/reset.css">
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
    <a href="#main">Skip to Main Content</a>
    <nav>
        <ul>
            <li><a href="index.html">Home Page</a></li>
            <li><a href="mens.html">Men's Team</a></li>
            <li><a href="womens.html">Women's Team</a></li>
        </ul>
    </nav>
    <header>
        <h1>Skyline High School Men's Cross Country Team</h1>
    </header>
    <main id="main">
        <section id="team-members">
            <h2>Men's Team Roster</h2>
            <ul>
    '''

    # Correct link generation
    for page in athlete_pages:
        athlete_name = page.replace(".html", "").replace("_", " ").title()  # Format name from file name
        link = f'<li><a href="{folder_path}/{page}">{athlete_name}</a></li>'  # Add a slash
        html_content += link
    
    # Close the HTML tags
    html_content += '''
            </ul>
        </section>
    </main>
    <footer>
        <p>Skyline High School<br>
        <address>
            2552 North Maple Road<br>
            Ann Arbor, MI 48103
        </address><br>
        <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
       
    </footer>
    </body>
    </html>
    '''
    
    # Write the HTML content to the output file
    with open(outfile, 'w') as output:
        output.write(html_content)

def main():
    # Define the folder path for the men's team
    mens_folder_path = 'mens_team/'
    # Get all CSV files in the men's team folder
    mens_csv_files = glob.glob(os.path.join(mens_folder_path, '*.csv'))

    # Process each men's team CSV file
    for file in mens_csv_files:
        athlete_data = process_athlete_data(file)
        gen_athlete_page(athlete_data, file.replace(".csv", ".html"))

    # Generate the men's team page
    gen_mens_team_page(mens_folder_path, 'mens.html')

    # Define the folder path for the women's team
    womens_folder_path = 'womens_team/'
    # Get all CSV files in the women's team folder
    womens_csv_files = glob.glob(os.path.join(womens_folder_path, '*.csv'))

    # Process each women's team CSV file
    for file in womens_csv_files:
        athlete_data = process_athlete_data(file)
        gen_athlete_page(athlete_data, file.replace(".csv", ".html"))

    # Generate the women's team page
    gen_womens_team_page(womens_folder_path, 'womens.html')

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
