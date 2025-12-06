# Azure DevOps Interview Questions & Answers

## 🚀 **Azure DevOps Fundamentals**

### 1. What is Azure DevOps and what are its main components?

**Answer:**
Azure DevOps is a comprehensive DevOps platform that provides a complete set of tools for software development, testing, and deployment. It's a cloud-based service that integrates multiple DevOps capabilities.

**Main Components:**
1. **Azure Repos**: Git repositories for source control
2. **Azure Pipelines**: CI/CD for building, testing, and deploying
3. **Azure Boards**: Work tracking and project management
4. **Azure Artifacts**: Package management (NuGet, npm, Maven, etc.)
5. **Azure Test Plans**: Test management and planning

**Key Features:**
- Cloud-hosted and self-hosted options
- Integration with Azure services
- Supports multiple languages and platforms
- Extensible through marketplace extensions

---

### 2. What is Azure Pipelines and how does it work?

**Answer:**
Azure Pipelines is a cloud service for automatically building, testing, and deploying code to any platform. It supports both YAML-based and classic (UI-based) pipelines.

**Pipeline Types:**
- **YAML Pipelines**: Code-based, version-controlled pipeline definitions
- **Classic Pipelines**: UI-based pipeline creation

**Key Concepts:**
- **Pipelines**: Automated workflows
- **Stages**: Major divisions (build, test, deploy)
- **Jobs**: Units of work that run on agents
- **Steps**: Individual tasks within jobs
- **Agents**: Machines that execute pipeline jobs (Microsoft-hosted or self-hosted)

---

### 3. Explain the structure of an Azure Pipeline YAML file.

**Answer:**
Azure Pipelines use YAML files to define pipeline configurations.

**Basic Structure:**
```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - README.md

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: my-variable-group
  - name: buildConfiguration
    value: 'Release'
  - name: major
    value: 1

stages:
- stage: Build
  displayName: 'Build Application'
  jobs:
  - job: BuildJob
    displayName: 'Build Job'
    steps:
    - task: NodeTool@0
      inputs:
        versionSpec: '18.x'
      displayName: 'Install Node.js'
    
    - script: |
        npm install
        npm run build
      displayName: 'Build'
    
    - task: PublishBuildArtifacts@1
      inputs:
        pathToPublish: 'dist'
        artifactName: 'drop'

- stage: Test
  displayName: 'Run Tests'
  dependsOn: Build
  jobs:
  - job: TestJob
    steps:
    - download: current
      artifact: drop
    - script: npm test
      displayName: 'Run Tests'

- stage: Deploy
  displayName: 'Deploy to Production'
  dependsOn: Test
  condition: succeeded()
  jobs:
  - deployment: DeployJob
    environment: production
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploying to production"
            displayName: 'Deploy'
```

---

### 4. What are Azure Pipeline agents and agent pools?

**Answer:**
Agents are machines that execute pipeline jobs. Agent pools are collections of agents.

**Types of Agents:**
1. **Microsoft-hosted Agents**: Managed by Microsoft, pre-installed with common tools
2. **Self-hosted Agents**: Your own machines, more control and customization

**Agent Pools:**
- **Default**: Default pool for organization
- **Azure Pipelines**: For public and private projects
- **Deployment Groups**: For deployment targets

**Self-hosted Agent Setup:**
```bash
# Download agent
mkdir myagent && cd myagent
wget https://vstsagentpackage.azureedge.net/agent/2.211.1/vsts-agent-linux-x64-2.211.1.tar.gz
tar zxvf vsts-agent-linux-x64-2.211.1.tar.gz

# Configure
./config.sh --url https://dev.azure.com/org --auth pat --token TOKEN --pool Default --agent agent-name --acceptTeeEula

# Run as service
sudo ./svc.sh install
sudo ./svc.sh start
```

---

### 5. How do you use variables and variable groups in Azure Pipelines?

**Answer:**
Variables store values that can be used across pipeline runs.

**Variable Types:**
1. **Pipeline Variables**: Defined in YAML or UI
2. **Variable Groups**: Reusable variable collections
3. **Library Variables**: Secure variables stored in Azure Key Vault
4. **System Variables**: Built-in variables (e.g., `$(Build.SourcesDirectory)`)

**Using Variables:**
```yaml
variables:
  - group: my-variable-group
  - name: buildConfiguration
    value: 'Release'
  - name: major
    value: 1
    readonly: true

stages:
- stage: Build
  variables:
    minor: 0
  jobs:
  - job: BuildJob
    steps:
    - script: |
        echo "Build configuration: $(buildConfiguration)"
        echo "Version: $(major).$(minor).$(Build.BuildId)"
        echo "Source directory: $(Build.SourcesDirectory)"
```

**Variable Groups:**
- Created in Pipelines → Library → Variable groups
- Can link to Azure Key Vault
- Can be scoped to specific pipelines

---

### 6. How do you implement conditional execution and approvals in Azure Pipelines?

**Answer:**
Azure Pipelines supports conditional execution and manual approvals.

**Conditional Execution:**
```yaml
stages:
- stage: Deploy
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - job: DeployJob
    steps:
    - script: echo "Deploying"
      condition: ne(variables['Build.Reason'], 'PullRequest')

- stage: Notify
  condition: always()
  jobs:
  - job: NotifyJob
    steps:
    - script: echo "Notify"
      condition: failed()
```

**Manual Approvals:**
Configured in Environments:
1. Go to Pipelines → Environments
2. Create/Edit environment
3. Add approval checks (users/groups)
4. Add branch filters

```yaml
- stage: Deploy
  jobs:
  - deployment: DeployJob
    environment: 
      name: production
      resourceType: VirtualMachine
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploy"
```

---

### 7. How do you use artifacts in Azure Pipelines?

**Answer:**
Artifacts are files produced by pipelines that can be consumed by other stages/jobs.

**Publishing Artifacts:**
```yaml
- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: '$(Build.ArtifactStagingDirectory)'
    artifactName: 'drop'
    publishLocation: 'Container'
```

**Downloading Artifacts:**
```yaml
- download: current
  artifact: drop
  displayName: 'Download artifacts'

- download: none
  displayName: 'Download nothing'

- download: pipeline
  artifact: drop
  pipeline: 123
  displayName: 'Download from specific pipeline'
```

**Universal Packages:**
```yaml
- task: UniversalPackages@0
  inputs:
    command: 'publish'
    publishDirectory: '$(Build.ArtifactStagingDirectory)'
    vstsFeedPublish: 'my-feed'
    vstsFeedPackagePublish: 'my-package'
    versionOption: 'patch'
```

---

### 8. How do you implement multi-stage pipelines in Azure DevOps?

**Answer:**
Multi-stage pipelines allow organizing work into logical stages.

**Example:**
```yaml
stages:
- stage: Build
  displayName: 'Build Stage'
  jobs:
  - job: BuildJob
    steps:
    - script: npm run build
      displayName: 'Build'

- stage: Test
  displayName: 'Test Stage'
  dependsOn: Build
  condition: succeeded()
  jobs:
  - job: UnitTests
    steps:
    - script: npm test
      displayName: 'Unit Tests'
  
  - job: IntegrationTests
    steps:
    - script: npm run test:integration
      displayName: 'Integration Tests'

- stage: DeployStaging
  displayName: 'Deploy to Staging'
  dependsOn: Test
  condition: succeeded()
  jobs:
  - deployment: DeployStaging
    environment: staging
    strategy:
      runOnce:
        deploy:
          steps:
          - script: ./deploy.sh staging

- stage: DeployProduction
  displayName: 'Deploy to Production'
  dependsOn: DeployStaging
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: DeployProduction
    environment: production
    strategy:
      runOnce:
        deploy:
          steps:
          - script: ./deploy.sh production
```

---

### 9. How do you use templates in Azure Pipelines?

**Answer:**
Templates allow reusing pipeline logic across multiple pipelines.

**Template Example:**
```yaml
# templates/build-template.yml
parameters:
  - name: buildConfiguration
    default: 'Release'
  - name: projectPath
    type: string

steps:
- task: DotNetCoreCLI@2
  displayName: 'Build'
  inputs:
    command: 'build'
    projects: '${{ parameters.projectPath }}'
    arguments: '--configuration ${{ parameters.buildConfiguration }}'

- task: DotNetCoreCLI@2
  displayName: 'Test'
  inputs:
    command: 'test'
    projects: '${{ parameters.projectPath }}'
```

**Using Templates:**
```yaml
# azure-pipelines.yml
resources:
  repositories:
    - repository: templates
      type: git
      name: MyProject/PipelineTemplates

extends:
  template: build-template.yml@templates
  parameters:
    buildConfiguration: 'Release'
    projectPath: 'src/MyApp/MyApp.csproj'
```

**Include Templates:**
```yaml
stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - template: templates/build-steps.yml
      parameters:
        nodeVersion: '18.x'
```

---

### 10. How do you implement deployment strategies in Azure Pipelines?

**Answer:**
Azure Pipelines supports various deployment strategies through deployment jobs.

**1. RunOnce Strategy:**
```yaml
- deployment: DeployJob
  environment: production
  strategy:
    runOnce:
      deploy:
        steps:
        - script: ./deploy.sh
```

**2. Rolling Strategy:**
```yaml
- deployment: DeployJob
  environment: production
  strategy:
    rolling:
      maxParallel: 2
      preDeploy:
        steps:
        - script: echo "Pre-deploy"
      deploy:
        steps:
        - script: ./deploy.sh
      postRouteTraffic:
        steps:
        - script: echo "Post route traffic"
      on:
        failure:
          steps:
          - script: echo "Rollback"
        success:
          steps:
          - script: echo "Success"
```

**3. Canary Strategy:**
```yaml
- deployment: DeployJob
  environment: production
  strategy:
    canary:
      increments: [10, 20, 100]
      preDeploy:
        steps:
        - script: echo "Pre-deploy"
      deploy:
        steps:
        - script: ./deploy.sh
      routeTraffic:
        steps:
        - script: ./route-traffic.sh
      postRouteTraffic:
        steps:
        - script: echo "Post route"
      on:
        failure:
          steps:
          - script: ./rollback.sh
        success:
          steps:
          - script: echo "Success"
```

---

### 11. How do you integrate Azure Pipelines with Azure services?

**Answer:**
Azure Pipelines integrates seamlessly with Azure services.

**1. Azure Service Connections:**
```yaml
- task: AzureWebApp@1
  inputs:
    azureSubscription: 'my-service-connection'
    appName: 'my-web-app'
    package: '$(Pipeline.Workspace)/drop'
```

**2. Azure Key Vault:**
```yaml
variables:
- group: my-variable-group  # Linked to Key Vault

steps:
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'my-service-connection'
    KeyVaultName: 'my-keyvault'
    SecretsFilter: 'secret1,secret2'
```

**3. Azure Container Registry:**
```yaml
- task: Docker@2
  inputs:
    containerRegistry: 'my-acr-connection'
    repository: 'myapp'
    command: 'buildAndPush'
    Dockerfile: '**/Dockerfile'
    tags: |
      $(Build.BuildId)
      latest
```

**4. Azure Kubernetes Service:**
```yaml
- task: Kubernetes@1
  inputs:
    connectionType: 'Azure Resource Manager'
    azureSubscriptionEndpoint: 'my-service-connection'
    azureResourceGroup: 'my-rg'
    kubernetesCluster: 'my-aks'
    command: 'apply'
    arguments: '-f deployment.yaml'
```

---

### 12. How do you implement security and secrets management in Azure Pipelines?

**Answer:**
Azure DevOps provides multiple security features.

**1. Variable Groups with Key Vault:**
- Create variable group in Library
- Link to Azure Key Vault
- Variables automatically synced from Key Vault

**2. Secure Files:**
```yaml
- task: DownloadSecureFile@1
  name: mySecureFile
  inputs:
    secureFile: 'certificate.pfx'
  
- script: |
    echo "Using secure file: $(mySecureFile.secureFilePath)"
```

**3. Service Connections:**
- Use service principals with least privilege
- Store credentials securely
- Use managed identities when possible

**4. Pipeline Permissions:**
- Limit who can modify pipelines
- Use branch policies
- Require approvals for production

**5. Secret Variables:**
```yaml
variables:
  - name: mySecret
    value: 'secret-value'  # Mark as secret in UI
    isSecret: true
```

---

### 13. How do you implement parallel jobs and matrix strategies in Azure Pipelines?

**Answer:**
Azure Pipelines supports parallel execution and matrix builds.

**Matrix Strategy:**
```yaml
jobs:
- job: Build
  strategy:
    matrix:
      Linux:
        imageName: 'ubuntu-latest'
      Windows:
        imageName: 'windows-latest'
      MacOS:
        imageName: 'macos-latest'
    maxParallel: 3
  pool:
    vmImage: '$(imageName)'
  steps:
  - script: npm run build
    displayName: 'Build on $(imageName)'
```

**Parallel Jobs:**
```yaml
jobs:
- job: BuildFrontend
  steps:
  - script: npm run build:frontend

- job: BuildBackend
  steps:
  - script: npm run build:backend

- job: Deploy
  dependsOn:
  - BuildFrontend
  - BuildBackend
  condition: succeeded()
  steps:
  - script: ./deploy.sh
```

---

### 14. How do you implement release pipelines in Azure DevOps?

**Answer:**
Release pipelines (classic) provide UI-based deployment management, though YAML pipelines are recommended.

**Classic Release Pipeline:**
1. Create release pipeline in Releases
2. Add artifacts (build outputs)
3. Define stages (Dev, Staging, Production)
4. Configure deployment tasks
5. Set approvals and gates

**YAML-based Release (Recommended):**
```yaml
stages:
- stage: DeployDev
  displayName: 'Deploy to Dev'
  jobs:
  - deployment: DeployDev
    environment: dev
    strategy:
      runOnce:
        deploy:
          steps:
          - script: ./deploy.sh dev

- stage: DeployStaging
  displayName: 'Deploy to Staging'
  dependsOn: DeployDev
  condition: succeeded()
  jobs:
  - deployment: DeployStaging
    environment: staging
    strategy:
      runOnce:
        deploy:
          steps:
          - script: ./deploy.sh staging

- stage: DeployProduction
  displayName: 'Deploy to Production'
  dependsOn: DeployStaging
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: DeployProduction
    environment: production
    strategy:
      runOnce:
        deploy:
          steps:
          - script: ./deploy.sh production
```

---

### 15. How do you optimize Azure Pipeline performance?

**Answer:**
**Optimization Strategies:**

1. **Use Caching:**
```yaml
- task: Cache@2
  inputs:
    key: 'npm | "$(Agent.OS)" | package-lock.json'
    restoreKeys: |
      npm | "$(Agent.OS)"
    path: 'node_modules'
```

2. **Parallel Jobs:**
```yaml
jobs:
- job: Job1
  steps: ...
- job: Job2
  steps: ...
```

3. **Conditional Execution:**
```yaml
condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
```

4. **Use Appropriate Agents:**
```yaml
pool:
  vmImage: 'ubuntu-latest'  # Faster startup
```

5. **Optimize Artifacts:**
```yaml
- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: 'dist'  # Only publish what's needed
```

6. **Use Templates:**
- Reuse pipeline logic
- Reduce duplication

---

## 📝 **Best Practices**

1. **Use YAML pipelines**: Version-controlled, easier to review
2. **Implement proper error handling**: Use conditions and retry logic
3. **Use variable groups**: Centralize configuration
4. **Implement approvals**: Protect production deployments
5. **Cache dependencies**: Speed up builds
6. **Use templates**: DRY principle
7. **Monitor pipeline performance**: Track duration and optimize
8. **Security first**: Use Key Vault, secure variables, least privilege
9. **Document pipelines**: Add comments and descriptions
10. **Test pipelines**: Validate changes before merging

---

**Good luck with your Azure DevOps interview preparation!**
