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

global prefix_see
prefix_see = ''

with open('./src/communities.json', 'r+') as prefix_file:
    r_prefix_file = json.load(prefix_file)
    prefix_local_dict = r_prefix_file


async def get_prefix_custom(bot, message):
    
    # Print chat: to manage and debug.
    print(f'{message.author}: {message.content} \t [{message.guild.name}]')




    global prefix_see
    guild = message.guild

    if str(guild.id) in list(prefix_local_dict.keys()):        
        prefix_see = prefix_local_dict[str(guild.id)]['prefix']
        return prefix_local_dict[str(guild.id)]['prefix']


    else:
        prefix_see = prefix_local_dict['General']['prefix']
        return prefix_local_dict['General']['prefix']


client = commands.Bot(command_prefix = get_prefix_custom, intents=intents)





# Incio del servidor.
@client.event
async def on_ready():
    print(f'\n\n= = = = = Started bot! 🌟 | {client.user} = = = = =') # Bot iniciado.



@client.command()
async def prefix(ctx, *args):
    args = list(args)


    

    if ctx.author.guild_permissions.administrator:
        if len(args) == 1:
            new_prefix = args[0]

            with open('./src/communities.json', 'r+') as file_json:
                communities_json = json.load(file_json)
                

                if str(ctx.guild.id) in list(communities_json.keys()):
                    communities_json[str(ctx.guild.id)]['prefix'] = new_prefix

                else:
                    communities_json[str(ctx.guild.id)] = {'communityName': ctx.guild.name, 'prefix': new_prefix}
                


                global prefix_local_dict            
                prefix_local_dict['SEXO'] = 'sí?' # xd?
                prefix_local_dict = communities_json
                    

                # communities_json[ctx.guild.id] = {'communityName': ctx.guild.name, 'prefix': new_prefix}
                file_json.seek(0)
                json.dump(communities_json, file_json, indent = 4)
                file_json.truncate()


        

            embed = discord.Embed(title = 'Change prefix | BOTMBI', description=f'New prefix > **{new_prefix}** < !!', color=0xFFD062)
            embed.set_footer(text = f'view more with {new_prefix}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
            embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)

            await ctx.reply(embed = embed)


        else:
            embed = discord.Embed(title = 'Error to set prefix | BOTMBI', description=f'Error setting your new prefix, follow the following format:\n```{prefix_see}prefix [new prefix]```', url='https://github.com/elhaban3ro', color=0xFFD062)
            embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)
            embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

            await ctx.reply(embed = embed)


    else:
        embed = discord.Embed(title = 'No administrator permission | BOTMBI', description=f'You do not have administrator permission. Please contact an administrator.', color=0xFFD062)
        embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)
        embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

        await ctx.reply(embed = embed)








@client.command()
async def config(ctx, *args):
    
    if ctx.author.guild_permissions.administrator:

        args = list(args)

        if len(args) == 3:
            config_app = args[0]
            config_name = args[1]
            config_value = args[2]

            if config_app == 'ombi': # Si se quiere configurar ombi!
                if config_name == 'host':
                    if 'https://' in config_value or 'http://' in config_value:

                        with open('./src/communities.json', 'r+') as f_u:
                            read_f_u = json.load(f_u)

                            if str(ctx.guild.id) in list(read_f_u.keys()): # Si está ya en la lista, solo puede significar 2 cosas: o ya se configuró antes, o se estableció antes el prefixs

                                read_f_u[str(ctx.guild.id)]['ombiHost'] = config_value


                            else:
                                read_f_u[str(ctx.guild.id)] = {
                                    'communityName': ctx.guild.name,
                                    'ombiHost': config_value,
                                    'prefix': read_f_u['General']['prefix']
                                }


                            

                            f_u.seek(0)
                            json.dump(read_f_u, f_u, indent = 4)
                            f_u.truncate()


                            embed = discord.Embed(title = 'BOTMBI CONFIGURED!', description=f"Your Botmbi's custom host was configured correctly as: ***{config_value}***", color=0xFFD062)
                            embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)
                            embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

                            await ctx.reply(embed = embed)

                    else:
                        embed = discord.Embed(title = 'Ombi host incorrect | BOTMBI', description=f'The provided **host** of your Ombi is incorrect. Remember to add the http method. Enter the command as follows: ```{prefix_see}config ombi host http://myombi.io/```', color=0xFFD062)
                        embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)
                        embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

                        await ctx.reply(embed = embed)





                elif config_name == 'apikey':
                    with open('./src/communities.json', 'r+') as json_file:
                        read_f = json.load(json_file)

                        if str(ctx.guild.id) in list(read_f.keys()):
                            if 'prefix' not in list(read_f[str(ctx.guild.id)]):
                                read_f[str(ctx.guild.id)]['prefix'] = read_f['General']['prefix']


                            read_f[str(ctx.guild.id)]['ombiApikey'] = config_value

                        else:
                            read_f[str(ctx.guild.id)] = {'communityName': ctx.guild.name, 'prefix': read_f['General']['prefix']}




                        json_file.seek(0)
                        json.dump(read_f, json_file, indent = 4)
                        json_file.truncate()
                
                    embed = discord.Embed(title = 'BOTMBI CONFIGURED!', description=f"Your Botmbi's custom **apikey** was configured correctly as: ***{config_value}***", color=0xFFD062)
                    embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)
                    embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

                    await ctx.reply(embed = embed)






                    


                elif config_name == 'apikey': # Si se quiere configurar 
                    pass


                else:
                    embed = discord.Embed(title = 'BOTMBI', description=f'Option not available\nFollow the format below:\n\t```{prefix_see}config [ombi] [host, apikey] [value]```', url='https://github.com/elhaban3ro', color=0xFFD062)

                    embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
                    embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)

                    await ctx.reply(embed = embed)


            else:
                embed = discord.Embed(title = 'BOTMBI', description=f'Option not available\nFollow the format below:\n\t```{prefix_see}config [ombi] [host, apikey] [value]```', url='https://github.com/elhaban3ro', color=0xFFD062)

                embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
                embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)

                await ctx.reply(embed = embed)


        else:
            embed = discord.Embed(title = 'BOTMBI', description=f'Be sure to pass the appropriate parameters.\nFollow the format below:\n\t```{prefix_see}config [ombi] [host, apikey] [value]```', url='https://github.com/elhaban3ro', color=0xFFD062)
            embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
            embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)

            await ctx.reply(embed = embed)



    else:
        embed = discord.Embed(title = 'No administrator permission | BOTMBI', description=f'You do not have administrator permission. Please contact an administrator.', color=0xFFD062)
        embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)
        embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

        await ctx.reply(embed = embed)














client.remove_command('help')
@client.command()
async def help(message, *args):
    
    help_text = f'**Configure your Ombi app:** ```{prefix_see}config [ombi] [host, apikey] [value]```\n\n**Configure your bot:**```{prefix_see}prefix [new prefix]```'

    embed = discord.Embed(title = 'Commands Help | BOTMBI', description=help_text, url='https://github.com/elhaban3ro', color=0xFFD062)
    embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)
    embed.set_footer(text = f'Recommendation: Automate everything with the help of MovieTool, click title.', icon_url='https://cdn-icons-png.flaticon.com/512/25/25231.png')
    

    await message.reply(embed = embed)








with open(os.path.abspath('./private/config_bot.txt'), 'r') as f: # Se tiene que correr el script desde la carpeta principal.
    configs = f.readlines() # Lista de lines del archivo config!
    token = configs[0]
    
    client.run(token) # Login en sí con el bot!