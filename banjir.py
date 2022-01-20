import os
import telebot
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

#----UNTUK MANGSA---
#---- TELEGRAM --- 
@bot.message_handler(commands=['mula'])
def salam(message):
    bot.reply_to(message,
                 """🚨🚨🚨
                 \nJika anda terperangkap, tarik nafas dan bertenang. 
                \n Adakah anda seorang mangsa atau penyelamat?
                Jika mangsa, tekan ini ---> /sos
                Jika penyelamat, tekan ini --> /penyelamat
                 
                 """)
# --- kecemasan minta tolong -- 
@bot.message_handler(commands=["sos"])
def set_loc(message):
    bot.send_message(message.chat.id, """Masukkan info dengan format berikut; 
                                        \n /help /Lokasi/ Negeri/ Koordinat/ Bilangan mangsa

                                        \n Contoh: /help /Ipoh/Perak/ 4.5975° N, 101.0901° E/ 5 orang""")
    bot.send_message(message.chat.id, "Jika anda memerlukan barang/makanan/powerbank/kit kecemasan, \ntekan ini ---> /hidup")

@bot.message_handler(commands=["help"])
def get_loc(message):
    user_text = message.text.split('/')
    loc = user_text[2]
    neg = user_text[3]
    coo = user_text[4]
    bilmang = user_text[5]
    val = [loc,neg,coo,bilmang]
    mycursor.execute("INSERT INTO banjir_info (Lokasi, Negeri, Koordinat, Bil_mangsa) VALUES (%s, %s, %s, %s)", val)

    mydb.commit()
    bot.reply_to(message, 'data anda telah disimpan')

#---request barang keperluan
@bot.message_handler(commands=["hidup"])
def set_loc(message):
    bot.send_message(message.chat.id, """Masukkan info dengan format berikut; 
                                        \n /kit /Barang/ Kuantiti/ Keterangan lain

                                        \n Contoh: /kit/Powerbank/5/ Bateri habis""")

@bot.message_handler(commands=["kit"])
def get_loc(message):
    user_text = message.text.split('/')
    barang = user_text[2]
    kuantiti = user_text[3]
    catatan = user_text[4]
    
    val = [barang, kuantiti, catatan]
    mycursor.execute("INSERT INTO barang_info (Barang, Kuantiti, Catatan) VALUES (%s, %s, %s)", val)
    mydb.commit()
    bot.reply_to(message, 'data anda telah disimpan')      

################################################################################################################

#---------------------- UNTUK PENYELAMAT 

@bot.message_handler(commands=["penyelamat"])
def greet_message(message):
    bot.send_message(message.chat.id, """Jika anda seorang penyelamat, ikut format seperti berikut untuk mengetahui lokasi mangsa banjir
                                        \n /mangsa/negeri
                                        \n Contoh:
                                        \n /mangsa/Perak""" )

@bot.message_handler(commands=["mangsa"])
def get_info(message):
    user_text = message.text.split(" ")

    negeri = user_text[1]
    
    bot.send_message(message.chat.id, "Carian sedang dilakukan...")
    #time.sleep(1)
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
    

print('bot start running')
bot.infinity_polling()