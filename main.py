import random
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

# Настройки записи
sample_rate = 44100
duration = 4  # секунды для записи одного слова

# Слова по уровням
words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["хирургия", "университет", "информация", "произношение", "воображение"]
}

translator = Translator()
recognizer = sr.Recognizer()

def record_voice():
    print(f"🎙 Говорите слово на английском, у вас {duration} секунд...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("temp.wav", sample_rate, recording)

    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="en-US").lower()
        print(f"📝 Вы сказали: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Не удалось распознать речь.")
        return ""
    except sr.RequestError as e:
        print(f"⚠ Ошибка сервиса: {e}")
        return ""

def play_game():
    print("Добро пожаловать в голосовую игру 'Переводчик'!")
    level = input("Выберите уровень сложности (easy / medium / hard): ").lower()

    if level not in words_by_level:
        print("Нет такого уровня. Попробуйте снова.")
        return

    words = words_by_level[level].copy()
    random.shuffle(words)

    score = 0

    for word in words:
        print(f"\nПереведите слово на английский: {word}")
        correct_translation = translator.translate(word, src="ru", dest="en").text.lower()

        answer = record_voice()
        print(f"Правильный перевод: {correct_translation}")

        if answer == correct_translation:
            print("✅ Правильно!")
            score += 1
        else:
            print("❌ Ошибка!")

    print(f"\nИгра окончена. Ваши баллы: {score}")
    if score >= 3:
        print("🎉 Поздравляем! Вы выиграли.")
    else:
        print("😔 К сожалению, вы проиграли. Нужно минимум 3 балла для победы.")

if __name__ == "__main__":
    play_game()
