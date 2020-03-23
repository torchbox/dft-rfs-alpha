# DFT ML experiments

## Process data

1. Make the two spreadsheets available locally as `domestic-data.xslx` and `international-data.xslx`
2. `workon dft-ml-experiments`
3. Clean up the data and export as CSV: `python pre-process.py`

## Create the Model (AutoML approach)

1. Create a Google Cloud project and [enable AutoML tables](https://cloud.google.com/automl-tables/docs/quickstart#before_you_begin)
2. [Create a dataset](https://cloud.google.com/automl-tables/docs/quickstart#create_a_dataset_and_train_a_model), using the 'Upload files from your computer' option.
3. Upload `clean-domestic-data.csv` to a bucket, which must be in the same region as your project
4. Disable Nullabilty for all fields
5. Set the 'category' column to 'Categorical' and make it the target
6. Inside 'Edit additional parameters', select a Manual data split and specify 'ML' as the data split column
7. Click 'Train model'

## Notes

- The training data must have at least 1,000 and no more than 100,000,000 rows.
-  Categorical targets must have at least 2 and no more than 500 distinct values
- It [costs to keep a prediction model running](https://cloud.google.com/automl-tables/pricing). "Model deployment costs $0.005 per GiB per hour per machine that a model is deployed, billed at the granularity of MiB per second. We currently replicate your model to memory in 9 machines for low latency serving purposes, so there is a 9x multiplier applied to this cost. For example, if the size of your model is 10 GiB, and you deploy for 3 hours, you would be charged $0.005 * 10 * 3 * 9, or $1.35." Our model is ~200MB, so this is about $8 per month (0.005 * 0.25 * 9 * 24 * 30).

## Create the Model (Ludwig approach)
- `pip install -r ludwig-requirements.txt`
- Create a model: `ludwig train --data_csv domestic-data.csv --model_definition "{input_features: [{name: description, type: text}], output_features: [{name: category, type: category}]}" --output_directory domestic-results` or `ludwig train --data_csv international-data.csv --model_definition "{input_features: [{name: description, type: text}], output_features: [{name: category, type: category}]}" --output_directory international-results`
- Run a prediction server from the trained model: `ludwig serve -m international-results/experiment_run/model/`
- Test the model `curl -s http://0.0.0.0:8000/predict -X POST -F 'description=parcels' | jq '.["category_predictions","category_probability"]'`

## Deploy the Ludwig model to Cloud Run
- `cd ludwig/backend`
- move the relevant model into this directory and update `ENV FLASK_APP` in `Dockerfile`
- `gcloud auth login`
- `gcloud config set project [project ID]`
- `gcloud builds submit --tag gcr.io/[project ID]/ludwig-dft-international`
- `gcloud run deploy --image gcr.io/ml-for-dft/ludwig-dft-international --platform managed --memory=512Mi --allow-unauthenticated --region=europe-west4`

curl -s https://ludwig-dft-international-yrm3wokmna-ez.a.run.app/predict -X POST -F 'description=parcels' | jq '.["category_predictions","category_probability"]'

## Frontend

- `cd frontend`
- `netlifyctl deploy`

## Optimisation strategies

- Combine both sets of data into a single model, mark as international or domestic, supply this at prediction time.