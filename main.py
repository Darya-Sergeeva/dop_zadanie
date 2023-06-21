from kivy.app import App                   # основной класс приложения
from kivy.uix.gridlayout import GridLayout # графический интерфейс
from kivy.uix.button import Button         # виджет для создания кнопки
from kivy.uix.textinput import TextInput   #Виджет для ввода текста
from kivy.uix.label import Label           #виджет для отоьражения текста

from sqlalchemy import create_engine, Column, Integer, String # для подключения к базе данных
from sqlalchemy.ext.declarative import declarative_base # описание таблицы
from sqlalchemy.orm import sessionmaker #для создания сессии


engine = create_engine('sqlite:///:memory:', echo=True) #подключение к базе данных находящейся в памяти (stateless)
Base = declarative_base() #объект, который описывает классы таблицы
Session = sessionmaker(bind=engine) #связывает базу данных с сессией

"Создание таблицу базы данных"
class Message(Base):
    __tablename__ = 'Гостевая книга'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    message = Column(String)



class MainApp(App):
    "Создание графического интерфейса"
    def build(self):
        self.title = 'Гостевая книга'

        layout = GridLayout(cols=1, row_force_default=True, row_default_height=40)
        self.name_input = TextInput(text='Имя', size_hint_x=None, width=500)
        self.email_input = TextInput(text='Электронная почта', size_hint_x=None, width=500)
        self.message_input = TextInput(text='Текст сообщения', size_hint_x=None, width=2500)
        self.submit_button = Button(text='Отправить', size_hint_x=None, width=150, on_press=self.submit_form)
        self.message_label = Label(text='', size_hint_x=None, width=190)

        layout.add_widget(self.name_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.message_input)
        layout.add_widget(self.submit_button)
        layout.add_widget(self.message_label)

        return layout

    "Сохранение данных в базу данных"
    def submit_form(self, data):
        name = self.name_input.text.strip()
        email = self.email_input.text.strip()
        message = self.message_input.text.strip()
        if not name or not email or not message:
            self.message_label.text = 'Заполните все поля'
            return
        session = Session()
        session.add(Message(name=name, email=email, message=message))
        session.commit()
        self.name_input.text = 'Имя'
        self.email_input.text = 'Электронная почта'
        self.message_input.text = 'Ваше сообщение'
        self.message_label.text = 'Сообщение отправлено'




if __name__ == '__main__':
    Base.metadata.create_all(engine)
    MainApp().run()




