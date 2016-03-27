from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='csslint',
        output_format='regex',
        output_regex=r'(?P<file_name>.+):\s* (?:line (?P<line>\d+), '
                     r'col (?P<col>\d+), )?(?P<severity>Error|Warning) - '
                     r'(?P<message>.*)')
class CSSLintBear:
    """
    Checks the code with ``csslint``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--format=compact', filename
