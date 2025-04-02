# Please add "stream : true" for faster responses
# pip install krutrim-cloud
from krutrim_cloud import KrutrimCloud
from dotenv import load_dotenv

load_dotenv()

client = KrutrimCloud()

model_name = "DeepSeek-R1-Llama-8B"
messages = [
    {"role": "user", "content": "How to drain a k8s node?"}
]

try:
    response = client.chat.completions.create(model=model_name, messages=messages)

    # Access generated output
    txt_output_data = response.choices[0].message.content  # type:ignore
    print(f"Output: \n{txt_output_data}")

    # OR
    # Save generated output
    response.save(output_dirpath="./output")
except Exception as exc:
    print(f"Exception: {exc}")