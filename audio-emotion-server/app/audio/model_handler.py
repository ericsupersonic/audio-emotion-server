import torch
from transformers import HubertForSequenceClassification, Wav2Vec2FeatureExtractor

# Dictionary for translating indices to emotions
num2emotion = {0: 'neutral', 1: 'angry', 2: 'positive', 3: 'sad', 4: 'other'}

def save_model():
    """Function for initial model saving"""
    # Load feature extractor and model
    feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/hubert-large-ls960-ft")
    model = HubertForSequenceClassification.from_pretrained("xbgoose/hubert-speech-emotion-recognition-russian-dusha-finetuned")
    
    # Save models in directories
    feature_extractor.save_pretrained("./my_hubert_feature_extractor")
    model.save_pretrained("./my_hubert_model")
    
    # Monolithic save to one file
    torch.save({
        'model_state_dict': model.state_dict(),
        'feature_extractor_config': feature_extractor.to_dict()
    }, 'hubert_emotion_model_complete.pt')
    
    return feature_extractor, model

def load_model():
    """Function for loading the model from local storage"""
    try:
        # Try loading from directories (preferred method)
        feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(
            "./my_hubert_feature_extractor", 
            local_files_only=True
        )
        model = HubertForSequenceClassification.from_pretrained(
            "./my_hubert_model", 
            local_files_only=True
        )
    except Exception:
        try:
            # Create empty models for loading weights
            feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(
                "facebook/hubert-large-ls960-ft",
                local_files_only=False
            )
            model = HubertForSequenceClassification.from_pretrained(
                "xbgoose/hubert-speech-emotion-recognition-russian-dusha-finetuned",
                local_files_only=False
            )
            
            # Load weights from monolithic file
            checkpoint = torch.load('hubert_emotion_model_complete.pt')
            model.load_state_dict(checkpoint['model_state_dict'])
        except Exception:
            feature_extractor, model = save_model()
    
    return feature_extractor, model