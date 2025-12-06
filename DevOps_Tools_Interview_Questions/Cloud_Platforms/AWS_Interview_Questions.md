# AWS Interview Questions & Answers

## ☁️ **AWS Fundamentals**

### 1. What is AWS and what are its main service categories?

**Answer:**
Amazon Web Services (AWS) is a comprehensive cloud computing platform offering over 200 services.

**Main Service Categories:**
- **Compute**: EC2, Lambda, ECS, EKS, Fargate
- **Storage**: S3, EBS, EFS, Glacier
- **Networking**: VPC, CloudFront, Route53, API Gateway
- **Database**: RDS, DynamoDB, Redshift, ElastiCache
- **Security**: IAM, Secrets Manager, KMS, WAF
- **Monitoring**: CloudWatch, CloudTrail, X-Ray
- **Management**: CloudFormation, Systems Manager, OpsWorks

---

### 2. Explain EC2 and its instance types.

**Answer:**
EC2 (Elastic Compute Cloud) provides resizable compute capacity in the cloud.

**Instance Types:**
- **General Purpose**: t3, t4g, m5, m6i (balanced compute, memory, networking)
- **Compute Optimized**: c5, c6i (high-performance processors)
- **Memory Optimized**: r5, r6i (high memory-to-CPU ratio)
- **Storage Optimized**: i3, i4i (high IOPS)
- **Accelerated Computing**: p3, p4 (GPUs)

**Key Features:**
- On-demand instances
- Reserved instances (cost savings)
- Spot instances (discounted)
- Dedicated hosts

---

### 3. What is VPC and explain its components?

**Answer:**
VPC (Virtual Private Cloud) is a logically isolated network in AWS.

**Components:**
- **Subnets**: Network segments (public/private)
- **Route Tables**: Traffic routing rules
- **Internet Gateway (IGW)**: Internet access for public subnets
- **NAT Gateway**: Internet access for private subnets
- **Security Groups**: Virtual firewall (stateful)
- **NACL**: Network Access Control List (stateless)
- **VPC Peering**: Connect VPCs
- **Transit Gateway**: Hub for VPC connections
- **VPC Endpoints**: Private connectivity to AWS services

**Example Architecture:**
```
VPC (10.0.0.0/16)
├── Public Subnet (10.0.1.0/24)
│   ├── Internet Gateway
│   ├── NAT Gateway
│   └── Load Balancer
└── Private Subnet (10.0.2.0/24)
    ├── Application Servers
    └── Database
```

---

### 4. What is IAM and how do you manage access?

**Answer:**
IAM (Identity and Access Management) controls access to AWS resources.

**Components:**
- **Users**: Individual accounts
- **Groups**: Collections of users
- **Roles**: Permissions for AWS services/resources
- **Policies**: JSON documents defining permissions

**Policy Example:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

**Best Practices:**
- Least privilege principle
- Use roles instead of users for applications
- Enable MFA
- Regular access reviews
- Use policy conditions

---

### 5. Explain S3 and its features.

**Answer:**
S3 (Simple Storage Service) is object storage for any amount of data.

**Key Features:**
- **Buckets**: Containers for objects
- **Objects**: Files stored in buckets
- **Versioning**: Keep multiple versions
- **Lifecycle Policies**: Automate transitions
- **Storage Classes**: Standard, IA, Glacier, Deep Archive
- **Encryption**: Server-side encryption
- **Access Control**: Bucket policies, ACLs

**Storage Classes:**
- **Standard**: Frequently accessed
- **Standard-IA**: Infrequently accessed
- **Glacier**: Archive storage
- **Deep Archive**: Long-term archive

**Lifecycle Policy:**
```json
{
  "Rules": [
    {
      "Id": "Transition to IA",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        }
      ]
    }
  ]
}
```

---

### 6. What are Load Balancers and their types?

**Answer:**
Load balancers distribute incoming traffic across multiple targets.

**Types:**
- **ALB (Application Load Balancer)**: Layer 7, HTTP/HTTPS
- **NLB (Network Load Balancer)**: Layer 4, TCP/UDP
- **CLB (Classic Load Balancer)**: Legacy

**ALB Features:**
- Path-based routing
- Host-based routing
- SSL/TLS termination
- Health checks
- Sticky sessions

**Use Cases:**
- ALB: Web applications
- NLB: High performance, low latency
- CLB: Legacy applications

---

### 7. What is Autoscaling and how does it work?

**Answer:**
Autoscaling automatically adjusts capacity based on demand.

**Components:**
- **Auto Scaling Group (ASG)**: Group of EC2 instances
- **Launch Template**: Instance configuration
- **Scaling Policies**: When to scale
- **Health Checks**: Replace unhealthy instances

**Scaling Policies:**
- **Target Tracking**: Maintain target metric
- **Step Scaling**: Scale by steps
- **Simple Scaling**: Simple scale up/down

**Example:**
```bash
# Create ASG
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name my-asg \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 3 \
  --launch-template LaunchTemplateId=lt-123
```

---

### 8. Explain CloudWatch and its components.

**Answer:**
CloudWatch is a monitoring and observability service.

**Components:**
- **Metrics**: System and application metrics
- **Alarms**: Automated actions based on metrics
- **Logs**: Centralized logging
- **Dashboards**: Visualize metrics
- **Events**: Event-driven automation

**Metrics:**
- **EC2**: CPU, Network, Disk
- **S3**: Requests, Bucket size
- **RDS**: CPU, Connections, Storage

**Alarm Example:**
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name high-cpu \
  --metric-name CPUUtilization \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

---

### 9. What is Route53 and how does it work?

**Answer:**
Route53 is a scalable DNS and domain name registration service.

**Features:**
- Domain registration
- DNS management
- Health checks
- Routing policies

**Routing Policies:**
- **Simple**: Standard DNS
- **Weighted**: Distribute traffic
- **Latency**: Route to lowest latency
- **Failover**: Active-passive
- **Geolocation**: Route by location

---

### 10. Explain RDS and its features.

**Answer:**
RDS (Relational Database Service) is a managed relational database service.

**Supported Engines:**
- MySQL
- PostgreSQL
- MariaDB
- Oracle
- SQL Server
- Aurora

**Features:**
- Automated backups
- Multi-AZ deployment (high availability)
- Read replicas (read scaling)
- Automated patching
- Encryption at rest and in transit

**Multi-AZ:**
- Synchronous replication
- Automatic failover
- High availability

---

### 11. What is Lambda and when to use it?

**Answer:**
Lambda is a serverless compute service that runs code in response to events.

**Key Features:**
- No server management
- Pay per execution
- Automatic scaling
- Event-driven

**Use Cases:**
- API backends
- Data processing
- Real-time file processing
- Scheduled tasks
- Event-driven applications

**Example:**
```python
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

---

### 12. What is EKS and how does it differ from ECS?

**Answer:**
**EKS (Elastic Kubernetes Service):**
- Managed Kubernetes service
- Full Kubernetes compatibility
- More control and flexibility
- Complex setup

**ECS (Elastic Container Service):**
- AWS-native container service
- Simpler setup
- Integrated with AWS services
- Less control

**When to Use:**
- **EKS**: Need Kubernetes features, multi-cloud
- **ECS**: AWS-only, simpler management

---

### 13. Explain CloudTrail and its use cases.

**Answer:**
CloudTrail logs API calls and events in your AWS account.

**Features:**
- API call logging
- Audit trail
- Compliance
- Security analysis

**Use Cases:**
- Security auditing
- Compliance
- Troubleshooting
- Change tracking

**Configuration:**
```bash
aws cloudtrail create-trail \
  --name my-trail \
  --s3-bucket-name my-cloudtrail-bucket
```

---

### 14. What is Secrets Manager and how does it work?

**Answer:**
Secrets Manager helps you protect secrets needed to access your applications.

**Features:**
- Automatic rotation
- Encryption at rest
- Fine-grained access control
- Integration with RDS, Redshift, DocumentDB

**Example:**
```bash
# Store secret
aws secretsmanager create-secret \
  --name my-secret \
  --secret-string "my-password"

# Retrieve secret
aws secretsmanager get-secret-value \
  --secret-id my-secret
```

---

### 15. Explain CodePipeline and its components.

**Answer:**
CodePipeline is a fully managed CI/CD service.

**Components:**
- **Pipeline**: Workflow definition
- **Stage**: Logical division
- **Action**: Task in stage
- **Artifact**: Output from action

**Stages:**
1. Source: CodeCommit, S3, GitHub
2. Build: CodeBuild
3. Deploy: CodeDeploy, ECS, Lambda

**Example:**
```json
{
  "pipeline": {
    "name": "my-pipeline",
    "stages": [
      {
        "name": "Source",
        "actions": [
          {
            "name": "SourceAction",
            "actionTypeId": {
              "category": "Source",
              "provider": "CodeCommit"
            }
          }
        ]
      }
    ]
  }
}
```

---

## 📝 **Best Practices**

1. **Use IAM Roles**: Avoid hardcoded credentials
2. **Enable MFA**: Multi-factor authentication
3. **Use VPC**: Network isolation
4. **Enable CloudTrail**: Audit logging
5. **Use Tags**: Resource organization
6. **Backup**: Regular backups
7. **Monitor**: Use CloudWatch
8. **Cost Optimization**: Right-size resources
9. **Security Groups**: Restrict access
10. **Encryption**: Encrypt data at rest and in transit

---

**Good luck with your AWS interview preparation! ☁️**
