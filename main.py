# from base64 import b64encode
import logging
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
from IPython.display import Audio, display, HTML
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Login.login import insert_user_data

# from text_images.image_genration import process_image
# from text_music.music import generate_music
# from text_chart import chart
#
# from Transcript.Youtube_video_sub import process_video
# from Transcript.Youtube_sub import process_youtube_subtitles
# from Transcript.Youtube_Mp4 import process_youtube_video
# from Transcript.Mp4_Mp3 import process_video_to_audio  # Import the function from the module
# from Transcript.Mp4_video_sub import process_video_with_subtitles
# from Transcript.Mp4_sub import process_video_and_return_subtitles
# from Transcript.Mp3_sub import generate_and_translate_subtitles_route
# from text_voice import text_voice
# from voice_clone import voice_clone

#
# from Credits.Creditsassign import credit_bp

# Create a logger instance
logger = logging.getLogger(__name__)

# Set the logging level (You can adjust this as needed)
logger.setLevel(logging.DEBUG)

# Create a file handler to log to a file (optional)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Create a console handler to log to the console (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter to specify the log message format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]
# Replace with your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_messages = exc.errors()
    return JSONResponse(content={"detail": error_messages}, status_code=422)


# Include routers for different parts of your application
# app.include_router(credit_bp, prefix="/api")


# Call the process_image function from image_generation.py
# @app.post("/api/image_generation/process_image")
# def call_process_image(prompt: str):
#     image_result = process_image(prompt)  # Call the process_image function from image_generation.py
#     return image_result
#
#
# # Call the generate_music function from image_generation.py
# @app.post("/api/music_gen/generate_music")
# def call_generate_music(prompts: list, duration: int):
#     music_response = generate_music(prompts, duration)  # Call the generate_music function
#     return music_response
#
#
# # Define the route for generating the pie chart
# @app.post("/api/pie_chart/generate_pie_chart")
# def call_generate_pie_chart(instruction: str):
#     generated_text = chart.generate_pie_chart(instruction)  # Call the generate_pie_chart function from chart.py
#     return {"result": generated_text}
#

@app.post("/insert_user/")
async def insert_user(
        first_name: str = Form(...),
        last_name: str = Form(...),
        username: str = Form(...),
        phone_number: str = Form(...),
        email: str = Form(...),
):
    try:
        logger.info("Received data: %s, %s, %s, %s, %s", first_name, last_name, username, phone_number, email)

        # Call the insert_user_data function from login.py to insert data into MongoDB
        result = insert_user_data(first_name, last_name, username, phone_number, email)

        return {"message": result}
    except Exception as e:
        logger.error("Error processing insert_user request: %s", str(e))
        return {"error": "An error occurred while processing the request."}


# Implement FastAPI endpoint to process video using functions from Youtube_video_sub.py
# @app.post("/process_youtube_video/")
# async def process_youtube_video(
#         video_file: UploadFile = File(...),
#         target_lang_code: str = Form(...),
#         subtitle_type: str = Form(...),
# ):
#     try:
#         # Save the uploaded video
#         with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
#             temp_video.write(video_file.file.read())
#             video_path = temp_video.name
#
#         # Process video using functions from Youtube_video_sub.py
#         response = process_video(video_path, target_lang_code, subtitle_type)
#         return JSONResponse(content=response, status_code=200)
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)
#
#
# @app.post("/process_youtube_sub/")
# async def process_youtube_video(
#         youtube_url: str = Form(...),
#         target_lang_code: str = Form(...),
#         subtitle_type: str = Form(...),
# ):
#     try:
#         subtitles_file = process_youtube_subtitles(youtube_url, target_lang_code, subtitle_type)
#         # Return a response indicating success
#         return {"message": "Subtitles processed and translated successfully", "subtitles_file": subtitles_file}
#     except Exception as e:
#         return {"error": str(e)}
#
#
# @app.post("/process_youtube_video/")
# async def process_youtube_video_route(
#         youtube_url: str = Form(...),
#         TARGET_LANG_CODE: str = Form(...),
#         SUBTITLE_TYPE: str = Form(...),
#         MODEL_SIZE: str = 'medium'  # Set the desired model size here
# ):
#     try:
#         result = process_youtube_video(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE)
#         # Return a response indicating success
#         return {"message": result}
#     except Exception as e:
#         return {"error": str(e)}
#
#
# @app.post("/convert_video_to_audio/")
# async def convert_video_to_audio_route(
#         video_path: str = Form(...),
# ):
#     try:
#         audio_path = process_video_to_audio(video_path)
#         # Return a response indicating success
#         return {"message": "Video converted to audio successfully", "audio_path": audio_path}
#     except Exception as e:
#         return {"error": str(e)}
#
#
# @app.post("/process_video_with_subtitles/")
# async def process_video_with_subtitles_route(
#         youtube_url: str = Form(...),
#         MODEL_SIZE: str = 'medium',  # Set the desired model size here
#         TARGET_LANG_CODE: str = 'de',
#         SUBTITLE_TYPE: str = 'vtt',
# ):
#     try:
#         output_video_path = process_video_with_subtitles(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE)
#         # Display the video with subtitles
#         mp4 = open(output_video_path, 'rb').read()
#         data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
#         display(HTML("""
#         <video width=400 controls>
#               <source src="%s" type="video/mp4">
#         </video>
#         """ % data_url))
#         # Return a response indicating success
#         return {"message": "Video processed and subtitled successfully"}
#     except Exception as e:
#         return {"error": str(e)}
#
#
# @app.post("/process_video_and_get_subtitles/")
# async def process_video_and_get_subtitles_route(
#         youtube_url: str = Form(...),
#         MODEL_SIZE: str = 'medium',  # Set the desired model size here
#         TARGET_LANG_CODE: str = 'de',
#         SUBTITLE_TYPE: str = 'vtt',
# ):
#     try:
#         subtitles = process_video_and_return_subtitles(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE)
#         # Return the generated subtitles
#         return {"subtitles": subtitles}
#     except Exception as e:
#         return {"error": str(e)}
#
#
# @app.post("/process_audio_and_get_subtitles/")
# async def process_audio_and_get_subtitles_route(
#         audio_file: UploadFile = File(...),
#         TARGET_LANG_CODE: str = 'de',
#         SUBTITLE_TYPE: str = 'vtt',
# ):
#     try:
#         response = await generate_and_translate_subtitles_route(audio_file, TARGET_LANG_CODE, SUBTITLE_TYPE)
#         return response
#     except Exception as e:
#         return {"error": str(e)}
#
#
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")
#
#
# @app.post("/convert/")
# async def convert(voice_id: str = Form(...), text: str = Form(...)):
#     result = await text_voice.convert_text_to_speech(voice_id, text)
#     return result
#
#
# @app.post("/clone_voice/")
# async def clone_voice(
#         name: str = Form(...),
#         labels: str = Form(...),
#         description: str = Form(...),
#         audio_files: list[UploadFile] = File(...)
# ):
#     return await voice_clone.clone_voice(name, labels, description, audio_files)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8000)
