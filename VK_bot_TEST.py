import requests
import vk_api
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os
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
                         '/game(в разработке)\n'
                         'разрабатываются новые возможности.', peer_id)

                elif s == '/game':
                    send('разработка...', peer_id)
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
                            peer_id=peer_id,
                            attachment=','.join(attachments),
                            random_id=get_random_id()
                        )

                    except Exception as E:
                        send("error\n " + str(E), peer_id)

                elif s[0] == '/':
                    send('нет такой команды\n'
                         'попробуйте написать "/info"', peer_id)
    except Exception as ec:
        print(ec)
