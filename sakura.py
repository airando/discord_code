@client.command(aliases=['ui','uinfo'])
async def userinfo(ctx,name=None):
    def return_value(content):
        value = content.replace('online','オンライン').replace('offline','オフライン')
        value.replace('idle','退席中').replace('dnd','取り込み中')
        value.replace("`create_instant_invite`","` `").replace("`kick_members`","` `").replace("`ban_members`","` `")
        value.replace("`administrator`","` `").replace("`manage_channels`","` `").replace("`manage_guild`","` `")
        value.replace("`add_reactions`","` `").replace("`view_audit_log`","` `").replace("`priority_speaker`","` `")
        value.replace("`stream`","` `").replace("`read_messages`","` `").replace("`send_messages`","` `")
        value.replace("`send_tts_messages`","` `").replace("`manage_messages`","` `").replace("`embed_links`","` `")
        value.replace("`attach_files`","` `").replace("`read_message_history`","` `").replace("`mention_everyone`","` `")
        value.replace("`external_emojis`","` `").replace("`view_guild_insights`","` `").replace("`connect`","` `")
        value.replace("`speak`","` `").replace("`mute_members`","` `").replace("`deafen_members`","` `")
        value.replace("`move_members`","` `").replace("`use_voice_activation`","` `").replace("`change_nickname`","` `")
        value.replace("`manage_nicknames`","` `").replace("`manage_roles`","` `").replace("`manage_webhooks`","` `")
        value.replace("`manage_emojis`","` `")
        return value

    if name is None:member = ctx.author
    else:
        member = discord.utils.get(client.get_all_members(),mention=name)
        if member is None:member = discord.utils.get(client.get_all_members(),name=name)
        if member is None:
            try:int(name)
            except ValueError:pass
            else:
                member = discord.utils.get(client.get_all_members(),id=int(name))
    if member is not None:user = await client.fetch_user(member.id)
    else:
        try:user = await client.fetch_user(int(name))
        except:return
    member_ = ctx.guild.get_member(user.id)
    embed = discord.Embed(color=0xFF0000)
    embed.set_author(name="User Info")
    if user.is_avatar_animated():embed.set_thumbnail(url=member.avatar_url)
    else:embed.set_thumbnail(url=user.avatar_url_as(format='png'))
    embed.add_field(name="ユーザー名",value=str(user))
    embed.add_field(name="ID",value=str(user.id))
    embed.add_field(name="ボット",value=str(user.bot))
    if member is not None:
        embed.add_field(name="ステータス",value=str(member.status),inline=False)
        if member.activities:
            embed.add_field(name=f"アクティビティ({len(member.activities)})",value="\n".join(c.name for c in member.activities))
        else:embed.add_field(name="アクティビティ(0)",value="None")
        embed.add_field(name="アカウント作成時刻",value=member.created_at.strftime("%F %T"))
    if member_:
        embed.add_field(name="サーバー参加時刻",value=member_.joined_at.strftime("%F %T"))
        embed.add_field(name="ニックネーム",value=str(member_.nick))
        embed.add_field(name=f"役職({len(member_.roles)})",value=','.join(c.mention for c in list(reversed(member_.roles))[:20:]))
        pers = [f"`{c}`" for c in dict(member_.guild_permissions) if dict(member_.guild_permissions)[c] is True]
        embed.add_field(name=f"権限({len(pers)})",value=",".join(pers))
    await ctx.send(embed=embed)
