import discord

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

questions = {
    "What is your first name?": "first_name",
    "What is your mother's maiden name?": "mothers_maiden_name",
    "What is your last name?": "last_name",
    "What is the city where you were born?": "city_of_birth",
}

responses = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!starwarsname'):
        # create a private channel with the user
        private_channel = await message.author.create_dm()

        for question in questions:
            await private_channel.send(question)
            response = await client.wait_for('message', check=lambda message: message.author == message.author)
            responses[questions[question]] = response.content

        # generate the Star Wars name
        star_wars_first_name = responses["first_name"][:3].capitalize() + responses["last_name"][:2].lower()
        star_wars_last_name = responses["mothers_maiden_name"][:2] + responses["city_of_birth"][:3].lower()
        star_wars_name = f"{star_wars_first_name} {star_wars_last_name.capitalize()}"

        # reply with the generated Star Wars name in the channel where the command was written
        await message.channel.send(f"{message.author.mention}, your Star Wars name is: {star_wars_name}")

# run the bot
client.run('KEY')
