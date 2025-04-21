from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from .audio_processor import analyze_audio_file

router = APIRouter()

@router.post("/analyze")
async def analyze_audio(audio: UploadFile = File(...)):
    # Сохраняем файл временно
    with open(f"temp_{audio.filename}", "wb") as buffer:
        buffer.write(await audio.read())
    
    # Анализируем аудио
    emotion, probabilities = analyze_audio_file(f"temp_{audio.filename}")
    
    # Удаляем временный файл
    import os
    os.remove(f"temp_{audio.filename}")
    
    if emotion is None:
        raise HTTPException(status_code=400, detail="Failed to process audio")
    
    return {
        "emotionCode": list(num2emotion.keys())[list(num2emotion.values()).index(emotion)],
        "emotionName": emotion,
        "probabilities": probabilities
    }