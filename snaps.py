class OnboardingTutorial:
    #Construct onboarding message
    welcome_block = {
        "type" : "section",
        "text" : {
            "type" : "mrkdwn",
            "text" : (
                "Test Message :wave: "
            ),
        },
    }
    divider_block = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "TestBot"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.reaction_task_completed = False
        self.pin_task_completed = False 
    
    #gets message
    def get_message_payload(self):
        return {
            "ts" : self.timestamp,
            "channel" : self.channel,
            "username" : self.username,
            "icon_emoji" : self.icon_emoji,
            "blocks": [
                self.welcome_block,
                self.divider_block,
                *self._get_reaction_block(),
                self.divider_block,
                *self._get_reaction_block(),
            ],
        }
    def _get_reaction_block(self):
        task_checkmark = self._get_checkmark(self.reaction_task_completed)
        text = (
            f'{task_checkmark} Add an emoji to react :thinking_face: \n'
            "Test Message"
            "Reactions used "
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/206870317-Emoji-reactions|"
            "Learn how to use emoji reactions"
        )
        return self._get_task_block(text, information)

    def _get_pin_block(self):
        task_checkmark = self._get_checkmark(self.pin_task_completed)
        text = (
            f"{task_checkmark} :round_pushpin:\n"
            "Pin messages"
        )
        information = (
            "info source"
        )
        return self._get_task_block(text, information)

    @staticmethod
    def _get_checkmark(task_completed: bool) -> str:
        if task_completed:
            return ":white_checkmark:"
        return ":white_large_square:"

    @staticmethod
    def _get_task_block(text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements":[{"type": "mrkdwn", "text":information}]},
        ]