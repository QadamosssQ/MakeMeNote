import openai

def make_notes(audio_path, custom_prompt):
    openai.api_key = ""

    with open(audio_path, "rb") as audio_file:
        transcription = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file
        )
    return transcription["text"]

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
    elif command == "run":
        print("Running maker")
        audio_path = input("Enter the path to the audio file: ")
        custom_prompt = input("Enter the custom prompt: ")
        try:
            print(make_notes(audio_path, custom_prompt))
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Unknown command")
