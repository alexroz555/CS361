from flask import Flask, render_template, request, redirect, url_for
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def index():
    # You can process data here and pass it to the template
    name = "World"
    date = request.args.get('date')
    open_website(date)
    return render_template('index.html', name=name)

def convert_date(date_str):
    date_item = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date_item.strftime('%d %B %Y')
    return formatted_date 


@app.route('/tide_form', methods=['POST'])
def tide_form():
    #process form data
    location = request.form['location']
    date = request.form['date']
    formatted_date = convert_date(date)
    #time = request.form['time']
    formatted_high, formatted_low = open_website(formatted_date)

    return redirect(url_for('new_page', location=location, date=formatted_date, formatted_high=formatted_high, formatted_low=formatted_low))

@app.route('/new_page')
def new_page():
    location = request.args.get('location')
    date = request.args.get('date')
    formatted_high = request.args.get('formatted_high')
    formatted_low = request.args.get('formatted_low')
    return render_template('new_page.html', location=location, date=date, formatted_high=formatted_high, formatted_low=formatted_low)

@app.route("/return_home", methods=['GET'])
def return_home():
    return redirect(url_for('index'))

def open_website(date):
    high_data = {}
    low_data = {}

    formatted_high = ""
    formatted_low = ""


    url = "https://www.tide-forecast.com/locations/Newport-Yaquina-River-Oregon/tides/latest"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    
    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text()
    formatted_text = BeautifulSoup(text, "html.parser").prettify()
    with open("output.txt","w") as file:
        file.write(formatted_text)
    
    with open("output.txt", "r") as file:
        print_flag = False
        lines = file.read()
        target = date
        start_index = lines.find(target)
        if start_index != -1:
            next_index = lines.find("Tide Times", start_index + 1)
            if next_index != -1:
                tide_times = lines[start_index:next_index]
            else:
                tide_times = lines[start_index:]
            with open("text.txt","w") as file:
                file.write(tide_times)

    with open("text.txt", "r") as file:
        data = file.read()

    #for some idiot reason the low tide data have a space in between it but the high tide data sometimes does and sometimes doesn't
    #put optional space after first two words
    low_info = re.findall(r'(Low) Tide\s?(\d+:\d+ [AP]M)\(\w+ \d+ \w+\)(-?\d+\.\d+ ft)', data)
    high_info = re.findall(r'(High) Tide\s?(\d+:\d+ [AP]M)\(\w+ \d+ \w+\)(-?\d+\.\d+ ft)', data)    

    for tide in high_info:
        tide_type, tide_time, tide_height = tide
        if tide_type not in high_data:
            high_data[tide_type] = []
        high_data[tide_type].append((tide_time, tide_height))

    for tide in low_info:
        tide_type, tide_time, tide_height = tide
        if tide_type not in low_data:
            low_data[tide_type] = []
        low_data[tide_type].append((tide_time, tide_height))

    for tide_type, tide_data in high_data.items():
        formatted_high += f"{tide_type} Tide: "
        for i, (time, height) in enumerate(tide_data):
            formatted_high += f"{time}, {height}"
            if i < len(tide_data) - 1:
                formatted_high += "; "
        formatted_high += "; "

    for tide_type, tide_data in low_data.items():
        formatted_low += f"{tide_type} Tide: "
        for i, (time, height) in enumerate(tide_data):
            formatted_low += f"{time}, {height}"
            if i < len(tide_data) - 1:
                formatted_low += "; "
        formatted_low += "; "

    return formatted_high, formatted_low

if __name__ == '__main__':
    app.run(debug=True)
