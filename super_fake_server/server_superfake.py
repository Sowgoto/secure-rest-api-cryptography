from flask import Flask, Response

app = Flask(__name__)

@app.get("/weather")
def weather():
    #Storing the response of the request
    with open("response.bin", "rb") as f:
        saved_response = f.read()

    # Send back exactly the previously recorded response body
    return Response(saved_response, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5037, debug=True)