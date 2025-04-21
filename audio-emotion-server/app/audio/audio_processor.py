import torch
import torchaudio
import torch.nn.functional as F
import os
from .model_handler import load_model, num2emotion

def convert_audio_to_wav(audio_file):
    """Convert audio file to WAV format"""
    if audio_file.lower().endswith('.m4a'):
        wav_filename = os.path.splitext(audio_file)[0] + '.wav'
        
        try:
            from pydub import AudioSegment
            sound = AudioSegment.from_file(audio_file, format='m4a')
            sound.export(wav_filename, format='wav')
            return wav_filename
        except Exception:
            return audio_file
    
    return audio_file

def process_audio(feature_extractor, model, audio_file):
    """Function for processing audio file and determining emotions"""
    # Convert audio if needed
    audio_file = convert_audio_to_wav(audio_file)
    
    # Load audio using torchaudio
    waveform, sample_rate = torchaudio.load(audio_file)
    
    # Resample audio to 16kHz (model requirement)
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(sample_rate, 16000)
        waveform = resampler(waveform)
        sample_rate = 16000
    
    # Prepare input data for the model
    inputs = feature_extractor(waveform[0], sampling_rate=sample_rate, return_tensors="pt")
    
    # Predict emotions
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    
    # Get probabilities for each emotion
    probs = F.softmax(logits, dim=-1)
    
    # Get the most likely emotion
    predicted_class_id = logits.argmax(-1).item()
    predicted_emotion = num2emotion[predicted_class_id]
    
    # Prepare emotion probabilities dictionary
    emotion_probabilities = {}
    for i, emotion in num2emotion.items():
        probability = probs[0][i].item()
        percent = probability * 100
        emotion_probabilities[emotion] = percent
    
    return predicted_emotion, emotion_probabilities

def analyze_audio_file(audio_path):
    """Main function for analyzing an audio file"""
    # Check if file exists
    if not os.path.exists(audio_path):
        return None, None
    
    # Check if model exists and load
    if (os.path.exists("./my_hubert_feature_extractor") and 
        os.path.exists("./my_hubert_model")) or os.path.exists("hubert_emotion_model_complete.pt"):
        feature_extractor, model = load_model()
    else:
        from model_handler import save_model
        feature_extractor, model = save_model()
    
    # Process audio
    return process_audio(feature_extractor, model, audio_path)

if __name__ == "__main__":
    # Path to audio file (replace with yours)
    audio_file = 'audio-1.m4a'
    
    # Analyze file
    emotion, probabilities = analyze_audio_file(audio_file)