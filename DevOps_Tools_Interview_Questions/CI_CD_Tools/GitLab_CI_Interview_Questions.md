# GitLab CI/CD Interview Questions & Answers

## 🚀 **GitLab CI/CD Fundamentals**

### 1. What is GitLab CI/CD and how does it differ from Jenkins?

**Answer:**
GitLab CI/CD is a built-in continuous integration and continuous deployment tool that's integrated directly into GitLab. Unlike Jenkins, which is a separate application, GitLab CI/CD is part of the GitLab platform, providing seamless integration with version control, issue tracking, and other GitLab features.

**Key Differences:**
- **Integration**: GitLab CI/CD is natively integrated with GitLab, while Jenkins requires separate setup
- **Configuration**: GitLab CI/CD uses `.gitlab-ci.yml` files stored in the repository, while Jenkins uses web UI or Jenkinsfile
- **Runners**: GitLab uses GitLab Runners (can be self-hosted or GitLab.com shared runners), Jenkins uses agents
- **Pricing**: GitLab offers free CI/CD minutes for public projects and GitLab.com users

---

### 2. What is a GitLab Runner and what are the different types?

**Answer:**
A GitLab Runner is an application that runs jobs defined in `.gitlab-ci.yml` files. It can be installed on various platforms and executes the CI/CD pipeline.

**Types of Runners:**
- **Shared Runners**: Available to all projects in a GitLab instance (provided by GitLab.com for public projects)
- **Group Runners**: Available to all projects within a specific group
- **Project Runners**: Available only to a specific project
- **Instance Runners**: Available to all projects on a GitLab instance (self-hosted)

**Runner Executors:**
- **Docker**: Runs jobs in Docker containers
- **Shell**: Runs jobs directly on the runner's host machine
- **Kubernetes**: Runs jobs in Kubernetes pods
- **VirtualBox/Parallels**: Runs jobs in VMs

---

### 3. Explain the structure of a `.gitlab-ci.yml` file.

**Answer:**
A `.gitlab-ci.yml` file defines the CI/CD pipeline configuration using YAML syntax.

**Basic Structure:**
```yaml
# Define stages
stages:
  - build
  - test
  - deploy

# Define variables
variables:
  DOCKER_DRIVER: overlay2

# Define jobs
build-job:
  stage: build
  script:
    - echo "Building the application"
    - npm install
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

test-job:
  stage: test
  script:
    - echo "Running tests"
    - npm test
  only:
    - main
    - develop

deploy-job:
  stage: deploy
  script:
    - echo "Deploying application"
    - ./deploy.sh
  environment:
    name: production
  when: manual
  only:
    - main
```

**Key Components:**
- **stages**: Defines the order of pipeline stages
- **variables**: Global or job-specific variables
- **jobs**: Individual tasks that run in stages
- **script**: Commands to execute
- **artifacts**: Files to pass between jobs
- **only/except**: Control when jobs run
- **when**: Control job execution (on_success, on_failure, manual, always)

---

### 4. What are GitLab CI/CD stages and how do they work?

**Answer:**
Stages define the order of job execution in a pipeline. Jobs in the same stage run in parallel, and stages run sequentially.

**Default Stages:**
- `.pre` (always runs first)
- `build`
- `test`
- `deploy`
- `.post` (always runs last)

**Example:**
```yaml
stages:
  - build
  - test
  - deploy

build-frontend:
  stage: build
  script:
    - npm run build

build-backend:
  stage: build
  script:
    - mvn package

test-frontend:
  stage: test
  script:
    - npm test
  needs: ["build-frontend"]

test-backend:
  stage: test
  script:
    - mvn test
  needs: ["build-backend"]

deploy:
  stage: deploy
  script:
    - ./deploy.sh
  needs: ["test-frontend", "test-backend"]
```

---

### 5. How do you use GitLab CI/CD variables and secrets?

**Answer:**
GitLab CI/CD supports variables at multiple levels: instance, group, project, and job.

**Variable Types:**
- **Protected Variables**: Only available to protected branches/tags
- **Masked Variables**: Hidden in job logs
- **File Variables**: Stored as files in the runner

**Setting Variables:**
1. **Project Level**: Settings → CI/CD → Variables
2. **Group Level**: Group Settings → CI/CD → Variables
3. **Instance Level**: Admin Area → Settings → CI/CD → Variables

**Using Variables:**
```yaml
variables:
  NODE_VERSION: "18"
  DATABASE_URL: $DATABASE_URL  # From CI/CD variables

build:
  script:
    - echo "Using Node $NODE_VERSION"
    - echo "Database: $DATABASE_URL"
    - echo "Secret: $SECRET_TOKEN"  # Masked variable
```

**Best Practices:**
- Use masked variables for sensitive data
- Use protected variables for production secrets
- Use file variables for certificates and keys
- Never commit secrets in `.gitlab-ci.yml`

---

### 6. What are GitLab CI/CD artifacts and how are they used?

**Answer:**
Artifacts are files created by jobs that are saved and can be passed to subsequent jobs or downloaded.

**Artifact Configuration:**
```yaml
build:
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
      - build/
    exclude:
      - dist/*.map
    expire_in: 1 week
    reports:
      junit: junit.xml
      coverage: coverage.json
    when: on_success
    name: "$CI_COMMIT_REF_NAME-build"
```

**Artifact Features:**
- **paths**: Files/directories to save
- **exclude**: Files to exclude
- **expire_in**: How long to keep artifacts
- **reports**: Test reports, coverage, etc.
- **when**: When to save (on_success, on_failure, always)
- **name**: Custom artifact name

**Using Artifacts:**
```yaml
test:
  script:
    - ls -la dist/  # Artifacts from previous job available
    - npm test
  dependencies:
    - build  # Explicitly download artifacts from build job
```

---

### 7. Explain GitLab CI/CD caching and when to use it.

**Answer:**
Caching stores files between pipeline runs to speed up builds by avoiding redundant downloads.

**Cache Configuration:**
```yaml
cache:
  key: "$CI_COMMIT_REF_SLUG"
  paths:
    - node_modules/
    - .npm/
  policy: pull-push

build:
  script:
    - npm install
    - npm run build
  cache:
    key: "$CI_COMMIT_REF_SLUG"
    paths:
      - node_modules/
    policy: pull  # Only pull, don't push
```

**Cache Policies:**
- **pull-push**: Pull before job, push after (default)
- **pull**: Only pull cache
- **push**: Only push cache

**Cache vs Artifacts:**
- **Cache**: For dependencies (node_modules, packages) - can be shared between pipelines
- **Artifacts**: For build outputs (dist, binaries) - specific to pipeline

---

### 8. How do you implement conditional job execution in GitLab CI/CD?

**Answer:**
GitLab CI/CD provides several ways to control when jobs run:

**1. Using `only` and `except`:**
```yaml
deploy:
  script:
    - ./deploy.sh
  only:
    - main
    - tags
  except:
    - branches
```

**2. Using `rules` (recommended):**
```yaml
deploy:
  script:
    - ./deploy.sh
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
    - if: $CI_COMMIT_TAG
      when: on_success
    - when: never
```

**3. Using `only:variables`:**
```yaml
deploy:
  script:
    - ./deploy.sh
  only:
    variables:
      - $DEPLOY == "true"
```

**4. Using `workflow`:**
```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH
```

---

### 9. What are GitLab CI/CD environments and how do you use them?

**Answer:**
Environments represent deployment targets (staging, production, etc.) and provide deployment tracking.

**Environment Configuration:**
```yaml
deploy-staging:
  stage: deploy
  script:
    - ./deploy.sh staging
  environment:
    name: staging
    url: https://staging.example.com
    on_stop: stop-staging

deploy-production:
  stage: deploy
  script:
    - ./deploy.sh production
  environment:
    name: production
    url: https://example.com
    deployment_tier: production
  when: manual
  only:
    - main
```

**Environment Features:**
- **Deployment Tracking**: See what's deployed where
- **Rollback**: Easy rollback to previous deployments
- **URLs**: Direct links to environments
- **Tiers**: Categorize environments (development, staging, production)
- **On Stop**: Actions to run when environment is stopped

---

### 10. How do you implement parallel jobs and job dependencies in GitLab CI/CD?

**Answer:**
Jobs in the same stage run in parallel. Use `needs` to create a dependency graph.

**Parallel Jobs:**
```yaml
stages:
  - test

test-unit:
  stage: test
  script:
    - npm run test:unit

test-integration:
  stage: test
  script:
    - npm run test:integration

test-e2e:
  stage: test
  script:
    - npm run test:e2e
```

**Job Dependencies with `needs`:**
```yaml
build:
  stage: build
  script:
    - npm run build
  artifacts:
    paths:
      - dist/

test:
  stage: test
  script:
    - npm test
  needs: ["build"]  # Only runs after build completes

deploy:
  stage: deploy
  script:
    - ./deploy.sh
  needs: ["test"]  # Only runs after test completes
```

**DAG (Directed Acyclic Graph):**
```yaml
build-frontend:
  stage: build
  script:
    - npm run build

build-backend:
  stage: build
  script:
    - mvn package

deploy:
  stage: deploy
  script:
    - ./deploy.sh
  needs: ["build-frontend", "build-backend"]  # Waits for both
```

---

### 11. How do you handle secrets and sensitive data in GitLab CI/CD?

**Answer:**
GitLab provides several mechanisms for managing secrets:

**1. CI/CD Variables (Recommended):**
- Set in Project/Group/Instance Settings → CI/CD → Variables
- Mark as "Protected" for protected branches only
- Mark as "Masked" to hide in job logs
- Use "File" type for certificates/keys

**2. External Secret Managers:**
```yaml
deploy:
  script:
    - |
      export AWS_ACCESS_KEY_ID=$(vault read -field=access_key secret/aws)
      export AWS_SECRET_ACCESS_KEY=$(vault read -field=secret_key secret/aws)
      - ./deploy.sh
  before_script:
    - apk add --no-cache vault
```

**3. HashiCorp Vault Integration:**
```yaml
include:
  - template: Jobs/Secrets.gitlab-ci.yml

vault secrets:
  id_tokens:
    VAULT_ID_TOKEN:
      aud: https://vault.example.com
  secrets:
    DATABASE_PASSWORD:
      vault: database/password@ops  # vault/path@env
```

**Best Practices:**
- Never commit secrets in `.gitlab-ci.yml`
- Use masked variables for sensitive data
- Rotate secrets regularly
- Use least privilege principle
- Use external secret managers for production

---

### 12. How do you implement multi-project pipelines in GitLab CI/CD?

**Answer:**
Multi-project pipelines allow triggering pipelines in other projects.

**Triggering Another Project:**
```yaml
trigger-library:
  stage: deploy
  trigger:
    project: group/library-project
    branch: main
    strategy: depend
```

**Passing Variables:**
```yaml
trigger-downstream:
  stage: deploy
  trigger:
    project: group/downstream-project
    branch: main
  variables:
    UPSTREAM_VERSION: $CI_COMMIT_SHA
    DEPLOY_ENV: "production"
```

**Using `include` for Reusable Configurations:**
```yaml
include:
  - project: 'group/shared-configs'
    file: '/templates/.gitlab-ci-template.yml'
    ref: main
  - local: '/path/to/local/config.yml'
  - remote: 'https://example.com/ci-config.yml'
  - template: Security/SAST.gitlab-ci.yml
```

---

### 13. What are GitLab CI/CD templates and how do you use them?

**Answer:**
GitLab provides built-in CI/CD templates for common tasks and security scanning.

**Using Built-in Templates:**
```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Jobs/Deploy/ECS.gitlab-ci.yml
```

**Creating Custom Templates:**
```yaml
# .gitlab-ci-template.yml
.build_template:
  image: node:18
  before_script:
    - npm install
  cache:
    key: "$CI_COMMIT_REF_SLUG"
    paths:
      - node_modules/

build:
  extends: .build_template
  script:
    - npm run build
```

**Using in Projects:**
```yaml
include:
  - project: 'group/shared-templates'
    file: '.gitlab-ci-template.yml'
    ref: main

build:
  extends: .build_template
  script:
    - npm run build
```

---

### 14. How do you debug and troubleshoot GitLab CI/CD pipelines?

**Answer:**
Several techniques for debugging pipelines:

**1. Enable Debug Mode:**
```yaml
variables:
  CI_DEBUG_TRACE: "true"  # Shows all commands
  DEBUG: "true"
```

**2. Use `script` with Debugging:**
```yaml
debug-job:
  script:
    - echo "Debug information"
    - env | grep CI_
    - pwd
    - ls -la
    - cat .gitlab-ci.yml
```

**3. Check Runner Logs:**
```bash
# On runner host
sudo gitlab-runner --debug run
```

**4. Use Artifacts for Debugging:**
```yaml
debug:
  script:
    - ./debug-script.sh > debug.log 2>&1
  artifacts:
    paths:
      - debug.log
    when: always
    expire_in: 1 day
```

**5. Common Issues:**
- **Runner not picking up jobs**: Check runner tags, status
- **Artifacts not found**: Check job dependencies
- **Variables not available**: Check variable scope, protection
- **Cache issues**: Clear cache or use different cache key

---

### 15. How do you implement blue-green or canary deployments with GitLab CI/CD?

**Answer:**
GitLab CI/CD supports advanced deployment strategies:

**Blue-Green Deployment:**
```yaml
deploy-blue:
  stage: deploy
  script:
    - ./deploy.sh blue
  environment:
    name: production-blue
    url: https://blue.example.com

deploy-green:
  stage: deploy
  script:
    - ./deploy.sh green
    - ./switch-traffic.sh green
  environment:
    name: production-green
    url: https://green.example.com
  when: manual
  only:
    - main
```

**Canary Deployment:**
```yaml
deploy-canary:
  stage: deploy
  script:
    - ./deploy.sh canary --replicas=1
  environment:
    name: production-canary
    url: https://canary.example.com
  only:
    - main

deploy-full:
  stage: deploy
  script:
    - ./deploy.sh production --replicas=10
  environment:
    name: production
    url: https://example.com
  when: manual
  needs: ["deploy-canary"]
```

---

## 🎯 **Advanced Topics**

### 16. How do you implement dynamic child pipelines in GitLab CI/CD?

**Answer:**
Dynamic child pipelines allow generating pipeline configurations at runtime.

**Example:**
```yaml
generate-pipeline:
  stage: build
  script:
    - |
      cat > child-pipeline.yml <<EOF
      test-job-1:
        script: echo "Test 1"
      test-job-2:
        script: echo "Test 2"
      EOF
  artifacts:
    paths:
      - child-pipeline.yml

child-pipeline:
  stage: test
  trigger:
    include:
      - artifact: child-pipeline.yml
        job: generate-pipeline
    strategy: depend
```

---

### 17. How do you optimize GitLab CI/CD pipeline performance?

**Answer:**
**Optimization Strategies:**

1. **Use Caching:**
```yaml
cache:
  key: "$CI_COMMIT_REF_SLUG"
  paths:
    - node_modules/
    - .cache/
```

2. **Parallel Jobs:**
```yaml
test:
  parallel:
    matrix:
      - NODE_VERSION: ["16", "18", "20"]
```

3. **Use `needs` for DAG:**
```yaml
deploy:
  needs: ["test"]  # Don't wait for all jobs in stage
```

4. **Selective Job Execution:**
```yaml
test:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - changes:
        - "**/*.js"
```

5. **Optimize Docker Images:**
```yaml
build:
  image: node:18-alpine  # Smaller image
```

6. **Use Shared Runners Efficiently:**
- Use tags to route to specific runners
- Use `resource_group` to limit concurrent jobs

---

### 18. How do you implement security scanning in GitLab CI/CD?

**Answer:**
GitLab provides built-in security scanning templates:

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Security/DAST.gitlab-ci.yml
  - template: Security/API-Security.gitlab-ci.yml
```

**Custom Security Scanning:**
```yaml
security-scan:
  stage: test
  image: aquasec/trivy:latest
  script:
    - trivy fs --security-checks vuln,config .
    - trivy image --exit-code 0 --severity HIGH,CRITICAL $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  artifacts:
    reports:
      sast: gl-sast-report.json
```

---

## 📝 **Best Practices**

1. **Keep `.gitlab-ci.yml` DRY**: Use `extends`, `include`, and templates
2. **Use `rules` instead of `only/except`**: More flexible and maintainable
3. **Cache dependencies**: Speed up pipeline execution
4. **Use artifacts wisely**: Only save what's needed
5. **Implement proper secrets management**: Never commit secrets
6. **Use job dependencies**: Optimize pipeline execution with `needs`
7. **Monitor pipeline performance**: Track duration and optimize slow jobs
8. **Use environment-specific configurations**: Different settings for dev/staging/prod
9. **Implement proper error handling**: Use `allow_failure` and `when` conditions
10. **Document your pipelines**: Add comments explaining complex configurations

---

**Good luck with your GitLab CI/CD interview preparation!**
