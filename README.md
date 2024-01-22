# secure_prompt
Example of using GCP Secret Manager with LLM's

This code implements a FastAPI application that utilizes Vertex AI Generative Models to generate text based on an uploaded image and a prompt.

## main.py
Defines a FastAPI application with routes for the main page and image upload endpoint.
Renders an HTML template for the main page.
Handles image uploads, encodes them into base64, and passes them to the generate_text() function.
Retrieves the prompt from a secret stored in Google Secret Manager using the SecurePrompt class.
Calls the generate_text() function to generate text based on the image and prompt.
Returns the generated text as a JSON response.

## pkg/SecurePrompt.py
Provides a class SecurePrompt with a static method GetValue().
Uses the Google Cloud Secret Manager client to securely retrieve the prompt from a secret.

## How it works:
A user visits the main page and uploads an image.
The image is encoded into base64 and sent to the /upload endpoint.
The code retrieves the prompt from GCP Secret Manager using SecurePrompt. An example secret is included as secure-prompt-example.json
The generate_text() function uses the Vertex AI Generative Model to generate text based on the image and prompt.
The generated text is returned as a JSON response.

## How to run it:
Ensure you have the current gcloud command line tool installed and python packages outlined in requirements.txt. You can run "gcloud init" to setup your local evniroment and "pip install -r requirements.txt" to install the python packages.

1. Start by creating a new secret in GCP Secret Manager. This can be done using the GCP console or using the below command:
gcloud secrets create secure-prompt-example --data-file=secure-prompt-example.json

2. Start the web service locally by running:
python3 -m uvicorn main:app --reload

3. Open a browser and go to http://localhost:8000. Enter your GCP project ID and the name of the secret used in step 1. Use the oj.jpg image included in this repo for initial testing and select "Parse Image"

4. After a few seconds, you will be presended with the results in json format. The size should be in ounces, but let's change it to gallons.

5. Make a copy of the secure-prompt-example.json file and name it "test.json". change the value for the "text" attribute to the following: 
"Briefly describe each product you see in this picture. Provide your response in JSON format including the brand, description and size, with the size in gallons. If you can not determine the size, mark it as NA. Do not include the json prefix in your response."

6. Create a new version of the secret in GCP Secret Manager with the updated prompt.  With the web service still running, open a new command line window and run:
gcloud secrets versions add secure-prompt-example --data-file=test.json

7. Hit your browsers back button and parse the image again. You should now see the result listing the size in gallons.

8. List the available versions of the prompt. You should see two versions.
gcloud secrets versions list secure-prompt-example

9. Rollback to the origianl prompt by deploying a new version using the origianl secure-prompt-example.json file. 
gcloud secrets versions add secure-prompt-example --data-file=secure-prompt-example.json


This example shows how we can quickly and securely update our LLM integrated applicaitons without the need to make any modifications to our applicaiton code or even restarting the service. 