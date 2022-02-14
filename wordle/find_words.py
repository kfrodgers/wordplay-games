#
#
#
import pymongo
import re
import random


class FindWords(object):
    URL = 'mongodb://localhost:27017'

    def __init__(self, length=5):
        self.db = None
        self.db_name = 'wordplay'
        self._collection = 'words'
        self._length = length

    @property
    def collection(self):
        if self.db is None:
            mongo_client = pymongo.MongoClient(self.URL, connect=False)
            self.db = mongo_client.get_database(self.db_name)

        return self.db[self._collection]

    def load_words(self, filename):
        with open(filename, 'rb') as fp:
            words = fp.readlines()

        count = 0
        new_items = []
        for w in words:
            try:
                if isinstance(w, bytes):
                    w = w.decode('ascii', 'ignore')

                if not isinstance(w, str) or not re.match(r'^[a-z]+$', w.strip()):
                    print('... skipping', w.strip())
                    continue

                w = w.strip().lower()
                item = {
                    'name': w,
                    'letters': ''.join(sorted(w)),
                    'length': len(w)
                }
                doc = self.collection.find_one({'name': w})
                if doc is None:
                    new_items.append(item)

                if len(new_items) > 3000:
                    self.collection.insert_many(new_items)
                    count += len(new_items)
                    new_items = []

            except Exception as e:
                print(f'Exception: {w}, {e}')

        if len(new_items) > 0:
            self.collection.insert_many(new_items)
            count += len(new_items)

        print(f'... added {count} words')

    def count(self):
        return self.collection.count_documents({'length': self._length})

    def get_random_word(self):
        total_words = self.count()
        while True:
            word = self.get_word_by_offset(random.randint(0, total_words))
            if word is not None and "'" not in word:
                break
        return word

    def get_word_by_offset(self, offset):
        word = self.collection.find_one({'length': self._length}, skip=offset, limit=1, sort=[('name', 1)])
        return word['name'] if word is not None else None

    def is_valid_word(self, word):
        word = self.collection.find_one({'name': word, 'length': self._length})
        return word is not None

    @staticmethod
    def get_unique_letters(word):
        return ''.join(set([x for x in word]))

    @staticmethod
    def has_repeating_letter(word):
        return len(word) > len(FindWords.get_unique_letters(word))

    def get_matches(self, matches, remaining_ids=None):
        search = {
            'length': self._length,
            'name': {'$regex': re.compile(f"{matches.lower()}")}
        }
        if isinstance(remaining_ids, list):
            search['_id'] = {'$in': remaining_ids}
        return self.collection.distinct('_id', search)

    def get_unmatches(self, unmatches, remaining_ids=None):
        unmatched_ids = [] if remaining_ids is None else remaining_ids.copy()
        for idx, letter in enumerate(unmatches.lower()):
            if letter != '.':
                pattern = ['.'] * self._length
                pattern[idx] = letter
                regex = ''.join(pattern)
                search = {
                    'length': self._length,
                    'name': {'$not': {'$regex': re.compile(regex)}}
                }
                if len(unmatched_ids) > 0:
                    search['_id'] = {'$in': unmatched_ids}
                unmatched_ids = self.collection.distinct('_id', search)

        return unmatched_ids

    def get_excludes(self, excludes, remaining_ids=None):
        search = {
            'length': self._length,
            'name': {'$not': {'$regex': re.compile(f'[{excludes.lower()}]')}}
        }
        if isinstance(remaining_ids, list):
            search['_id'] = {'$in': remaining_ids}
        return self.collection.distinct('_id', search)

    def get_includes(self, includes, remaining_ids=None):
        regex = '+\\w*'.join(sorted(list(set([x for x in includes.lower()])))) + '+'
        search = {
            'length': self._length,
            'letters': {'$regex': re.compile(regex)}
        }
        if isinstance(remaining_ids, list):
            search['_id'] = {'$in': remaining_ids}
        return self.collection.distinct('_id', search)

    def get_possibles(self, matches='', unmatches='', includes='', excludes='', remaining=None):
        remaining_ids = None
        if remaining is not None:
            remaining_ids = self.collection.distinct('_id', {'name': {'$in': remaining}})

        if len(excludes) > 0:
            remaining_ids = self.get_excludes(excludes, remaining_ids=remaining_ids)

        if len(includes) > 0:
            remaining_ids = self.get_includes(includes, remaining_ids=remaining_ids)

        if len(matches) > 0:
            remaining_ids = self.get_matches(matches, remaining_ids=remaining_ids)

        if len(unmatches) > 0 and unmatches != '.....':
            remaining_ids = self.get_unmatches(unmatches, remaining_ids=remaining_ids)

        return self.collection.distinct('name', {'_id': {'$in': remaining_ids}})
