import datetime
import os
import time
import pygame
import re
import edge_tts
import asyncio
import speech_recognition as sr
from langdetect import detect  

def is_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF]', text))

async def speak(text):
    voice = "ar-EG-SalmaNeural"  if is_arabic(text) else "en-US-JennyNeural"
    if os.path.exists("output.mp3"):
        os.remove("output.mp3")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("output.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("🎙️ Listening...", end="", flush=True)
        audio = r.listen(source, phrase_time_limit=10)

    try:
        text = r.recognize_google(audio, language="en")
        print(f"\n🗣️ User said: {text}\n")
        detected_language = detect(text)
        return text.lower(), detected_language
    except sr.UnknownValueError:
        try:
            text = r.recognize_google(audio, language="ar")
            print(f"\n🗣️ User said: {text}\n")
            return text.lower(), "ar"
        except sr.UnknownValueError:
            print("\n❌ Could not understand speech in English. Trying Arabic...")
            return None, None

def cal_day(language="en"):
    day_dict_en = {
        0: "Monday", 1: "Tuesday", 2: "Wednesday",
        3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"
    }
    
    day_dict_ar = {
        0: "الاثنين", 1: "الثلاثاء", 2: "الأربعاء",
        3: "الخميس", 4: "الجمعة", 5: "السبت", 6: "الأحد"
    }

    today_index = datetime.datetime.today().weekday()
    day_of_week = day_dict_ar[today_index] if language == "ar" else day_dict_en[today_index]
    message = f"📅 Today is {day_of_week}" if language == "en" else f"📅 اليوم هو {day_of_week}"
    asyncio.run(speak(message))


def wish_me(language="en", include_greeting=True):
    hour = datetime.datetime.now().hour
    t = time.strftime("%I:%M %p")

    if language == "ar":
        greeting = "صباح الخير" if hour < 12 else "مساء الخير" if hour < 17 else "مساء النور"
        out = t.split()
        if out[1] == "PM":
            t = out[0] + " مساءا"
        else:
            t = out[0] + " صباحا"
        time_message = f"الساعة الآن {t}."
    else:
        greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
        time_message = f"The time now is {t}."

    if include_greeting:
        message = f"{greeting}, {time_message}"
    else:
        message = time_message
    asyncio.run(speak(message))
def exit_message(language="en"):
    message = "Goodbye! Have a great day!" if language == "en" else "وداعًا! أتمنى لك يومًا رائعًا!"
    asyncio.run(speak(message))   

async def intro(language="en"):
    if language == "ar":
        introduction_text = (
            "أهلاً بك! اسمي سونيا، وأنا مساعد افتراضي متقدم مدعوم بأحدث تقنيات الذكاء الاصطناعي. "
            "تم تطويري بواسطة المهندس أحمد أشرف. أنا هنا لأساعدك في أداء المهام المختلفة بكفاءة ودقة عالية."
        )
    else:
        introduction_text = (
            "Hello! My name is Sonia, and I am an advanced virtual assistant powered by cutting-edge artificial intelligence. "
            "I was developed by Engineer Ahmed Ashraf. I am here to assist you with a wide range of tasks with the highest level of efficiency and accuracy."
        )
    await speak(introduction_text)
def play_audio():
    audio_file = "audio.wav"
    working_dir = os.path.dirname(os.path.abspath(__file__))
    audio_file = os.path.join(working_dir,audio_file)
    if os.path.exists(audio_file):
        asyncio.run(speak("نغمة الموبايل هي رب كل شيء"))
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
    else:
        print("❌ Audio file not found!")

if __name__ == "__main__":
    initial_text, language = command() or (None, None)
    if initial_text:
        asyncio.run(intro(language))

    while True:
        query, language = command() or (None, None)
        if query:
            if "time" in query or "الوقت" in query:
                language = "ar" if "الوقت" in query else "en"
                wish_me(language, include_greeting=False)
            elif "day" in query or "اليوم" in query:
                language = "ar" if "اليوم" in query else "en"
                cal_day(language)
            elif "نغمه" in query or "رنه" in query or "ringtone" in query:
                print("🔊 Playing ringtone...")
                play_audio()
            elif "exit" in query or "bye" in query or "خروج" in query or "وداعا" in query or "باي" in query or "وداع" in query:
                language = "ar" if any(word in query for word in ["خروج", "وداعا", "باي", "وداع"]) else "en"
                exit_message(language)
                break
