# Releases Bot

This is a simple Telegram Bot to tell you when a new (fixed) Android Release is available. You can find this bot as [@AndroidReleasesBot](https://t.me/AndroidReleasesBot)

### This is not a branch tracking bot! You must manually define the URL to track.

# Setup

 - Go to [@BotFather](https://t.me/BotFather) and send the `/setprivacy` command and then disable it.
 - Install dependencies with `pip3 install -r requirements.txt`
 - Create a new config.py file with the following:
```python
token = "TOKEN:HERE"
url = "https://android.googlesource.com/platform/manifest/+/refs/tags/android-10.0.0_r1"
```
 - Run the bot
