import os
import telebot
from telebot import types
import sqlite3
from create_db import create_db
import db_functions
import time

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')
user = bot.get_me()

connect = sqlite3.connect('database.db')
cursor = connect.cursor()
cursor.execute('SELECT * FROM users')
users = cursor.fetchall()

total_users = len(users)



photos_id = []
videos_id = []
documents_id = []

admins = ["list of useradmin id"]
admins_usersnames = []
caption_photo = []
caption_video = []

photos_id_to_use = []
video_id_to_use = []
document_id_to_use = []

users_id_to_delete = []


def main_admin_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(types.InlineKeyboardButton("Выполнить рассылку", callback_data="/send_msg"),
               types.InlineKeyboardButton("Текущий статус", callback_data="/usr_stats")
               )
    
    return markup

def main_users_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("Тех. поддержка", url='https://t.me/proweb_support'),
               types.InlineKeyboardButton("Коворкинг", callback_data="/coworking"),
               types.InlineKeyboardButton("Конкурсы", callback_data="/contests"),
               types.InlineKeyboardButton("Посетить сайт", url="https://proweb.uz"),
               types.InlineKeyboardButton("Базовый курс", callback_data="/basic_course"),
               types.InlineKeyboardButton("Оставить отзыв", callback_data="/reviews"),
               types.InlineKeyboardButton("Правила обучения", callback_data="/learning_rules"))
    
    return markup


def nav_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_m = types.KeyboardButton("На главную")
    item_h = types.KeyboardButton('Help ❓')
    markup.row(item_m,item_h)
    return markup


def send_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        types.InlineKeyboardButton("Отменить", callback_data="/cancel"),
        types.InlineKeyboardButton("Отправить", callback_data="/send")
               )
    
    return markup

def whats_next():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        # types.InlineKeyboardButton("Показать", callback_data="/show_msg"),
        types.InlineKeyboardButton("Закрепить", callback_data="/pinn_msg"),
        types.InlineKeyboardButton("Удалить", callback_data="/dell_msg"),
               )
    return markup



for user in users:
    for admin in admins:
        if admin in user:
            admins_usersnames.append(user[1])

  
def get_adm_names():
    return " ,".join(admins_usersnames)

@bot.message_handler(commands=['start'])
def handle_command(message):
    id = message.from_user.id
    username = message.from_user.username
    msg_id = id
    db_functions.add_user(id, username, msg_id)

    if message.chat.id in admins:

        bot.send_message(message.chat.id, 
                    "Данный интерфейс разработан специально для админов центра <b>PROWEB</b> \n \n" +
                    "Возможности бота: \n \n" +

                    '&#9632 <b>Рассылка/Пересылка сообщений</b> - (text, photo, video, document, media-group, poll) пользователям \n \n' +
                    '&#9632 <b>Закрепление сообщений</b> \n \n' +
                    '&#9632 <b>Удаление сообщений</b> \n \n' +
                    '&#9632 <b>Отчет после Рассылки/Пересылки</b> -  кол-во отправленных и не отправленных сообщении \n \n' +
                    '&#9632 <b>Текущий статус</b> - показывать кол-во пользователей бота: актив/не актив (пользователи которые заблокировали бота) \n \n' +
                    'Чем займемся?'
                      ,reply_markup=main_admin_markup())

    else:
        bot.send_message(message.chat.id, 'Вас приветствует бот курсов современных профессий PROWEB! 🤗', reply_markup = nav_markup())
        bot.send_message(message.chat.id, 
                         'Данный бот разработан специально для студентов центра <b>PROWEB</b>. \n \n' +
                         'Возможности бота: \n \n' +
                         '&#9632 <b>Отправить текстовое сообщение</b> - задать любой вопрос, связанный с вашим обучением, и получить обратную связь в ближайшее время. \n \n' +
                         '&#9632 <b>Тех. поддержка</b> - связаться с технической поддержкой и решить вопросы, связанные с компьютерной техникой. Также можно получить консультацию и помощь в сборке личного комьютера. \n \n' +
                         '&#9632 <b>Коворкинг</b> - связаться с коворкинг администратором и забронировать место на посещение. \n \n' +
                         '&#9632 <b>Конкурсы</b> - принять участие в ежемесечных конкурсах, где можно выиграть ценные призы. \n \n' +
                         '&#9632 <b>Посетить сайт</b> - переход на страницу центра PROWEB, где вы найдете всю подробную информацию о центре и о доступных курсах. \n \n' +
                         '&#9632 <b>Базовый курс</b> - записаться на бесплатный базовый курс по компьютерной грамотности. \n \n' +
                         '&#9632 <b>Оставить отзыв</b> - возможность поделиться приятными впечетлениями об обучении в центре PROWEB. Если вы столкнулись с трудностями, можно оставить жалобу или пожелание. Мы благодарны каждому отзыву. \n \n' +                         
                         '&#9632 <b>Правила обучения</b> - подробная информация о правилах обучения в центре PROWEB \n \n' +
                         '&#9632 <b>На главную</b> - возможность вернуться на главную страницу бота и увидеть все его возможности. \n \n' +
                         '&#9632 <b>Ozbek tili</b> - переключение языка с русского на узбекский.'
                        ,reply_markup=main_users_markup())
      



@bot.message_handler(commands=['help'])
def help_command(message):
   keyboard = telebot.types.InlineKeyboardMarkup()
   keyboard.add(
       telebot.types.InlineKeyboardButton(
           'Написать разработчику', url='telegram.me/darl1ne'
           
       )
   )
   bot.send_message(
       message.chat.id,
       '1) \n' +
       '2) \n' +
       '3) \n' +
       '4) \n' +
       '5) ',
       reply_markup=keyboard
   )




@bot.callback_query_handler(func=lambda call: call.message.chat.id in admins)
def callback_query(call):
    global messages
    caption_photo_str = ''.join(caption_photo)
    caption_video_str = ''.join(caption_video)
    
    if call.data == '/usr_stats':
        bot.send_message(call.message.chat.id, 
                " <b>Текущий статус отчет:</b> \n \n" +
                "Всего в базе пользователей: " + str(total_users) + "\n"
                "Админов бота:" +str(len(admins_usersnames)) + "\n"  + get_adm_names()                                    
                )
                        
    elif call.data == '/send_msg':
        bot.send_message(call.message.chat.id, 'Отправьте сообщение, оно будет разослано всем активным пользователям:' , reply_markup=nav_markup())
        
    elif call.data == '/send':        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('SELECT id FROM users')
        users = cursor.fetchall()
        cursor.execute('SELECT * FROM messages ORDER BY id DESC LIMIT 1')
        
        messages = cursor.fetchall()
        msg_id = messages[0][0]
        
        active_users = 0
        block_users = 0               

        for user in users:
            for user_id in user:
                media = []
                if call.message.reply_to_message.content_type == 'poll':
                    try:
                        active_users += 1                        
                        
                        s = bot.forward_message(user_id, message_id=msg_id, from_chat_id=call.message.chat.id).message_id 
                    except:
                        block_users += 1
                    m = str(s)
                    db_functions.update_value(m, user_id)
                
                elif call.message.reply_to_message.content_type == 'photo':
                    for index, photo in enumerate(photos_id):
                        if index == 0:
                            media.append(types.InputMediaPhoto(media=photo, caption=caption_photo_str))
                        else:   
                            media.append(types.InputMediaPhoto(media=photo))                  
                    try:
                        s = bot.send_media_group(user_id, media)
                        active_users += 1
                        for i in s:
                            q = i.message_id
                            c = i.chat.id
                            photos_id_to_use.append((q, c))
                    
                    except:
                        block_users += 1
                    
                
                elif call.message.reply_to_message.content_type == 'video':
                    for index, video in enumerate(videos_id):
                        if index == 0:
                            media.append(types.InputMediaVideo(media=video, caption=caption_video_str))
                        else:   
                            media.append(types.InputMediaVideo(media=video))
                    
                    try:
                        s = bot.send_video(user_id, video=video, caption=caption_video_str)
                        active_users += 1
                    except:
                        block_users += 1
                    q = s.message_id
                    c = s.chat.id
                    video_id_to_use.append((q, c))
                elif call.message.reply_to_message.content_type == 'text':
                    try:
                        s = bot.copy_message(chat_id=user_id, from_chat_id=call.message.chat.id, message_id=msg_id).message_id  
                        active_users += 1
                        active_user_list += 1
                    except:
                        block_users += 1
                    m = str(s)     
                    db_functions.update_value(m, user_id)
            
                elif call.message.reply_to_message.content_type == 'document':
                    for doc_id in documents_id:
                        media.append(types.InputMediaDocument(media=doc_id))

                    try:
                        s = bot.send_document(user_id, document=doc_id)
                        active_users += 1
                    except:
                        block_users += 1
                
                    
                    q = s.message_id
                    c = s.chat.id
                    document_id_to_use.append((q, c))
                    
                

        loader =  bot.send_message(call.message.chat.id, 'Отправляется,ожидайте..')
        time.sleep(3)
        bot.delete_message(call.message.chat.id, loader.id)
        bot.send_message(call.message.chat.id, 
                     " <b>Краткий отчет:</b> \n \n" +
                     "Количество получивших пользователей: " + str(active_users) + "\n"
                     "Количество неактивных пользователей: " + str(block_users) + "\n \n"
                     "Всего в базе пользователей: " + str(total_users) + "\n"
                     "Из них админов:" +str(len(admins)) + "\n"
                     )
        bot.reply_to(call.message.reply_to_message, 
                         " <b>Что дальше?:</b> \n \n" 
                         , reply_markup=whats_next())
        
        time.sleep(3)


    elif call.data == '/cancel':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        handle_command(call.message)
    

    elif call.data == '/pinn_msg':
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()

        pin_count = 0
        unp_count = 0
        if call.message.reply_to_message.content_type == 'photo':
            for i in photos_id_to_use:
                bot.pin_chat_message(chat_id = i[1], message_id = i[0])
                
        elif call.message.reply_to_message.content_type == 'video':
            for i in video_id_to_use:
                bot.pin_chat_message(chat_id = i[1], message_id = i[0])

        elif call.message.reply_to_message.content_type == 'text':
            for user in users:
                user_id = user[0]
                user_msg_id = user[2]
                try:
                    bot.pin_chat_message(chat_id = user_id, message_id = user_msg_id)
                    pin_count += 1
                except:
                    unp_count += 1


        elif call.message.reply_to_message.content_type == 'document':
            for i in document_id_to_use:
                try:
                    bot.pin_chat_message(chat_id = i[1], message_id = i[0])
                    pin_count += 1
                except:
                    unp_count += 1
        elif call.message.reply_to_message.content_type == 'poll':
            for user in users:
                user_id = user[0]
                user_msg_id = user[2]
                try:
                    bot.pin_chat_message(chat_id = user_id, message_id = user_msg_id)
                    pin_count += 1
                except:
                    unp_count += 1

        bot.send_message(call.message.chat.id, 
                             " <b>Краткий отчет:</b> \n \n" +
                     "Закрепленно: " + str(pin_count) + "\n"
                     "Неудалось: " + str(unp_count) + "\n \n"
                     "Всего запросов: " + str(total_users) + "\n")
            
        time.sleep(3)
        handle_command(call.message)
        
        
    elif call.data == '/dell_msg':
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        del_count = 0
        fail_cout = 0
        # users_count = len(users)

        if call.message.reply_to_message.content_type == 'photo':
            for i in photos_id_to_use:
                try:
                    bot.delete_message(chat_id = i[1], message_id = i[0])
                    del_count += 1
            
                except:
                    fail_cout += 1

        elif call.message.reply_to_message.content_type == 'video':
            for i in video_id_to_use:
                try:
                    del_count += 1
                    bot.delete_message(chat_id = i[1], message_id = i[0])
            
                except:
                    fail_cout += 1
        
        elif call.message.reply_to_message.content_type == 'document':
            for i in document_id_to_use:
                try:
                    del_count += 1
                    bot.delete_message(chat_id = i[1], message_id = i[0])
            
                except:
                    fail_cout += 1
        
        elif call.message.reply_to_message.content_type == 'text':
            for user in users:
                user_id = user[0]
                user_msg_id = user[2]
                try:
                    del_count += 1
                    bot.delete_message(chat_id = user_id, message_id = user_msg_id)
                except:
                    fail_cout += 1

        elif call.message.reply_to_message.content_type == 'poll':
            for user in users:
                user_id = user[0]
                user_msg_id = user[2]
                try:
                    del_count += 1
                    bot.delete_message(chat_id = user_id, message_id = user_msg_id)
                except:
                    fail_cout += 1

        bot.send_message(call.message.chat.id, 
                             " <b>Краткий отчет:</b> \n \n" +
                     "Удалено: " + str(del_count) + "\n"
                     "Неудалось: " + str(fail_cout) + "\n \n"
                     "Всего пользователей: " + str(total_users) + "\n")
            
        time.sleep(3)
        handle_command(call.message)


@bot.callback_query_handler(func=lambda call: call.message.chat.id not in admins)
def usr_callback_query(call):
    if call.data == '/coworking':
        bot.send_message(call.message.chat.id, 
                         'Для того, чтобы посетить коворкинг, вам необходимо заранее забронировать конкретное время, когда вы хотите прийти. Коворкинг работает каждый день, без выходных, с 9:00 до 21:00. \n \n' +
                         'Для записи свяжитесь с администратором по телефону или в Telegram. \n \n' +
                         '<b>Контакты:</b> \n \n' +
                         '<b>ЧИЛАНЗАР</b> \n Telegram: t.me/proweb_coworking \n Тел: +998 99 531 66 32 \n \n' +
                         '<b>ОЙБЕК</b> \n Telegram: t.me/coworking_oybek \n Тел: +998 94 210 35 35 \n \n' +
                         '<b>ОЙБЕК 2</b> \n Telegram: t.me/proweb_oybek2 \n Тел: +998 94 210 34 34 \n \n' 
                         )
    if call.data == '/contests':
        bot.send_message(call.message.chat.id,
                         '‍ Ежемесячно для студентов центра <b>PROWEB</b> проводятся конкурсы с ценными призами! 🎉  \n \n' +
                         'Для участия в конкурсах важно оставаться подписанным на нашего бота. \n \n' +
                         'Подробные объявления с условиями конкурсов будут приходить личным сообщением всем подписчикам. Для того, чтобы оставаться подписанным, достаточно просто не удалять и не блокировать бота. \n \n'+ 
                         'Также мы проводим дополнительные конкурсы для наших подписчиков в <a href="https://www.instagram.com/proweb.uz/">Instagram</a> , <a href="https://www.youtube.com/channel/UCyxKtTHz9mN-ospm1vrkYPQ">Youtube</a>, <a href="http://t.me/proweb">Telegram</a>, <a href="https://facebook.com/proweb.uz">Facebook</a> - подписывайтесь и участвуйте сразу в нескольких конкурсах. \n \n' +
                         'Всем удачи, шанс выиграть есть у каждого студента! 🍀'
                         )
        
    if call.data == '/basic_course':
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            types.InlineKeyboardButton("Записаться на базовый курс (Чиланзар)", url="https://t.me/proweb_basic"),
            types.InlineKeyboardButton("Записаться на базовый курс (Айбек)", url="https://t.me/proweb_base_oybek")
                )
        bot.send_message(call.message.chat.id, 
                              'Вы совершенно не разбираетесь в комьютере, но при этом хотите обучаться в <b>PROWEB</b>? С нашим базовым курсом это возможно. Для этого вам просто необходимо нажать на кнопку <b>“Записаться на базовый курс”</b> и наш преподаватель вас подробно обо всём проконсультирует.' + '<a href="https://telegra.ph/file/f67524120efa0ff0e7436.jpg"></a>'
                              , reply_markup=markup)
        
    if call.data == '/reviews':
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(
            types.InlineKeyboardButton("Отзывы 😍", url="https://proweb.uz/reviews-page"),
            types.InlineKeyboardButton("Жалобы и пожелания 😔", callback_data = '/test')
                )
        
        bot.send_message(call.message.chat.id,
                         'Вам нравится обучение в центре <b>PROWEB</b> и вам не трудно поделиться об этом в наших социальных сетях? Тогда переходите по ссылке <b>“Отзывы”</b> и опишите свои впечатления, мы будем очень признательны. \n \n'

                         'У вас возникли трудности во время обучения или вам что-то не понравилось, а может есть предложения и пожелания? Тогда переходите по ссылке <b>“Жалобы и пожелания”</b>, распишите подробнее и мы сделаем все возможное, чтобы улучшить наш учебный центр.'
                         , reply_markup=markup)
        
        if call.data == '/learning_rules':
            bot.send_message(call.message.chat.id, 
                             '<b>Правила обучения в учебном центре PROWEB</b> \n \n'
                             '1. В одном учебном месяце - 8 занятий. Студентам, оплатившим месяц обучения гарантируется 8 проведенных уроков по утвержденному графику. \n \n' 

                             '2. Если урок отменяется в связи с праздником или по уважительной причине со стороны преподавателя, урок ни в коем случае не сгорает, а просто переносится. Пока все 8 официальных уроков не будут проведены, учебный месяц не закончится. \n \n'

                             '3. Если студент пропускает запланированный урок, данный урок засчитывается, так как студент состоит в Telegram группе, в которую скидывается каждый пройденный урок в видео формате. \n \n'

                             '4. Если студент не может посетить урок, он должен оповестить об этом преподавателя и <a href="http://t.me/proweb_admin">администрацию.</a>  \n \n'

                             '5. Если студент пропустил урок, то ему рекомендуется посетить <a href="http://t.me/proweb_coworking">коворкинг</a>, в котором находятся преподаватели всех направлений. <a href="http://t.me/proweb_coworking">Преподаватели коворкинга</a> могут помочь разобрать пропущенную тему и помочь в сложных учебных моментах. \n \n'

                             'В период обучения студент может посещать <a href="http://t.me/proweb_coworking">коворкинг</a> каждый день, заранее регистрируясь в доступное время. Для регистрации необходимо связаться с <a href="http://t.me/proweb_coworking">преподавателем коворкинга</a> и забронировать место. \n \n'

                             'Перед стартом курса, или уже во время обучения, студентам с плохими знаниями компьютера рекомендуется записаться на <a href="http://t.me/proweb_basic">бесплатный базовый курс</a>. За месяц студенты изучат основы компьютерной грамотности. Обучение проходит параллельно с основным курсом. Для записи нужно написать в <a href="http://t.me/proweb_basic">Telegram</a>. \n \n'

                             '8. Каждый студент учебного центра PROWEB должен вносить своевременную оплату за каждый месяц обучения в начале учебного месяца, во избежание исключения из группы. Если студент имеет финансовые трудности, то <a href="http://t.me/proweb_admin">администрация</a> может предоставить недельную отсрочку в выплате, либо студент может вносить частичную оплату в период текущего месяца обучения. \n \n'
                             
                             '9. Если студент не вносит своевременную оплату и не посещает более трех уроков без уважительной причины, то данный студент автоматически исключается из группы. Для восстановления в группу студент должен погасить задолженность, только после этого он будет восстановлен в свою группу, если та не ушла вперёд. Либо <a href="http://t.me/proweb_admin">администрация</a>  подберет группу, наиболее подходящую данному студенту. \n \n'
            
                            '10. Если студент хочет прекратить или приостановить обучение, нужно обязательно оповестить <a href="http://t.me/proweb_admin">администрацию</a> и объяснить причину, чтобы будущие уроки, которые студент не будет посещать, не засчитывались. <a href="http://t.me/proweb_admin">Администрация</a> своевременно приостановит обучение и удалит студента из Telegram группы. \n \n'

                           '11. Студент, приостановивший обучение, может восстановить своё обучение ровно с того месяца и урока, на котором приостановил. <a href="http://t.me/proweb_admin">Администрация</a> не гарантирует, что восстановиться получится именно к своему преподавателю. \n \n'
                             )
            
@bot.message_handler(func=lambda message: message.chat.id in admins, content_types=['text', 'document', 'audio', 'poll', 'photo', 'video'])
def on_adm_message(message):   
    if message.content_type == 'text':
        if message.text == 'На главную':
            handle_command(message)
        elif message.text == 'Help ❓':
            help_command(message)
        else:
            try:
                db_functions.add_sms(message.id, message.text)
                s = bot.reply_to(message, text='Что делаем?', reply_markup=send_markup())
            except:
                pass
    
    elif message.content_type == 'poll':
        text = ''
        db_functions.add_sms(message.id, text)
        bot.reply_to(message, text='Что делаем?', reply_markup=send_markup())       
        
    elif message.content_type == 'photo':
        if message.caption:            
            caption_photo.append(message.caption) 
        m_p = message.photo[2].file_id

        photos_id.append(m_p)
        # media_id = message.media_group_id
        
        s = bot.reply_to(message, text='Что делаем?', reply_markup=send_markup())

    elif message.content_type == 'video':
        if message.caption:            
            caption_video.append(message.caption) 
        m_p = message.video.file_id
        
        videos_id.append(m_p)
        # media_id = message.media_group_id
        
        s = bot.reply_to(message, text='Что делаем?', reply_markup=send_markup())

        # print(message)


    elif message.content_type == 'document':
        d_i = message.document.file_id
        documents_id.append(d_i)
        s = bot.reply_to(message, text='Что делаем?', reply_markup=send_markup())


@bot.message_handler(func=lambda message: message.chat.id not in admins, content_types=['text'])
def on_adm_message(message):
    if message.text == 'На главную':
            handle_command(message)
    elif message.text == 'Help ❓':
            help_command(message)


            
print('Started succesful..')
create_db()
bot.infinity_polling(interval=0, timeout=20)

