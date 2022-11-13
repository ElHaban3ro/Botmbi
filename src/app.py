# Libraries basics.
import json
import os
import codecs


# Third Libraries
import discord
import requests
from discord.ext import commands

import encryption

# Security Settings
key = 'testtesttesttest'








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
    presence = discord.Streaming(name = 'Ombi Requests', url = 'https://github.com/elhaban3ro', details = 'Use /help', platform = 'GitHub')
    await client.change_presence(activity=presence, status = discord.Status.dnd)



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

            config_value_en = encryption.encrypt(bytes(key, encoding='UTF-8'), bytes(config_value, encoding='UTF-8'))
            
            config_value_en = config_value_en




            if config_app == 'ombi': # Si se quiere configurar ombi!
                if config_name == 'host':
                    if 'https://' in config_value or 'http://' in config_value:

                        with open('./src/communities.json', 'r+') as f_u:
                            read_f_u = json.load(f_u)

                            if str(ctx.guild.id) in list(read_f_u.keys()): # Si está ya en la lista, solo puede significar 2 cosas: o ya se configuró antes, o se estableció antes el prefixs


                                read_f_u[str(ctx.guild.id)]['ombiHost'] = config_value_en.decode('latin')


                            else:
                                read_f_u[str(ctx.guild.id)] = {
                                    'communityName': ctx.guild.name,
                                    'ombiHost': config_value_en.decode('latin'),
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


                            read_f[str(ctx.guild.id)]['ombiApikey'] = config_value_en.decode('latin')

                        else:
                            read_f[str(ctx.guild.id)] = {'communityName': ctx.guild.name, 'prefix': read_f['General']['prefix']}




                        json_file.seek(0)
                        json.dump(read_f, json_file, indent = 4)
                        json_file.truncate()
                
                    embed = discord.Embed(title = 'BOTMBI CONFIGURED!', description=f"Your Botmbi's custom **apikey** was configured correctly as: ***{config_value}***", color=0xFFD062)
                    embed.set_author(name = f'Hi, {str(ctx.author)[:str(ctx.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = ctx.author.avatar)
                    embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

                    await ctx.reply(embed = embed)

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




@client.command()
async def add(message, *args):

    if message.author.guild_permissions.administrator:

        p_mentions = list(args)
        mentions = []
        person_in_mentions = False

        if len(p_mentions) >= 1:

            for mention in p_mentions:
                
                if '<@&' in mention:
                    mentions.append(mention[3:-1])

                else:
                    person_in_mentions = True

            if person_in_mentions:
                await message.channel.send('*You have sent in mentions to a user, remember that you cannot set permissions to a member, only to a role.*')

            with open('./src/communities.json', 'r+') as file_json_z:
                open_z = json.load(file_json_z)

                if str(message.guild.id) in list(open_z.keys()):

                    if 'allowed_roles_ombi' in list(open_z[str(message.guild.id)].keys()):
                        for role in mentions:
                            if role not in open_z[str(message.guild.id)]['allowed_roles_ombi']:
                                open_z[str(message.guild.id)]['allowed_roles_ombi'].append(role)


                    else:
                        open_z[str(message.guild.id)]['allowed_roles_ombi'] = mentions



                else:
                    open_z[str(message.guild.id)] = {
                        'communityName': message.guild.name,
                        'prefix': open_z['General']['prefix'],
                        'allowed_roles_ombi': mentions
                    }


                file_json_z.seek(0)
                json.dump(open_z, file_json_z, indent=4)
                file_json_z.truncate()

                mention_roles = ''

                for role in mentions:
                    mention_roles = f'{mention_roles}, <@&{role}>'

                
                if len(mentions) >= 1:
                    embed = discord.Embed(title = 'Add Permissions | BOTMBI', description=f'Permissions were successfully added for {mention_roles[1:]}.', url='https://github.com/elhaban3ro', color=0xFFD062)
                    embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
                    embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)

                    await message.reply(embed = embed)


        else:
            embed = discord.Embed(title = 'No mentions roles | BOTMBI', description=f'You have not mentioned any role :( Remember that to give permissions you must make mention of any one. Use: ```{prefix_see}add [@roles]```', color=0xFFD062)
            embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)
            embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

            await message.reply(embed = embed)

    else:
        embed = discord.Embed(title = 'No administrator permission | BOTMBI', description=f'You do not have administrator permission. Please contact an administrator.', color=0xFFD062)
        embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)
        embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

        await message.reply(embed = embed)





@client.command()
async def remove(message, *args):
    p_mentions = list(args)

    if message.author.guild_permissions.administrator:

        p_mentions = list(args)
        mentions = []
        removes_roles = []
        person_in_mentions = False

        if len(p_mentions) >= 1:

            for mention in p_mentions:
                
                if '<@&' in mention:
                    mentions.append(mention[3:-1])

                else:
                    person_in_mentions = True

            if person_in_mentions:
                await message.channel.send('*You have sent in mentions to a user, remember that you cannot set permissions to a member, only to a role.*')

            with open('./src/communities.json', 'r+') as file_json_z:
                open_z = json.load(file_json_z)

                if str(message.guild.id) in list(open_z.keys()):

                    if 'allowed_roles_ombi' in list(open_z[str(message.guild.id)].keys()):
                        for role in mentions:
                            if role in open_z[str(message.guild.id)]['allowed_roles_ombi']:
                                print(role)
                                removes_roles.append(role)
                                open_z[str(message.guild.id)]['allowed_roles_ombi'].remove(role)


                    else:                        
                        embed = discord.Embed(title = 'There are no roles with assigned permissions | BOTMBI', description=f'None of the above roles have permissions configured.', url='https://github.com/elhaban3ro', color=0xFFD062)
                        embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
                        embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)

                        await message.reply(embed = embed)



                else:
                    embed = discord.Embed(title = 'There are no roles with assigned permissions | BOTMBI', description=f'None of the above roles have permissions configured.', url='https://github.com/elhaban3ro', color=0xFFD062)
                    embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
                    embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)

                    await message.reply(embed = embed)


                file_json_z.seek(0)
                json.dump(open_z, file_json_z, indent=4)
                file_json_z.truncate()

                mention_roles = ''

                for role in removes_roles:
                    mention_roles = f'{mention_roles}, <@&{role}>'

                
                if len(removes_roles) >= 1:
                    embed = discord.Embed(title = 'Permits removed | BOTMBI', description=f'Petition permits were removed in  {mention_roles[1:]}.', url='https://github.com/elhaban3ro', color=0xFFD062)
                    embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
                    embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)

                    await message.reply(embed = embed)

                    print(mentions)





        else:
            embed = discord.Embed(title = 'No mentions roles | BOTMBI', description=f'You have not mentioned any role :( Remember that to give permissions you must make mention of any one. Use: ```{prefix_see}remove [@roles]```', color=0xFFD062)
            embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)
            embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

            await message.reply(embed = embed)

    else:
        embed = discord.Embed(title = 'No administrator permission | BOTMBI', description=f'You do not have administrator permission. Please contact an administrator.', color=0xFFD062)
        embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)
        embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

        await message.reply(embed = embed)





@client.command()
async def search(message, *args):
    if len(list(args)) >= 1:

        pu_roles = message.author.roles
        user_roles = []

        for role in pu_roles:
            role = str(role.id)
            user_roles.append(role)


        global host
        host = ''
        config_host = False


        global apikey
        apikey = ''
        config_apikey = False

        params = {'ApiKey': apikey}

        search = ''
        search_clean = ''

        for word in args:
            search = f'{search}%20{word}'
            search_clean = f'{search_clean} {word}'

        user_allow = False
        search_continue = False


        with open('./src/communities.json') as file_c:
            json_c = json.load(file_c)



            if str(message.guild.id) in list(json_c.keys()):
                if 'allowed_roles_ombi' in list(json_c[str(message.guild.id)].keys()):
                    
                    for role_allow in json_c[str(message.guild.id)]['allowed_roles_ombi']:
                        for role_user in user_roles:

                            if role_allow == role_user:
                                user_allow = True
                                break


            if message.author.guild_permissions.administrator or user_allow:
                if str(message.guild.id) in list(json_c.keys()):

                    



                    if 'ombiHost' in list(json_c[str(message.guild.id)].keys()):
                        host = json_c[str(message.guild.id)]['ombiHost']

                        host_encrypted = bytes(host, encoding = 'latin')
                        
                        host = str(encryption.decrypt(bytes(key, encoding = 'UTF-8'), host_encrypted))[2:-1]
                        


                        if host[-1] == '/':
                            host = host[:-1]


                        config_host = True


                    else:
                        embed = discord.Embed(description=f'The application is not configured. Try to configurate *host*```{prefix_see}config [ombi] [host] [value]```', color=0xFFD062)


                        embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
                        await message.reply(embed = embed)


                        


                    if 'ombiApikey' in list(json_c[str(message.guild.id)].keys()):
                        apikey = json_c[str(message.guild.id)]['ombiApikey']
                        apikey_encrypted = bytes(apikey, encoding = 'latin')
                        apikey = str(encryption.decrypt(bytes(key, encoding = 'UTF-8'), apikey_encrypted))[2:-1]

                        params['ApiKey'] = apikey

                        
                        config_apikey = True
                        

                    else:
                        embed = discord.Embed(description=f'The application is not configured. Try to configurate *apikey*:```{prefix_see}config [ombi] [apikey] [value]```', color=0xFFD062)


                        embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
                        await message.reply(embed = embed)



                if config_host and config_apikey:

                    try:
                        r_movie = requests.post(f'{host}/api/v2/Search/multi/{search[3:]}',
                        params = params, 
                        headers={'Content-Type':'application/json'},
                        data = json.dumps({'movies': 'true', 'tvShows': 'true'}))

                        p_results = r_movie.json()
                        global results
                        results = []
                        
                        if len(p_results) != 0:
                            for content in p_results:
                                search_continue = True
                                try:
                                    results.append({'name': content["title"], 'id': content["id"], 'cover': f'https://image.tmdb.org/t/p/w300/{content["poster"][1:]}', 'contentType': content['mediaType'], 'description': content['overview']})

                                except:
                                    pass
                        
                        else:
                            embed_eror_nocontent = discord.Embed(title = f'No retults to {search_clean[1:]}', description=f'No content found for your search. Make sure you are typing your search correctly.', color=0xFFD062)
                            
                            embed_eror_nocontent.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}.', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)

                            embed_eror_nocontent.set_footer(text = f'View more with {prefix_see}help')

                            await message.reply(embed = embed_eror_nocontent)


                        
                        if search_continue:
                            global img_index
                            img_index = 0

                            embed_img = discord.Embed(title = f'Result to: {results[img_index]["name"]}', description=f'***ID:*** {results[img_index]["id"]}, ***TYPE:*** {results[img_index]["contentType"]}', color=0xFFD062)

                            embed_img.set_image(url = results[img_index]['cover'])

                            embed_img.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}.', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)

                            embed_img.set_footer(text = f'Request with Botmbi 👉👈 to Ombi', icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Sign-check-icon.png/800px-Sign-check-icon.png')



                            class movieButtons(discord.ui.View):
                                @discord.ui.button(label='⬅', style=discord.ButtonStyle.blurple)
                                async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
                                    

                                    embed_img.set_image(url = results[img_index]['cover'])
                                    embed_img.title = f'{results[img_index]["name"]}'
                                    embed_img.description = f'***ID:*** {results[img_index]["id"]}, ***TYPE:*** {results[img_index]["contentType"]}'


                                    button.style = discord.ButtonStyle.green

                                    embed_img.set_thumbnail(url = '')

                                    await interaction.message.edit(embed=embed_img, view=ImageButtons())




                                @discord.ui.button(label = '💌 ORDER', style = discord.ButtonStyle.primary)
                                async def req_movie(self, interaction: discord.Interaction, button: discord.ui.Button):
                                    add_movie = requests.post(f'{host}/api/v1/Request/movie',
                                    params = params, 
                                    headers={'Content-Type':'application/json'},
                                    data = json.dumps({'theMovieDbId': results[img_index]['id']}))
                                    add_movie_status = add_movie.status_code




                                    if add_movie_status == 200:
                                        embed_img.title = f'{results[img_index]["name"]} request.'
                                        embed_img.description = f'Your content request was successful! 💦'

                                        embed_img.set_footer(text = f'Consult status: {add_movie_status}', icon_url='https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQh5hlcX0nvUOGsx8DdQBJjIAVHubSaIAlp1fb3cyhW-NmkkoyS2aCtZ-qFwW4JvMQlj7CVp9qn2Aaw_0ZtZ2z6JYbGIFQ-YV_X81btlOvxxcjrQyWGkSc/330x192')




                                    else:
                                        embed_img.title = f'{results[img_index]["name"]} REQUEST ERROR !!!!'
                                        embed_img.description = f'There was an error with the request. Check your url and apikey.'

                                        embed_img.set_footer(text = f'Consult status: {add_movie_status}', icon_url='https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQh5hlcX0nvUOGsx8DdQBJjIAVHubSaIAlp1fb3cyhW-NmkkoyS2aCtZ-qFwW4JvMQlj7CVp9qn2Aaw_0ZtZ2z6JYbGIFQ-YV_X81btlOvxxcjrQyWGkSc/330x192')


                                    await interaction.message.edit(embed = embed_img, view=None)
    




                            class tvButtons(discord.ui.View):
                                
                                show_info = requests.get(f'https://api.themoviedb.org/3/tv/{results[img_index]["id"]}?api_key=5eb7e21201ae0b13d5e4f992ee9d5471&language=en-US')
                                show_dict = show_info.json()
                                global seasons_count
                                seasons_count = len(show_dict['seasons'])

                                options = []

                                for season in range(1, seasons_count + 1):
                                    if season <= 9:
                                        options.append(discord.SelectOption(label = f'Season 0{season}', description=f'Send request for the season 0{season}'))
                                    
                                    else:
                                        options.append(discord.SelectOption(label=f'Season {season}', description=f'Send request for the season {season}'))



                                # ===================================
                                @discord.ui.select(placeholder = 'Select a season:', min_values = 1, max_values = 1, options = options)
                                async def select_callback(self, interaction, select):
                                
                                    global select_option
                                    select_option = select.values[0]
                                    select_option = select_option[select_option.find(' ') + 1:]

                                    print(select_option)

                                    # if select_option

                                    data_dict = {'theMovieDbId': results[img_index]['id'],
                                                'requestAll': 'false', 
                                                'latestSeason': 'false',
                                                'firstSeason': 'false',
                                                'seasons': [
                                                    {
                                                    'seasonNumber': select_option
                                                    }
                                                ]}

                                    add_movie = requests.post(f'{host}/api/v2/Requests/tv',
                                    params = params, 
                                    headers={'Content-Type':'application/json'},
                                    data = json.dumps(data_dict))
                                    
                                    add_tv_status = add_movie.status_code

                                    if add_tv_status == 200:
                                        embed_img.title = f'{results[img_index]["name"]} season {select_option} request.'
                                        embed_img.description = f'Your content request was successful! 🍟'

                                        embed_img.set_footer(text = f'Consult status: {add_tv_status}', icon_url='https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQh5hlcX0nvUOGsx8DdQBJjIAVHubSaIAlp1fb3cyhW-NmkkoyS2aCtZ-qFwW4JvMQlj7CVp9qn2Aaw_0ZtZ2z6JYbGIFQ-YV_X81btlOvxxcjrQyWGkSc/330x192')




                                    else:
                                        embed_img.title = f'{results[img_index]["name"]} REQUEST ERROR !!!!'
                                        embed_img.description = f'There was an error with the request. Check your url and apikey.'

                                        embed_img.set_footer(text = f'Consult status: {add_tv_status}', icon_url='https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQh5hlcX0nvUOGsx8DdQBJjIAVHubSaIAlp1fb3cyhW-NmkkoyS2aCtZ-qFwW4JvMQlj7CVp9qn2Aaw_0ZtZ2z6JYbGIFQ-YV_X81btlOvxxcjrQyWGkSc/330x192')



                                    await interaction.message.edit(embed = embed_img, view=None)







                                        


                                @discord.ui.button(label='⬅', style=discord.ButtonStyle.blurple)
                                async def back(self, interaction: discord.Interaction, button: discord.ui.Button):

                                    global img_index

                                    embed_img.set_image(url = results[img_index]['cover'])
                                    embed_img.title = f'{results[img_index]["name"]}'
                                    embed_img.description = f'***ID:*** {results[img_index]["id"]}, ***TYPE:*** {results[img_index]["contentType"]}'


                                    button.style = discord.ButtonStyle.green

                                    embed_img.set_thumbnail(url = '')

                                    await interaction.message.edit(embed=embed_img, view=ImageButtons())










                            # print(results)
                            class ImageButtons(discord.ui.View):


                                # Before Image.
                                @discord.ui.button(label='<', style=discord.ButtonStyle.green)
                                async def before(self, interaction: discord.Interaction, button: discord.ui.Button):
                                    global img_index
                                    if img_index == 0:
                                        img_index = len(results) - 1

                                    else:
                                        img_index = img_index - 1


                                    embed_img.set_image(url = results[img_index]['cover'])
                                    embed_img.title = f'{results[img_index]["name"]}'
                                    embed_img.description = f'***ID:*** {results[img_index]["id"]}, ***TYPE:*** {results[img_index]["contentType"]}'


                                    button.style = discord.ButtonStyle.green
                                    await interaction.message.edit(embed=embed_img, view=self)



                                # Next Image.
                                @discord.ui.button(label='>', style=discord.ButtonStyle.green)
                                async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
                                    global img_index
                                    if img_index == len(results) - 1:
                                        img_index = 0

                                    else:
                                        img_index = img_index + 1



                                    embed_img.set_image(url = results[img_index]['cover'])
                                    embed_img.title = f'{results[img_index]["name"]}'
                                    embed_img.description = f'***ID:*** {results[img_index]["id"]}, ***TYPE:*** {results[img_index]["contentType"]}'
                                    

                                    button.style = discord.ButtonStyle.green
                                    await interaction.message.edit(embed=embed_img, view=self)


                                # Request
                                @discord.ui.button(label='🍔 See More ', style=discord.ButtonStyle.green)
                                async def more(self, interaction: discord.Interaction, button: discord.ui.Button):
                                    

                                    
                                    
                                    embed_img.set_image(url = '')
                                    embed_img.set_thumbnail(url = results[img_index]['cover'])

                                    embed_img.title = f'{results[img_index]["name"]}'
                                    embed_img.description = f'{results[img_index]["description"]}'
                                    # print(results[img_index]['contentType'])

                                    if results[img_index]['contentType'] == 'movie':
                                        view = movieButtons()
                                    
                                    else:
                                        view = tvButtons()



                                    await interaction.message.edit(embed=embed_img, view=view)







                            await message.reply(embed = embed_img, view = ImageButtons())


                        


                        if r_movie.status_code != 200:
                            embed = discord.Embed(title = f'SEARCH: {search_clean[1:]}', description=f'Something happened...', color=0xFFD062)
                            embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}, thanks for shearch with Botmbi.', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)
                            embed.set_footer(text = f'Consult status: {r_movie.status_code}', icon_url='https://www.freeiconspng.com/thumbs/warning-icon-png/sign-warning-icon-png-7.png')

                            await message.reply(embed = embed)




                    # except:
                    #     embed = discord.Embed(description=f'Error in the connection to your server, please check your connection. This may be due to an error in the API Key or in the Host itself.:```{prefix_see}config [ombi] [host, apikey] [value]```', color=0xFFD062)


                    #     embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')
                    #     await message.reply(embed = embed)




            else:
                embed = discord.Embed(description=f'You are not authorized to make requests to the Ombi API. Ask the absolute king of your server to give access.', color=0xFFD062)


                embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)

                
                embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

                await message.reply(embed = embed)

    else:

        embed = discord.Embed(title = 'Search not provided | BOTMBI', description=f'You have not entered any value to make your search in Ombi, please follow the following format:```{prefix_see}search [search movie/tv show]```', color=0xFFD062)


        embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)

        
        embed.set_footer(text = f'view more with {prefix_see}help', icon_url='https://www.pngmart.com/files/12/Twitter-Verified-Badge-PNG-HD.png')

        await message.reply(embed = embed)

            



















client.remove_command('help')
@client.command()
async def help(message, *args):
    
    help_text = f"""
    **Configure your Ombi app:** ```{prefix_see}config [ombi] [host, apikey] [value]```\n

    **Configure your prefix:**```{prefix_see}prefix [new prefix]```\n
    
    **Add permissions to a role so that they can make requests:**```{prefix_see}add [@roles]```\n
    
    **Remove permissions to a role so that they can't make requests:**```{prefix_see}remove [@roles]```\n
    
    **Make a content request to your ombi:**```{prefix_see}search [your content to search]```\n"""

    embed = discord.Embed(title = 'Commands Help | BOTMBI', description=help_text, url='https://github.com/elhaban3ro', color=0xFFD062)
    embed.set_author(name = f'Hi, {str(message.author)[:str(message.author).find("#")]}', url = 'https://github.com/elhaban3ro', icon_url = message.author.avatar)
    embed.set_footer(text = f'Recommendation: Automate everything with the help of MovieTool, click title.', icon_url='https://cdn-icons-png.flaticon.com/512/25/25231.png')
    

    await message.reply(embed = embed)










with open(os.path.abspath('./private/config_bot.txt'), 'r') as f: # Se tiene que correr el script desde la carpeta principal.
    configs = f.readlines() # Lista de lines del archivo config!
    token = configs[0]
    
    client.run(token) # Login en sí con el bot!