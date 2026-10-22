# brain_of_the_doctor.py


# brain_of_the_doctor.py


import os
import base64
import mimetypes
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def encode_image(image_path):
    with open(image_path, "rb") as image:
        return base64.b64encode(image.read()).decode("utf-8")


def analyze_image_with_query(query, model, encoded_image=None, image_path=None):

    content = [{"type": "text", "text": query}]

    if encoded_image:
        mime_type = mimetypes.guess_type(image_path or "image.jpg")[0]
        mime_type = mime_type or "image/jpeg"

        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{mime_type};base64,{encoded_image}"
            }
        })

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )

    return response.choices[0].message.content

model = "qwen/qwen3.8-27b"
image_path = "acne.jpg"
query = "Is there something wrong with my face?"

encoded_image = encode_image(image_path)
result = analyze_image_with_query(query, model, encoded_image)
print(result)