import openai
import requests
import json
import asyncio

# Replace with your actual API key and endpoint
openai.api_key = "YOUR_OPENAI_API_KEY"
api_endpoint = "YOUR_API_ENDPOINT"

async def stream_and_send(prompt):
    try:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or another suitable model
            messages=messages,
            stream=True,
        )

        collected_chunks = []
        collected_messages = []
        full_response_text = ""

        async def send_to_api(text_to_send):
            headers = {'Content-Type': 'application/json'}
            payload = {'text': text_to_send}
            try:
                api_response = requests.post(api_endpoint, data=json.dumps(payload), headers=headers, timeout=5) # Add a timeout
                api_response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                print(f"Sent to API: {text_to_send[:20]}... Status Code: {api_response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error sending to API: {e}")


        for chunk in response:
            if "delta" in chunk["choices"][0] and "content" in chunk["choices"][0]["delta"]:
                chunk_content = chunk["choices"][0]["delta"]["content"]
                collected_chunks.append(chunk_content)  # save the chunks
                full_response_text += chunk_content
                print(chunk_content, end="", flush=True)

                # Send the accumulated text to the API periodically (e.g., every few words or sentences)
                if len(full_response_text.split()) % 5 == 0: # Send every 5 words. Adjust as needed
                    await send_to_api(full_response_text)
        
        #Send the remaining text in case the word count wasn't a multiple of 5
        if len(full_response_text.split()) % 5 != 0:
            await send_to_api(full_response_text)

        print() # New line after the response is complete

    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

async def main():
    prompt = "Write a short story about a robot learning to feel emotions."
    await stream_and_send(prompt)

if __name__ == "__main__":
    asyncio.run(main())

