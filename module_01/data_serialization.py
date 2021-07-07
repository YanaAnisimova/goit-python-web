from abc import ABC, abstractmethod
import json
import os
import pickle


class User:
    # class for tests
    def __init__(self, name):
        self.name = name


data = [
    {'type': 'Cat', 'name': 'Alaska', 'age': 1, 'color': 'blue'},
    ('Dog', 'Bob', 3, 'black', {'1', 2}, (3, '4'), {1: 'one'}),
    {False: 'this data', 42: 'answer', 'foo': 'bar', 'Vasya':{'age': 20, 'sex': 'm', 1: True}, '123': [1, 2, 3]}
    ]


class SerializationInterface(ABC):
    @abstractmethod
    def serialize(self, file_name, data):
        pass

    @abstractmethod
    def deserialize(self, file_name):
        pass


class JSONSerialization(SerializationInterface):

    # Serialization
    def serialize(self, file_name, data):
        with open(f'data/{file_name}', 'w') as file:
            json.dump(self.parse_data(data), file, ensure_ascii=False, indent=4)

    def parse_data(self, data):
        parser = {'str': self.parse_str_bool_float_int_none, 'bool': self.parse_str_bool_float_int_none,
                  'float': self.parse_str_bool_float_int_none, 'int': self.parse_str_bool_float_int_none,
                  'NoneType': self.parse_str_bool_float_int_none, 'dict': self.parse_dict, 'list': self.parse_list,
                  'tuple': self.parse_tuple, 'set': self.parse_set}
        try:
            return parser[type(data).__name__](data)
        except KeyError:
            raise KeyError(f'Object of type {type(data).__name__} is not JSON serializable')
        except TypeError:
            raise

    # {1: 'one', '2': 'two'} => {'int:1': 'one', 'str:2': 'two'}
    def formatting_key_dict(self, data):
        return '{}:{}'.format(type(data).__name__, data)

    types_not_parse = ('str', 'bool', 'float', 'int', 'NoneType')

    def parse_str_bool_float_int_none(self, data):
        return data

    def parse_dict(self, data):
        parsed_dict = {}
        for key, value in data.items():
            if type(key).__name__ in self.types_not_parse and type(value).__name__ in self.types_not_parse:
                parsed_dict[self.formatting_key_dict(key)] = value
                continue
            if type(key).__name__ not in self.types_not_parse:
                key = self.parse_data(key)
            if type(value).__name__ not in self.types_not_parse:
                value = self.parse_data(value)
            try:
                parsed_dict[key] = value
            except TypeError:
                raise TypeError(f'A dictionary with a key of type "tuple" is not JSON serializable.')

        return parsed_dict

    def parse_list_tuple_set(self, data):
        parsed_list = []
        for el in data:
            if type(el).__name__ in self.types_not_parse:
                parsed_list.append(el)
                continue
            else:
                el = self.parse_data(el)
            parsed_list.append(el)
        return parsed_list

    def parse_list(self, data):
        return self.parse_list_tuple_set(data)

    # converts a tuple to a list and makes it a dictionary value: '{"tuple": [..., ]}'
    def parse_tuple(self, data):
        return dict(tuple=(self.parse_list_tuple_set(data)))

    # converts a set to a list and makes it a dictionary value: '{"set": [..., ]}'
    def parse_set(self, data):
        return dict(set=(self.parse_list_tuple_set(data)))

    # Deserialization
    def deserialize(self, file_name):
        with open(f'data/{file_name}') as file:
            data = json.load(file)
            print('Data serialized: ', data)
            return self.de_parse_iter(data)

    iter_type = {'dict': dict, 'list': list, 'tuple': tuple, 'set': set}
    oll_type = {'dict': dict, 'list': list, 'tuple': tuple, 'set': set, 'str': str, 'int': int, 'float': float,
                'bool': bool}

    # converts dictionary keys, tuples, sets to their original form
    def de_parse_iter(self, data):
        if type(data).__name__ == 'dict':
            if list(data.keys())[0] == 'tuple':
                return tuple([self.de_parse_data(el) for value in data.values() for el in value])
            elif list(data.keys())[0] == 'set':
                return set([self.de_parse_data(el) for value in data.values() for el in value])
            return {self.de_parse_data(k): self.de_parse_data(v) for k, v in data.items()}
        if type(data).__name__ == 'tuple':
            return tuple([self.de_parse_data(el) for el in data])
        if type(data).__name__ == 'list':
            return [self.de_parse_data(el) for el in data]
        if type(data).__name__ == 'set':
            return {self.de_parse_data(el) for el in data}
        return self.de_parse_data(data)

    def de_parse_data(self, data):
        if type(data).__name__ == 'str':
            data = self.de_parse_str(data)
            # print('DATA STR: ', data)
        if type(data).__name__ in self.iter_type:
            return self.de_parse_iter(data)
        if type(data).__name__ not in self.iter_type:
            return data

    def de_parse_str(self, data):
        if len(data.split(':')) >= 2:
            type_data = self.oll_type[data.split(':')[0]]
            if type_data == bool and ''.join(data.split(':')[1:]) == 'False':
                data = False
            else:
                data = type_data(''.join(data.split(':')[1:]))
        return data


class BinSerialization(SerializationInterface):
    def serialize(self, file_name, data):
        with open(f'data/{file_name}', 'wb') as file:
            pickle.dump(data, file)

    def deserialize(self, file_name):
        with open(f'data/{file_name}', 'rb') as file:
            return pickle.load(file)


if __name__ == '__main__':
    file_name = 'somedata.json'

    try:
        os.mkdir('data')
    except FileExistsError:
            pass

    if file_name.endswith('json'):
        Serialization = JSONSerialization
    else:
        Serialization = BinSerialization

    try:
        Serialization().serialize(file_name, data)
    except KeyError as e:
        print(e)
    except TypeError as e:
        print(e)
    else:
        deserialized_data = Serialization().deserialize(file_name)
        print('Data source: ', data)
        print('Data deserialized: ', deserialized_data)
        print('Data source == Data deserialized: ', data == deserialized_data)