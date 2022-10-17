import json


def response_as_dict(response):
    return json.loads(response.data.decode("utf-8"))


class Matcher:
    def __init__(self, dictionary):
        self.keyset = set(dictionary.keys())

    def only_contains_the_following_keys(self, *keyset):
        return self.keyset == set(*keyset)


def keyset_of(response):
    if type(response) == dict:
        return Mather(response)
    return Matcher(response_as_dict(response))
