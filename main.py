from pyrogram import Client, filters
from pyrogram.types import Message
import sqlite3
from src import const

# Настройка базы данных
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                  (id INTEGER PRIMARY KEY, name TEXT,  img TEXT)''')
conn.commit()


# Конфигурация бота
app = Client(
    "my_shop_bot",
    bot_token=const.BOT_TOKEN,
    api_id=const.API_ID,
    api_hash=const.API_HASH
)


# Обработчик команды /add
@app.on_message(filters.command("add") & filters.private)
async def add_product(client: Client, message: Message):
    print(message)
    # args, name = message.text.split(" ", 1)
    # if name:
    #     cursor.execute("INSERT INTO products (name, img) VALUES (?, ?)",
    #                    (name.strip(), img))
    #     conn.commit()
    #     await message.reply("✅ Товар успешно добавлен!")
    # else:
    #     await message.reply("❌ Используйте: `/add Название | Описание`", parse_mode="Markdown")


# Обработчик команды /search (ищет товар и отправляет в ЛС)
@app.on_message(filters.command("search") & filters.group)
async def search_product(client: Client, message: Message):
    query = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
    if not query:
        await message.reply("❌ Укажите название товара: `/search Название`", parse_mode="Markdown")
        return

    cursor.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{query}%",))
    products = cursor.fetchall()

    if products:
        for product in products:
            await client.send_message(
                message.from_user.id,  # Отправляем в личку
                f"**🔍 {product[1]}**\n\n{product[2]}",
            )
        await message.reply(f"✅ {query} : Sizning lichkangizga yuborildi.")
    else:
        await message.reply(f"😢 {query} : Topilmadi keyinroq xabar oling")


if __name__ == "__main__":
    print("Bot has been started")
    app.run()
