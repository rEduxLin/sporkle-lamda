from discord_lambda import Interaction, Embedding, CommandArg, CommandRegistry
import time


def ping_command(inter: Interaction) -> None:
    inter.send_response(content="pong your mom!")

def lock_command(inter: Interaction) -> None:

    channel = inter.channel
    perm_list = inter.channel.permission_overwrite_list


    inter.send_response(content=f"Thread locked, bye. \nCheck out this shit: \n{inter.channel_raw}")



def setup(registry: CommandRegistry) -> None:
    registry.register_cmd(func=ping_command, name="ping", desc="I will pong your mom.", options=[
        # CommandArg(name="input", desc="Add some input to the command!", type=CommandArg.Types.STRING)
    ])

    registry.register_cmd(func=lock_command, name="lock", desc="This thread will be locked for everyone, but you.", options=[
        # CommandArg(name="input", desc="Add some input to the command!", type=CommandArg.Types.STRING)
    ])