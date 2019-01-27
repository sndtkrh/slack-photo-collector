# Slack Photo Collector

## Overview
This Slack bot collect photos in joined channel and upload them to Google Photo album.

## Requirement
- Python 3

## Deployment
1. Prepare Slack App
    - For example, see https://github.com/lins05/slackbot >`Usage`>`Generate the slack api token`.
1. Invite your slack bot to channels that you want to collect photos
1. Enable Google Photo API and prepare Google Client ID and secret
    - See https://developers.google.com/photos/library/guides/get-started .
1. Clone this repository
    ```bash
    git clone https://github.com/sndtkrh/slack-photo-collector.git
    ```
1. Install slackbot
    ```bash
    python -m pip install slackbot
    ```
1. Initialize token information
    - Following command will ask you about your slack OAuth token and Google Client ID and secret.
        ```bash
        python initialize.py
        ```
    - After initialization, `token.json` will be generated.
1. Start bot
    ```bash
    python run.py
    ```

