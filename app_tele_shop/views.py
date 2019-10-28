from django.http import JsonResponse
from django.conf import settings
import telebot
from django.views.decorators.csrf import csrf_exempt
import json

from app_tele_shop import models

def get_keyboard(callback_name, queryset):
    bot_keyboard = telebot.types.InlineKeyboardMarkup()

    for item in queryset:
        bot_keyboard.add(telebot.types.InlineKeyboardButton(text=item.title,
                                                        callback_data='{}:{}'.format(callback_name, item.id)))

    return bot_keyboard

def start(chat_id, select_item_id=None, message=None):
    bot_keyboard = get_keyboard('select_category', models.Category.objects.all())
    settings.BOT.send_message(chat_id,
                              "Выберите категорию",
                              reply_markup=bot_keyboard)


def get_product_list(chat_id, select_item_id=None, message=None):
    for product in models.Product.objects.filter(category_id=select_item_id):
        bot_keyboard = telebot.types.InlineKeyboardMarkup()
        bot_keyboard.add(telebot.types.InlineKeyboardButton(text='Заказать',
                                                            callback_data='{}:{}'.format('order', product.id)))
        file = open(product.img.path, 'rb')
        settings.BOT.send_photo(chat_id, file,
                                caption='{}\n{}\n{}\n{}'.format(product.title, product.description, product.price,
                                                                product.currency.show_title),
                                reply_markup=bot_keyboard)


def create_order(chat_id, select_item_id=None, message=None):
    models.Order.objects.create(telegram_id=chat_id, product_id=select_item_id)


action_dict = {
    'start': start,
    'select_category': get_product_list,
    'order': create_order
}

# Вид для обработки запросов от телеграм
@csrf_exempt
def action(request):
    # Обрабатываем тело запроса от телеграм
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    update = telebot.types.Update.de_json(body)
    settings.BOT.process_new_updates([update])

    # Создаем функцию которая обрабатывает ввод команд пользователем.
    # Принимает список команд для обработки ['start', ]
    @settings.BOT.message_handler(commands=['start', ])
    def send_welcome(message):
        chat_id = message.chat.id
        start(chat_id)

    # Функция обрабатывает клики пользователей по кнопкам в клавиатуре
    @settings.BOT.callback_query_handler(func=lambda message: True)
    def process_step(message):
        action, return_value = message.data.split(':')
        action_dict.get(action)(message.from_user.id, return_value, message)

    # Функция обрабатывает данные вводимые пользователем, принимает список данных которые необходимо обработать ['text']
    @settings.BOT.message_handler(func=lambda message: True, content_types=['text'])
    def add_answer(message):
        print(message)

    return JsonResponse({})
