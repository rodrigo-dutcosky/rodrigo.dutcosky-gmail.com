
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton
from config import *
import dynamo as d

def get_closed_markup():
    
    markup = ReplyKeyboardMarkup(one_time_keyboard = False)
    markup.row(InlineKeyboardButton(text = "Abaroldo esta tirando uma soneca"))
    
    return markup

def get_menu_markup():
    
    markup = ReplyKeyboardMarkup(one_time_keyboard = False)
    for i in MENU:
        markup.row(InlineKeyboardButton(text = i))
        
    return markup

def get_place_markup():
    
    markup = ReplyKeyboardMarkup(row_width = 4, one_time_keyboard = False)
    
    for i in PLACE:
        markup.row(InlineKeyboardButton(text = i))
        
    return markup

def get_session_markup():
    
    markup = ReplyKeyboardMarkup(row_width = 4, one_time_keyboard = False)
    markup.row(InlineKeyboardButton(text = "Retornar pro Menu"))
    
    for i in SESSION:
        markup.row(InlineKeyboardButton(text = i))
        
    return markup

def get_item_markup(text):
    
    session_numb = int(text[ : text.find('.')].strip())
    
    markup = ReplyKeyboardMarkup(row_width = 3, one_time_keyboard = False)
    markup.row(InlineKeyboardButton(text = "Retornar para sessoes"))
    
    for i in ITEM[session_numb]:
        markup.row(InlineKeyboardButton(text = ITEM[session_numb][i]['item']))
        
    return markup

def remain_item_markup(text):
    
    session_numb = int(text[ : text.find('.')].strip())
    
    markup = ReplyKeyboardMarkup(row_width = 3, one_time_keyboard = False)
    markup.row(InlineKeyboardButton(text = "Retornar para sessoes"))
    
    for i in ITEM[session_numb]:
        markup.row(InlineKeyboardButton(text = ITEM[session_numb][i]['item']))
        
    return markup

def get_remove_list_markup(checked_item):
    
    retornar = ["Retornar pro Menu"]
    if len(checked_item) > 0:
        checked_item = list(map(lambda x: "[R] {}".format(x), checked_item))
        retornar += checked_item
    
    markup = ReplyKeyboardMarkup(row_width = 3, one_time_keyboard = False)
    for i in retornar:
        markup.row(InlineKeyboardButton(text = i))
        
    return markup


def get_remove_list_markup(checked_item):
    
    retornar = ["Retornar pro Menu"]
    if len(checked_item) > 0:
        checked_item = list(map(lambda x: "[R] {}".format(x), checked_item))
        retornar += checked_item
    
    markup = ReplyKeyboardMarkup(row_width = 3, one_time_keyboard = False)
    for i in retornar:
        markup.row(InlineKeyboardButton(text = i))
        
    return markup

def get_visit_id_markup():
    
    checked_out_visits = ["Retornar pro Menu"]
    checked_out_visits += d.list_checked_out_visits()
    
    markup = ReplyKeyboardMarkup(row_width = 4, one_time_keyboard = False)
    for i in checked_out_visits:
        markup.row(InlineKeyboardButton(text = i))
        
    return markup
    
    
    
    
    
    
    
    
    

