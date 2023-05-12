import os
import unittest
import xml.dom.minidom

from junit_conversor import _parse, _convert


current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.join(current_dir, os.pardir)
output_dir = os.path.join(current_dir, 'output')
example_files_dir = os.path.join(current_dir, 'yamllint_example_results')
failed_yamllint = os.path.join(example_files_dir, 'failed_yamllint.txt')
failed_yamllint_with_invalid_lines = os.path.join(
    example_files_dir, 'failed_yamllint_with_invalid_lines.txt')
valid_yamllint = os.path.join(example_files_dir, 'valid_yamllint.txt')

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
    def test_should_parse_a_yamllint_file_with_errors(self):
        parsed = _parse(failed_yamllint)

        self.assertEqual(parsed, {
            '.yamllint.yml:1:1': [{
                'name': '.yamllint.yml:1:1', 'file': '.yamllint.yml', 'line': '1', 'col': '1', 'detail': '[warning] missing document start "---" (document-start)', 'code': '[warning] missing document start "---" (document-start)'
            }],
            '.yamllint.yml:1:7': [{
                'name': '.yamllint.yml:1:7', 'file': '.yamllint.yml', 'line': '1', 'col': '7', 'detail': '[error] wrong new line character: expected \\n (new-lines)', 'code': '[error] wrong new line character: expected \\n (new-lines)'
            }],
            '.yamllint.yml:7:32': [{
                'name': '.yamllint.yml:7:32', 'file': '.yamllint.yml', 'line': '7', 'col': '32', 'detail': '[warning] too few spaces before comment (comments)', 'code': '[warning] too few spaces before comment (comments)'
            }],
            '.yamllint.yml:7:81': [{
                'name': '.yamllint.yml:7:81', 'file': '.yamllint.yml', 'line': '7', 'col': '81', 'detail': '[error] line too long (114 > 80 characters) (line-length)', 'code': '[error] line too long (114 > 80 characters) (line-length)'
            }]
        })

    def test_should_return_an_empty_dict_when_parsing_a_yamllint_success_file(self):
        self.assertEqual({}, _parse(valid_yamllint))

    def test_should_skip_invalid_lines(self):
        parsed = _parse(failed_yamllint_with_invalid_lines)

        self.assertEqual(parsed, {
            '.yamllint.yml:1:1': [{
                'name': '.yamllint.yml:1:1', 'file': '.yamllint.yml', 'line': '1', 'col': '1', 'detail': '[warning] missing document start "---" (document-start)', 'code': '[warning] missing document start "---" (document-start)'
            }],
            '.yamllint.yml:7:32': [{
                'name': '.yamllint.yml:7:32', 'file': '.yamllint.yml', 'line': '7', 'col': '32', 'detail': '[warning] too few spaces before comment (comments)', 'code': '[warning] too few spaces before comment (comments)'
            }],
            '.yamllint.yml:7:81': [{
                'name': '.yamllint.yml:7:81', 'file': '.yamllint.yml', 'line': '7', 'col': '81', 'detail': '[error] line too long (114 > 80 characters) (line-length)', 'code': '[error] line too long (114 > 80 characters) (line-length)'
            }]
        })

class ConvertTest(TestCase):
    def setUp(self):
        self.destination = os.path.join(output_dir, 'junit.xml')

        try:
            os.remove(self.destination)
        except OSError:
            pass

    def test_should_convert_a_file_with_yamllint_errors_to_junit_xml(self):
        _convert(failed_yamllint, self.destination)

        self.assertFileExist(self.destination)
        self.assertXmlIsValid(self.destination)

    def test_should_create_a_file_even_when_there_are_no_errors(self):
        _convert(valid_yamllint, self.destination)
        self.assertFileExist(self.destination)
