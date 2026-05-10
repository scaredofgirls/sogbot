# TODO

## Manage Roles via "Reaction"s
For any arbitray role that can be defined in discord we should be able to have a message with reaction emojis on it, and clicking on the emoji
will add a user to the specified role.

If bot is set to do role management enable `intents.members = True` in the code

## Config validation
Should certainly be a thing.
Maybe a default config so that we can just operate with assumption on what's defined

## Logging
Work on improving logging in all places

## Features
Each module should be setup to check the config for a list of guild_ids to register with. This lets us restrict some slashcommands availability to a subset of the servers we're connected to.
Modules that do not check this will load on all registered discord guilds.

## In progress
getting mcrcon to only load on slips server. ultimately each extension only loads on specified servers
bot_config is now it's own object instead of bot.config
config file got bot.extensions objet to figure out which servers load which extentions

while we're no longer adding properties to "bot", we will need to pass in storage to extensions like we do with the config

### Methods to Restrict Extension Servers
To restrict Nextcord extensions (cogs) to specific servers, define guild_ids within your slash commands or initialize the bot with restricted guild IDs, preventing commands from registering globally. For dynamic restriction within a cog, use checks in the cog_load or command decorators to verify interaction.guild_id against a allowed list

- Define guild_ids in Slash Commands: In your cog file, explicitly set which guilds a command belongs to. If this is omitted, they may become global.
```python
@nextcord.slash_command(name="test", guild_ids=[1234567890, 9876543210])
async def test(self, interaction: nextcord.Interaction):
    await interaction.send("This is a restricted command.")
```
- Set default_guild_ids on Bot Initialization: Define these on the bot instance to apply restrictions to all commands in the extension that don't override it.
```python
bot = commands.Bot(command_prefix="!", default_guild_ids=[1234567890])
```
- Use application_checks: Import application_checks to create a decorator that verifies if the user is in a permitted guild, acting as a secondary restriction.

- Command Registration Timing: If an extension is loaded after on_ready, guild-specific commands may not register immediately, making it best to load them during bot initialization.

#### Best Practices
Use guild_ids in commands for precise, granular control over which extension functionality is available in which server. Ensure the bot has Developer Mode turned on in Discord to easily copy IDs. Remember that using guild_ids keeps commands scoped to those servers, preventing them from being seen or used elsewhere.
