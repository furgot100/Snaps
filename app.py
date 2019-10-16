import os
import slack
import logging
import ssl as ssl_lib
import certifi
from snaps import OnboardingTutorial

snaps_sent = {}

def start_onboarding(web_client: slack.WebClient, user_id: str, channel: str):
    snaps = OnboardingTutorial(channel)
    message = snaps.get_message_payload()

    response = web_client.chat_postMessage(**message)

    snaps.timestamp = response["ts"]

    if channel not in snaps_sent:
        snaps_sent[channel] = {}
    snaps_sent[channel][user_id] = snaps


@slack.RTMClient.run_on(event="team_join")
def onboarding_message(**payload):
    user_id = payload["data"]["user"]["id"]

    web_client = payload["web_client"]

    response = web_client.im_open(user=user_id)
    channel = response["channel"]["id"]

    start_onboarding(web_client, user_id, channel)

@slack.RTMClient.run_on(event="reaction_added")
def update_emoji(**payload):
    # Checks for reaction added and changes timestamp

    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data["item"]["channel"]
    user_id = data["user"]

    snaps = snaps_sent[channel_id][user_id]

    snaps.reaction_task_completed = True
