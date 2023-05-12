import os
import unittest
import xml.dom.minidom

from junit_conversor import _parse, _convert


current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.join(current_dir, os.pardir)
output_dir = os.path.join(current_dir, 'output')
example_files_dir = os.path.join(current_dir, 'mend_example_results')
failed_mend = os.path.join(example_files_dir, 'failed_mend.json')
failed_mend_with_invalid_lines = os.path.join(
    example_files_dir, 'failed_mend_with_invalid_lines.json')
valid_mend = os.path.join(example_files_dir, 'valid_mend.json')

junit_conversor_cli = os.path.join(
    current_dir, os.pardir, 'bin', 'junit_conversor')


class TestCase(unittest.TestCase):
    def assertXmlIsValid(self, xml_file):
        try:
            with open(xml_file) as f:
                content = f.read()

            xml.dom.minidom.parseString(content)
        except xml.parsers.expat.ExpatError:
            raise Exception('The specified file is not a valid XML (%s)'
                            % content[0:30])

    def assertFileExist(self, file_name):
        self.assertTrue(os.path.exists(file_name),
                        'File %s does not exist' % file_name)

    def assertFileDoesNotExist(self, file_name):
        self.assertFalse(os.path.exists(file_name),
                         'File %s exist' % file_name)


class ParseTest(TestCase):
    def test_should_parse_a_mend_file_with_errors(self):
        parsed = _parse(failed_mend)

        self.assertEqual(parsed, {
            'py-1.11.0-py2.py3-none-any.whl:CVE-2022-42969': [
                {'name': 'py-1.11.0-py2.py3-none-any.whl:CVE-2022-42969', 'file': 'py-1.11.0-py2.py3-none-any.whl', 'code': 'CVE', 'severity': 'HIGH', 'score': 7.5, 'detail': 'The py library through 1.11.0 for Python allows remote attackers to conduct a ReDoS (Regular expression Denial of Service) attack via a Subversion repository with crafted info data, because the InfoSvnCommand argument is mishandled.'}]
        })

    def test_should_return_an_empty_dict_when_parsing_a_mend_success_file(self):
        self.assertEqual({}, _parse(valid_mend))

    def test_should_skip_invalid_lines(self):
        parsed = _parse(failed_mend_with_invalid_lines)

        self.assertEqual(parsed, {
            'py-1.11.0-py2.py3-none-any.whl:CVE-2022-42969': [
                {'name': 'py-1.11.0-py2.py3-none-any.whl:CVE-2022-42969', 'file': 'py-1.11.0-py2.py3-none-any.whl', 'code': 'CVE', 'severity': 'HIGH', 'score': 7.5, 'detail': 'The py library through 1.11.0 for Python allows remote attackers to conduct a ReDoS (Regular expression Denial of Service) attack via a Subversion repository with crafted info data, because the InfoSvnCommand argument is mishandled.'}]
        })


class ConvertTest(TestCase):
    def setUp(self):
        self.destination = os.path.join(output_dir, 'junit.xml')

        try:
            os.remove(self.destination)
        except OSError:
            pass

    def test_should_convert_a_file_with_mend_errors_to_junit_xml(self):
        _convert(failed_mend, self.destination)

        self.assertFileExist(self.destination)
        self.assertXmlIsValid(self.destination)

    def test_should_create_a_file_even_when_there_are_no_errors(self):
        _convert(valid_mend, self.destination)
        self.assertFileExist(self.destination)
