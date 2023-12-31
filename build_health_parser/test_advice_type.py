from advice_type import AdviceType, parse_advice_type


def test_parse_advice_type():
    assert (
        parse_advice_type("Unused dependencies which should be removed:")
        == AdviceType.REMOVE_UNUSED
    )
    assert parse_advice_type("Something else") is None


def test_parse_existing_gradle_line():
    simple_line = 'api(project(":common:common-guice"))'
    change_line = 'testImplementation(project(":common:common-guice")) (was api)'

    assert (
        AdviceType.REMOVE_UNUSED.parse_existing_gradle_line(simple_line) == simple_line
    )
    assert (
        AdviceType.REMOVE_UNUSED.parse_existing_gradle_line(change_line) == change_line
    )

    assert (
        AdviceType.ADD_TRANSITIVE_DEPENDENCY.parse_existing_gradle_line(simple_line)
        == "dependencies {"
    )

    assert (
        AdviceType.MODIFY_DEPENDENCY.parse_existing_gradle_line(change_line)
        == simple_line
    )

    assert (
        AdviceType.REMOVE_OR_CHANGE_TO_RUNTIME_ONLY.parse_existing_gradle_line(
            change_line
        )
        == simple_line
    )

    assert (
        AdviceType.CHANGE_TO_COMPILE_ONLY.parse_existing_gradle_line(change_line)
        == simple_line
    )

    assert (
        AdviceType.REMOVE_ANNOTATION_PROCESSOR.parse_existing_gradle_line(simple_line)
        == simple_line
    )
    assert (
        AdviceType.REMOVE_ANNOTATION_PROCESSOR.parse_existing_gradle_line(change_line)
        == change_line
    )

    assert (
        AdviceType.REMOVE_GRADLE_PLUGIN.parse_existing_gradle_line(
            "org.jetbrains.kotlin.jvm: Unused"
        )
        == "org.jetbrains.kotlin.jvm"
    )
