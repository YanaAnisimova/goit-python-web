import json
import os
import pickle

data = [
        {"type": "Cat", "name": "Alaska", "age": 1, "color": "blue"},
        {"type": "Dog", "name": "Bob", "age": 3, "color": "black"}
    ]


class SerializationInterface:
    def serialize(self, file_name, data):
        raise NotImplementedError()


class JSONSerialization(SerializationInterface):
    def serialize(self, file_name, data):
        with open(f'data/{file_name}', 'w') as file:
            json.dump(data, file)


class BINSerialization(SerializationInterface):
    def serialize(self, file_name, data):
        with open(f'data/{file_name}', 'wb') as file:
            pickle.dump(data, file)


if __name__ == '__main__':
    file_name = 'somedata.bin'

    try:
        os.mkdir('data')
    except FileExistsError:
            pass

    if file_name.endswith('json'):
        Serialization = JSONSerialization
    else:
        Serialization = BINSerialization

    Serialization().serialize(file_name, data)