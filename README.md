# dependency-analysis-reportdog-action
Provides a @reviewdog/reviewdog check for @autonomousapps/dependency-analysis-gradle-plugin


## Examples

### Run action if and only if `./gradlew buildHealth` report is generated

Following running `./gradlew buildHealth`, on failure, `build-health-report.txt` is generated. If
the file exists, run the commenting task.

```yaml
name: Run build health

on: [ pull_request ]

permissions:
  contents: read
  pull-requests: write
  
jobs:
  ci-steps:
    name: Run CI
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        
      - name: Run Build Health
        uses: gradle/gradle-build-action@v2
        id: build-health
        with:
          arguments: buildHealth
          
      - name: "Check buildHealth failed"
        id: build_health_report
        uses: andstor/file-existence-action@v2
        with:
          files: "build/reports/dependency-analysis/build-health-report.txtt"
          
      - name: Add code review comments
        # Only run this if the build-health check fails
        if: ${{ steps.build_health_report.outputs.files_exists == 'true' }}
        uses: navatwo/dependency-analysis-reportdog-action@v0
        with:
          reviewdog_github_token: ${{ secrets.GITHUB_TOKEN }}
          
          # Default: build/reports/dependency-analysis/build-health-report.txt
          build-report-path: build/reports/my-reports/build-health-report.txt
          # Default: buildHealth
          reviewdog-check-name: 'FancyName'
          # Default: github-pr-check
          reviewdog-reporter: github-pr-review
```

### Run action if and only if `./gradlew buildHealth` failed

Following running `./gradlew buildHealth`, add github-checks on the PR with advice to fix.

```yaml
name: Run build health

on: [ pull_request ]

permissions:
  contents: read
  pull-requests: write
  
jobs:
  ci-steps:
    name: Run CI
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        
      - name: Run Build Health
        uses: gradle/gradle-build-action@v2
        id: build-health
        with:
          # If configured to `fail` on buildHealth failure, `--continue` is required.
          arguments: buildHealth
          
      - name: Add code review comments
        # Only run this if the build-health check fails
        if: ${{ steps.build-health.outcome == 'failure' }}
        uses: navatwo/dependency-analysis-reportdog-action@v0
        with:
          reviewdog_github_token: ${{ secrets.GITHUB_TOKEN }}
          
          # Default: build/reports/dependency-analysis/build-health-report.txt
          build-report-path: build/reports/my-reports/build-health-report.txt
          # Default: buildHealth
          reviewdog-check-name: 'FancyName'
          # Default: github-pr-check
          reviewdog-reporter: github-pr-review
```
