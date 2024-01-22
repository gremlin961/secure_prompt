from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import base64
import json
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from pkg import SecurePrompt


# Create a FastAPI app
app = FastAPI()

# Mount the static files directory for serving static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create a Jinja2Templates object for rendering HTML templates
templates = Jinja2Templates(directory="templates")


# Function to generate text using a Vertex AI generative model
def generate_text(project_id: str, location: str, b64_image: str, prompt: str) -> str:
    # Initialize Vertex AI client
    vertexai.init(project=project_id, location=location)

    # Create a GenerativeModel object for the specified model
    multimodal_model = GenerativeModel("gemini-pro-vision")

    # Generate content using the model, passing the image and prompt
    response = multimodal_model.generate_content(
        [
            Part.from_data(
                data=base64.b64decode(b64_image), mime_type="image/jpeg" # You can also use mime_type="image/png"
            ),
            Part.from_text(prompt),  # Encapsulate the prompt in a Part object
        ]
    )

    # Return the generated text
    return response.text


# Route for the main page
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    # Render the main.html template
    return templates.TemplateResponse("main.html", {"request": request})


# Route for uploading an image
@app.post("/upload")
async def upload_image(image: UploadFile = File(...), project_id: str = Form(), secret_name: str = Form()):
    # Read the image contents
    contents = await image.read()

    # Encode the image in base64
    encoded_image = base64.b64encode(contents).decode("utf-8")

    # Get the prompt from the secret
    prompt_data = json.loads(SecurePrompt.GetValue(project_id, secret_name))
    vqa_prompt = prompt_data['prompt']['parts'][0]['text']

    # Generate text using the image and prompt
    qa_response = json.loads(generate_text(project_id, 'us-central1', encoded_image, vqa_prompt))

    # Return the generated text as a JSON response
    return JSONResponse(content=qa_response)