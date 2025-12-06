# Pulumi Interview Questions & Answers

## 🚀 **Pulumi Fundamentals**

### 1. What is Pulumi and how does it differ from Terraform?

**Answer:**
Pulumi is an Infrastructure as Code (IaC) tool that allows you to write infrastructure code using general-purpose programming languages instead of domain-specific languages.

**Key Differences:**

| Feature | Pulumi | Terraform |
|---------|--------|-----------|
| **Language** | Python, TypeScript, Go, C#, Java, YAML | HCL (HashiCorp Configuration Language) |
| **Type Safety** | Strong (with TypeScript/Python) | Limited |
| **IDE Support** | Full (autocomplete, refactoring) | Basic |
| **Testing** | Unit tests with real languages | Limited |
| **Reusability** | Functions, classes, packages | Modules |
| **State Management** | Pulumi Service (cloud) or self-hosted | Terraform Cloud or local |
| **Provider Support** | Growing (uses Terraform providers) | Extensive |

**Advantages of Pulumi:**
- Use familiar programming languages
- Better IDE support and tooling
- Strong type safety
- Easier to test infrastructure code
- Better code reuse and abstraction
- Can use existing libraries and packages

**When to Use Pulumi:**
- Team familiar with programming languages
- Need complex logic and abstractions
- Want strong type safety
- Need to test infrastructure code
- Prefer cloud-based state management

---

### 2. How do you install and configure Pulumi?

**Answer:**
**Installation:**

**macOS:**
```bash
brew install pulumi
```

**Linux:**
```bash
curl -fsSL https://get.pulumi.com | sh
```

**Windows:**
```powershell
choco install pulumi
```

**Verify Installation:**
```bash
pulumi version
```

**Configuration:**
```bash
# Login to Pulumi Cloud (optional)
pulumi login

# Or use local backend
pulumi login --local

# Create new project
pulumi new

# Initialize project
pulumi new aws-typescript
pulumi new aws-python
pulumi new azure-typescript
```

---

### 3. What is the structure of a Pulumi project?

**Answer:**
**Project Structure:**
```
my-project/
  Pulumi.yaml          # Project metadata
  Pulumi.dev.yaml      # Stack configuration (dev)
  Pulumi.prod.yaml     # Stack configuration (prod)
  index.ts             # Main program (TypeScript)
  # or
  __main__.py          # Main program (Python)
  package.json         # Node.js dependencies
  # or
  requirements.txt     # Python dependencies
  node_modules/        # Node.js packages
  # or
  venv/                # Python virtual environment
```

**Pulumi.yaml:**
```yaml
name: my-project
runtime:
  name: nodejs
  options:
    typescript: true
description: My infrastructure project
```

**Stack Configuration (Pulumi.dev.yaml):**
```yaml
config:
  aws:region: us-east-1
  my-project:environment: dev
  my-project:instanceType: t2.micro
```

---

### 4. How do you create infrastructure with Pulumi (TypeScript example)?

**Answer:**
**Basic Example:**
```typescript
// index.ts
import * as aws from "@pulumi/aws";
import * as pulumi from "@pulumi/pulumi";

// Get configuration
const config = new pulumi.Config();
const instanceType = config.get("instanceType") || "t2.micro";

// Create VPC
const vpc = new aws.ec2.Vpc("my-vpc", {
    cidrBlock: "10.0.0.0/16",
    tags: {
        Name: "my-vpc",
    },
});

// Create subnet
const subnet = new aws.ec2.Subnet("my-subnet", {
    vpcId: vpc.id,
    cidrBlock: "10.0.1.0/24",
    availabilityZone: "us-east-1a",
    tags: {
        Name: "my-subnet",
    },
});

// Create security group
const sg = new aws.ec2.SecurityGroup("my-sg", {
    vpcId: vpc.id,
    ingress: [{
        protocol: "tcp",
        fromPort: 80,
        toPort: 80,
        cidrBlocks: ["0.0.0.0/0"],
    }],
    egress: [{
        protocol: "-1",
        fromPort: 0,
        toPort: 0,
        cidrBlocks: ["0.0.0.0/0"],
    }],
    tags: {
        Name: "my-sg",
    },
});

// Create EC2 instance
const instance = new aws.ec2.Instance("my-instance", {
    ami: "ami-0c55b159cbfafe1f0",
    instanceType: instanceType,
    subnetId: subnet.id,
    vpcSecurityGroupIds: [sg.id],
    tags: {
        Name: "my-instance",
    },
});

// Export outputs
export const vpcId = vpc.id;
export const instanceId = instance.id;
export const publicIp = instance.publicIp;
```

**Running:**
```bash
# Install dependencies
npm install

# Preview changes
pulumi preview

# Deploy
pulumi up

# Destroy
pulumi destroy
```

---

### 5. How do you create infrastructure with Pulumi (Python example)?

**Answer:**
**Python Example:**
```python
# __main__.py
import pulumi
import pulumi_aws as aws

# Get configuration
config = pulumi.Config()
instance_type = config.get("instanceType") or "t2.micro"

# Create VPC
vpc = aws.ec2.Vpc(
    "my-vpc",
    cidr_block="10.0.0.0/16",
    tags={
        "Name": "my-vpc",
    }
)

# Create subnet
subnet = aws.ec2.Subnet(
    "my-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-east-1a",
    tags={
        "Name": "my-subnet",
    }
)

# Create security group
sg = aws.ec2.SecurityGroup(
    "my-sg",
    vpc_id=vpc.id,
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=80,
        to_port=80,
        cidr_blocks=["0.0.0.0/0"],
    )],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        protocol="-1",
        from_port=0,
        to_port=0,
        cidr_blocks=["0.0.0.0/0"],
    )],
    tags={
        "Name": "my-sg",
    }
)

# Create EC2 instance
instance = aws.ec2.Instance(
    "my-instance",
    ami="ami-0c55b159cbfafe1f0",
    instance_type=instance_type,
    subnet_id=subnet.id,
    vpc_security_group_ids=[sg.id],
    tags={
        "Name": "my-instance",
    }
)

# Export outputs
pulumi.export("vpc_id", vpc.id)
pulumi.export("instance_id", instance.id)
pulumi.export("public_ip", instance.public_ip)
```

---

### 6. How do you manage stacks in Pulumi?

**Answer:**
Stacks are isolated instances of your infrastructure (dev, staging, prod).

**Creating Stacks:**
```bash
# Create new stack
pulumi stack init dev
pulumi stack init prod

# List stacks
pulumi stack ls

# Select stack
pulumi stack select dev

# Show current stack
pulumi stack

# Remove stack
pulumi stack rm dev
```

**Stack-specific Configuration:**
```bash
# Set stack config
pulumi config set aws:region us-east-1
pulumi config set instanceType t2.micro

# Get config
pulumi config get aws:region

# Set secret (encrypted)
pulumi config set --secret dbPassword mypassword

# List config
pulumi config
```

**Using Stack in Code:**
```typescript
// index.ts
import * as pulumi from "@pulumi/pulumi";

const stack = pulumi.getStack();
const config = new pulumi.Config();

// Stack-specific logic
if (stack === "prod") {
    // Production configuration
} else {
    // Development configuration
}
```

---

### 7. How do you use components and modules in Pulumi?

**Answer:**
Components allow creating reusable infrastructure abstractions.

**Creating a Component (TypeScript):**
```typescript
// components/WebServer.ts
import * as aws from "@pulumi/aws";
import * as pulumi from "@pulumi/pulumi";

export interface WebServerArgs {
    instanceType: string;
    ami: string;
    vpcId: pulumi.Input<string>;
    subnetId: pulumi.Input<string>;
}

export class WebServer extends pulumi.ComponentResource {
    public readonly instanceId: pulumi.Output<string>;
    public readonly publicIp: pulumi.Output<string>;

    constructor(name: string, args: WebServerArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:WebServer", name, {}, opts);

        // Create security group
        const sg = new aws.ec2.SecurityGroup(
            `${name}-sg`,
            {
                vpcId: args.vpcId,
                ingress: [{
                    protocol: "tcp",
                    fromPort: 80,
                    toPort: 80,
                    cidrBlocks: ["0.0.0.0/0"],
                }],
            },
            { parent: this }
        );

        // Create instance
        const instance = new aws.ec2.Instance(
            `${name}-instance`,
            {
                ami: args.ami,
                instanceType: args.instanceType,
                subnetId: args.subnetId,
                vpcSecurityGroupIds: [sg.id],
            },
            { parent: this }
        );

        this.instanceId = instance.id;
        this.publicIp = instance.publicIp;

        this.registerOutputs({
            instanceId: this.instanceId,
            publicIp: this.publicIp,
        });
    }
}
```

**Using Component:**
```typescript
// index.ts
import { WebServer } from "./components/WebServer";

const webServer = new WebServer("web1", {
    instanceType: "t2.micro",
    ami: "ami-0c55b159cbfafe1f0",
    vpcId: vpc.id,
    subnetId: subnet.id,
});

export const instanceId = webServer.instanceId;
```

---

### 8. How do you handle outputs and exports in Pulumi?

**Answer:**
Outputs allow exposing values from your infrastructure.

**Exporting Values:**
```typescript
// Simple export
export const vpcId = vpc.id;

// Export with transformation
export const instanceUrl = instance.publicIp.apply(ip => `http://${ip}`);

// Export multiple values
export const outputs = {
    vpcId: vpc.id,
    instanceId: instance.id,
    publicIp: instance.publicIp,
};
```

**Using Outputs:**
```typescript
// Outputs are asynchronous
const instanceId = instance.id;

// Use apply for transformations
const url = instance.publicIp.apply(ip => `http://${ip}:8080`);

// Use all for multiple outputs
const combined = pulumi.all([vpc.id, subnet.id]).apply(([vpcId, subnetId]) => {
    return { vpcId, subnetId };
});
```

**Viewing Outputs:**
```bash
# Show all outputs
pulumi stack output

# Show specific output
pulumi stack output instanceId

# Show as JSON
pulumi stack output --json
```

---

### 9. How do you test Pulumi code?

**Answer:**
Pulumi supports unit testing with real programming languages.

**TypeScript Testing (Jest):**
```typescript
// __tests__/index.test.ts
import * as pulumi from "@pulumi/pulumi";
import * as infra from "../index";

// Mock Pulumi
pulumi.runtime.setMocks({
    newResource: (args: pulumi.runtime.MockResourceArgs): { id: string; state: any } => {
        return {
            id: `${args.name}-id`,
            state: args.inputs,
        };
    },
    call: (args: pulumi.runtime.MockCallArgs) => {
        return args.inputs;
    },
});

describe("Infrastructure", () => {
    let infra: typeof import("../index");

    beforeAll(async () => {
        infra = await import("../index");
    });

    it("should create VPC", () => {
        expect(infra.vpcId).toBeDefined();
    });
});
```

**Python Testing (pytest):**
```python
# tests/test_infra.py
import pulumi
import pytest

@pytest.fixture
def mock_pulumi(monkeypatch):
    def mock_new_resource(self, *args, **kwargs):
        return {"id": "mock-id", "state": {}}
    
    monkeypatch.setattr(pulumi, "new_resource", mock_new_resource)
```

---

### 10. How do you manage secrets in Pulumi?

**Answer:**
Pulumi provides built-in secret management.

**Setting Secrets:**
```bash
# Set secret (automatically encrypted)
pulumi config set --secret dbPassword mypassword

# Or use set-secret
pulumi config set-secret dbPassword mypassword
```

**Using Secrets in Code:**
```typescript
// index.ts
import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config();

// Get secret (automatically decrypted)
const dbPassword = config.requireSecret("dbPassword");

// Use secret
const db = new aws.rds.Instance("db", {
    // ... other config
    masterPassword: dbPassword,
});
```

**Secret Providers:**
```bash
# Use AWS Secrets Manager
pulumi config set --secret-provider aws-secrets-manager dbPassword

# Use HashiCorp Vault
pulumi config set --secret-provider vault dbPassword
```

---

### 11. How do you use Pulumi with CI/CD?

**Answer:**
Pulumi integrates with various CI/CD platforms.

**GitHub Actions:**
```yaml
# .github/workflows/pulumi.yml
name: Pulumi
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - uses: pulumi/actions@v3
        with:
          stack-name: dev
        env:
          PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
```

**GitLab CI:**
```yaml
# .gitlab-ci.yml
deploy:
  image: pulumi/pulumi:latest
  script:
    - pulumi stack select dev
    - pulumi up --yes
  only:
    - main
```

---

## 📝 **Best Practices**

1. **Use components**: Create reusable abstractions
2. **Type safety**: Leverage TypeScript/Python types
3. **Testing**: Write unit tests for infrastructure
4. **Stack management**: Use separate stacks for environments
5. **Secrets**: Use Pulumi's secret management
6. **Version control**: Keep code in git
7. **Documentation**: Add comments and README
8. **Outputs**: Export important values
9. **Error handling**: Handle errors gracefully
10. **CI/CD**: Automate deployments

---

**Good luck with your Pulumi interview preparation!**
