import os
import wave
import contextlib
import datetime
import speech_recognition as sr
from pydub import AudioSegment

def get_audio_duration(path):
    """
    Calculates the duration of a WAV audio file.

    Args:
        path (str): Path to the WAV audio file.

    Returns:
        float: Duration of the audio in seconds, or 0 if error occurs.
    """
    try:
        with contextlib.closing(wave.open(path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = round(frames / float(rate), 2)
            return duration
    except Exception as e:
        print(f"Warning: Could not calculate duration: {e}")
        return 0

def transcribe_audio(path):
    """
    Transcribes a WAV audio file to text using Google Speech Recognition API.

    Args:
        path (str): Path to the WAV audio file.

    Returns:
        str: Transcribed text, or an error message.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        print("Listening to audio...")
        audio_data = recognizer.record(source)
    try:
        print("Transcribing using Google Speech Recognition API...")
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Warning: Audio was not clear enough to recognize."
    except sr.RequestError as e:
        return f"Error: Could not reach Google API: {e}"

def main():
    """
    Main function to handle audio file input, optional MP3 conversion,
    duration calculation, transcription, and saving results.
    """
    file_path = input("Enter path to your WAV or MP3 file: ").strip()

    if not os.path.exists(file_path):
        print("Error: File not found.")
        return

    ext = file_path.split('.')[-1].lower()

    # Convert MP3 to WAV if necessary
    if ext == "mp3":
        print("Converting MP3 to WAV...")
        try:
            sound = AudioSegment.from_mp3(file_path)
            wav_file = file_path.replace(".mp3", ".wav")
            sound.export(wav_file, format="wav")
            file_path = wav_file
            print(f"Conversion complete: {file_path}")
        except Exception as e:
            print(f"Error during conversion: {e}")
            return

    # Get audio duration
    duration = get_audio_duration(file_path)
    print(f"Audio Duration: {duration} seconds")

    # Transcribe audio
    transcription = transcribe_audio(file_path)

    # Prepare report
    report = "\n" + "=" * 70 + "\n"
    report += "TRANSCRIPTION REPORT\n"
    report += "=" * 70 + "\n"
    report += f"File Name     : {file_path}\n"
    report += f"Duration      : {duration} seconds\n"
    report += f"Time Processed: {datetime.datetime.now()}\n"
    report += "\nTranscribed Text:\n\n"
    report += transcription + "\n"
    report += "=" * 70

    # Print report
    print(report)

    # Ask to save
    save_choice = input("Do you want to save the transcription to a file? (y/n): ").strip().lower()
    if save_choice == 'y':
        output_file = input("Enter filename to save (e.g., output.txt): ").strip()
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Transcription saved to '{output_file}'")
        except Exception as e:
            print(f"Error saving file: {e}")

if __name__ == "__main__":
    main()