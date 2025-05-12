from pyrogram import Client, filters
from pyrogram.types import Message
import sqlite3


# Настройка базы данных
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                  (id INTEGER PRIMARY KEY, name TEXT,  img TEXT, description TEXT)''')
conn.commit()

# Конфигурация бота
app = Client(
    "my_shop_bot",
    bot_token="YOUR_BOT_TOKEN",  # Замени на свой токен от @BotFather
    api_id=12345,  # Получи на my.telegram.org
    api_hash="your_api_hash"  # Получи там же
)


# Обработчик команды /add
@app.on_message(filters.command("add") & filters.group)
async def add_product(client: Client, message: Message):
    args = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
    if args and "|" in args:
        name, description = args.split("|", 1)
        cursor.execute("INSERT INTO products (name, description) VALUES (?, ?)",
                       (name.strip(), description.strip()))
        conn.commit()
        await message.reply("✅ Товар успешно добавлен!")
    else:
        await message.reply("❌ Используйте: `/add Название | Описание`", parse_mode="Markdown")


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
                parse_mode="Markdown"
            )
        await message.reply("✅ Результаты отправлены в личные сообщения!")
    else:
        await message.reply("😢 Товар не найден")


if __name__ == "__main__":
    print("Бот запущен!")
    app.run()