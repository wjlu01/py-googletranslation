"""A conversion module for googletrans"""
import json
import nltk
import unidecode

def format_querystringlang():
    querystring = {
        "client":"te",
    }
    return querystring

def format_querystring(token, text, src='auto', dest='en'):
    querystring = {
        "anno":"3",
        "format":"html",
        "key":"",
        "logld":"vTE_20201130_00",
        "client":"te",
        "v":"1.0",
        "sl": src,
        "tl": dest,
        "tk": token,
        "q": text.encode('utf-8'),
        "tc":"1",
        "sr":"1",
        "mode":"1"
    }
    return querystring


def format_param(rpcids):
    params = {
        'rpcids': rpcids,
        'bl': 'boq_translate-webserver_20201207.13_p0', 
        'soc-app': 1, 
        'soc-platform': 1, 
        'soc-device': 1, 
        'rt': 'c'
    }
    return params

def format_data(rpcids, text, src, dest):
        return {'f.req': json.dumps([[
            [
                rpcids,
                json.dumps([[text, src, dest, True],[None]], separators=(',', ':')),
                None,
                'generic',
            ],
        ]], separators=(',', ':'))}

def format_response(a):
    result = {}
    b = a.split('\n')
    li_filter = []
    flag = False
    for _b in b:
        if _b.isnumeric():
            flag = not flag
            _b = 'pygoogletranslation'
        if flag:
            li_filter.append(_b)
    fi_data = str(''.join(li_filter)).replace('"[', '[').replace(']"', ']').replace('\\n', '').replace('\\','')    
    li_data = json.loads(fi_data.split('pygoogletranslation')[1].replace('"[', '[').replace(']"', ']'),strict=False)
    return li_data
    
def tokenize_sentence(text):
    text_len = 0
    token_text = ''
    text_list = []
    if len(text) <= 5000:
        text_list.append(text)
        return text_list
    tokens = nltk.sent_tokenize(text)
    for t in tokens:
        text_len += len(t)
        if text_len < 5000:
            token_text += t
        else:
            text_list.append(token_text)
            text_len = 0
            token_text = t
    if text_len < 5000:
        text_list.append(token_text)
    return text_list


def format_translation(translated,dest):
    text = ''
    pron = ''
    for _translated in translated:
        try:
            try:
                if dest=="fr":
                    tran_list = _translated[0][2][1][0][0][0] if _translated[0][2][1][0][0][2]=='(masculine)' else _translated[0][2][1][0][1][0]
                else:
                    tran_list = _translated[0][2][1][0][0][5]
                for tmp_tran in tran_list:
                    text += tmp_tran[0]
            except:
                tran_list = _translated[0][2][1][0]
                for tmp_tran in tran_list:
                    text += tmp_tran[0]
        except:
            text += fix_trans_error(_translated)
        try:
            pron += unidecode.unidecode(_translated[0][2][1][0][0][1])
        except:
            pron += ''

    for _translated in translated:
        try:
            _translated[0][2][1][0][0][5][0][0] = text
            break
        except:
            _translated[0][2][1][0][0][0]=text
    try:
        _translated[0][2][1][0][0][1] = pron
    except:
        pass
    return _translated


def fix_trans_error(translated):
    if len(translated) > 0:
        if len(translated[0]) > 2:
            if len(translated[0][2]) > 1:
                if len(translated[0][2][1]) > 0:
                    if len(translated[0][2][1][0]) > 0:
                        if len(translated[0][2][1][0][0]) > 5:
                            if len(translated[0][2][1][0][0][5]) > 0:
                                if len(translated[0][2][1][0][0][5][0]) > 0:
                                    text = translated[0][2][1][0][0][5][0][0]
                                else:
                                    text = translated[0][2][1][0][0][5][0]
                            else:
                                text = translated[0][2][1][0][0][5]
                        else:
                            text = translated[0][2][1][0][0]
                    else:
                        text = translated[0][2][1][0]
                else:
                    text = translated[0][2][1]
            else:
                text = translated[0][2]
        else:
            text = translated[0]
    else:
        text = translated
    return str(text)

