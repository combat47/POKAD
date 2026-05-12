import sys
import ctranslate2
from transformers import AutoTokenizer
import torch
from googletrans import Translator
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
import threading
from datetime import datetime
import sqlite3

import os
model_path = os.environ.get("POKAD_MODEL_PATH", "./core/llama-2-7b-chat-int8")


class OfflineLLM:
    def __init__(self, model_path):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"دستگاه: {device}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = ctranslate2.Generator(model_path, device=device, compute_type="int8")
        self.translator = Translator()
        self.name = "Podak"
        self.creator = "امیرحسین جهازی"
        self.db_path = "chat_history.db"
        self.user_name = None  # برای ذخیره اسم کاربر
        self.clear_history()

    def clear_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS history")
        cursor.execute('''CREATE TABLE history 
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, user_text TEXT, podak_text TEXT, timestamp TEXT)''')
        conn.commit()
        conn.close()
        print("تاریخچه پاک شد")

    def save_to_db(self, user_text, podak_text):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO history (user_text, podak_text, timestamp) VALUES (?, ?, ?)",
                      (user_text, podak_text, timestamp))
        conn.commit()
        conn.close()

    def get_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_text, podak_text FROM history ORDER BY id DESC LIMIT 5")
        history = cursor.fetchall()
        conn.close()
        return history

    def translate_to_english(self, text):
        try:
            translated = self.translator.translate(text, src="fa", dest="en").text
            print(f"ترجمه به انگلیسی: {translated}")
            return translated
        except Exception as e:
            print(f"خطا در ترجمه به انگلیسی: {e}")
            return text

    def translate_to_persian(self, text):
        try:
            translated = self.translator.translate(text, src="en", dest="fa").text
            print(f"ترجمه به فارسی: {translated}")
            return translated
        except Exception as e:
            print(f"خطا در ترجمه به فارسی: {e}")
            return text

    def search_web(self, query):
        try:
            urls = list(search(query, num_results=3))
            web_info = ""
            for url in urls:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = soup.find_all("p")
                web_info += " ".join([p.get_text() for p in paragraphs[:2]]) + "\n"
            return web_info.strip()
        except Exception as e:
            print(f"خطا در جستجوی وب: {e}")
            return ""

    def generate_answer(self, prompt):
        prompt_en = self.translate_to_english(prompt)

        # تشخیص سبک زبانی
        style = "formal" if "است" in prompt or "می‌باشد" in prompt else "casual"
        input_prompt = f"You are Podak, created by Amirhossein Jahazi. Answer naturally in {style} style based on the conversation history:\n"
        history = self.get_history()
        input_prompt += "Conversation history:\n"
        for user_text, podak_text in history[::-1]:
            input_prompt += f"User: {user_text}\nPodak: {podak_text}\n"
        input_prompt += f"Current question: {prompt_en}\nPodak: "

        # برندسازی
        if "تو کی هستی" in prompt.lower() or "what are you" in prompt_en.lower() or "who are you" in prompt_en.lower() or "توسط" in prompt:
            answer_en = f"I am {self.name}, created by {self.creator}. I'm here to help with anything you ask, no limits!"
            answer_fa = self.translate_to_persian(answer_en)
            self.save_to_db(prompt, answer_fa)
            return answer_fa

        # ذخیره و یادآوری اسم کاربر
        if "اسم من" in prompt or "my name is" in prompt_en.lower():
            self.user_name = prompt.split("اسم من")[-1].strip() if "اسم من" in prompt else prompt_en.split("is")[-1].strip()
            print(f"اسم کاربر ذخیره شد: {self.user_name}")
        if "یادت میاد" in prompt or "اسمم چی" in prompt or "remember" in prompt_en.lower():
            if self.user_name:
                answer_en = f"Yes, I remember! Your name is {self.user_name}. How can I assist you now?" if style == "formal" else f"Yeah, I remember! Your name’s {self.user_name}. What’s up?"
                answer_fa = self.translate_to_persian(answer_en)
                self.save_to_db(prompt, answer_fa)
                return answer_fa

        # جستجوی وب
        web_info = ""
        if "?" in prompt or "بگو" in prompt or "چگونه" in prompt:
            def web_search_thread(result):
                result[0] = self.search_web(prompt_en)

            web_result = [""]
            t = threading.Thread(target=web_search_thread, args=(web_result,))
            t.start()
            t.join()
            web_info = web_result[0]
            print(f"اطلاعات وب: {web_info[:200]}...")
            if web_info:
                input_prompt += f"\nWeb info: {web_info}"

        tokens = self.tokenizer.tokenize(input_prompt)
        output = self.model.generate_batch(
            [tokens],
            max_length=300,
            sampling_topk=50,
            sampling_temperature=0.9,
            repetition_penalty=1.2
        )
        answer_en = self.tokenizer.decode(output[0].sequences_ids[0], skip_special_tokens=True).split("Podak:")[-1].strip()
        answer_fa = self.translate_to_persian(answer_en)
        self.save_to_db(prompt, answer_fa)

        # تاریخ و زمان
        if "تاریخ" in prompt or "ساعت" in prompt or "time" in prompt_en.lower() or "date" in prompt_en.lower():
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            answer_fa += f"\nتاریخ و ساعت فعلی: {current_time}"

        return answer_fa

class ChatbotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("چت‌بات فارسی - Podak")
        self.setGeometry(100, 100, 600, 400)
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.input_field = QLineEdit(self)
        self.send_button = QPushButton("ارسال", self)
        layout = QVBoxLayout()
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_field)
        layout.addWidget(self.send_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)
        self.llm = OfflineLLM()
        self.chat_display.append("من Podak هستم، ساخته‌شده توسط امیرحسین جهازی. چطور می‌تونم کمکت کنم؟")

    def send_message(self):
        user_input = self.input_field.text().strip()
        if user_input.lower() == "خروج":
            QApplication.quit()
            return
        if user_input:
            self.chat_display.append(f"شما: {user_input}")
            def process_answer():
                answer = self.llm.generate_answer(user_input)
                self.chat_display.append(f"Podak: {answer}")
            threading.Thread(target=process_answer).start()
            self.input_field.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatbotWindow()
    window.show()
    sys.exit(app.exec())
