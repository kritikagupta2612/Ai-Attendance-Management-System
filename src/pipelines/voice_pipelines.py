from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import streamlit as st
import io
import librosa

@st.cache_resource
def load_voice_encoder():
     return VoiceEncoder()

def get_voice_embedding(audio_bytes):
     try:
          encoder = load_voice_encoder()
          audio , sr = librosa.load(io.BytesIO(audio_bytes), sr=1600)
          wav = preprocess_wav(audio)
          embedding = encoder.embed_utterance(wav) 
          return embedding.tolist()  # Convert the embedding to a list for easier storage and retrieval
     except Exception as e:
            st.error("Voice recog error")
            return None
def identify_speaker(new_embedding, candidates_dict , threshold=0.65):
    """
    Identify the speaker by comparing the new embedding with candidate embeddings.

    Parameters:
    - new_embedding: The embedding of the new audio sample.
    - candidates_dict: A dictionary where keys are candidate IDs and values are their embeddings.
    - threshold: The similarity threshold for identification.

    Returns:
    - The ID of the identified speaker if a match is found, otherwise None.
    """
    if new_embedding is None or not candidates_dict:
        return None,0.0
    best_sid = None
    best_score=-1.0
    for sid, stored_embedding in candidates_dict.items():
         if stored_embedding:
              similarity = np.dot(new_embedding, stored_embedding) 
              if similarity > best_score:
                        best_score = similarity
                        best_sid = sid
    if best_score >= threshold:
        return best_sid, best_score  
    return None, best_score  # Return None if no match is found

def process_bulk_audio(audio_bytes , candidates_dict , threshold=0.65):
    """
    Process bulk audio data to identify speakers.

    Parameters:
    - audio_bytes: The audio data in bytes.
    - candidates_dict: A dictionary where keys are candidate IDs and values are their embeddings.
    - threshold: The similarity threshold for identification.

    Returns:
    - A list of identified speaker IDs and their corresponding similarity scores.
    """
    try:
        encoder = load_voice_encoder()
        audio , sr = librosa.load(io.BytesIO(audio_bytes), sr=1600)
        segments = librosa.effects.split(audio, top_db=20)  # Split audio into segments based on silence
        identified_results = {}

        for start, end in segments:
         if (end - start) < sr *0.5:
             continue  # Skip segments shorter than 0.5 seconds
        segment_audio = audio[start:end]
        wav = preprocess_wav(segment_audio)
        embedding = encoder.embed_utterance(wav)

        sid, score = identify_speaker(embedding, candidates_dict, threshold)
        if sid :
             if sid not in identify_speaker or score > identified_results[sid]:
                 identified_results[sid] = score
        return identified_results
    except Exception as e:
      st.error("Bulk process error")
      return {}
 