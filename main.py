from fastapi import FastAPI

from text_images.image_genration import process_image
from text_music.music import generate_music
from text_chart import chart

from Transcript.Youtube_sub import mp4_sub_bp
from Credits.Creditsassign import credit_bp
from Login.models import db  # Assuming your database models are defined in 'models.py'
from Login.login import registration_router

app = FastAPI()

# Simulating your database configuration
database_url = "sqlite:///./test.db"  # Use your actual database URL

# Initialize the database
db.init_app(app, database_url)

# Include routers for different parts of your application
app.include_router(credit_bp, prefix="/api")
app.include_router(mp4_sub_bp, prefix="/api")
app.include_router(registration_router, prefix="/api")


# Call the process_image function from image_generation.py
@app.post("/api/image_generation/process_image")
def call_process_image(prompt: str):
    image_result = process_image(prompt)  # Call the process_image function from image_generation.py
    return image_result


# Call the generate_music function from image_generation.py
@app.post("/api/music_gen/generate_music")
def call_generate_music(prompts: list, duration: int):
    music_response = generate_music(prompts, duration)  # Call the generate_music function
    return music_response


# Define the route for generating the pie chart
@app.post("/api/pie_chart/generate_pie_chart")
def call_generate_pie_chart(instruction: str):
    generated_text = chart.generate_pie_chart(instruction)  # Call the generate_pie_chart function from chart.py
    return {"result": generated_text}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8000)
