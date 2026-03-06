from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/api/emotion", tags=["Emotion"])


@router.post("/audio")
async def audio_emotion(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    print("Received audio chunk:", len(audio_bytes))
    return audio_bytes


@router.post("/video")
async def video_emotion(file: UploadFile = File(...)):
    image_bytes = await file.read()
    print("Received video frame:", len(image_bytes))
    return image_bytes