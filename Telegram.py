import telebot
import openai

bot = telebot.TeleBot('token')

openai.api_key = "api_key"

print("Bot successfully launched.")

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Good afternoon, I am Bot, ready to listen to your questions.')

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    question = message.text
    try:
        bot.send_message(message.chat.id, 'Wait, I am forming an answer...')
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Question: {question}\nAnswer:",
            max_tokens=2024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        answer = response['choices'][0]['text'].strip()
        if len(answer) <= 4096:
            bot.send_message(message.chat.id, answer)
        else:
            chunks = [answer[i:i+4096] for i in range(0, len(answer), 4096)]
            for chunk in chunks:
                bot.send_message(message.chat.id, chunk)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")

bot.polling(none_stop=True)
