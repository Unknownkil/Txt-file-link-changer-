from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

# Replace 'YOUR_API_KEY' with your Telegram Bot API key
API_KEY = '6748460867:AAFzQkFcCfg1kqISiV4499pGxIcPtu4qe1w'

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a file containing master.mpd URLs.")

def process_file(update: Update, context: CallbackContext):
    file = context.bot.get_file(update.message.document.file_id)
    file.download('input_file.txt')
    
    with open('input_file.txt', 'r') as infile, open('output_file.txt', 'w') as outfile:
        content = infile.read()
        # Regular expression to find all master.mpd URLs
        urls = re.findall(r'https://[^\s]+/master\.mpd', content)
        
        for url in urls:
            ffmpeg_command = f'ffmpeg -i "https://kashurtek.site?url={url}&quality=480" -c copy output.mp4'
            content = content.replace(url, ffmpeg_command)
        
        outfile.write(content)
    
    update.message.reply_document(document=open('output_file.txt', 'rb'))

def main():
    updater = Updater(API_KEY, use_context=True)
    
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.document.mime_type("text/plain"), process_file))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()