# Discord Minecraft Whitelist bot

This docker image provides a discord bot that you can self host to whitelist players on a remote Minecraft server. To set it up, create a new channel with info for your server. Put in a single message and set the permissions so that members can't post there, but they can respond to messages. Users will be able to respond to that message, and the bot will send them a DM asking for their username. The bot will then verify the username with Mojang and if it comes back as a valid user, the server will whitelist that username. 

To run the bot you will need to use each ENV variable so that the bot can connect to the Minecraft Server and the Discord Server. \
| ENV      | Description |
| ----------- | ----------- |
| `DIS_MC_TOKEN`      | The token for the bot. Can only be added by the bot owner|
| `DIS_MC_HOSTNAME`   | The IP or domain name for the server        |
|`DIS_MC_USERNAME` | A user on the Minecraft server. Must have ability to access the server commands|
| `DIS_MC_PASSWORD`| the `DIS_MC_USERNAME`'s password|
|`DIS_MC_SERVER_INFO_MESSAGE_ID` | The ID of the message that the bot will watch for user reactions|
| `DIS_MC_MAIN_CHANNEL_ID` | The channel where the `DIS_MC_SERVER_INFO_MESSAGE_ID` message resides|

link to [DockerHub repo](https://hub.docker.com/repository/docker/wmsmckay/discord-minecraft-whitelist)

To simply use the latest stable version, run

```bash 
docker run \
-e DIS_MC_TOKEN=1234567890qwertyuiopasdfghjklzxcvbnm \
-e DIS_MC_HOSTNAME="10.0.0.16" \
-e DIS_MC_USERNAME="username" \
-e DIS_MC_PASSWORD="password \
-e DIS_MC_SERVER_INFO_MESSAGE_ID=1234567890 \
-e DIS_MC_MAIN_CHANNEL_ID=234567012456 \
-d wmsmckay/discord-minecraft-whitelist```
