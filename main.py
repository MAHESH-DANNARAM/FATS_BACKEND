from base64 import b64encode

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
from IPython.display import Audio, display, HTML

from text_images.image_genration import process_image
from text_music.music import generate_music
from text_chart import chart
from Login.login import init_db, create_user, UserCreate
from Transcript.Youtube_video_sub import process_video
from Transcript.Youtube_sub import process_youtube_subtitles
from Transcript.Youtube_Mp4 import process_youtube_video
from Transcript.Mp4_Mp3 import process_video_to_audio  # Import the function from the module
from Transcript.Mp4_video_sub import process_video_with_subtitles
from Transcript.Mp4_sub import process_video_and_return_subtitles
from Transcript.Mp3_sub import generate_and_translate_subtitles_route

from Credits.Creditsassign import credit_bp

app = FastAPI()

drivers = 'SQL+Server'
server = 'DESKTOP-7ONCVVN\\MAHESH'
database = 'LOGIN'
port = '1433'
id = 'sa'
password = 'Mahesh@divya'
database_url = f'mssql+pyodbc://{id}:{password}@{server}/{database}?driver={drivers}'

db = init_db(database_url)

# Include routers for different parts of your application
app.include_router(credit_bp, prefix="/api")


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


@app.post("/api/create_user")
def call_create_user(user: UserCreate):
    created_user = create_user(db, user)
    return created_user


# Implement FastAPI endpoint to process video using functions from Youtube_video_sub.py
@app.post("/process_youtube_video/")
async def process_youtube_video(
        video_file: UploadFile = File(...),
        target_lang_code: str = Form(...),
        subtitle_type: str = Form(...),
):
    try:
        # Save the uploaded video
        with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(video_file.file.read())
            video_path = temp_video.name

        # Process video using functions from Youtube_video_sub.py
        response = process_video(video_path, target_lang_code, subtitle_type)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/process_youtube_sub/")
async def process_youtube_video(
        youtube_url: str = Form(...),
        target_lang_code: str = Form(...),
        subtitle_type: str = Form(...),
):
    try:
        subtitles_file = process_youtube_subtitles(youtube_url, target_lang_code, subtitle_type)
        # Return a response indicating success
        return {"message": "Subtitles processed and translated successfully", "subtitles_file": subtitles_file}
    except Exception as e:
        return {"error": str(e)}


@app.post("/process_youtube_video/")
async def process_youtube_video_route(
        youtube_url: str = Form(...),
        TARGET_LANG_CODE: str = Form(...),
        SUBTITLE_TYPE: str = Form(...),
        MODEL_SIZE: str = 'medium'  # Set the desired model size here
):
    try:
        result = process_youtube_video(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE)
        # Return a response indicating success
        return {"message": result}
    except Exception as e:
        return {"error": str(e)}


@app.post("/convert_video_to_audio/")
async def convert_video_to_audio_route(
        video_path: str = Form(...),
):
    try:
        audio_path = process_video_to_audio(video_path)
        # Return a response indicating success
        return {"message": "Video converted to audio successfully", "audio_path": audio_path}
    except Exception as e:
        return {"error": str(e)}


@app.post("/process_video_with_subtitles/")
async def process_video_with_subtitles_route(
        youtube_url: str = Form(...),
        MODEL_SIZE: str = 'medium',  # Set the desired model size here
        TARGET_LANG_CODE: str = 'de',
        SUBTITLE_TYPE: str = 'vtt',
):
    try:
        output_video_path = process_video_with_subtitles(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE)
        # Display the video with subtitles
        mp4 = open(output_video_path, 'rb').read()
        data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
        display(HTML("""
        <video width=400 controls>
              <source src="%s" type="video/mp4">
        </video>
        """ % data_url))
        # Return a response indicating success
        return {"message": "Video processed and subtitled successfully"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/process_video_and_get_subtitles/")
async def process_video_and_get_subtitles_route(
        youtube_url: str = Form(...),
        MODEL_SIZE: str = 'medium',  # Set the desired model size here
        TARGET_LANG_CODE: str = 'de',
        SUBTITLE_TYPE: str = 'vtt',
):
    try:
        subtitles = process_video_and_return_subtitles(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE)
        # Return the generated subtitles
        return {"subtitles": subtitles}
    except Exception as e:
        return {"error": str(e)}


@app.post("/process_audio_and_get_subtitles/")
async def process_audio_and_get_subtitles_route(
        audio_file: UploadFile = File(...),
        TARGET_LANG_CODE: str = 'de',
        SUBTITLE_TYPE: str = 'vtt',
):
    try:
        response = await generate_and_translate_subtitles_route(audio_file, TARGET_LANG_CODE, SUBTITLE_TYPE)
        return response
    except Exception as e:
        return {"error": str(e)}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8000)
