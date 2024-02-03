from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    # You can process data here and pass it to the template
    name = "World"
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


if __name__ == '__main__':
    app.run(debug=True)
