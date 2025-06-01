from pyrogram import Client, filters
from pyrogram.types import Message
from src import const
import re
import asyncio


# base_chat = -1002126520443
main_chat = -1001133580711
base_chat = -1002552659808 # dev
# main_chat = -1001667858531 #dev


TypeHito = 5754619101
main_admin = 452377448


admins = [TypeHito, main_admin]


fiter = ["bormi", "борми", "kerak", "керак", "bomi", "боми"]


app = Client(
    const.SESSION_NAME,
    api_id=const.API_ID,
    api_hash=const.API_HASH
)


def clean_text(text):
    new_text = text
    for rgx_match in fiter:
        new_text = re.sub(rgx_match, '', new_text)
    return new_text


def match_text(text):
    for rgx_match in fiter:
        match = re.search(rgx_match, text)
        if match:
            return True
    return False


def get_price(text):
    price = str(text).split("@")[1]
    if price:
        return price


async def match_get_products(client, message):
    text = str(message.text).lower()
    if match_text(text):
        products = await get_products(client, message)
        return products


async def get_products(client, message):
    text = str(message.text).lower()
    query = clean_text(text)
    products = []
    async for msg in client.search_messages(base_chat, query):
        products.append(msg.id)
    return products

def is_target_chat(chat_id):
    # return chat_id == chat_id
    return chat_id == main_chat and chat_id != base_chat


async def forward_products(client: Client, message: Message, products, user_id=None):
    if products:
        user_id = user_id if user_id else message.from_user.id
        for product in products:
            try:
                await client.copy_media_group(user_id, base_chat, product)
            except ValueError:
                await client.forward_messages(user_id, base_chat, product)

        reply_message = await message.reply(f"✅ Barcha ''{message.text}'' lichkezga (@mainAdmin23) yuborildi")
    else:
        reply_message = await message.reply(f"Iltimos maxsulot nomini tekshirib yozing! "
                            f"\n'maxsulit nomi' bormi "
                            f"\n'mahsulot nomi' kerak")
    await asyncio.sleep(10)
    await reply_message.delete()

@app.on_message(filters.reply & filters.group)
async def reply_products(client: Client, message: Message):
    print(message.chat.id)
    print("ww")
    if is_target_chat(message.chat.id):
        products = await get_products(client, message)
        await forward_products(client, message, products, message.reply_to_message.from_user.id)
        await message.delete()


@app.on_message(filters.group & filters.text)
async def search_products(client: Client, message: Message):
    print(message.chat.id)
    print("ww")
    if is_target_chat(message.chat.id):
        products = await match_get_products(client, message)
        await forward_products(client, message, products)


if __name__ == "__main__":
    print("Bot has been started...")
    app.run()
    print("Bot has been STOPED...")
