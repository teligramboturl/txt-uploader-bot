# Add a list of sudo users (replace with your Telegram user ID and other sudo users)
SUDO_USERS = [1147534909]  # Add your Telegram user ID here

# Function to check if a user is authorized
def is_authorized(user_id):
    return user_id in SUDO_USERS

# Sudo command to add/remove sudo users
@bot.on_message(filters.command("sudo"))
async def sudo_command(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in SUDO_USERS:
        await message.reply_text("**🚫 You are not authorized to use this command.**")
        return

    try:
        args = message.text.split(" ", 2)
        if len(args) < 2:
            await message.reply_text("**Usage:** `/sudo add <user_id>` or `/sudo remove <user_id>`")
            return

        action = args[1].lower()
        target_user_id = int(args[2])

        if action == "add":
            if target_user_id not in SUDO_USERS:
                SUDO_USERS.append(target_user_id)
                await message.reply_text(f"**✅ User {target_user_id} added to sudo list.**")
            else:
                await message.reply_text(f"**⚠️ User {target_user_id} is already in the sudo list.**")
        elif action == "remove":
            if target_user_id in SUDO_USERS:
                SUDO_USERS.remove(target_user_id)
                await message.reply_text(f"**✅ User {target_user_id} removed from sudo list.**")
            else:
                await message.reply_text(f"**⚠️ User {target_user_id} is not in the sudo list.**")
        else:
            await message.reply_text("**Usage:** `/sudo add <user_id>` or `/sudo remove <user_id>`")
    except Exception as e:
        await message.reply_text(f"**Error:** {str(e)}")

# Modify the start command to check authorization
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    if not is_authorized(message.from_user.id):
        await message.reply_text("**🚫 You are not authorized to use this bot.**")
        return

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption,
        reply_markup=keyboard
    )

# Modify the upload command to check authorization
@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, message: Message):
    if not is_authorized(message.from_user.id):
        await message.reply_text("**🚫 You are not authorized to use this bot.**")
        return

    # Rest of the upload command logic remains the same
    editable = await m.reply_text('𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀 𝐓𝐱𝐭 𝐅𝐢𝐥𝐞 𝐒𝐞𝐧𝐝 𝐇𝐞𝐫𝐞 📄')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("**∝ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐢𝐧𝐩𝐮𝐭.**")
        os.remove(x)
        return

    # Rest of the upload command logic...

# Modify the stop command to check authorization
@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    if not is_authorized(m.from_user.id):
        await m.reply_text("**🚫 You are not authorized to use this bot.**")
        return

    await m.reply_text("**𝐒𝐭𝐨𝐩𝐩𝐞𝐝**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

# Run the bot
bot.run()
