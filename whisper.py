import whisper
import numpy as np
import numpy.typing as npt
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, Pipeline, pipeline
import sys
import time
from fastapi import FastAPI, File, UploadFile
from typing import List
from pydantic import BaseModel

model_id = "distil-whisper/distil-medium.en"
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
print(f"Using device {device}.")


def build_pipeline(model_id: str, torch_dtype: torch.dtype, device: str) -> Pipeline:
    """Creates a Hugging Face automatic-speech-recognition pipeline on the given device."""
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True,
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        torch_dtype=torch_dtype,
        device=device,
    )
    return pipe


print("Building model pipeline...")
pipe = build_pipeline(model_id, torch_dtype, device)
print(type(pipe))
print("Done")

app = FastAPI()


class AudioData(BaseModel):
    audio: List[float]


@app.post("/voice_to_text")
def voice_to_text(data: AudioData):
    np_audio = np.array(data.audio, dtype=np.float32)
    # Now pass np_audio to your model
    transcript = pipe(np_audio)
    return {"text": transcript}
