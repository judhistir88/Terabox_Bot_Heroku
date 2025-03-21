# Terabox Downloader Bot

This is a Telegram Bot written in Python for Downloading Videos From Terabox.

## Setup Environment Variables:

- `BOT_TOKEN`: The Telegram Bot Token that you got from [@BotFather](https://t.me/BotFather). `Str`
- `OWNER_ID`: Your Telegram User ID (required for admin commands). `Int`
- `DUMP_CHAT_ID`: The Dump Channel, all leeched videos will be forwarded here. (Enter the Channel/Group ID starting with -100). `Int`
- `MONGO_URL`: Your MongoDB connection string. `Str`
- `WEBHOOK_URL`: The URL for setting up the webhook. `Str`
- `PORT`: The port number for the Flask app. Default is `8443`.

## Deployment

### Deploy on Heroku

1. **Fork the Repository:**
   - Fork this repository to your own GitHub account.

2. **Create a New App on Heroku:**
   - Go to the [Heroku Dashboard](https://dashboard.heroku.com/) and create a new app.

3. **Connect GitHub to Heroku:**
   - Under the "Deploy" tab in your Heroku app, select GitHub as the deployment method.
   - Search for your forked repository and connect it.

4. **Set Environment Variables:**
   - Go to the "Settings" tab in your Heroku app and click on "Reveal Config Vars".
   - Add the environment variables listed above with their corresponding values.

5. **Deploy the App:**
   - Go to the "Deploy" tab and deploy the app either by enabling automatic deploys or by manually deploying the branch.

6. **Set the Webhook:**
   - After deploying, set the webhook by visiting `https://<your-app-name>.herokuapp.com/set_webhook`.

## Usage

1. **Start the Bot:**
   - Open Telegram and start a chat with your bot by searching for its username.
   - Send the `/start` command to initiate interaction with the bot.

2. **Send Terabox Links:**
   - Send any valid Terabox link to the bot, and it will download the video and send it to you.

3. **Admin Commands:**
   - `/ban <user_id>`: Ban a user from using the bot.
   - `/unban <user_id>`: Unban a user.
   - `/broadcast <message>`: Broadcast a message to all users.

## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License.
