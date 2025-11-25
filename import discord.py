import discord
import random
import asyncio


class MyClient(discord.Client):
    # Suppress error on the User attribute being None since it fills up later
    user: discord.ClientUser

    async def on_ready(self):
        print(f'Logado como {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('$adivinhar'):
            await message.channel.send('adivinhe um número entre 1 e 10.')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Desculpa, você demorou muito para responder. a resposta era {answer}.')

            if int(guess.content) == answer:
                await message.channel.send('Você acertou!')
            else:
                await message.channel.send(f'Ops. O número era {answer}.')


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('token')