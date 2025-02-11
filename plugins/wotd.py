from datetime import datetime
import json
import random
import re

import pinhook.plugin as p

def write_wotd(word_info):
    with open('wotd.json', 'w') as wj:
        json.dump(word_info, wj, sort_keys=True, indent=2)

def get_wotd():
    today = datetime.now().strftime('%Y%m%d')
    with open('wotd.json') as wj:
        word_info = json.load(wj)
    if not word_info:
        word_info = {
                'day': today,
                'word': pick_wotd(),
                'said': 0,
                'said_by': [],
                }
        write_wotd(word_info)
    if word_info['day'] != today:
        word_info = {
                'day': today,
                'word': pick_wotd(),
                'said': 0,
                'said_by': []
                }
        write_wotd(word_info)
    return word_info

def pick_wotd():
    with open('words.txt') as w:
        words = [word.strip() for word in w.readlines()]
    return random.choice(words)

@p.listener('Secret Word of the Day')
def wotd_listener(msg):
    wotd_info = get_wotd()
    word = wotd_info['word']
    if msg.text:
        user_said = re.search(r'\b'+word+r'\b', msg.text, re.IGNORECASE)
    if msg.msg_type == 'message' and user_said and msg.channel == '#tildetown':
        if not wotd_info['said']:
            msg.privmsg(msg.channel, f'{msg.nick}: Congrats! You have said "{word}" which is today\'s Secret Word of the Day!')
        wotd_info['said'] += 1
        if msg.nick not in wotd_info['said_by']:
            wotd_info['said_by'].append(msg.nick)
        write_wotd(wotd_info)

@p.command('!wotd')
def wotd_command(msg):
    wotd_info = get_wotd()
    if wotd_info['said']:
        m = f"Today's (no longer) Secret Word of the Day is \"{wotd_info['word']}\"! It has been said {wotd_info['said']} time(s) by {', '.join(wotd_info['said_by'])}!"
    else:
        m = 'The Secret Word of the Day has yet to be revealed!'
    return p.message(m)
