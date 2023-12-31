from enum import Enum
from typing import Optional


class AdviceType(Enum):
    """Defines advice types for actions"""

    REMOVE_UNUSED = 1
    ADD_TRANSITIVE_DEPENDENCY = 2
    MODIFY_DEPENDENCY = 3
    REMOVE_OR_CHANGE_TO_RUNTIME_ONLY = 4
    CHANGE_TO_COMPILE_ONLY = 5
    REMOVE_ANNOTATION_PROCESSOR = 6
    REMOVE_GRADLE_PLUGIN = 7

    def advice(self, advice: str) -> str:
        if self == AdviceType.REMOVE_UNUSED:
            return f"Remove unused dependency: {advice}"
        elif self == AdviceType.ADD_TRANSITIVE_DEPENDENCY:
            return f"Add transitive dependency: {advice}"
        elif self == AdviceType.MODIFY_DEPENDENCY:
            return f"Modify existing dependency: {advice}"
        elif self == AdviceType.REMOVE_OR_CHANGE_TO_RUNTIME_ONLY:
            return f"Remove or change to runtime-only dependency: {advice}"
        elif self == AdviceType.CHANGE_TO_COMPILE_ONLY:
            return f"Remove or change to compile-only dependency: {advice}"
        elif self == AdviceType.REMOVE_ANNOTATION_PROCESSOR:
            return f"Remove annotation processor: {advice}"
        elif self == AdviceType.REMOVE_GRADLE_PLUGIN:
            return f"Remove gradle plugin: {advice}"
        else:
            raise ValueError(f"Unknown advice type: {self}")

    def parse_existing_gradle_line(self, advice: str) -> str:
        """
        Parse the existing gradle line from the advice
        """

        def extract_was() -> str:
            #   implementation(project(":common:common-guice")) (was api)
            new_advice = advice.split(" ")[0]
            opening_parenthesis_index = new_advice.index("(")
            content = new_advice[opening_parenthesis_index + 1 : -1]
            original_configuration = advice.split("was ")[1][:-1]
            return f"{original_configuration}({content})"

        if self == AdviceType.REMOVE_UNUSED:
            return advice
        elif self == AdviceType.ADD_TRANSITIVE_DEPENDENCY:
            return "dependencies {"
        elif self == AdviceType.MODIFY_DEPENDENCY:
            return extract_was()
        elif self == AdviceType.REMOVE_OR_CHANGE_TO_RUNTIME_ONLY:
            return extract_was()
        elif self == AdviceType.CHANGE_TO_COMPILE_ONLY:
            return extract_was()
        elif self == AdviceType.REMOVE_ANNOTATION_PROCESSOR:
            return advice
        elif self == AdviceType.REMOVE_GRADLE_PLUGIN:
            return advice.split(" ")[0].strip(":")
        else:
            raise ValueError(f"Unknown advice type: {self}")


def parse_advice_type(line: str) -> Optional[AdviceType]:
    if line == "Unused dependencies which should be removed:":
        return AdviceType.REMOVE_UNUSED
    elif line == "These transitive dependencies should be declared directly:":
        return AdviceType.ADD_TRANSITIVE_DEPENDENCY
    elif line == "Existing dependencies which should be modified to be as indicated:":
        return AdviceType.MODIFY_DEPENDENCY
    elif line == "Dependencies which should be removed or changed to runtime-only:":
        return AdviceType.REMOVE_OR_CHANGE_TO_RUNTIME_ONLY
    elif line == "Dependencies which could be compile-only:":
        return AdviceType.CHANGE_TO_COMPILE_ONLY
    elif line == "Unused annotation processors that should be removed:":
        return AdviceType.REMOVE_ANNOTATION_PROCESSOR
    elif line == "Unused plugins that can be removed:":
        return AdviceType.REMOVE_GRADLE_PLUGIN
    else:
        return None
