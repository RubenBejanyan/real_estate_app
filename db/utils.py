from googletrans import Translator


def create_city_dict(city):
    if city == 'Երևան':
        city = 'Երեւան'
    elif city == 'Jermuk' or city == 'Джермук':
        city = 'Ջերմուկ'
    translator = Translator()
    detected = translator.detect(city).lang
    if detected == 'hy':
        return {'name': city}
    if detected not in {'en', 'ru'}:
        detected = 'en'
    return {'name': translator.translate(city, dest='hy', src=detected).text}
