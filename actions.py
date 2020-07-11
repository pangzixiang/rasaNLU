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
from neo4j import GraphDatabase

def check_entity_unique(entity_name, session):
    cypher = "match(a) where a.name =~'.*"+entity_name+".*' and not 'attribute' in labels(a) return a.name"
    query = session.run(cypher).data()
    result = [i['a.name'] for i in query]
    return result

def check_attribute(entity_name, session):
    cypher = "match(a)-[c]->() where a.name =~'.*"+entity_name+".*' and not 'attribute' in labels(a) return type(c)"
    query = session.run(cypher).data()
    result = [i['type(c)'] for i in query]
    return result

def final_query(entity_name, attribute, session):
    cypher = "match(a)-[c]->(b) where a.name =~'.*"+entity_name+".*' and not 'attribute' in labels(a) and type(c) = '"+attribute+"' return b.name"
    result = session.run(cypher).data()[0]['b.name']
    return result

class ActionAskAttribute(Action):
    """Action for querying a specific attribute of an entity."""

    def name(self):
        return "action_ask_attribute"

    def run(self, dispatcher, tracker, domain):
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Aa-12345678"))
        session = driver.session()
        entity_name = tracker.get_slot("entity_type")
        attribute = tracker.get_slot("attribute")

        check_entity = check_entity_unique(entity_name, session)
        if len(check_entity) == 0:
            dispatcher.utter_message(text="对不起，我不是很了解'"+entity_name+"'")
            return []
        elif len(check_entity) > 1:
            dispatcher.utter_message(text="关于'"+entity_name+"'，我了解到以下内容和它类似，请重新告诉我您想知道哪一个：")
            for i, e in enumerate(check_entity):
                dispatcher.utter_message(f"{i + 1}: {e}")
            return []
        else:
            checkAttr = check_attribute(entity_name, session)
            if attribute not in checkAttr:
                dispatcher.utter_message(text="对不起，我不知道'" + entity_name + "'的'" + attribute + "'是什么")
                dispatcher.utter_message(text="我只知道'"+entity_name+"'的以下属性：")
                for i, e in enumerate(checkAttr):
                    dispatcher.utter_message(f"{i + 1}: {e}")
                return []
            else:
                dispatcher.utter_message(text="'" + entity_name + "'的'" + attribute + "'为'" + final_query(entity_name, attribute, session) + "'")
                return []


        # dispatcher.utter_message(text=result)
        # print(tracker.current_slot_values(),tracker.get_slot("attribute"),tracker.get_slot("entity_type"))
        # return []