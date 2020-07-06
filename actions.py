# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
class ActionAskAttribute(Action):
    """Action for querying a specific attribute of an entity."""

    def name(self):
        return "action_ask_attribute"

    def run(self, dispatcher, tracker, domain):
        with open("./data.json","r",encoding='utf-8') as f:
            data = json.loads(f.read())
        result = data[tracker.get_slot("entity_type")][tracker.get_slot("attribute")]
        dispatcher.utter_message(text=result)
        print(tracker.current_slot_values())
        return []