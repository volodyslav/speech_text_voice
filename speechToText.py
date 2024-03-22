from PyQt5.QtWidgets import QApplication, QComboBox, QTextEdit, QWidget, QVBoxLayout, QLabel, QFileDialog, QPushButton, QMenuBar
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import speech_recognition as sr
import pyttsx3
from textblob import TextBlob


class TextToSpeech(QWidget):
    def __init__(self):
        super().__init__()
        self.recognized_text = ""
        self.initUI()
        self.setWindowTitle("Your Speech")
        self.setGeometry(400, 200, 600, 800)
        self.connect_buttons()

    def initUI(self):
        # Main Layout for all objects(btn, labels)
        main_layout = QVBoxLayout()
        # Title of the program
        title = QLabel("Speech to Text")
        title.setFont(QFont("Arial", 30))
        # Text where text is going to be
        self.text_field = QTextEdit("")
        # Button to start recording text using microphone
        self.button_start = QPushButton("Say it!")
        self.button_record = QPushButton("Record!")
        self.button_start.setObjectName("record_btn")
        self.button_record.setObjectName("record_btn")

        self.combo_box = QComboBox(self)
        self.combo_box.addItem("File")
        self.combo_box.addItem("Save")
        self.combo_box.setStyleSheet(
            "background-color: #002642; color: white; padding: 8px; border-style: outset; border-width: 2px; border-radius: 8px;")
        self.combo_box.activated.connect(self.option_selected)

        self.sentence = QLabel("")
        # Add Q labels and to main layout
        main_layout.addWidget(self.combo_box, alignment=Qt.AlignLeft)
        main_layout.addWidget(title, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.text_field)
        main_layout.addWidget(self.sentence)
        main_layout.addWidget(self.button_start)
        main_layout.addWidget(self.button_record)


        self.setLayout(main_layout)

        self.setStyleSheet(
            """
            QComboBox{
              
                
                padding: 10px;  
            }
            QPushButton#record_btn{
                background-color: #002642;
                color: white;
                padding: 20px;
                border-radius: 10px;
                border: none;
                font-size: 20px;
            }
            QPushButton#record_btn:hover{
                background-color: #222642;
            }
            QTextEdit {
                    border: 2px solid #aaa;
                    padding: 5px;
                    color: #555;
                    font-size: 22px;
                    font-family: Mynamar MN;
            }
            """
        )

    def option_selected(self):
        current_option = self.combo_box.currentText()
        if current_option == "Save":
            current_text = self.text_field.toPlainText()
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save', "", 'Text Files (*.txt);;All Files (*)')
            if file_path:
                with open(file_path, "w") as f:
                    f.write(current_text)
        else: pass

    def text_to_speech(self):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

        # Convert text to speech
        try:
            engine.say(self.text_field.toPlainText())
            engine.runAndWait()
        except Exception as e:
            print("Error: ", e)


    def get_sentiment(self, text):
        if text:
            try:
                response = TextBlob(text)
            except Exception as e:
                print("Error: ", e)

            if response.sentiment.polarity > 0.3:
                return "Positive"
            elif response.sentiment.polarity < -0.3:
                return "Negative"
            else:
                return "Neutral"
        return None

    def connect_buttons(self):
        self.button_start.clicked.connect(self.text_to_speech)
        self.button_record.clicked.connect(self.speech_record)

    def speech_record(self):
        specker = sr.Recognizer()
        text = ""
        with sr.Microphone() as source:
            try:
                audio = specker.listen(source, timeout=2)
                text = specker.recognize_google(audio)
                print(text)
            except sr.RequestError as e:
                print(f"Can't get request ", e)
            except sr.UnknownValueError as e:
                print("Can't get your speech ", e)
            except Exception as e:
                print("There is an error: ", e)
            self.recognized_text = text
            return text

    def speech_btn(self):
        response = self.speech_record()
        sentiment = self.get_sentiment(response)
        if response and sentiment is not None:
            self.text_field.setPlainText(response)
            self.sentence.setText("Your sentence is ", str(sentiment))


if __name__ == "__main__":
    app = QApplication([])
    main = TextToSpeech()
    main.show()
    app.exec_()

