#!/usr/bin/python3
"""Defines the unittests for the console.py module"""
import os
import unittest
from io import StringIO
from unittest.mock import patch
from models.__init__ import storage
from console import HBNBCommand, error_messages, classes


class TestConsoleExitOp(unittest.TestCase):
    """Testing the exit methods of the console."""

    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd("quit")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "")

    def test_EOF(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd("EOF")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "\n")


class TestBaseModel(unittest.TestCase):
    """Testing the BaseModel"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.c_name = "BaseModel"

    @classmethod
    def tearDown(cls):
        if os.path.exists("hbnb.json"):
            os.remove("hbnb.json")

    def test_create(self):
        """Test the create method using the <method> <class> formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"create {self.c_name}")
        output = mock_stdout.getvalue().strip()
        self.assertIsInstance(output, str)
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self.c_name}.{output}", storage.all().keys())

    def test_create_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_create_with_params(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"create {self.c_name} name=\"X\"")
        output = mock_stdout.getvalue().strip()
        obj = classes[self.c_name]()
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "X")
        self.assertEqual(output, obj.id)

    def test_show(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.c_name} {obj.id}")
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.c_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.c_name} {obj.id} name \"x\""
            self.console.onecmd(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "x")

    def test_update_with_extra_attrs(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.c_name} {obj.id} age \"20\" name \"x\""
            self.console.onecmd(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")
        self.assertEqual(obj.__dict__["name"], "x")

    def test_update_with_dict(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.c_name} {obj.id} {{\"email\": \"x@g.c\"}}"
            self.console.onecmd(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "x@g.c")

    def test_update_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.c_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.c_name} 123 age 20")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.c_name} {obj.id} ''")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.c_name} {obj.id} name")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"count {self.c_name}")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) is classes[self.c_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"destroy {self.c_name} {obj.id}")
        self.assertNotIn(f"{self.c_name}.{obj.id}", storage.all().keys())

    def test_destroy_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.c_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.c_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestBaseModelDotNotation(unittest.TestCase):
    """Testing with the method.notation formate"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.c_name = "BaseModel"

    @classmethod
    def tearDown(cls):
        if os.path.exists("hbnb.json"):
            os.remove("hbnb.json")

    def test_invalid_method(self):
        """Test invalid method output message"""
        method_name = "invalid_method_name"
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(
                self.console.precmd(f"{self.c_name}.{method_name}()")
            )
        output = mock_stdout.getvalue().strip()
        self.assertEqual(
            output, f'{error_messages["no_method"]}: {method_name} **'
        )

    def test_create(self):
        """Test the create method using the <class>.<method>() formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"{self.c_name}.create()"))
        output = mock_stdout.getvalue().strip()
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self.c_name}.{output}", storage.all().keys())

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd("base.create()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(
                self.console.precmd(f"{self.c_name}.show({obj.id})")
            )
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd("base.show()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"{self.c_name}.show()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"{self.c_name}.show(123)"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.c_name}.update({obj.id}, name \"x\")"
            self.console.onecmd(self.console.precmd(cmd))
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "x")

    def test_update_with_extra_attrs(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.c_name}.update({obj.id}, age \"20\", name \"x\")"
            self.console.onecmd(self.console.precmd(cmd))
        self.assertIn("age", obj.__dict__.keys())
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")
        self.assertEqual(obj.__dict__["name"], "x")

    def test_update_with_dict(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.c_name}.update({obj.id}, {{\"email\": \"x@g.c\"}})"
            self.console.onecmd(self.console.precmd(cmd))
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "x@g.c")

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"base.update()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"{self.c_name}.update()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(
                self.console.precmd(f"{self.c_name}.update(123, age 20)")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(
                self.console.precmd(f"{self.c_name}.update({obj.id}, '')")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(
                self.console.precmd(f"{self.c_name}.update({obj.id}, age)")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"{self.c_name}.count()"))
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) is classes[self.c_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.c_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(
                self.console.precmd(f"{self.c_name}.destroy({obj.id})")
            )
        self.assertNotIn(f"{self.c_name}.{obj.id}", storage.all().keys())

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"base.destroy()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"{self.c_name}.destroy()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(
                self.console.precmd(f"{self.c_name}.destroy(123)")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
