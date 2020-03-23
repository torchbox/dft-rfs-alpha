from flask import Flask, request, jsonify
from flask_cors import CORS
from ludwig.api import LudwigModel

app = Flask(__name__)
CORS(app)

model = LudwigModel.load("./domestic-results/experiment_run/model/")


@app.route("/predict", methods=["POST"])
def predict():
    description = request.form.get("description")
    input = {"description": [description]}
    pred = model.predict(data_dict=input, return_type=dict)
    prediction = {}
    prediction["source"] = "domestic"
    prediction["category"] = pred["category"]["predictions"][0]
    prediction["probability"] = str(pred["category"]["probability"][0])
    print(prediction)
    # return the predictions as json
    return jsonify(prediction)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
