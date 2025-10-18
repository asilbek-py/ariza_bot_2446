from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# tashqi knopka  -> Default Keyboard
telefon_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📞 Telefon raqam jo'natish", request_contact=True)]
], resize_keyboard=True)

# ichki knopka -> Inline Keyboard
tasdiqlash_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅  HA", callback_data='yes'),
        InlineKeyboardButton(text="❌ YO'Q", callback_data='no'),
    ]
])
