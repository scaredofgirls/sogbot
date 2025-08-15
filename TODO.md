# TODO

## Manage Roles via "Reaction"s
For any arbitray role that can be defined in discord we should
be able to have a message with reaction emojis on it, and clicking on the emoji
will add a user to the specified role.

If bot is set to do role management enable `intents.members = True` to the code

## Logging
Work on improving logging in all places

## Features
Each module should be setup to check the config for a list of guild_ids to register with. This lets us restrict some slashcommands availability to a subset of the servers we're connected to.
