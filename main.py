import speech_recognition as sr
import re

# Аудио файл .wav преобразует в текст
class ConverterAudioToText:
    def get_text_from_audio(self, filepath: str) -> str:
        recognizer = sr.Recognizer()
        with sr.AudioFile(filepath) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language='ru-RU')
        return text

# Класс для преобразований текста в хороший вид
class ClearText:
    def remove_punctuation(self, text):
            return re.sub(r'[^\w\s]', '', text.strip())

# Простой компаратор двух слов в тексте.
# Поскольку конвертация аудио в текст может быть не совсем идеальной,
# то сравнивать два слова на равенство не лучшая идея.
# Можно усовершенствовать, например проверять, что слова похожи до разницы в максимум двух буквах
# или, что расстояние левенштейна меньше 2-3
class Comparator:
    def equalWords(self, word1: str, word2: str) -> bool:
        word1 = word1.lower()
        word2 = word2.lower()
        word1 = ClearText().remove_punctuation(word1)
        word2 = ClearText().remove_punctuation(word2)
        return word1 == word2

class FinderAudioBugs:
    def find_audio_bugs(self, audio_filepath: str, start_text_filepath) -> bool:
        converter = ConverterAudioToText()
        audio_text = converter.get_text_from_audio(audio_filepath)
        with open(start_text_filepath, "r", encoding="utf-8") as f:
            start_text = f.read()
        words_in_start_text = ClearText().remove_punctuation(start_text).split()
        words_in_audio_text = ClearText().remove_punctuation(audio_text).split()
        for i in range(len(words_in_start_text)):
            if not Comparator().equalWords(words_in_start_text[i], words_in_audio_text[i]):
                result_bugs = ""
                now_index = i
                while not Comparator().equalWords(words_in_start_text[now_index], words_in_audio_text[i]):
                    result_bugs += words_in_start_text[now_index] + " "
                    now_index += 1
                return result_bugs.strip()
        return ""

def main() -> None:
    audio_filepath = "tests/audio01.wav" # В этом примере есть потеряшка
    start_text_filepath = "tests/text01.txt"
    finder = FinderAudioBugs()
    is_bug = finder.find_audio_bugs(audio_filepath, start_text_filepath)
    print("Найдена потеряшка:" if is_bug else "Потеряшка не найдена")
    if is_bug:
        print(is_bug)

if __name__ == "__main__":
    main()
