from pathlib import Path

from parse_build_health_report import main
from test_fix_advice import build_health_report, simple_project_root  # noqa: F401


def test_main(
    # noqa: F811 This is used and imported
    simple_project_root: Path,
    tmp_path: Path,
):
    output_file = tmp_path / "output.txt"

    main(
        [
            str(simple_project_root / build_health_report),
            "--output",
            str(output_file),
            "--gradle_root",
            str(simple_project_root),
        ]
    )

    with output_file.open() as f:
        lines = f.readlines()
        assert len(lines) == 2

        assert (
            f"{simple_project_root}/some/project/build.gradle.kts:3:4: "
            'Remove unused dependency: api(project(":common"))\n' in lines
        )
        assert (
            f"{simple_project_root}/some/project/build.gradle.kts:2:0: "
            'Add transitive dependency: testImplementation(project(":common"))\n'
            in lines
        )
