import discord
import time
import asyncio

messages = joined = 0


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = discord.Client()

channels = ["general-chat", "mods-room", "graba", "logs", "server-level", "test"]


async def update_stats():  # get discord stats
    await client.wait_until_ready()
    global messages, joined
    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())},Messages : {messages},Members joined : {joined} \n")

            messages = 0
            joined = 0

            await asyncio.sleep(86400)  # update it every 1 day
        except Exception as e:
            print(e)
            await asyncio.sleep(86400)


@client.event  # welcome a new member
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.sesrver.channels:
        if channel == "👋🏼-welcome":
            await client.send_message(f"""Welcome to the server {member.mention}""")


@client.event  # bot commands
async def on_message(message):
    id = client.get_guild(734912759359340835)
    ch_server = ["general-chat", "mods-room", "graba", "logs", "server-level", "test"]
    bad_words = ["nigga", "shrmota", "kos amk", "bad"]
    for word in bad_words:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)


    if message.content == "?help":
        embed=discord.Embed(title="Help", description="Some useful commands")
        embed.add_field(name="?hello", value="Great the user")
        embed.add_field(name="?users", value="Prints number of users")
        await message.channel.send(content=None , embed=embed)
    global messages
    messages += 1
    if str(message.channel) in ch_server:
        if message.content.find("?hello") != -1:
            await message.channel.send("Hi")
        elif message.content == "?users":
            await message.channel.send(f"""Number of Members is : {id.member_count}""")


client.loop.create_task(update_stats())

client.run(token)
