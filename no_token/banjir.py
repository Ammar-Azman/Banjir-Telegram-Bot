import os
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import mysql.connector 
import time 


API_TOKEN = ""
bot = telebot.TeleBot(API_TOKEN)

mydb = mysql.connector.connect(
    user = 'root', 
    passwd = '',
    host = 'localhost',
    port = "",
    database = ''
)
mycursor = mydb.cursor()

#<---------------------TELEGRAM: MANGSA------------------------------------> 
# handle command, /start
@bot.message_handler(commands=['start', 'mula'])
def start(message):
    
    user = message.from_user

    bot.reply_to(message, "BOT BANJIR TELAH DIAKTIFKAN 🚩")
    time.sleep(2)

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Mangsa 🆘", callback_data="mangsa"),
                InlineKeyboardButton("Penyelamat 🔰", callback_data="penyelamat"))

    bot.send_message(message.chat.id,
                 """🚨
                \nKepada {0} {1}
                \nSebelum BOT BANJIR mula, sila pilih perananan anda. 
                \nAdakah anda seorang 
                \n▶ mangsa 
                \natau 
                \n▶ penyelamat
                \nJika mangsa, 
                tekan ini 👉 [Mangsa🆘 ] 
                \nJika penyelamat, 
                tekan ini 👉 [Penyelamat🔰]
                \nTekan butang dibawah 👇
                 
                 """.format(user.first_name,user.last_name), reply_markup=markup) #reply_markup=markup)

# command, /Mangsa -- untuk mangsa banjir

@bot.message_handler(commands=["mangsa"])
def start_mangsa(message):
    user = message.from_user
    
    bot.send_message(message.chat.id, """🚨
                                        \nTarik nafas dan bertenang. 
                                        \nIni adalah proses pemberian maklumat supaya anda dapat diselamatkan.
                                        \nMasukkan maklumat lokasi anda dengan format berikut; 
                                        \n/lokasi[jarak]/nama_lokasi
                                        \n Contoh👇 \n/lokasi /Ipoh \n/lokasi /Sri Muda
                                        \n🌟Pastikan anda meletakkan [jarak] dan "/" seperti format diatas.
                                        """)

@bot.message_handler(commands=["lokasi"])
def get_lokasi(message):
    user_chat_id = message.chat.id
    
    user_text_lokasi = message.text.split('/')

    user_lokasi_info = user_text_lokasi[2].title()
    val = (user_chat_id, user_lokasi_info)

    mycursor.execute("INSERT INTO banjir_info (tele_chat_id, Lokasi) VALUES (%s,%s)", val)
    mydb.commit()
    bot.reply_to(message, '''🚨 RESPON 🚨
                            \nMaklumat berjaya disimpan.✅ 
                            \n----------------------------------------------------------------
                            \nSila masukkan negeri dengan format berikut:
                            \n/neg[jarak]/nama_lokasi
                            \n Contoh👇 \n/neg /Perak
                            
                            \n🌟Pastikan anda meletakkan [jarak] dan "/" seperti format diatas.''')

        

@bot.message_handler(commands=["neg"])
def get_negeri(message):
    user_chat_id = message.chat.id
    
    user_text_neg = message.text.split('/')

    user_neg_info =user_text_neg[2].title()
    
    val = (user_neg_info,user_chat_id)
    

    mycursor.execute("UPDATE banjir_info SET Negeri = (%s) WHERE tele_chat_id = (%s)", val)
    mydb.commit()
    bot.reply_to(message, '''🚨 RESPON 🚨
                            \nMaklumat berjaya disimpan.✅
                            \n----------------------------------------------------------------
                            \nKemudian, sila hantar pin lokasi anda dari tempat kejadian. 
                            \nCaranya:
                            \n1-Tekan logo klip kertas di bahagian chat
                            \n2-Pilih "location"
                            \n3-Pin setepat-tepatnya pada lokasi anda
                            \n4-Tekan "Send selected location"''')

@bot.message_handler(content_types=["location"])     
def accept_location(message):
    user_chat_id = message.chat.id
    
    user_longitude = message.location.longitude
    user_latitude = message.location.latitude
    location_url = "https://www.google.com/maps/search/?api=1&query={0}%2C{1}".format(user_latitude,user_longitude)
    
    val = (location_url,user_chat_id)
    mycursor.execute("UPDATE banjir_info SET Koordinat = (%s) WHERE tele_chat_id = (%s)", val)
    mydb.commit()
    bot.reply_to(message, '''🚨 RESPON 🚨
                            \nPin lokasi berjaya disimpan.✅
                            \n----------------------------------------------------------------
                            \nAkhir sekali, sila update jumlah mangsa di lokasi dengan format berikut
                            \nbil_mangsa[jarak]/bilangan_mangsa
                            \n Contoh👇 \n/bil_mangsa /5 orang''')

@bot.message_handler(commands=["bil_mangsa"])
def get_bil_mangsa(message):
    user_chat_id = message.chat.id
    user_text_bil_mangsa = message.text.replace(" ", "")
    user_text_bil_mangsa = user_text_bil_mangsa.split('/')

    user_bil_mangsa = user_text_bil_mangsa[2]

    val = (user_bil_mangsa,user_chat_id)
    mycursor.execute("UPDATE banjir_info SET Bil_mangsa = (%s) WHERE tele_chat_id = (%s)", val)
    mydb.commit()
    bot.reply_to(message, '''🚨 RESPON 🚨
                            \nKesemua maklumat berjaya disimpan.✅
                            \n----------------------------------------------------------------
                            \nHarap bersabar menunggu penyelamat datang. 🙏
                            \nTerus kuat dan berdoa 🤲''')
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("MOHON ✅", callback_data="mohon"),
                InlineKeyboardButton("TIADA❌", callback_data="tiada"))

    time.sleep(4)
    bot.send_message(message.chat.id, """🚨 PERMINTAAN 🚨
                                            \nUntuk memohon keperluan barang/makanan/powerbank/kit disebabkan kecemasan, \nTekan ➡ [MOHON✅] 
                                            \nJika tiada permintaan, \nTekan ➡[TIADA❌] """, reply_markup=markup)

   
#### ----------------- input dari mangsa tempat kejadian---------------------

#---request barang keperluan
@bot.message_handler(commands=["hidup"])
def hidup(message):
    bot.send_message(message.chat.id, """\n 🚨 INPUT 🚨
                                        \nMasukkan info dengan format berikut; 
                                        \n 👉 /barang [jarak]/nama_Barang/ kuantiti/ keterangan_lain
                                        \n 🌟Pastikan anda meletakkan [jarak] dan "/" seperti format diatas.
                                        \n 🌟Jika anda mempunyai lebih daripada satu permintaan, gunakan arahan /barang yang baru.
                                        \n 👇 \nContoh: 
                                        \n Barang 1️⃣: 
                                        \n/barang /Powerbank/ 5 / Bateri habis ---> [Hantar]
                                        \n Barang 2️⃣: 
                                        \n/barang /Biskut/ 2 / Lapar ---> [Hantar]""")
    user = message.from_user
    #reminder 
@bot.message_handler(commands=["barang"])
def get_barang(message):
    try:
        user = message.from_user
        user_text = message.text.split('/')
        barang = user_text[2]
        kuantiti = user_text[3]
        catatan = user_text[4]
        
        val = [barang, kuantiti, catatan]
        mycursor.execute("INSERT INTO barang_info (Barang, Kuantiti, Catatan) VALUES (%s, %s, %s)", val)
        mydb.commit()
        time.sleep(3)
        bot.reply_to(message, 'Maklumat berjaya disimpan. ✅ \nPenyelamat akan cuba sedaya upaya memenuhi keperluan anda. 🙏')  

        time.sleep(4)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("SELAMAT✅", callback_data="selamat"))

        for i in range(3):
            bot.reply_to(message, """🚨 PERINGATAN 🚨 
                                    \nKepada anda, jika anda TELAH DISELAMATKAN, sila tekan butang [SELAMAT✅]👇. 
                                    \nJika BELUM, ABAIKAN mesej ini sehingga anda diselamatkan.""", reply_markup = markup)
            timing = 60*60
            time.sleep(timing) # remind again after 1 hrs  

    except Exception as e1:
        bot.send_message(message.chat.id, "⚠ Format Salah: Sila ikut format 👉\n\n/barang [jarak]/nama_Barang/ kuantiti/ keterangan_lain")

#jika tiada barang
@bot.message_handler(commands=["tiada"])
def tiada_permintaan_barang(message):
    bot.reply_to(message, "Baik, maklumat diterima. Buat masa sekarang, cuba sedaya upaya untuk berada di tempat tinggi atau selamat sebelum penyelamat sampai. 💪")
    user = message.from_user
    time.sleep(4)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("SELAMAT✅", callback_data="selamat"))
    for i in range(3):
        bot.reply_to(message, """🚨 PERINGATAN 🚨 
                                \nKepada anda, jika anda TELAH DISELAMATKAN, sila tekan butang [SELAMAT✅]👇. 
                                \nJika BELUM, ABAIKAN mesej ini sehingga anda diselamatkan.""", reply_markup = markup)
        timing = 60*60
        time.sleep(timing) # remind again after 1 hrs

@bot.message_handler(commands=["selamat"])
def update_selamat(message):
    user = message.from_user          
    msg = bot.reply_to(message, "Keadaan terkini anda sedang dikemaskini...")
    bot.register_next_step_handler(msg, update_status_mangsa(message))

def update_status_mangsa(message):
    user_chat_id = message.chat.id
    
    mycursor.execute("UPDATE banjir_info SET Status = 'TELAH SELAMAT✅' WHERE tele_chat_id = {}".format(user_chat_id))
    mydb.commit()

    time.sleep(2)
    bot.reply_to(message, """Kemaskini status berjaya.👍\nTerima kasih kerana terus kuat menghadapi musibah ini. 
    \nSemoga Tuhan memberkati kita.🤲""")               



################################################################################################################

#------------------command,  /Penyelamat ------------------- 

@bot.message_handler(commands=["penyelamat"])
def start_penyelamat(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    button_1 = InlineKeyboardButton('CARI 🔍', callback_data="semak")
    
    markup.add(button_1)
    bot.send_message(message.chat.id, """Jika anda seorang Penyelamat🔰, ikut langkah berikut:
                                        \n1️⃣ Ketahui senarai negeri mangsa banjir, \ntekan butang ➡ [CARI🔍]
                                       """, reply_markup=markup)

### semak negeri terbabit dalam banjir
@bot.message_handler(commands=["semak"])
def get_negeri_list(message):
    mycursor.execute("SELECT Negeri from banjir_info")
    list_negeri = mycursor.fetchall()

    list_remove_tuple_in_list_negeri = [k for x in list_negeri for k in x]
    my_dict = {i:list_remove_tuple_in_list_negeri.count(i) for i in list_remove_tuple_in_list_negeri}
    
    emp_set = ""
    for k in my_dict:
        emp_set = emp_set + str(k) +  " ➡ " + str(my_dict[k]) + " laporan" +  "\n\n"
    
    bot.reply_to(message, """Penyelamat🔰 \nBerikut senarai data nama negeri yang terdapat dalam database: 
                            \n{} \nUntuk menjejaki lokasi mangsa banjir, patuhi format dibawah. 
                            \n /negeri[jarak]/nama_negeri
                            \nnama_negeri menggunakan nama negeri terpapar diatas 👆
                            \n Contoh 👇
                            \n/negeri /Perak""".format((emp_set)))


@bot.message_handler(commands=["negeri"])
def get_info_negeri(message):
    try:
        
        user_text = message.text.split("/")

        negeri = user_text[2].title()
        bot.send_message(message.chat.id, "Carian sedang dilakukan...")
        #time.sleep(1)
        mycursor.execute("SELECT Negeri from banjir_info")
        list_negeri = mycursor.fetchall()

        no_tuple_list_negeri = [list(data) for data in list_negeri]
    
        flat_list = [y for data in no_tuple_list_negeri for y in data]
        

        # check wether the Negeri is exist in the Database
        if negeri not in flat_list:
            bot.reply_to(message, '❌Ralat: Tiada maklumat mangsa dalam negeri dinyatakan. \nSila cuba nama negeri di dalam senarai semak.')

        elif negeri in flat_list:
            mycursor.execute("SELECT Lokasi, Koordinat, Bil_mangsa, Status FROM banjir_info WHERE Negeri = '{}'".format(negeri))
            hasil_carian = mycursor.fetchall()

            # balas informasi mangsa  kepada Penyelamat
            balas = ""
            for full_info in hasil_carian:
                balas = balas + "🆘" + str(full_info) + "\n\n"
            
            # delete simbol tak perlu
            balas = balas.replace("'", "")
            balas = balas.replace(",", " -- ")
            balas = balas.replace("(", "")
            balas = balas.replace(")", "")

            msg = bot.reply_to(message, balas)
            bot.register_next_step_handler(msg, mesej_keperluan(message))
            

    except Exception as e2:
        bot.reply_to(message, "⚠ Format Salah: Sila ikut format 👉\n\n/negeri[jarak]/nama_Negeri")

def mesej_keperluan(message):
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    button_2 = InlineKeyboardButton('KEPERLUAN 🍫', callback_data="mesej" )
    markup.add(button_2)

    bot.reply_to(message, "2️⃣ Ketahui barang keperluan mangsa banjir, \ntekan butang ➡  [KEPERLUAN 🍫]", reply_markup=markup)

### semak barang keperluan mangsa 
@bot.message_handler(commands=["keperluan"])
def get_barang_from_db(message):
    mycursor.execute("SELECT Barang from barang_info")
    list_barang = mycursor.fetchall()
    convert_to_set_avoid_duplicate = set(list_barang)

    emp_set = ""
    for k in convert_to_set_avoid_duplicate:
        emp_set = emp_set + str(k) + "\n"

    emp_set = emp_set.replace("'", "")
    emp_set = emp_set.replace(" ", "")
    emp_set = emp_set.replace(",", "")
    emp_set = emp_set.replace("(", "▶ ")
    emp_set = emp_set.replace(")", "")

    bot.reply_to(message, "Penyelamat🔰 \nKala ini, berikut adalah senarai barang keperluan mangsa: \n\n{}".format(emp_set))

## -- handle all inline keyboard --
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "mangsa":
        start_mangsa(call.message)
    elif call.data == 'penyelamat':
        start_penyelamat(call.message)
    elif call.data == 'mohon':
        hidup(call.message)
    elif call.data == "tiada":
        tiada_permintaan_barang(call.message)
    elif call.data == "selamat":
        update_selamat(call.message)
    elif call.data == 'semak':
        get_negeri_list(call.message)
    elif call.data == "mesej":
        get_barang_from_db(call.message)


#------------- handle wrong input ----------------------
@bot.message_handler(func=lambda message:True)
def echo_all(message):
    bot.reply_to(message, "⚠ Input Salah: Sila masukkan input mengikut format yang ditetapkan.")

print('bot start running')
bot.infinity_polling()