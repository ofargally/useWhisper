import torch
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available
from transformers.models.whisper import WhisperProcessor
import os
import gc
import psutil
import json
import time
from dotenv import load_dotenv


class WhisperLogger:
    def __init__(self):
        self.process = psutil.Process()
        self.start_time = time.time()

    def log(self, level, msg):
        current_time = time.time()
        elapsed = current_time - self.start_time
        memory_usage = self.process.memory_info().rss / 1024 / 1024
        print(f"[{level}] [{elapsed:.2f}s] {msg} (Memory: {memory_usage:.2f} MB)")

    def info(self, msg): self.log("INFO", msg)
    def debug(self, msg): self.log("DEBUG", msg)
    def warning(self, msg): self.log("WARNING", msg)
    def error(self, msg): self.log("ERROR", msg)


# Initialize logger
logger = WhisperLogger()

# Load environment variables
load_dotenv()
# audio_path = os.getenv('AUDIO_LINK')
audio_path = "./downloads/untitled.mp3"
logger.info(f"Audio Link: {audio_path}")

if audio_path == "":
    logger.error("Please add a link to the .env file")
    exit()

logger.info("Initializing Whisper model...")
pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3",
    torch_dtype=torch.float16,
    device="cpu",  # use "mps" for Mac devices
    model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {
        "attn_implementation": "sdpa"},
)

# Load processor from a specific Whisper checkpoint
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3")

logger.info("Starting transcription...")
gc.collect()
torch.cuda.empty_cache()

logger.info("Processing audio...")
outputs = pipe(
    audio_path,
    chunk_length_s=10,
    batch_size=4,
    return_timestamps=True,
)
print(outputs)
# logger.info("outputs: ", outputs)
logger.info("Saving transcription...")
if not os.path.exists('downloads'):
    os.makedirs('downloads')

output_file = os.path.join('downloads', 'transcription1.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputs, f, ensure_ascii=False, indent=2)
logger.info(f"Transcription saved to {output_file}")
