import unittest
from discourse import generate_discourse_report_url


class DiscourseFetchTestCase(unittest.TestCase):
    """Tests for Discourse fetch functions"""

    def test_can_generate_discourse_report_url(self):
        """Can generate a report url query"""

        self.assertEqual(generate_discourse_report_url(
            'foo', 'bar', '2019-02-01', '2019-02-07', 'fred', 'hunter2'), 'foo/admin/reports/bar.json?end_date=2019-02-07&start_date=2019-02-01&api_key=hunter2&api_username=fred')


if __name__ == '__main__':
    unittest.main()
