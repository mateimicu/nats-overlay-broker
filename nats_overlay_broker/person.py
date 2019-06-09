#!/usr/bin/env python3
import random
import datetime
import json
import copy
import pprint
import math

import faker


def random_date():
    fake = faker.Faker()
    return str(fake.date_time_between(start_date='-30y', end_date='+30y'))

def random_name():
    return random.choice(["bob", "maria", "maricica"])

def random_color():
    return random.choice(["rosu", "cacaniu", "plm"])

def random_heartrate():
    return random.randint(80, 150)

def random_height():
    return random.randint(140, 190) / 100

def random_operator(eq_proc=None):
    if eq_proc is None:
        return random.choice(["<", "<=", "==", ">=", ">"])

    if random.random() > eq_proc:
        return random.choice(["<", "<=", ">=", ">"])
    else:
        return "=="

OPPERATIONS = {
    "<": lambda x, y: x < y,
    "<=": lambda x, y: x <= y,
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
    "==": lambda x, y: x == y,
}


FIELDS = {
    "name": random_name,
    "dob": random_date,
    "heartrate": random_heartrate,
    "color": random_color,
    "height": random_height
}

class Person():

    def __init__(self, name, dob, heartrate, color, height):
        self._name = name
        self._dob = dob
        self._heartrate = heartrate
        self._color = color
        self._height = height

    def as_dict(self):
        return {
            "name": self._name,
            "dob": self._dob,
            "heartrate": self._heartrate,
            "color": self._color,
            "height": self._height,
        }

    def as_json(self):
        return json.dumps(self.as_dict())

    @staticmethod
    def get_random_person():
        vals = {key: gen() for key, gen in FIELDS.items()}
        return Person(**vals)

    def applies_to(self, _filter):
        d_person = self.as_dict()

        for rule in _filter:
            field = rule['name']
            cmp_func = OPPERATIONS[rule['op']]
            val = rule['val']

            try:
                if not cmp_func(d_person[field], val):
                    return False 
            except:
                return False
        return True



def gen_subscriptions(subscriptions_count, rules, eq_rules):
    """Generate a random number of subscriptions.

    :param subscriptions_count: Number of subscriptions to generate
    :param rules: A list with the rules representing on how nay (percentage based)
                  subscriptions there should be a filter based on that field.

        :Examnpel:
            RULES = [
                ("name", .5),
                ("dob", .7),
                ("color", 1),
                ("height", .5),
            ]

    :param eq_rules: A dict representing the percentage of equality checks made 
                     on the specific filter. For the example 90% of the filters
                     made for `dob` will be equality checks(take in to account
                     that 70% of the subscriptions will have a dob check, so 90%
                     from 70% from the total subscriptions will have this)

        :Example:
            EQ_RULE = {'dob': .9}

    """
    subscriptions = [[] for _ in range(subscriptions_count)]
    local_rules = copy.deepcopy(rules)
    # fill all subscriptions first with at least a filter
    first_index = 0
    for field, proc in local_rules[:]:
        eq_proc = eq_rules.get(field, None)
        items_left = float(subscriptions_count - first_index)
        proc_items_left = math.floor(items_left / subscriptions_count)
        
        local_rules.pop(0)
        if proc_items_left >= proc:
            for sub in subscriptions[first_index:first_index+int(proc*subscriptions_count)]:
                sub.append({
                    "name": field,
                    "op": random_operator(eq_proc),
                    "val": FIELDS[field]()
                })
            first_index += int(proc*subscriptions_count)
        else:
            # split the proc and break
            proc_to_be_used = proc - proc_items_left
            local_rules.append((field, proc_to_be_used))

            for sub in subscriptions[first_index:first_index+int(proc_items_left*subscriptions_count)]:
                sub.append({
                    "name": field,
                    "op": random_operator(eq_proc),
                    "val": FIELDS[field]()
                })
            break



    # fill other subscriptions 
    for field, proc in local_rules:
        eq_proc = eq_rules.get(field, None)
        random.shuffle(subscriptions)
        for sub in subscriptions[:int(proc*subscriptions_count)]:
            sub.append({
                "name": field,
                "op": random_operator(eq_proc),
                "val": FIELDS[field]()
            })

    return subscriptions

