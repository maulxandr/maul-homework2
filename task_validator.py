from abc import ABCMeta, abstractmethod
from datetime import datetime



class ValidatorException(Exception):
    pass


class Validator(metaclass=ABCMeta):
    validators = {}

    @abstractmethod
    def validate(self):
        pass

    @classmethod
    def add_type(cls, name, validator):
        if not name:
            raise ValidatorException('Validator must have a name!')

        if not issubclass(validator, cls):
            raise ValidatorException(
                'Class "{}" is not Validator!'.format(validator))
        cls.validators[name] = validator

    @classmethod
    def get_instance(cls, name):
        validator = cls.validators.get(name)

        if validator is None:
            raise ValidatorException(
                'Validator with name "{}" not found'.format(name))

        return validator


class EMailValidator(Validator):

    def validate(email):
        if '@' in email:
            return True
        else:
            return False




class DateTimeValidator(Validator):
    validators = [
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d %H:%M:%S',
        '%d.%m.%Y',
        '%d.%m.%Y %H:%M',
        '%d.%m.%Y %H:%M:%S',
        '%d/%m/%Y',
        '%d/%m/%Y %H:%M',
        '%d/%m/%Y %H:%M:%S',
    ]

    @classmethod
    def validate(cls, value):
        for validator in cls.validators:

                try:
                    datetime.strptime(value, validator)
                    return True

                except ValueError:
                    continue

        return False

