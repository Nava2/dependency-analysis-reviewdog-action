# dependency-analysis-reportdog-action
Provides a @reviewdog/reviewdog check for @autonomousapps/dependency-analysis-gradle-plugin

## Examples

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
        with:
          arguments: buildHealth --continue
          
      - name: Add code review comments
        uses: navatwo/dependency-analysis-reportdog-action@v0
        with:
          reviewdog_github_token: ${{ secrets.GITHUB_TOKEN }}
```
