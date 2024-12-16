import unittest
import io
from unittest.mock import patch
from secretary import check_document_existance, documents, directories, get_doc_owner_name, \
    get_all_doc_owners_names, remove_doc_from_shelf, add_new_shelf, append_doc_to_shelf, delete_doc, get_doc_shelf, \
    move_doc_to_shelf, show_document_info, show_all_docs_info, add_new_doc


class TestFunctionCheck(unittest.TestCase):

    def setUp(self):
        global documents
        documents.clear()
        documents.append({"type": "passport", "number": "12345", "name": "Иванов Иван"})

    def test_document_exists(self):
        self.assertTrue(check_document_existance("12345"))

    def test_document_does_not_exist(self):
        self.assertFalse(check_document_existance("11111"))


class TestFunctionGet(unittest.TestCase):

    def setUp(self):
        global documents
        documents.clear()
        documents.append({"type": "passport", "number": "12345", "name": "Иванов Иван"})

    @patch('builtins.input', return_value='12345')
    def test_get_doc_owner_name(self, mock_input):
        self.assertEqual(get_doc_owner_name(), 'Иванов Иван')

    @patch('builtins.input', return_value='9999999')
    def test_get_doc_owner_name_none(self, mock_input):
        self.assertIsNone(get_doc_owner_name())


class TestFunctionGetAll(unittest.TestCase):

    def setUp(self):
        global documents
        documents.clear()
        documents.append({"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"})
        documents.append({"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"})
        documents.append({"type": "insurance", "number": "10006", "name": "Аристарх Павлов"})
        documents.append({"type": "passport", "number": "9999"})

    def test_get_all_doc_owners_names(self):
        self.assertEqual(get_all_doc_owners_names(), {'Аристарх Павлов', 'Геннадий Покемонов', 'Василий Гупкин'})

    def test_empty_documents(self):
        documents.clear()
        result = get_all_doc_owners_names()
        self.assertEqual(result, set())


class TestFunctionRemoveDoc(unittest.TestCase):

    def setUp(self):
        global directories
        directories.clear()
        directories.update({'1': ['2207 876234', '11-2', '5455 028765']})

    def test_remove_doc_from_shelf(self):
        remove_doc_from_shelf('11-2')
        self.assertNotIn('11-2', directories['1'])


class TestFunctionAddNewShelf(unittest.TestCase):

    def setUp(self):
        global directories
        directories.clear()
        directories.update({'4': ['12345']})

    def _assert_shelf(self, shelf_number, expected_created, expected_directories):
        shelf_number_result, created = add_new_shelf(shelf_number)
        self.assertEqual(shelf_number_result, shelf_number)
        self.assertEqual(created, expected_created)
        self.assertEqual(directories, expected_directories)

    def test_add_new_shelf_with_number(self):
        self._assert_shelf('1', True, {'1': [], '4': ['12345']})

    def test_add_existing_shelf(self):
        self._assert_shelf('4', False, {'4': ['12345']})

    @patch('builtins.input', return_value='2')
    def test_add_new_shelf_with_input(self, mock_input):
        self._assert_shelf('2', True, {'2': [], '4': ['12345']})

    @patch('builtins.input', return_value='')
    def test_add_new_shelf_empty_input(self, mock_input):
        self._assert_shelf('', True, {'': [], '4': ['12345']})


class TestFunctionAppendDocShelf(unittest.TestCase):

    def setUp(self):
        global directories
        directories.clear()

    def test_append_doc_to_shelf(self):
        append_doc_to_shelf('777777', '1')
        self.assertIn('777777', directories['1'])


class TestFunctionDeleteDoc(unittest.TestCase):

    def setUp(self):
        global documents, directories
        directories.clear()
        documents.clear()
        documents.append({"type": "invoice", "number": "11-2", "name": "Геннадий"})
        directories.update({'1': ['11-2']})

    def _assert_doc(self, doc_number, expected_deleted, expected_directories, expected_documents):
        doc_number_result, deleted = delete_doc()
        self.assertEqual(doc_number_result, doc_number)
        self.assertEqual(deleted, expected_deleted)
        self.assertEqual(directories, expected_directories)
        self.assertEqual(documents, expected_documents)

    @patch('builtins.input', return_value='11-2')
    def test_delete_doc(self, mock_input):
        self._assert_doc('11-2', True, {'1': []}, [])

    @patch('builtins.input', return_value='99999')
    def test_delete_doc_none(self, mock_input):
        self._assert_doc(None, False, {'1': ['11-2']}, [{"type": "invoice", "number": "11-2", "name": "Геннадий"}])


class TestFunctionGetDocShelf(unittest.TestCase):

    def setUp(self):
        global documents, directories
        directories.clear()
        documents.clear()
        documents.append({"type": "invoice", "number": "11-2", "name": "Геннадий"})
        directories.update({'1': ['11-2']})

    @patch('builtins.input', return_value='11-2')
    def test_get_doc_shelf(self, mock_input):
        self.assertEqual(get_doc_shelf(), '1')

    @patch('builtins.input', return_value='99999')
    def test_get_doc_shelf_none(self, mock_input):
        self.assertIsNone(get_doc_shelf())


class TestFunctionMoveDoc(unittest.TestCase):

    def setUp(self):
        global documents, directories
        directories.clear()
        documents.clear()
        documents.append({"type": "invoice", "number": "11-2", "name": "Геннадий"})
        directories.update({'1': ['11-2']})

    @patch('builtins.input', side_effect=['11-2', '2'])
    def test_move_doc_to_shelf(self, mock_input):
        move_doc_to_shelf()
        self.assertNotIn('11-2', directories['1'])
        self.assertIn('11-2', directories['2'])

    @patch('builtins.input', side_effect=['11', '2'])
    def test_move_doc_to_shelf_none(self, mock_input):
        self.assertIsNone(move_doc_to_shelf())


class TestFunctionShowDoc(unittest.TestCase):

    @patch('builtins.print')
    def test_show_document_info(self, mock_print):
        document = {
            'type': 'passport',
            'number': '123456',
            'name': 'Вася'
        }

        show_document_info(document)
        mock_print.assert_called_once_with('passport "123456" "Вася"')


class TestFunctionShowAllDoc(unittest.TestCase):

    def setUp(self):
        global documents
        documents.clear()
        documents.append({"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"})
        documents.append({"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"})
        documents.append({"type": "insurance", "number": "10006", "name": "Аристарх Павлов"})

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_show_all_docs_info(self, mock_stdout):
        show_all_docs_info()
        output = mock_stdout.getvalue()
        expected_output = ('Список всех документов:\n'
                           '\n'
                           'passport "2207 876234" "Василий Гупкин"\n'
                           'invoice "11-2" "Геннадий Покемонов"\n'
                           'insurance "10006" "Аристарх Павлов"\n')

        self.assertEqual(output, expected_output)


class TestFunctionAddNewDoc(unittest.TestCase):

    def setUp(self):
        global documents, directories
        documents.clear()
        directories.clear()

    def _add_new_doc(self, input_values, expected_shelf_number, expected_documents, expected_directories):
        with patch('builtins.input', side_effect=input_values):
            result = add_new_doc()
            self.assertEqual(result, expected_shelf_number)
            self.assertEqual(documents, expected_documents)
            self.assertEqual(directories, expected_directories)

    def test_add_new_doc_with_valid_input(self):
        input_values = ['123', 'passport', 'Вася', '2']
        expected_shelf_number = '2'
        expected_documents = [{'type': 'passport', 'number': '123', 'name': 'Вася'}]
        expected_directories = {'2': ['123']}
        self._add_new_doc(input_values, expected_shelf_number, expected_documents, expected_directories)


if __name__ == '__main__':
    unittest.main()
