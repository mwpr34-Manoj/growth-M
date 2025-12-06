# GitHub Actions Interview Questions & Answers

## 🚀 **GitHub Actions Fundamentals**

### 1. What is GitHub Actions and how does it work?

**Answer:**
GitHub Actions is a CI/CD platform integrated directly into GitHub that allows you to automate workflows for building, testing, and deploying code. It's event-driven and runs workflows in response to GitHub events like pushes, pull requests, or scheduled triggers.

**Key Components:**
- **Workflows**: Automated processes defined in YAML files (`.github/workflows/`)
- **Events**: Triggers that start workflows (push, pull_request, schedule, etc.)
- **Jobs**: Sets of steps that run on the same runner
- **Steps**: Individual tasks that run commands or actions
- **Actions**: Reusable units of code (can be JavaScript or Docker containers)
- **Runners**: Virtual machines that execute workflows (GitHub-hosted or self-hosted)

---

### 2. What is the structure of a GitHub Actions workflow file?

**Answer:**
A workflow file is a YAML file located in `.github/workflows/` directory.

**Basic Structure:**
```yaml
name: CI/CD Pipeline

# When to trigger the workflow
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:  # Manual trigger

# Environment variables
env:
  NODE_VERSION: '18'
  REGISTRY: ghcr.io

# Jobs
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
      - name: Install dependencies
        run: npm install
      - name: Build
        run: npm run build
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/
```

---

### 3. What are the different types of triggers in GitHub Actions?

**Answer:**
GitHub Actions supports multiple trigger types:

**1. Push Events:**
```yaml
on:
  push:
    branches:
      - main
      - 'releases/**'
    tags:
      - 'v*'
    paths:
      - 'src/**'
      - 'package.json'
```

**2. Pull Request Events:**
```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - main
```

**3. Scheduled Events (Cron):**
```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily
    - cron: '0 */6 * * *'  # Every 6 hours
```

**4. Workflow Dispatch (Manual):**
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        type: choice
        options:
          - staging
          - production
```

**5. Repository Events:**
```yaml
on:
  repository_dispatch:
    types: [deploy]
  issues:
    types: [opened, labeled]
  release:
    types: [published]
```

**6. Webhook Events:**
```yaml
on:
  watch:
    types: [started]
```

---

### 4. What are GitHub Actions and how do you create custom actions?

**Answer:**
Actions are reusable units of code that can be used in workflows. They can be:
- **JavaScript Actions**: Run directly on the runner
- **Docker Actions**: Run in Docker containers
- **Composite Actions**: Combine multiple steps

**Creating a JavaScript Action:**
```yaml
# action.yml
name: 'Hello World'
description: 'Greet someone'
inputs:
  who-to-greet:
    description: 'Who to greet'
    required: true
    default: 'World'
outputs:
  time:
    description: 'The time we greeted you'
runs:
  using: 'node20'
  main: 'index.js'
```

```javascript
// index.js
const core = require('@actions/core');
const github = require('@actions/github');

const nameToGreet = core.getInput('who-to-greet');
console.log(`Hello ${nameToGreet}!`);

const time = new Date().toTimeString();
core.setOutput('time', time);
```

**Using the Action:**
```yaml
- name: Greet
  uses: ./.github/actions/hello-world
  with:
    who-to-greet: 'GitHub Actions'
```

---

### 5. How do you use secrets in GitHub Actions?

**Answer:**
Secrets are encrypted environment variables stored in GitHub repository settings.

**Setting Secrets:**
1. Go to Repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value

**Using Secrets:**
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          echo "Deploying with secrets"
          ./deploy.sh
```

**Best Practices:**
- Never log secrets: Use `::add-mask::` if needed
- Use organization secrets for shared secrets
- Use environment secrets for environment-specific values
- Rotate secrets regularly
- Use least privilege principle

---

### 6. How do you implement matrix builds in GitHub Actions?

**Answer:**
Matrix strategy allows running jobs across multiple configurations.

**Example:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [14, 16, 18, 20]
        os: [ubuntu-latest, windows-latest, macos-latest]
        include:
          - node-version: 18
            os: ubuntu-latest
            test-group: integration
        exclude:
          - node-version: 14
            os: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - name: Run tests
        run: npm test
        env:
          TEST_GROUP: ${{ matrix.test-group }}
```

**Matrix Features:**
- **include**: Add additional combinations**
- **exclude**: Remove specific combinations
- **fail-fast**: Stop all jobs if one fails (default: true)

---

### 7. How do you share data between jobs in GitHub Actions?

**Answer:**
Multiple ways to share data between jobs:

**1. Artifacts:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: npm run build
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/
          retention-days: 7

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist
      - name: Deploy
        run: ./deploy.sh
```

**2. Job Outputs:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - id: version
        run: echo "version=v1.0.0" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Use version
        run: echo "Deploying ${{ needs.build.outputs.version }}"
```

**3. Environment Variables:**
```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - name: Set output
        run: echo "VERSION=1.0.0" >> $GITHUB_ENV

  job2:
    needs: job1
    runs-on: ubuntu-latest
    steps:
      - name: Use env
        run: echo $VERSION
```

---

### 8. How do you implement conditional execution in GitHub Actions?

**Answer:**
Use `if` conditions to control step and job execution.

**Step-level Conditions:**
```yaml
steps:
  - name: Build
    if: github.ref == 'refs/heads/main'
    run: npm run build

  - name: Deploy
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    run: ./deploy.sh

  - name: Notify on failure
    if: failure()
    run: ./notify.sh

  - name: Always run
    if: always()
    run: ./cleanup.sh
```

**Job-level Conditions:**
```yaml
jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh staging

  deploy-production:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh production
```

**Context Functions:**
- `success()`: Previous step succeeded
- `failure()`: Previous step failed
- `cancelled()`: Workflow was cancelled
- `always()`: Always run

---

### 9. How do you use self-hosted runners in GitHub Actions?

**Answer:**
Self-hosted runners allow running workflows on your own infrastructure.

**Setting Up Self-hosted Runner:**
```bash
# Download runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure
./config.sh --url https://github.com/OWNER/REPO --token TOKEN

# Install service
sudo ./svc.sh install
sudo ./svc.sh start
```

**Using Self-hosted Runners:**
```yaml
jobs:
  build:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v3
      - run: npm run build
```

**Runner Labels:**
```yaml
jobs:
  build:
    runs-on: [self-hosted, linux, x64, gpu]
    steps:
      - run: npm run build
```

**Best Practices:**
- Use labels to route jobs to specific runners
- Keep runners updated
- Use ephemeral runners for security
- Isolate runners for sensitive workloads

---

### 10. How do you implement deployment strategies with GitHub Actions?

**Answer:**
GitHub Actions supports various deployment strategies:

**1. Blue-Green Deployment:**
```yaml
jobs:
  deploy-blue:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to blue
        run: ./deploy.sh blue

  deploy-green:
    needs: deploy-blue
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to green
        run: ./deploy.sh green
      - name: Switch traffic
        run: ./switch-traffic.sh green
```

**2. Canary Deployment:**
```yaml
jobs:
  deploy-canary:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy canary
        run: kubectl set image deployment/app app=image:v1 --replicas=1

  deploy-full:
    needs: deploy-canary
    if: success()
    runs-on: ubuntu-latest
    steps:
      - name: Deploy full
        run: kubectl set image deployment/app app=image:v1 --replicas=10
```

**3. Rolling Deployment:**
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: |
          kubectl rollout restart deployment/app
          kubectl rollout status deployment/app
```

---

### 11. How do you use environments and protection rules in GitHub Actions?

**Answer:**
Environments provide deployment protection and secrets management.

**Environment Configuration:**
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Deploy
        run: ./deploy.sh
```

**Environment Protection Rules:**
1. **Required Reviewers**: Manual approval required
2. **Wait Timer**: Delay before deployment
3. **Deployment Branches**: Restrict which branches can deploy
4. **Environment Secrets**: Secrets specific to environment

**Using Environment Secrets:**
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
        run: ./deploy.sh
```

---

### 12. How do you implement caching in GitHub Actions?

**Answer:**
Caching speeds up workflows by storing dependencies.

**Node.js Example:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Cache node modules
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
```

**Docker Example:**
```yaml
- name: Cache Docker layers
  uses: docker/build-push-action@v4
  with:
    cache-from: type=registry,ref=myregistry/myapp:buildcache
    cache-to: type=registry,ref=myregistry/myapp:buildcache,mode=max
```

**Cache Best Practices:**
- Use specific cache keys with file hashes
- Set appropriate restore-keys for fallback
- Clear cache when dependencies change
- Use cache scoping (branch, workflow)

---

### 13. How do you handle errors and implement retry logic in GitHub Actions?

**Answer:**
Multiple strategies for error handling:

**1. Continue on Error:**
```yaml
steps:
  - name: Non-critical step
    continue-on-error: true
    run: ./optional-script.sh
```

**2. Retry Logic:**
```yaml
steps:
  - name: Deploy with retry
    uses: nick-invision/retry@v2
    with:
      timeout_minutes: 10
      max_attempts: 3
      command: ./deploy.sh
```

**3. Error Handling:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        id: build
        run: npm run build
      - name: Notify on failure
        if: failure()
        run: ./notify-failure.sh
      - name: Cleanup
        if: always()
        run: ./cleanup.sh
```

**4. Job-level Error Handling:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  notify:
    needs: build
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - run: ./notify.sh
```

---

### 14. How do you implement reusable workflows in GitHub Actions?

**Answer:**
Reusable workflows allow sharing workflow logic across repositories.

**Creating Reusable Workflow:**
```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      version:
        required: false
        type: string
    secrets:
      DEPLOY_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: |
          echo "Deploying version ${{ inputs.version }} to ${{ inputs.environment }}"
          ./deploy.sh
```

**Using Reusable Workflow:**
```yaml
name: Deploy Application

on:
  push:
    branches: [main]

jobs:
  call-deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
      version: ${{ github.sha }}
    secrets:
      DEPLOY_KEY: ${{ secrets.PRODUCTION_DEPLOY_KEY }}
```

---

### 15. How do you optimize GitHub Actions workflows for performance?

**Answer:**
**Optimization Strategies:**

1. **Use Caching:**
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

2. **Parallel Jobs:**
```yaml
jobs:
  test-unit:
    runs-on: ubuntu-latest
    steps: ...
  test-integration:
    runs-on: ubuntu-latest
    steps: ...
```

3. **Matrix Strategy:**
```yaml
strategy:
  matrix:
    node-version: [16, 18, 20]
  fail-fast: false
```

4. **Conditional Execution:**
```yaml
if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

5. **Use Appropriate Runners:**
```yaml
runs-on: ubuntu-latest  # Faster than windows/macos
```

6. **Optimize Docker Images:**
```yaml
- uses: docker/build-push-action@v4
  with:
    cache-from: type=registry,ref=...
```

7. **Artifact Management:**
```yaml
- uses: actions/upload-artifact@v3
  with:
    retention-days: 1  # Shorter retention
```

---

## 🎯 **Advanced Topics**

### 16. How do you implement security scanning in GitHub Actions?

**Answer:**
GitHub provides built-in security features and supports third-party tools:

**1. GitHub Advanced Security:**
```yaml
on:
  push:
    branches: [main]
  pull_request:

jobs:
  security:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      actions: read
      contents: read
    steps:
      - uses: actions/checkout@v3
      - name: Run CodeQL Analysis
        uses: github/codeql-action/analyze@v2
```

**2. Third-party Security Tools:**
```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    scan-ref: '.'
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload Trivy results
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

---

### 17. How do you implement notifications in GitHub Actions?

**Answer:**
Multiple notification options:

**1. GitHub Notifications:**
```yaml
- name: Create issue on failure
  if: failure()
  uses: actions/github-script@v6
  with:
    script: |
      github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: 'Workflow failed',
        body: 'The workflow failed. Please check the logs.'
      })
```

**2. Slack Notifications:**
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Deployment completed'
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

**3. Email Notifications:**
```yaml
- name: Send email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: 'Deployment Status'
    to: team@example.com
    body: 'Deployment completed successfully'
```

---

## 📝 **Best Practices**

1. **Use versioned actions**: Always pin action versions (e.g., `@v3`)
2. **Minimize permissions**: Use least privilege for tokens and secrets
3. **Cache dependencies**: Speed up workflows with caching
4. **Use matrix for multiple configurations**: Efficient parallel execution
5. **Implement proper error handling**: Use `if: failure()` and `continue-on-error`
6. **Keep workflows DRY**: Use reusable workflows and composite actions
7. **Optimize for cost**: Use appropriate runners, cache effectively
8. **Security scanning**: Enable Dependabot and security scanning
9. **Document workflows**: Add comments explaining complex logic
10. **Monitor workflow performance**: Track duration and optimize slow steps

---

**Good luck with your GitHub Actions interview preparation!**
