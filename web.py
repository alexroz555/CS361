from flask import Flask, render_template, request, redirect, url_for
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
app = Flask(__name__)

@app.route('/')
def index():
    # You can process data here and pass it to the template
    name = "World"
    open_website()
    return render_template('index.html', name=name)

@app.route('/tide_form', methods=['POST'])
def tide_form():
    #process form data
    print(request.form)
    location = request.form['location']
    date = request.form['date']
    time = request.form['time']

    return redirect(url_for('new_page'))

@app.route('/new_page')
def new_page():
    return render_template('new_page.html')

@app.route("/return_home", methods=['GET'])
def return_home():
    return redirect(url_for('index'))

def open_website():
    try:
        url = "https://www.tide-forecast.com/locations/Newport-Yaquina-River-Oregon/tides/latest"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        #print(html)
        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text()
        formatted_text = BeautifulSoup(text, "html.parser").prettify()
        with open("output.txt","w") as file:
            file.write(formatted_text)
        

        with open("output.txt", "r") as file:
            print_flag = False
            lines = file.read()
            target = "Wednesday 21 February 2024"
            start_index = lines.find(target)
            if start_index != -1:
                next_index = lines.find("Tide Times", start_index + 1)
                if next_index != -1:
                    tide_times = lines[start_index:next_index]
                else:
                    tide_times = lines[start_index:]
                with open("text.txt","w") as file:
                    file.write(tide_times)
            else:
                ("No information found for this date")

        with open('text.txt', "r") as file:
            low_tides = []
            high_tides = []
            tokens = text.split()
            for i in range(len(tokens)):
                if tokens[i] == 'Low' and tokens[i + 1] == "Tide":
                    low_tides.append((tokens[i + 1]))
                elif tokens[i] == 'High' and tokens[i + 1] == 'Tide':
                    high_tides.append((tokens[i + 2], tokens[i + 4]))
            print("Low Tides:")
            for tide in low_tides:
                print(tide)
            print("\nHigh Tides:")
            for tide in high_tides:
                print(tide)
            # for line in file:
            #     if "Tide Times for Newport, Yaquina River:" in line:
            #         if "Wednesday 21 February 2024" in line:
            #             print_flag = True
            #     elif print_flag and "Thursday 22 February 2024" in line:
            #         break
            #     if print_flag:
            #         print(line)
        
        # month = soup.find_all(string=re.compile(r'11 February'))

        # tide_spans = soup.find_all('span', class_="tide-day-tides__secondary")
        # #print(tide_spans)

        
        # for i in range(0, len(tide_spans)):

        #     date_span = tide_spans[i]
        #     if date_span.get_text() == "(Sun 11 February)":
     
     
        #         low_tide_level = tide_spans[i + 1]
        #         low_tide_time = low_tide_level.get_text()
        #         print(f"Low Tide Level: {low_tide_time}")

        #         high_tide_level = tide_spans[i + 1]
        #         high_tide_time = high_tide_level.get_text()
        #         print(f"High Tide Level: {high_tide_time}")

                

    except Exception as e:
        print("Error occurred while fetching website:", e)

if __name__ == '__main__':
    app.run(debug=True)
