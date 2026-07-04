import discord

def intents():
    """Create and configure the Discord bot intents."""

    intents = discord.Intents.default()
    intents.message_content = True

    # TODO: XD
    # intents = discord.Intents.none()

    return intents