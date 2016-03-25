import json

from coalib.bearlib.abstractions.Linter import Linter
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@Linter(executable='hlint',
        provides_correction=True,
        severity_map={"Error": RESULT_SEVERITY.MAJOR,
                      "Warning": RESULT_SEVERITY.NORMAL,
                      "Suggestion": RESULT_SEVERITY.INFO})
class HaskellLintBear:
    """
    Checks the given file with hlint.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--json', filename

    def _process_output(self, output, filename, file):
        output = json.loads("".join(output))

        for issue in output:
            assert issue["startLine"] == issue["endLine"]
            diff = Diff(file)
            line_nr = issue["startLine"]
            line_to_change = file[line_nr-1]
            newline = line_to_change.replace(issue["from"], issue["to"])
            diff.change_line(line_nr, line_to_change, newline)

            yield Result.from_values(
                origin=self,
                message=issue["hint"],
                file=filename,
                severity=self.severity_map[issue["severity"]],
                line=issue["startLine"],
                diffs={filename: diff})
