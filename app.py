from flask import Flask, render_template, request

import requests
import nasapy

app = Flask(__name__)
keys = []

@app.route("/home", methods=["POST", "GET"])
def home():
    return render_template("home.html")

@app.route("/apod", methods=["POST", "GET"])
def apod():
    with open('keys.txt', 'r') as f:  
        for line in f:
            keys.append(line.strip())

    #NASA api key and url
    nasa_api_key = keys[0]
    url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}"

    response = requests.get(url)
    currentData = response.json()

    currentDate = currentData['date']

    # Initialize Nasa class
    nasa = nasapy.Nasa(key=nasa_api_key)

    pickedDate = currentDate

    if request.method == 'POST':
        print(request.form['date'])
        pickedDate = request.form['date'] 

    # get apod data for chosen date
    data = nasa.picture_of_the_day(pickedDate, hd=True) 

    # image data
    apod_date = data['date']
    apod_title = data['title']
    apod_explanation = data['explanation']

    # some APOD can be images and videos. this tests for which one to post and avoids the keyError
    try:
        apod_url = data['hdurl']
    except KeyError:
        apod_url = data['url']

    # some data recieved from the api doesn't always contain the credit for the picture
    try:
        apod_copyright = data['copyright']
        credit = "Credit: " + apod_copyright
    except KeyError:
        credit = ""

    title = apod_title + f" ({apod_date})"
    image_credit = credit

    # Render HTML with count variable
    return render_template("index.html", title=title, description=apod_explanation, credit=image_credit, url=apod_url)

@app.route("/ar", methods=["POST", "GET"])
def ar():
    return render_template("ar.html")


if __name__ == "__main__":
    app.run()