import os
from main.mongo import Mongo

import unittest2 as unittest
import requests


class TestWeb(unittest.TestCase):
    def test_add(self):
        url = "http://localhost:5000/add"

        mongodb = Mongo(
            db_name="language",
            collection_name="english",
            ip_address=os.environ['DB'] if os.environ.get('DB') else "localhost"
        )

        r = requests.get(url=url)
        self.assertEqual(r.status_code, 200, "Wrong status code")

        r = requests.post(url=url)
        self.assertEqual(r.status_code, 400, "Wrong status code")

        data = {"english": "boll"}
        r = requests.post(url=url, data=data)
        self.assertEqual(r.status_code, 400, "Wrong status code")
        _filter = {"word": "boll"}
        answer = mongodb.collection.find_one(filter=_filter)
        self.assertFalse(answer)

        data = {"russian": "мяч"}
        r = requests.post(url=url, data=data)
        self.assertEqual(r.status_code, 400, "Wrong status code")
        _filter = {"translation": "мяч"}
        answer = mongodb.collection.find_one(filter=_filter)
        self.assertFalse(answer)

        data = {"english": "boll", "russian": "мяч"}
        r = requests.post(url=url, data=data)
        self.assertEqual(r.status_code, 200, "Wrong status code")
        _filter = {"word": "boll", "translation": "мяч"}
        answer = mongodb.collection.find_one(filter=_filter)
        self.assertTrue(answer)
        mongodb.collection.delete_one(filter=_filter)

        document = {"word": "boll", "translation": "мяч"}
        mongodb.collection.insert_one(document=document)
        answer = mongodb.collection.find_one(filter=document)
        self.assertTrue(answer)
        count = mongodb.collection.count()
        data = {"english": "boll", "russian": "мяч"}
        r = requests.post(url=url, data=data)
        self.assertEqual(r.status_code, 200, "Wrong status code")
        new_count = mongodb.collection.count()
        self.assertEqual(count, new_count, "Wrong count records")
        mongodb.collection.delete_one(filter=document)




        # r = requests.get('http://httpbin.org/get', params={'key1': 'value1', 'key2': 'value2'})
        """
        print(r.content)
        print(r.text)
        print(r.status_code) #200
        print(r.headers)
        {
            'Content-Length': '2204', 
            'Content-Type': 'text/html; charset=utf-8', 
            'Server': 'Werkzeug/0.14.1 Python/3.5.2',
             'Date': 'Sat, 27 Jan 2018 17:14:51 GMT'
         }
        print(r.history) 
        []
        """


if __name__ == "__main__":
    unittest.main()
