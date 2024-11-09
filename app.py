import streamlit as st
from image_captioning import capture_image, describe_scene
from obstacle_detection import provide_supportive_guidance  # Updated to new function
from tts import narrate_text
import os

st.title("AI-Powered Smart Glasses Demo for Visually Impaired")

def reset_state():
    if os.path.exists("captured_image.jpg"):
        os.remove("captured_image.jpg")
    if os.path.exists("description_audio.mp3"):
        os.remove("description_audio.mp3")
    st.session_state['description'] = None
    st.session_state['guidance'] = None
    st.session_state['capture_again'] = False

# Initialize session state for description and guidance
if 'description' not in st.session_state:
    st.session_state['description'] = None
if 'guidance' not in st.session_state:
    st.session_state['guidance'] = None
if 'capture_again' not in st.session_state:
    st.session_state['capture_again'] = False

# Capture image and generate guidance
if st.button("Capture Image") or st.session_state['capture_again']:
    reset_state()  # Clear previous state if capturing again
    try:
        # Capture new image
        img_path = capture_image()
        st.image(img_path, caption="Captured Image")
        
        # Generate description
        description = describe_scene(img_path)
        st.session_state['description'] = description
        st.write("Description of Scene:", description)
        
        # Generate guidance
        guidance = provide_supportive_guidance(img_path)  # Use updated guidance function
        st.session_state['guidance'] = guidance
        st.write("Guidance:", guidance)
        
        # Generate and display audio narration
        audio_file = narrate_text(description + ". " + guidance)
        audio_bytes = open(audio_file, "rb").read()
        st.audio(audio_bytes, format="audio/mp3")
        
    except Exception as e:
        st.error(f"Error: {e}")

# Reset state when "Capture Again" is pressed
if st.button("Capture Again"):
    st.session_state['capture_again'] = True
    reset_state()
