import unittest
from unittest.mock import MagicMock
from models import PersonCreate, PersonUpdate, BookCreate, BookUpdate, RatingCreate
import usecases


class TestCRUD(unittest.TestCase):

    def setUp(self):
        usecases.g = MagicMock()

    def test_create_person(self):
        person = PersonCreate(name="John Doe")
        createdPerson = usecases.create_person(person)
        assert createdPerson.name == "John Doe"


if __name__ == "__main__":
    unittest.main()
