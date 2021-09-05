from django.conf import settings
from random import choice, random
from string import ascii_letters, digits

SIZE = getattr(settings, "MAXIMUM_URL_CHARS", 7)
AVAILABLE_CHARS = ascii_letters + digits

def CreateRandomCode(chars = AVAILABLE_CHARS):

    return "".join([choice(chars) for _ in range(SIZE)])

def CreateShortenedURL(model_instance):

    randomCode = CreateRandomCode()

    modelClass = model_instance.__class__

    if modelClass.objects.filter(shortURL = randomCode).exists() or randomCode == "api":
        return CreateShortenedURL(model_instance)

    return randomCode