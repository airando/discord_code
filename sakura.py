@client.command(aliases=['ui','uinfo'])
async def userinfo(ctx,name=None):
    def rv(content):
        if content == 'None':return 'なし'
        value = content.replace('online','オンライン').replace('offline','オフライン')
        value = value.replace('idle','退席中').replace('dnd','取り込み中')
        value = value.replace("`create_instant_invite`","`招待リンクを作成`").replace("`kick_members`","`メンバーをキック`").replace("`ban_members`","`メンバーをBan`")
        value = value.replace("`administrator`","`管理者`").replace("`manage_channels`","`チャンネルの管理`").replace("`manage_guild`","`サーバー管理`")
        value = value.replace("`add_reactions`","`リアクションの追加`").replace("`view_audit_log`","`サーバーログの表示`").replace("`priority_speaker`","`優先スピーカー`")
        value = value.replace("`stream`","`不明`").replace("`read_messages`","`メッセージを読む`").replace("`send_messages`","`メッセージを送信`")
        value = value.replace("`send_tts_messages`","`TTSメッセージを送信`").replace("`manage_messages`","`メッセージの管理`").replace("`embed_links`","`埋め込みリンク`")
        value = value.replace("`attach_files`","`ファイルの添付`").replace("`read_message_history`","`メッセージ履歴を読む`").replace("`mention_everyone`","`全員宛メンション`")
        value = value.replace("`external_emojis`","`外部の絵文字の使用`").replace("`view_guild_insights`","`サーバーインサイトを見る`").replace("`connect`","`接続`")
        value = value.replace("`speak`","`発言`").replace("`mute_members`","`発言`").replace("`mute_members`","`メンバーをミュート`") .replace("`deafen_members`","`メンバーのスピーカーをミュート`")
        value = value.replace("`move_members`","`メンバーの移動`").replace("`use_voice_activation`","`音声検出を使用`").replace("`change_nickname`","`ニックネームの変更`")
        value = value.replace("`manage_nicknames`","`ニックネームの管理`").replace("`manage_roles`","`役職の管理`").replace("`manage_webhooks`","`webhookの管理`")
        value = value.replace("`manage_emojis`","`絵文字の管理`")
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
        embed.add_field(name="ステータス",value=rv(str(member.status)),inline=False)
        if member.activities:
            activities = []
            for activity,count in zip(member.activities,range(len(member.activities))):
                content = f'[`{count}`]'
                if activity.type is discord.ActivityType.custom:
                    emoji = activity.emoji if activity.emoji else ''
                    content += f'CustomStatus({activity.emoji} {activity.name})'
                elif activity.type is discord.ActivityType.listening:
                    content += f'Spotify({activity.title})'
                elif activity.type is discord.ActivityType.playing:
                    content += f'Game({activity.name})'
                elif activity.type is discord.ActivityType.streaming:
                    content += f'Streaming({activity.name})'
                else:content += '不明'
                activities.append(content)
            embed.add_field(name=f"アクティビティ({len(member.activities)})",value="\n".join(activities))
        else:embed.add_field(name="アクティビティ(0)",value=rv(str(None)))
        embed.add_field(name="アカウント作成時刻",value=member.created_at.strftime("%F %T"))
    if member_:
        embed.add_field(name="サーバー参加時刻",value=member_.joined_at.strftime("%F %T"))
        embed.add_field(name="ニックネーム",value=rv(str(member_.nick)))
        period = '...' if len(member_.roles) > 20 else ''
        embed.add_field(name=f"役職({len(member_.roles)})",value=','.join(c.mention for c in list(reversed(member_.roles))[:20:]) + period)
        pers = [f"`{c}`" for c in dict(member_.guild_permissions) if dict(member_.guild_permissions)[c] is True]
        embed.add_field(name=f"権限({len(pers)})",value=rv(",".join(pers)))
        color = member_.color
    await ctx.send(embed=embed)
