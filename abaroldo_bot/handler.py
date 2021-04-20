
import json
import chatbot as c
import markup as m
import dynamo as d
import os

abaroldo = c.get_bot_client()

def lambda_handler(event, context):
    
    print(json.loads(event['body']))
    chat_id, text, file_id, sender = c.message_check(event)
    
    if sender != 'Dutcosky':
        abaroldo.send_message(1192910552, '{} | {}'.format(sender,text))
        
    # Image Handler
    if text == "#":
        image_key = c.put_image_on_bucket(file_id)
        d.register_image_key(image_key)
        abaroldo.send_message(chat_id, "Otima foto, guardei ela pra colocar no relatorio depois")

    elif text == '/menu':
        abaroldo.send_message(chat_id, "Como posso ajudar?", reply_markup = m.get_menu_markup())
        
    elif text == '/start':
        abaroldo.send_message(chat_id, "Muito prazer! Eu sou o Abaroldo e meu proposito é gerar relatorios da Abare")
        abaroldo.send_message(chat_id, "Se quiser qualquer ajuda, me envie o comando /menu")
        
    elif text[:4].upper() == "/OBS":
        d.register_obs(text)
        abaroldo.send_message(
            chat_id, 
            "Muito bem observado! Vou anotar aqui pra incluir no relatorio depois", 
            reply_markup = m.get_menu_markup()
        )
        
    elif text == "Retornar pro Menu":
        abaroldo.send_message(chat_id, "Back to menu!..", reply_markup = m.get_menu_markup())
        
    elif text == 'Fechar Menu':
        abaroldo.send_message(chat_id, "Qualquer coisa to por ai", reply_markup = m.get_closed_markup())
        
    elif text == "Ver Minha Lista":
        if d.check_in_exists():
            abaroldo.send_message(chat_id, "Deixa eu ver aqui, só um segundo")
            for item in d.list_items_checked():
                abaroldo.send_message(chat_id, item, reply_markup = m.get_menu_markup())
        else:
            abaroldo.send_message(chat_id, "Itens? Voce nem fez Check-In ainda. Eu heim..")
        
    elif text == 'Check-In':
        d.ensure_unique_check_in()
        abaroldo.send_message(chat_id, "Em qual sede?", reply_markup = m.get_place_markup())
        
    elif text in c.PLACE:
        d.new_visit_check_int(text)
        abaroldo.send_message(
            chat_id, 
            "Ahh {}?! Adoro essa sede! Bom.. Check-In feito. Nao esqueca de fazer o Check-Out depois de terminar ok? Tenha um otimo trabalho!!".format(text),
            reply_markup = m.get_menu_markup())

    elif text == 'Check-Out':
        response = d.check_out_visit()
        abaroldo.send_message(chat_id, response, reply_markup = m.get_menu_markup())
        
    elif text == 'Observacoes':
        abaroldo.send_message(chat_id, 
            "Quando quiser registrar novas observacoes é só me enviar uma mensagem inciada pelo comando /obs")
        abaroldo.send_message(chat_id, "Observacoes que voce tem registradas ate o momento:")
        for item in d.list_obs_checked():
            abaroldo.send_message(chat_id, item, reply_markup = m.get_menu_markup())
            
            
    elif text == 'Gerar Relatorio':  
        abaroldo.send_message(chat_id, 
            "Com prazer. Qual relatorio voce quer que eu te envie? Caso ele nao seja um desses, talvez voce tenha esquecido de fazer Check-Out", 
            reply_markup = m.get_visit_id_markup())
        
    elif text[0:4].upper() == 'SEDE':
        c.send_visit_report(text, chat_id)
            
    
    elif text == 'Marcar Item Irregular':
        if d.check_in_exists():
            abaroldo.send_message(chat_id, "Selecione uma sessao", reply_markup = m.get_session_markup())
        else:
            abaroldo.send_message(
                chat_id, 
                "Voce precisa fazer Check-In em uma sede primeiro!", 
                reply_markup = m.get_place_markup()
            )

    elif text == "Retornar para sessoes":
        abaroldo.send_message(chat_id, "Back to sessions!..", reply_markup = m.get_session_markup())
        
    elif text == 'Remover Item Marcado':
        if d.check_in_exists():
            remove_item = d.list_items_to_remove()
            markup = m.get_remove_list_markup(remove_item)
            abaroldo.send_message(
                chat_id, 
                "Qual desses itens voce quer remover?", 
                reply_markup = markup
            )
        else:
            abaroldo.send_message(
                chat_id, 
                "Itens? Voce nem fez Check-In ainda. Eu heim..", 
                reply_markup = m.get_menu_markup()
            )
            
    elif text.find("[R]") != -1:
        d.remove_item_from_checklist(text)
        abaroldo.send_message(
            chat_id, 
            "Ok! Removi este item da sua lista de irregularidades", 
            reply_markup = m.get_menu_markup()
        )

    elif text in c.SESSION:
        markup = m.get_item_markup(text)
        abaroldo.send_message(
            chat_id, 
            "Selecione as irregularidades da sessao {}".format(text[text.find(' '):].strip().upper()), 
            reply_markup = markup
        )
        
    elif text not in c.SESSION and text[:3].find('.') != -1:
        if d.put_item_on_checklist(text):
            abaroldo.send_message(
                chat_id, 
                "Ok! Anotei aqui", 
                reply_markup = m.remain_item_markup(text)
            )
        else:
            abaroldo.send_message(
                chat_id, 
                "Ei, esquecidinha! Eu ja anotei esse item agora pouco", 
                reply_markup = m.remain_item_markup(text)
            )
            

    elif text == "Abaroldo esta tirando uma soneca":
        abaroldo.send_message(chat_id, "Ei! To descansando aqui, mas se quiser minha ajuda é só me enviar o comando /menu")
        
    else:
        abaroldo.send_message(chat_id, "Nao entendi essa mensagem..")
        
        
        