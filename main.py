import speech_recognition as sr
import pyttsx3
from config import *
from tkinter import Tk, Label, Entry, Button
from tkinter import messagebox
from random import choice
import DataBase

en = pyttsx3.init()
voices = en.getProperty('voices')
en.setProperty('rate', 175)
for voice in voices:
    if voice.languages[0] == b'\x05pt-br':
        en.setProperty('voice', voice.id)
        break

#Criar janela de login
jan = Tk()
jan.title('Login System')
jan.geometry("250x150")
jan.resizable(width=False, height=False)

#Definir funções
def Logar():
    User = en1.get()
    Pass2 = en2.get()

    DataBase.cur.execute("""
    SELECT * FROM LoginUsers
    WHERE (User = ? and Password = ?)
    """, (User, Pass2))
    VerifyLogin = DataBase.cur.fetchone()
    try:
        if User in VerifyLogin and Pass2 in VerifyLogin:
            messagebox.showinfo(title='Login Info', message='Acesso Confirmado. Bem Vindo')
            jan.destroy()

        # Sistema de permanencia

    except:
        messagebox.showerror(title='Login Info', message='Acesso Negado. Verifique se você esta cadastrado no sistema.')

def RegisterData():
    Name = en1.get()
    Pass = en2.get()

    if Name == "" and Pass == "":
        messagebox.showerror(title="Register Error", message="Preencha todos os camos")
    else:
        DataBase.cur.execute("""
        INSERT INTO LoginUsers(User, Password) VALUES(?, ?)
        """, (Name, Pass))
        DataBase.conn.commit()
        messagebox.showinfo(title="Register Info", message="Register Sucessfull")

#Criar Widgets
text1 = Label(jan, text='Login: ')
text2 = Label(jan, text='Passworld: ')
en1 = Entry(jan)
en2 = Entry(jan, show='*')
bt1 = Button(jan, text='Confirm', command=Logar)
bt2 = Button(jan, text='Register', command=RegisterData)

#Posicionar Widgets
text1.grid(row=0, column=0)
text2.grid(row=1, column=0)
en1.grid(row=0, column=1)
en2.grid(row=1, column=1)
bt1.grid(row=2, column=1)
bt2.grid(row=3, column=1)

#Deixar a janela em loop
jan.mainloop()

# Sistema de permanencia

# Sistema de som
def sai_som(reposta):
    en.say(reposta)
    en.runAndWait()

user = "Bem vindo"

# Sistema principal
def assistente():
    print("=" * len(user))
    print(user)
    print("=" * len(user))
    sai_som(user)
    print("Ouvindo...")

    while True:
        resposta_erro_aleatoria = choice(lista_erros)
        # rec = sr.Recognizer()

        # with sr.Microphone() as s:
        # rec.adjust_for_ambient_noise(s)

        while True:
            try:
                # audio = rec.listen(s)
                entrada = input("")
                entrada = entrada.lower()
                print("User: {}".format(entrada.capitalize()))

                # Abri links no navegador
                if "abrir" in entrada:
                    resposta = abrir(entrada)

                # Tocar música do youtube
                elif entrada.startswith('tocar'):
                    sai_som("Carregando")
                    resposta = tocar(entrada)

                # Hibernar o sistema
                elif 'hibernar' in entrada:
                    sai_som('Hibernando')
                    while True:
                        hib = input('')
                        if hib == 'Sexta-feira':
                            resposta = 'Estou ouvindo mestre'
                            break

                # Fazer pesquisa no google
                elif "pesquisar por" in entrada:
                	resposta = pesquisa(entrada)

                # Operações matemáticas
                elif "quanto é" in entrada:
                    entrada = entrada.replace("quanto é", "")
                    resposta = calcula(entrada)

                # Pede tempo
                elif "qual a temperatura" in entrada:

                    lista_tempo = temperatura()
                    temp = lista_tempo[0]
                    temp_max = lista_tempo[1]
                    temp_min = lista_tempo[2]

                    resposta = "A temperatura de hoje é {:.2f}º. Temos uma máxima de {:.2f}º e uma minima de {:.2f}º".format(
                        temp, temp_max, temp_min)

                # Informações da cidade
                elif "informações" in entrada and "cidade" in entrada:

                    resposta = "Mostrando informações da cidade"
                else:
                    resposta = conversas[entrada]

                if resposta == "Mostrando informações da cidade":
                    # mostra informações da cidade

                    lista_infos = clima_tempo()
                    longitude = lista_infos[0]
                    latitude = lista_infos[1]
                    temp = lista_infos[2]
                    pressao = lista_infos[3]
                    humidade = lista_infos[4]
                    temp_max = lista_infos[5]
                    temp_min = lista_infos[6]
                    v_speed = lista_infos[7]
                    v_direc = lista_infos[8]
                    nebulosidade = lista_infos[9]
                    id_da_cidade = lista_infos[10]

                    print("Assistente:")
                    print("Mostrando informações de {}\n\n".format(cidade))
                    sai_som("Mostrando informações de {}".format(cidade))
                    print("Longitude: {}, Latitude: {}\nId: {}\n".format(longitude, latitude, id_da_cidade))
                    print("Temperatura: {:.2f}º".format(temp))
                    print("Temperatura máxima: {:.2f}º".format(temp_max))
                    print("Temperatura minima: {:.2f}º".format(temp_min))
                    print("Humidade: {}".format(humidade))
                    print("Nebulosidade: {}".format(nebulosidade))
                    print("Pressao atmosférica: {}".format(pressao))
                    print("Velocidade do vento: {}m/s\nDireção do vento: {}".format(v_speed, v_direc))

                else:
                    print("Assistente: {}".format(resposta))
                    sai_som("{}".format(resposta))

            except sr.UnknownValueError:
                sai_som(resposta_erro_aleatoria)
            except KeyError:
                pass


if __name__ == '__main__':
    intro()
    sai_som("Iniciando")
    assistente()