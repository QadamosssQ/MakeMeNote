import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


# sample run: >run -p C:\Users\sedki\PycharmProjects\MakeMeNote\src\sample-audio\sample.mp3 -c Make note for collage

def make_notes(audio_path, custom_prompt):

    with open(audio_path, "rb") as audio_file:
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {
            "Authorization": os.getenv('API_KEY')
        }

        data = {
            "model": "whisper-1"
        }

        files = {
            "file": audio_file
        }

        response = requests.request("POST", url, headers=headers, data=data, files=files)

        if response.status_code != 200:
            raise Exception(f"An error occurred: {response.text}")

    response_json = json.loads(response.text)
    result = response_json["text"]

    url_process = "https://api.openai.com/v1/chat/completions"
    headers_process = {
        "Authorization": os.getenv('API_KEY')
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Chciałbym, abyś wyciągnął z niego najważniejsze punkty i zrobił ładną, czytelną notatkę, która będzie zrozumiała dla ucznia średniej klasy. Utwórz tytuł notatki a następnie napisz notatkę, na końcu wypisz słowa klucz. Pisz po Polsku. Unikaj ciągłego wypunktowywania.  "
            },
            {
                "role": "user",
                "content": result
            }
        ]
    }

    response_process = requests.request("POST", url_process, headers=headers_process, json=data)

    if response_process.status_code != 200:
        raise Exception(f"An error occurred: {response_process.text}")

    response_json_process = json.loads(response_process.text)
    result_process = response_json_process["choices"][0]["message"]["content"]


    return result_process

print("MakeMeNotes CLI")
print("Type 'help' for a list of commands")

while True:
    command = input(">")
    if command == "help":
        print("Available commands: \n"
              "help - Display this message \n"
              "run - Run maker -p <audio path, mp3> -c <custom prompt> \n"
              "exit - Exit the program")
    elif command == "exit":
        break
    elif command.startswith("run"):
        parts = command.split()

        try:
            if "-p" in parts:
                audio_path = parts[parts.index("-p") + 1]

                if "-c" in parts:
                    custom_prompt = parts[parts.index("-c") + 1]
                else:
                    custom_prompt = ""

                print("Processing...\nResult:")

                print(make_notes(audio_path, custom_prompt))
            else:
                print("Error: The -p (path) argument is required.")
        except (ValueError, IndexError) as e:
            print(f"An error occurred: {e}")

    else:
        print("Unknown command. Type 'help' for available commands.")
