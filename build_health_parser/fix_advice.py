from pathlib import Path
from typing import Iterator
from advice_type import AdviceType, parse_advice_type


class FixAdvice:
    """
    Defines advice read from a build-health-report.txt file.
    """

    def __init__(
        self, gradle_root: Path, project_name: str, advice_type: AdviceType, advice: str
    ):
        self.project_name = project_name
        self.build_file = FixAdvice._get_build_file(gradle_root, project_name)
        self.advice_type = advice_type
        self.original_advice = advice
        self.existing_gradle_line = advice_type.parse_existing_gradle_line(advice)

    def to_errorformat(self) -> str:
        """
        Return the line with a comment added
        """

        found = False
        dependencies_line_number = 0
        with self.build_file.open() as f:
            for line_number, line in enumerate(f.readlines()):
                if line.strip() == "dependencies {":
                    dependencies_line_number = line_number
                    dependencies_line = line
                if self.existing_gradle_line in line:
                    found = True
                    break

        replace_text = self.existing_gradle_line
        if not found:
            line_number = dependencies_line_number
            replace_text = "dependencies {"
            line = dependencies_line

        # print(f'Line number: {line_number}, line: \'{replace_text.rstrip()}\'')
        line_number += 1

        line_index = line.index(replace_text)

        message = self.advice_type.advice(self.original_advice)
        return f"{self.build_file}:{line_number}:{line_index}: {message}"

    @staticmethod
    def _get_build_file(gradle_root: Path, project_gradle_path: str) -> Path:
        """
        Get the build file for the given project name
        :param gradle_root:
        :param project_gradle_path:
        :return:
        """
        project_path = project_gradle_path.strip(":").replace(":", "/")
        return gradle_root / project_path / "build.gradle.kts"


def parse_lines(gradle_root: Path, lines: Iterator[str]) -> Iterator[FixAdvice]:
    """
    Parse build health report lines into FixAdvice
    :param lines:
    :return:
    """

    striped_lines = filter(lambda x: x, map(lambda x: x.strip(), lines))

    project_name = "NONE"
    advice = None

    for line in striped_lines:
        if line.startswith("Advice for"):
            project_name = line.split(" ")[2]
            advice = "NONE"
        else:
            parsed_advice_type = parse_advice_type(line)
            if parsed_advice_type:
                advice = parsed_advice_type
            else:
                yield FixAdvice(gradle_root, project_name, advice, line)
