import unittest
import xmlrunner
import responses
from discourse import generate_discourse_report_url


class DiscourseFetchTestCase(unittest.TestCase):
    """Tests for Discourse fetch functions"""

    @responses.activate
    def test_can_generate_discourse_report_url(self):
        """Can generate a report url query"""

        responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                      json={'error': 'not found'}, status=404)

        self.assertEqual(generate_discourse_report_url(
            'foo', 'bar', '2019-02-01', '2019-02-07', 'fred', 'hunter2'), 'foo/admin/reports/bar.json?end_date=2019-02-07&start_date=2019-02-01&api_key=hunter2&api_username=fred')


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports/junit'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)
