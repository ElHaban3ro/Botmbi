# Libraries basics.
import os


# Third Libraries
import discord
from discord.ext import commands
import json





print('Running bot...')
intents = discord.Intents.default()
intents.message_content = True


# class Client(commands.Bot)
global prefix_local_dict
prefix_local_dict = {}

with open('./src/communities.json', 'r+') as prefix_file:
    r_prefix_file = json.load(prefix_file)
    prefix_local_dict = r_prefix_file


async def get_prefix_custom(bot, message):
    
    # Print chat: to manage and debug.
    print(f'{message.author}: {message.content} \t [{message.guild.name}]')




    guild = message.guild

    if str(guild.id) in list(prefix_local_dict.keys()):
        
        return prefix_local_dict[str(guild.id)]['prefix']

    else:
        return prefix_local_dict['General']['prefix']

        
client = commands.Bot(command_prefix = get_prefix_custom, intents=intents)





# Incio del servidor.
@client.event
async def on_ready():
    print(f'\n\n= = = = = Started bot! 🌟 | {client.user} = = = = =') # Bot iniciado.



@client.command()
async def prefix(ctx, *args):
    args = list(args)

    if len(args) == 1:
        new_prefix = args[0]

        with open('./src/communities.json', 'r+') as file_json:
            communities_json = json.load(file_json)
            

            if str(ctx.guild.id) in list(communities_json.keys()):
                communities_json.pop(str(ctx.guild.id))


            communities_json.update({str(ctx.guild.id): {'communityName': ctx.guild.name, 'prefix': new_prefix}})


            global prefix_local_dict            
            prefix_local_dict['SEXO'] = 'sí?'
            prefix_local_dict = communities_json
                

            # communities_json[ctx.guild.id] = {'communityName': ctx.guild.name, 'prefix': new_prefix}
            file_json.seek(0)
            json.dump(communities_json, file_json, indent = 4)
            file_json.truncate()


    

        embed = discord.Embed(title = 'Change prefix | BOTMBI', description=f'New prefix ---- > {new_prefix} < ---- !!', url='https://github.com/elhaban3ro', color=0xFFD062)
        embed.set_footer(text = f'view more with PREFIX_TESThelp', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
        embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)

        await ctx.reply(embed = embed)


    else:
        embed = discord.Embed(title = 'Error to set prefix | BOTMBI', description=f'Error setting your new prefix, follow the following format:\n```PREFIX_TESTprefix [new prefix]```', url='https://github.com/elhaban3ro', color=0xFFD062)
        embed.set_footer(text = f'view more with PREFIX_TESThelp', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
        embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)

        await ctx.reply(embed = embed)








@client.command()
async def config(ctx, *args):
    

    args = list(args)

    if len(args) == 3:
        config_app = args[0]
        config_name = args[1]
        config_value = args[2]

        if config_app == 'ombi': # Si se quiere configurar ombi!
            if config_name == 'host':
                if 'https://' in config_value or 'http://' in config_value:
                    await ctx.channel.send('*Valid Host*')
                    community_data = {'communityId': ctx.guild.id, 'communityName': ctx.guild.name, 'prefix': get_prefix_custom(str(ctx.author.id))}

                    print(community_data)

                else:
                    await ctx.reply('*Invalid value :(*')

                


            elif config_name == 'apikey': # Si se quiere configurar 
                pass


            else:
                embed = discord.Embed(title = 'BOTMBI', description='Option not available\nFollow the format below:\n\t```!config [ombi] [host, apikey] [value]```', url='https://github.com/elhaban3ro', color=0xFFD062)

                embed.set_footer(text = f'view more with PREFIX_TESThelp', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
                embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)

                await ctx.reply(embed = embed)


        else:
            embed = discord.Embed(title = 'BOTMBI', description='Option not available\nFollow the format below:\n\t```!config [ombi] [host, apikey] [value]```', url='https://github.com/elhaban3ro', color=0xFFD062)

            embed.set_footer(text = f'view more with PREFIX_TESThelp', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
            embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)

            await ctx.reply(embed = embed)


    else:
        embed = discord.Embed(title = 'BOTMBI', description='Be sure to pass the appropriate parameters.\nFollow the format below:\n\t```!config [ombi] [host, apikey] [value]```', url='https://github.com/elhaban3ro', color=0xFFD062)
        embed.set_footer(text = f'view more with PREFIX_TESThelp', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
        embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)

        await ctx.reply(embed = embed)




# History

# Pausa los comandos :( rari

# @client.event
# async def on_message(message):
#     # TODO: Guardar historial en un archivo. Por ahora lo dejo solo en consola.
#     print(f'{message.author}: {message.content}')






with open(os.path.abspath('./private/config_bot.txt'), 'r') as f: # Se tiene que correr el script desde la carpeta principal.
    configs = f.readlines() # Lista de lines del archivo config!
    token = configs[0]
    
    client.run(token) # Login en sí con el bot!