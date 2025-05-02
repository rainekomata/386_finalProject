from gpiozero import Button
from signal import pause
from ollama import Client
import requests
import sounddevice as sd
import numpy as np
import numpy.typing as npt

# in virtal env download

WHISPER_ENDPOINT: str = "http://10.1.69.213:1111/voice_to_text"
LLM_MODEL: str = "gemma3:27b"
WEATHER: str = "http://10.1.69.213:11434"
client: Client = Client(host="http://ai.dfec.xyz:11434")


def voice_to_text(audio: npt.NDArray) -> dict[str, str]:
    # Serialize the array
    payload = {"audio": audio.tolist()}  # convert to regular list for JSON

    r = requests.post(WHISPER_ENDPOINT, json=payload)
    result = r.json()  # parse JSON response
    return result["text"]  # extract only the transcribed text


def LLM_process(raw_text: str) -> str | None:
    """This script evaluates an LLM prompt for processing text so that it can be used for the wttr.in API"""
    response = client.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": raw_text},
            {
                "role": "system",
                "content": """You are processing raw text for programmatic input. I'm going to explain the wttr.in format to you. Your job is to extract and return **ONLY**
            the spot the user is asking about. 
            ## Instructions
            -for any location with a space in the name, use + instead of a space
            -use 3-letter airport codes in order to get the weather information at a certain airport
            -for any geographical location other than a town or city (it could be an attraction in the city, moutain name, or special location), 
            add the character ~ before the name to look up that special location name before the weather
            -if the word inclues a mountain, state it as "mt"
            ## Example: 
            -input: Rio Rancho, expected: Rio+Rancho
            -input: Empire State, expected: ~Empire+State
            -input: Honolulu airport, expected: HNL""",
            },
        ],
    )
    return response.message.content  # insert prompt - this functiuon talks to the LLM


def get_weather(spot: str) -> str:
    # GET wttr.in
    # return response object message content
    # look at system diagram
    fetch_url = f"https://wttr.in/{spot}"
    print(fetch_url)
    r = requests.get(fetch_url)
    if r.status_code == 200:
        return r.text

    return f"Error with wttr.in: {r.status_code}"


def record_audio(duration_seconds: int = 4) -> npt.NDArray:
    """Record duration_seconds of audio from default microphone.
    Return a single channel numpy array."""
    sample_rate = 16000  # Hz
    samples = int(duration_seconds * sample_rate)
    # Will use default microphone; on Jetson this is likely a USB WebCam
    audio = sd.rec(samples, samplerate=sample_rate, channels=1, dtype=np.float32)
    # Blocks until recording complete
    sd.wait()
    # Model expects single axis
    return np.squeeze(audio, axis=1)


def pressed():
    print("Recording...")
    audio = record_audio()
    print("Done")
    print(len(audio))  # Temporary line
    #whisper returns json but we only care about plain text 
    raw_text = voice_to_text(audio)['text'] 
    print(raw_text)
    spot = LLM_process(raw_text)
    print(spot)
    weather = get_weather(spot)
    print(weather)


if __name__ == "__main__":

    button = Button(
        17, pull_up=False
    )  # physical pin 11, enable internal pull-down resistor

    print("Waiting on GPIO")
    button.when_pressed = pressed  # Call this function on rising edge
    # send to server

    pause()  # Wait forever
