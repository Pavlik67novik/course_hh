import unittest
from unittest.mock import patch
from io import StringIO
from src.source import HeadHunterAPI, Vacancy, JSONSaver, user_interaction


class TestHeadHunterAPI(unittest.TestCase):
    @patch('src.source.requests.get')
    def test_get_vacancies_success(self, mock_get):
        mock_response = {'items': [{'name': 'Software Engineer', 'alternate_url': 'https://example.com', 'salary': '100 000-150 000 руб.', 'description': 'Job description'}]}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        hh_api = HeadHunterAPI()
        vacancies = hh_api.get_vacancies("Software Engineer")

        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]['name'], 'Software Engineer')
        self.assertEqual(vacancies[0]['alternate_url'], 'https://example.com')
        self.assertEqual(vacancies[0]['salary'], '100 000-150 000 руб.')
        self.assertEqual(vacancies[0]['description'], 'Job description')

    @patch('your_module.requests.get')
    def test_get_vacancies_failure(self, mock_get):
        mock_get.return_value.status_code = 404

        hh_api = HeadHunterAPI()
        vacancies = hh_api.get_vacancies("Software Engineer")

        self.assertEqual(len(vacancies), 0)


class TestJSONSaver(unittest.TestCase):
    def test_add_vacancy(self):
        vacancy = Vacancy("Software Engineer", "https://example.com", "100 000-150 000 руб.", "Job description")
        file_path = "test_vacancies.json"

        json_saver = JSONSaver(file_path)
        json_saver.add_vacancy(vacancy)

        with open(file_path, 'r') as file:
            saved_vacancy = file.readlines()[0]
            self.assertIn("Software Engineer", saved_vacancy)
            self.assertIn("https://example.com", saved_vacancy)
            self.assertIn("100 000-150 000 руб.", saved_vacancy)
            self.assertIn("Job description", saved_vacancy)



class TestUserInteraction(unittest.TestCase):
    @patch('builtins.input', side_effect=["Software Engineer", "3", "Python", "100000 - 150000"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_user_interaction(self, mock_stdout, mock_input):
        user_interaction()

        expected_output = "Software Engineer\n"
        self.assertIn(expected_output, mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
