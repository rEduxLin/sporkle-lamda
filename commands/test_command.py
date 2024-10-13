from discord_lambda import Interaction, Embedding, CommandArg, CommandRegistry, Channel, PermissionOverwrite, DiscordTypes

# BOT_TOKEN = os.environ.get['BOT_TOKEN']

def ping_command(inter: Interaction) -> None:
    inter.send_response(content="pong your mom!")

def lock_command(inter: Interaction) -> None:
    channel = Channel.get_by_id(inter.channel.id)
    if not channel.owner_id:
        return inter.send_response(content="There is nothing to lock, dummy...")
    if channel.owner_id != inter.author_id:
        return inter.send_response(content=f"You can't do that... {channel.owner_id} != {inter.author_id}")
    
    allow_overwrite = PermissionOverwrite(channel.owner_id, 1, allow=str(int(DiscordTypes.Permissions.SEND_MESSAGES | DiscordTypes.Permissions.Mana)), deny=0)
    channel.set_permissions_overwrite(allow_overwrite)

    response = channel.lock_thread()
    if response:
        return inter.send_response(content=response)
        
    inter.send_response(content="Thread locked, bye.")


def setup(registry: CommandRegistry) -> None:
    registry.register_cmd(func=ping_command, name="ping", desc="I will pong your mom.", options=[
        # CommandArg(name="input", desc="Add some input to the command!", type=CommandArg.Types.STRING)
    ])

    registry.register_cmd(func=lock_command, name="lock", desc="This thread will be locked for everyone, but you.", options=[
        # CommandArg(name="input", desc="Add some input to the command!", type=CommandArg.Types.STRING)
    ])