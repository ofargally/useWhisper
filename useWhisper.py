import torch
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available
import os
import gc
import psutil
import json
from dotenv import load_dotenv
load_dotenv()

audio_path = os.getenv('AUDIO_LINK')
print("Audio Link: ", audio_path)
if audio_path == "":
    print("Please add a link to the .env file")
    exit()
pipe = pipeline(
    "automatic-speech-recognition",
    # select checkpoint from https://huggingface.co/openai/whisper-large-v3#model-details
    model="openai/whisper-large-v3",
    torch_dtype=torch.float16,
    device="cpu",  # use "mps" for Mac devices
    model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {
        "attn_implementation": "sdpa"},
)


def print_memory_usage():
    process = psutil.Process()
    print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")


print("Transcribing...")
gc.collect()
torch.cuda.empty_cache()
print_memory_usage()
outputs = pipe(
    audio_path,
    chunk_length_s=10,
    batch_size=4,
    return_timestamps=True,
)
print_memory_usage()
print("Transcription: \n")
print(outputs)

output_file = os.path.join('downloads', 'transcription.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputs, f, ensure_ascii=False, indent=2)
print(f"Transcription saved to {output_file}")
