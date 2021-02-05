import telebot
import pandas as pd
import numpy as np
from random import choice

token = '<your token>'
file_name = 'statistics.xlsx'
stickers = ['CAACAgIAAxkBAALIxWAcTDlidYv-Bl2EtqFql7e96c5hAAJlAwACnNbnCpyHNttA8zmLHgQ',
            'CAACAgIAAxkBAALIzmAcTIMAAa3Rmsd3uVsjJrFf1x390AACZgMAApzW5wraeV_skp5vPB4E',
            'CAACAgIAAxkBAALI1GAcTLKL0Bwr0ZyxNFFAD1YI7jbeAAJpAwACnNbnCj4PrxP1TMazHgQ',
            'CAACAgIAAxkBAALI12AcTNddAvmgSDKzL7rM-cNSX9fbAAJ8AwACnNbnCg1D4wMvwXC_HgQ',
            'CAACAgIAAxkBAALI2mAcTP1WewtpIZL1DnlxZrmNYu86AAKBAwACnNbnCkaU6A-vIFCvHgQ']

bot = telebot.TeleBot(token)

#schedule
schedule = pd.read_excel(file_name, sheet_name='Timetable')
schedule_array_days = list(schedule['Day'])
schedule_array_events = list(schedule['Event'])
schedule_cat = np.column_stack((schedule_array_days, schedule_array_events))
schedule_message = '📒Schedule for the current month: '
for event in schedule_cat:
    schedule_message += '\n  • {}   -   {}'.format(event[0], event[1])

#statistics
df = pd.read_excel(file_name)

def footballerstatistics(name):
    visits = df.loc[df['Name'] == name].iloc[0]['Gms']
    goals = df.loc[df['Name'] == name].iloc[0]['Gls']
    passes = df.loc[df['Name'] == name].iloc[0]['Ps']
    saves = df.loc[df['Name'] == name].iloc[0]['Sv']
    total = int(df.loc[df['Name'] == name].iloc[0]['T'])
    answer = ' {}: \n • Visits:                  {}\n • Goals:                  {}\n • Passes:                {}\n • Saves:                  {}\n • Total:                    {}\n '.format(name, visits, goals, passes, saves, total)
    return answer

startmessage = """
⚽️ Hey!

 I'm a soccer club helper bot!

1. To find out the schedule for the current month, write me the word Schedule!

2. To find out your statistics, write me your name (for example Ivan Petrov),
 I think I can tell you something!

3. To see the club memo, write me the word Memo! ⚽️
"""

rulesmessage = """🤪 A match consists of two 45 minutes halves with a 15 minute rest period in between.
Each team can have a minimum off 11 players (including 1 goalkeeper who is the only player allowed to handle the ball within the 18 yard box) and a minimum of 7 players are needed to constitute a match.
The field must be made of either artificial or natural grass. The size of pitches is allowed to vary but must be within 100-130 yards long and 50-100 yards wide. The pitch must also be marked with a rectangular shape around the outside showing out of bounds, two six yard boxes, two 18 yard boxes and a centre circle. A spot for a penalty placed 12 yards out of both goals and centre circle must also be visible.
The ball must have a circumference of 58-61cm and be of a circular shape.
Each team can name up to 7 substitute players. Substitutions can be made at any time of the match with each team being able to make a maximum of 3 substitutions per side. In the event of all three substitutes being made and a player having to leave the field for injury the team will be forced to play without a replacement for that player.
Each game must include one referee and two assistant referee’s (linesmen). It’s the job of the referee to act as time keeper and make any decisions which may need to be made such as fouls, free kicks, throw ins, penalties and added on time at the end of each half. The referee may consult the assistant referees at any time in the match regarding a decision. It’s the assistant referee’s job to spot offside’s in the match (see below), throw ins for either team and also assist the referee in all decision making processes where appropriate.
If the game needs to head to extra time as a result of both teams being level in a match then 30 minutes will be added in the form of two 15 minute halves after the allotted 90 minutes.
If teams are still level after extra time then a penalty shootout must take place.
The whole ball must cross the goal line for it to constitute as a goal.
For fouls committed a player could receive either a yellow or red card depending on the severity of the foul; this comes down to the referee’s discretion. The yellow is a warning and a red card is a dismissal of that player. Two yellow cards will equal one red. Once a player is sent off then they cannot be replaced.
If a ball goes out of play off an opponent in either of the side lines then it is given as a throw in. If it goes out of play off an attacking player on the base line then it is a goal kick. If it comes off a defending player it is a corner kick.
 🤪"""



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, startmessage)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'memo':
        bot.send_message(message.chat.id, rulesmessage)
    elif message.text.lower() == 'schedule':
        bot.send_message(message.chat.id, schedule_message)
    else:
        try:
            bot.send_message(message.chat.id, footballerstatistics(message.text))
        except:
            bot.send_message(message.chat.id, "I don't know such a command! Sorry 🧐")
            bot.send_sticker(message.chat.id, choice(stickers))

bot.polling()