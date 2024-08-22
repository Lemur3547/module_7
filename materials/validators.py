from rest_framework.exceptions import ValidationError


class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value, *args, **kwargs):
        if 'https://www.youtube.com/' not in value['video_link']:
            raise ValidationError('Ссылка на видео должна быть на сервис youtube.com')
