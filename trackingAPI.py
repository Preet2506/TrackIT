from flask import Flask
from trackDHL import trackDHL
from ym import trackym
from safeExpress import trackSafeExpress
from ShreeMaruti import trackShreeMaaruti
from DeutschePost import trackDP
from ACS import trackACS
from CNEexpress import trackCNE
from BRT import trackBRT
from Asendia import trackAsendia
from trackingMore import trackingMore


app = Flask(__name__)

@app.route("/dhl/<int:tkno>")
def home(tkno):
    '''# Load the JSON data
    with open("/home/shipway/PycharmProjects/Project1/vrltask/vrltask/spiders/DHLresult.json", "r") as result:
        data = json.load(result)
    # Return the JSON data as a response
    return jsonify(data)'''
    data=trackDHL(tkno)
    return data

@app.route("/ShreeMaruti/<int:tkno>")
def shreeMaruti(tkno):
    data = trackShreeMaaruti(tkno)
    return data

@app.route("/SafeExpress/<int:tkno>")
def safeExpress(tkno):
    data = trackSafeExpress(tkno)
    return data

@app.route("/ym/<string:tkno>")
def ym(tkno):
    data = trackym(tkno)
    return data

@app.route("/DeutschePost/<string:tkno>")
def DP(tkno):
    data = trackDP(tkno)
    return data

@app.route("/ACS/<string:tkno>")
def ACS(tkno):
    data = trackACS(tkno)
    return data

@app.route("/CNE/<string:tkno>")
def CNE(tkno):
    data = trackCNE(tkno)
    return data

@app.route("/RoyalMail/<string:tkno>")
def RoyalMail(tkno):
    data = trackRoyalMail(tkno)
    return data

@app.route("/BRT/<string:tkno>")
def BRT(tkno):
    data = trackBRT(tkno)
    return data

@app.route("/Asendia/<string:tkno>")
def Asendia(tkno):
    data = trackAsendia(tkno)
    return data

@app.route("/fedex/<string:tkno>")
def fedex(tkno):
    data = trackFedex(tkno)
    return data

@app.route("/trackingmore/<string:tkno>")
def TrackingMore(tkno):
    data = trackingMore(tkno)
    return data
    
if __name__ == "__main__":
    app.run(debug=True)


