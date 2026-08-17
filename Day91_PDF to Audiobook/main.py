from pathlib import Path
from openai import OpenAI

client = OpenAI()

file = client.files.create(file=open("Research_Paper.pdf", "rb"), purpose="user_data")

text_response = client.responses.create(
    model="gpt-5.6-luna",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "file_id": file.id,
                },
                {
                    "type": "input_text",
                    "text": "Summerize all text in the document into a readable, natural python string (so text) equating to a couple of paragraphs."
                            "so that another model can generate text to speech audio based on your outputted text"
                            "Do not say anything else like: 'sure, I will get that done for you'",
                },
            ],
        }
    ],
)

speech_file_path = Path(__file__).parent / "speech.mp3"

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="coral",
    input=text_response.output_text,
    instructions="Speak in a tone that fits the context of the given text",
) as response:
    response.stream_to_file(speech_file_path)
