import requests
import vk_api
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os
from io import BytesIO
from vk_api.utils import get_random_id

while True:
    try:
        session = requests.Session()
        token_vk = os.environ.get('BOT_TOKEN')
        vk_session = vk_api.VkApi(token=str(token_vk), scope="message")

        from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

        longpoll = VkBotLongPoll(vk_session, "194404834")
        vk = vk_session.get_api()


        def key_b(peer_id):
            try:
                keyboard = VkKeyboard(one_time=True, inline=False)
                keyboard.add_button("/info", color=VkKeyboardColor.POSITIVE, payload=None)
                keyboard.add_button("/game", color=VkKeyboardColor.PRIMARY, payload=None)
                vk.messages.send(  # Отправляем собщение
                    peer_id=peer_id,
                    keyboard=keyboard.get_keyboard(), message='⌨', random_id=get_random_id())

            except Exception as ecc:
                vk.messages.send(  # Отправляем собщение
                    peer_id=peer_id,
                    message=str(ecc), random_id=get_random_id())


        def send(massage, peer_id):
            vk.messages.send(  # Отправляем собщение
                peer_id=peer_id,
                message=massage, random_id=get_random_id())

        def rasp():
            url = 'http://rasp.kolledgsvyazi.ru/spo.pdf'
            f = open(r'rasp.pdf', "wb")  # открываем файл для записи, в режиме wb
            ufr = requests.get(url)  # делаем запрос
            f.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
            f.close()
            from pdf2jpg import pdf2jpg
            inputpath = r"rasp.pdf"
            outputpath = r""
            # to convert all pages
            result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, pages="ALL")
            print(result)
            
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.object['text']:

                s = event.object['text']
                # Слушаем longpoll, если пришло сообщение то:
                peer_id = event.obj['peer_id']
                if peer_id < 2000000000:
                    key_b(peer_id)
                else:
                    if s[0] == '/':
                        key_b(peer_id)

                if s == '/info':
                    send('бота написал\n'
                         'https://vk.com/fantasticfeed\n'
                         '____________________________\n'
                         '/game(в разработке)\n/report\n'
                         'разрабатываются новые возможности.', peer_id)
                elif s == '/rasp':
                    try:
                        a = vk_session.method("photos.getMessagesUploadServer")
                        b = requests.post(a['upload_url'],
                                              files={'photo': BytesIO(open('rasp.pdf_dir\0_rasp.pdf.jpg'), 'rb')}).json()
                        c = vk_session.method('photos.saveMessagesPhoto',
                                                  {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
                        d = "photo{}_{}".format(c["owner_id"], c["id"])
                        vk.messages.send(  # Отправляем собщение
                                peer_id=peer_id,
                                attachment=d, random_id=get_random_id()
                            )
                    except Exception as E:
                        send("error\n " + str(E), peer_id)
                        
                elif s == '/game':
                    try:
                        attachments = []
                        upload = VkUpload(vk_session)
                        image_url = 'https://prolab-beauty.ru/images/blog/4/techrab-800x600.jpg'
                        image = session.get(image_url, stream=True)
                        photo = upload.photo_messages(photos=image.raw)[0]
                        attachments.append(
                            'photo{}_{}'.format(photo['owner_id'], photo['id'])
                        )
                        vk.messages.send(
                            peer_id=peer_id,message='разработка...',
                            attachment=','.join(attachments),
                            random_id=get_random_id()
                        )

                    except Exception as E:
                        send("error\n " + str(E), peer_id)
                        
                elif s == '/report':
                    if peer_id < 2000000000:
                        send('опишите вашу проблему',peer_id)
                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW and event.object['text']:
                                 vk.messages.send(  # Отправляем собщение
                                                    peer_id=165974848,message='сообщение об ошибке \nот https://vk.com/id'
                                     +str(event.object['peer_id'])+'\n"'+str(event.object['text'])+'"',
                                                     random_id=get_random_id())
                                 vk.messages.send(  # Отправляем собщение
                                                    peer_id=event.object['peer_id'],message=
                                     'спасибо за обращение, скоро с вами может связаться наш администратор⚙',
                                                     random_id=get_random_id())
                    else:
                        send('напишите в лс бота',peer_id)
                
                elif s == '/test':
                    for i in range(0,30):
                        send(str(i)+'spam)))',peer_id)
                elif s[0] == '/':
                    send('нет такой команды\n'
                         'попробуйте написать "/info"', peer_id)
                    
                
    except Exception as ec:
        print(ec)
