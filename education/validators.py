from rest_framework import serializers


class LinkValidator:
    def __init__(self, link):
        self.link = link

    def __call__(self, value):
        """ Проверка вхождения youtube.com в ссылке"""
        if (dict(value).get(self.link) and 'youtube.com' not in dict(value).get(self.link).split(
                '/')) and 'www.youtube.com' not in dict(value).get(self.link).split('/'):
            raise serializers.ValidationError('Ссылка на видео должна быть на youtube.com')
