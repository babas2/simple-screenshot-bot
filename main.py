import os
import time
from telethon import TelegramClient, events
from pyppeteer import launch
from settings import API_ID, API_HASH, BOT_TOKEN,WIDTH,HEIGHT
from utils import fetch_urls
import logging


logging.basicConfig(level=logging.INFO)

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

browser, page = None, None


async def start_browser():
    global browser, page
    browser = await launch(headless=True,args=['--no-sandbox'])
    page = await browser.newPage()
    await page.setViewport({'width':WIDTH,'height':HEIGHT})

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Salam! Mən bir səhifəni ss etmək üçün bir botam 🥳 Mənə link göndər və mən o səhifəni ss(ekran görüntüsü) alıb sizə atım📌\n\n❗DİQQƏT\nNümunə: google.com yerinə https://google.com yazın!')
    raise events.StopPropagation


@bot.on(events.NewMessage(outgoing=False))
async def echo(event):
    try:
        urls = fetch_urls(event.text)
        for url in urls:
            logging.info(url)
            await page.goto(url)


            file_name = f'{time.time()}.png'
            await page.screenshot(path=file_name, fullPage=False)
            await event.reply(event.text, file=file_name)
            os.remove(file_name)

    except Exception as err:
        await event.reply(event.text)
        await event.respond(str(err)[:2000])
        logging.exception(err)
        return


if __name__ == '__main__':

    with bot:
        bot.loop.run_until_complete(start_browser())
        bot.run_until_disconnected()
