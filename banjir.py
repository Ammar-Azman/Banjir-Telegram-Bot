import os
import telebot
from telebot import types
import mysql.connector 
import requests
import json
import time 

API_TOKEN = "5043764359:AAE8z5Vvl9qgzZPd8pbci4IXchAnpNqDTtc"
bot = telebot.TeleBot(API_TOKEN)

mydb = mysql.connector.connect(
    user = 'root', 
    passwd = '',
    host = 'localhost',
    port = 3307,
    database = 'banjir_bot'
)
mycursor = mydb.cursor()

#<---------------------TELEGRAM: MANGSA------------------------------------> 
# handle command, /start
@bot.message_handler(commands=['start', 'mula'])
def salam(message):
    user = message.from_user

    #button
    markup = types.ReplyKeyboardMarkup(row_width=0.5)
    button_1 = types.KeyboardButton('/Mangsa🆘') 
    button_2 = types.KeyboardButton('/Penyelamat🔰') 
    markup.row(button_1,button_2)
    

    bot.send_message(message.chat.id,
                 """🚨
                \nKepada {}.
                \nJika anda terperangkap, tarik nafas dan bertenang. 
                \nAdakah anda seorang mangsa atau penyelamat?
                \nJika mangsa, tekan ini 👉 /Mangsa 🆘
                \nJika penyelamat, tekan ini 👉 /Penyelamat🔰
                 
                 """.format(user.first_name), reply_markup=markup)

# command, /Mangsa -- untuk mangsa banjir
@bot.message_handler(commands=["Mangsa🆘"])
def set_loc(message):
      
    bot.send_message(message.chat.id, """Masukkan info dengan format berikut; 
                                        \n /tolong[jarak]/Lokasi/ Negeri / Koordinat/ Bilangan mangsa
                                        \n Contoh: 
                                        \n👉\n/tolong /Ipoh/ Perak/ 4.633028068476687, 101.08841026711355/ 5 orang""")

#### ----------------- input dari mangsa tempat kejadian---------------------

@bot.message_handler(commands=["tolong"])
def get_loc(message):
    try:
        
        user_text = message.text.replace(" ", "")
        user_text = user_text.split('/')
        nama_mangsa = user_text[2].title()
        loc = user_text[3].title()
        neg = user_text[4].title()
        coo = user_text[5]
        bilmang = user_text[6]
        val = [loc,neg,coo,bilmang]
        mycursor.execute("INSERT INTO banjir_info (Lokasi, Negeri, Koordinat, Bil_mangsa) VALUES (%s, %s, %s, %s)", val)

        mydb.commit()
        bot.reply_to(message, 'Maklumat anda telah disimpan. \nHarap bersabar menunggu penyelamat datang. \nTerus kuat dan berdoa 🤲')

        time.sleep(3)
        markup = types.ReplyKeyboardMarkup(row_width=2)
        button_1 = types.KeyboardButton('/hidup')
        markup.row(button_1)
        
        bot.send_message(message.chat.id, "Jika anda memerlukan barang/makanan/powerbank/kit kecemasan, \ntekan ini ---> /hidup", reply_markup=markup)

    except Exception as e0:
        bot.send_message(message.chat.id, "⚠ Format Salah: Sila ikut format 👉\n\n/tolong[jarak]/Lokasi/ Negeri / Koordinat/ Bilangan mangsa")         

#---request barang keperluan
@bot.message_handler(commands=["hidup"])
def set_loc(message):
    bot.send_message(message.chat.id, """Masukkan info dengan format berikut; 
                                        \n 👉 /barang [jarak]/nama_Barang/ kuantiti/ keterangan_lain
                                        \n 👉 Contoh: /barang /Powerbank/ 5 / Bateri habis""")
@bot.message_handler(commands=["barang"])
def get_loc(message):
    user_text = message.text.split('/')
    barang = user_text[2]
    kuantiti = user_text[3]
    catatan = user_text[4]
    
    val = [barang, kuantiti, catatan]
    mycursor.execute("INSERT INTO barang_info (Barang, Kuantiti, Catatan) VALUES (%s, %s, %s)", val)
    mydb.commit()
    bot.reply_to(message, 'Maklumat berjaya disimpan. Penyelamat akan cuba sedaya upaya memenuhi keperluan anda. 🙏')      

################################################################################################################

#---------------------- command, /Penyelamat 

@bot.message_handler(commands=["Penyelamat🔰"])
def greet_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button_1 = types.KeyboardButton('/semak')
    markup.row(button_1)
    bot.send_message(message.chat.id, """Jika anda seorang penyelamat, ikut format berikut:
                                        \n1- Untuk mengetahui senarai negeri dalam database---> /semak 
                                        \n2- Untuk mengesan lokasi mangsa banjir
                                        \n 👉 /negeri[jarak]/nama_negeri
                                        \n Contoh:
                                        \n 👉/negeri /Perak""", reply_markup=markup)
@bot.message_handler(commands=["semak"])
def get_negeri_list(message):
    mycursor.execute("SELECT Negeri from banjir_info")
    list_negeri = mycursor.fetchall()
    no_tuple_list_negeri = [list(data) for data in list_negeri]
    flat_list = [y for data in no_tuple_list_negeri for y in data]
    flat_set = set(flat_list)
    bot.reply_to(message, "Berikut senarai data nama negeri yang terdapat dalam database; {}".format(flat_set))

@bot.message_handler(commands=["negeri"])
def get_info(message):
    try:
        user_text = message.text.replace(" ", "")
        user_text = user_text.split("/")

        negeri = user_text[2]
        bot.send_message(message.chat.id, "Carian sedang dilakukan...")
        #time.sleep(1)
        mycursor.execute("SELECT Negeri from banjir_info")
        list_negeri = mycursor.fetchall()

        no_tuple_list_negeri = [list(data) for data in list_negeri]
        flat_list = [y for data in no_tuple_list_negeri for y in data]

        # check wether the Negeri is exist in the Database
        if negeri not in flat_list:
            bot.reply_to(message, 'Tiada maklumat mangsa dalam negeri dinyatakan. Sila cuba nama negeri lain.')

        elif negeri in flat_list:
            mycursor.execute("SELECT Lokasi, Koordinat, Bil_mangsa FROM banjir_info WHERE Negeri = '{}'".format(negeri))
            hasil_carian = mycursor.fetchall()
            # location in url format
            url_location = []
            url_info_list = [x[1] for x in hasil_carian]
            for coo in url_info_list:
                coo_split = coo.split(",")
                coo_1 = coo_split[0]
                coo_2 = coo_split[1]
                url_print = "https://www.google.com/maps/search/?api=1&query={0}%2C{1}".format(coo_1, coo_2)
                url_print = url_print.replace(" ", "")
                url_location.append(url_print)

            # balas informasi mangsa  kepada Penyelamat
            balas = ""
            for full_info, url_v in zip(hasil_carian, url_location):
                balas = balas + "🆘" + str(full_info) + "\n" + url_v + "\n\n"
            
            # delete simbol tak perlu
            balas = balas.replace("'", "")
            balas = balas.replace(",", " -- ")
            balas = balas.replace("(", "")
            balas = balas.replace(")", "")

            bot.reply_to(message, balas)

    except Exception as e1:
        bot.send_message(message.chat.id, "⚠ Format Salah: Sila ikut format 👉\n\n/negeri[jarak]/nama_Negeri")

#------------- handle wrong input ----------------------
@bot.message_handler(func=lambda message:True)
def echo_all(message):
    bot.reply_to(message, "⚠ Input Salah: Sila masukkan input mengikut format yang ditetapkan.")


print('bot start running')
bot.infinity_polling()