from pathlib import Path

import pytest

from advice_type import AdviceType
from fix_advice import FixAdvice, parse_lines

build_health_report = Path('build') / 'reports' / 'dependency-analysis' / 'build-health-report.txt'


@pytest.fixture
def simple_project_root(tmp_path: Path) -> Path:
    project_dir = tmp_path / 'some' / 'project'
    project_build_gradle_kts = project_dir / 'build.gradle.kts'

    project_build_gradle_kts.parent.mkdir(parents=True)
    project_build_gradle_kts.write_text('''
// Comment
dependencies {
    api(project(":common"))
}
    '''.strip())

    build_report_txt = tmp_path / build_health_report
    build_report_txt.parent.mkdir(parents=True)

    build_report_txt.write_text('''
    Advice for :some:project
    Unused dependencies which should be removed:
        api(project(":common"))
        
    These transitive dependencies should be declared directly:
        testImplementation(project(":common"))
    ''')

    return tmp_path


def test_init(simple_project_root: Path):
    gradle_root = simple_project_root
    project_name = ':some:project'
    advice_type = AdviceType.REMOVE_UNUSED
    advice = 'testImplementation(project(":common"))'
    fix_advice = FixAdvice(gradle_root, project_name, advice_type, advice)
    assert fix_advice.project_name == project_name
    assert fix_advice.build_file == gradle_root / 'some' / 'project' / 'build.gradle.kts'
    assert fix_advice.advice_type == advice_type
    assert fix_advice.original_advice == advice
    assert fix_advice.existing_gradle_line == advice


def test_to_error_format(simple_project_root: Path):
    with (simple_project_root / build_health_report).open() as f:
        fixes = list(parse_lines(simple_project_root, iter(f.readlines())))

    assert len(fixes) == 2

    assert fixes[0].to_errorformat() == \
           f'{simple_project_root}/some/project/build.gradle.kts:3:4: Remove unused dependency: api(project(":common"))'

    assert fixes[1].to_errorformat() == \
           f'{simple_project_root}/some/project/build.gradle.kts:2:0: Add transitive dependency: ' \
           'testImplementation(project(":common"))'
