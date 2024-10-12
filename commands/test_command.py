from discord_lambda import Interaction, Embedding, CommandArg, CommandRegistry, Channel, PermissionOverwrite, DiscordTypes

# BOT_TOKEN = os.environ.get['BOT_TOKEN']

def ping_command(inter: Interaction) -> None:
    inter.send_response(content="pong your mom!")

def lock_command(inter: Interaction) -> None:
    channel = Channel.get_by_id(inter.channel.id)
    if channel.owner_id != inter.author_id:
        inter.send_response(content="You can't do that...")
        return
    
    allow_overwrite = PermissionOverwrite(channel.owner_id, 1, allow=DiscordTypes.Permissions.SEND_MESSAGES, deny=0)
    channel.set_permissions_overwrite(allow_overwrite)

    for permission_overwrite in channel.permission_overwrite_list:
        if permission_overwrite.id == channel.owner_id:
            continue  
        elif permission_overwrite.is_allowed(DiscordTypes.Permissions.MANAGE_CHANNELS):
            continue

        channel.set_permissions_overwrite(permission_overwrite.id, permission_overwrite.type, allow=0, deny=DiscordTypes.Permissions.SEND_MESSAGES)

    inter.send_response(content=f"Thread locked, bye. \nAlso, take this:{inter.channel.permission_overwrite_list}\n{channel.json()}")


def setup(registry: CommandRegistry) -> None:
    registry.register_cmd(func=ping_command, name="ping", desc="I will pong your mom.", options=[
        # CommandArg(name="input", desc="Add some input to the command!", type=CommandArg.Types.STRING)
    ])

    registry.register_cmd(func=lock_command, name="lock", desc="This thread will be locked for everyone, but you.", options=[
        # CommandArg(name="input", desc="Add some input to the command!", type=CommandArg.Types.STRING)
    ])