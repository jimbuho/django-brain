# -*- coding: utf-8 -*-
"""
.. module:: dbu-telegrambot
   :platform: Unix, Windows
   :synopsis: Clase Base para enviar mensajes a un bot de telegram

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from . import configuration, vmixins, messages

import requests
import traceback


class TelegramBot:
    """

    Bot de Telegram para Liberi

    """
    def get_telegram_token(self):
        """

        Token Telegram

        :return:
        """
        return configuration.get_value('telegram.token', 'MY-TOKEN')

    def get_telegram_url(self):
        """

        URL Telegram

        :return:
        """
        return configuration.get_value('telegram.url', 'https://api.telegram.org')

    def send_message(self, message, chat_id):
        """

        Envia un msg

        :param message:
        :param chat_id:
        :return:
        """
        try:
            data = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }
            response = requests.post("%s/bot%s/sendMessage" % (self.get_telegram_url(), self.get_telegram_token()), data=data)
            return response is not None, 'BOT'
        except Exception as e:
            error = str(e)
            traceback.print_exc()

        return False, error