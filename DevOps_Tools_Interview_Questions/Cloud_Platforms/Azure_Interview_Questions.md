# Azure Interview Questions & Answers

## ☁️ **Azure Fundamentals**

### 1. What is Microsoft Azure and what are its main services?

**Answer:**
Microsoft Azure is a cloud computing platform offering 200+ services.

**Main Service Categories:**
- **Compute**: Virtual Machines, App Services, Functions, Container Instances
- **Storage**: Blob Storage, Files, Disks, Data Lake
- **Networking**: Virtual Network, Load Balancer, Application Gateway, VPN Gateway
- **Databases**: SQL Database, Cosmos DB, MySQL, PostgreSQL
- **Security**: Azure AD, Key Vault, Security Center
- **Monitoring**: Monitor, Log Analytics, Application Insights
- **Management**: Resource Manager, Automation, Policy

---

### 2. Explain Azure Virtual Machines and their types.

**Answer:**
Azure VMs provide on-demand, scalable computing resources.

**VM Series:**
- **General Purpose**: B, Dsv3, Dv3 (balanced CPU/memory)
- **Compute Optimized**: Fsv2 (high CPU-to-memory ratio)
- **Memory Optimized**: Esv3, M-series (high memory)
- **Storage Optimized**: Ls-series (high disk throughput)
- **GPU**: NC, ND-series (GPU-enabled)

**Key Features:**
- Pay-as-you-go
- Reserved instances (cost savings)
- Spot VMs (discounted)
- Availability Sets/Zones

---

### 3. What is Azure Virtual Network (vNET)?

**Answer:**
vNET is an isolated network in Azure.

**Components:**
- **Subnets**: Network segments
- **Network Security Groups (NSG)**: Firewall rules
- **Route Tables**: Custom routing
- **Virtual Network Gateway**: VPN/ExpressRoute
- **Peering**: Connect vNETs
- **Service Endpoints**: Private connectivity

**Example:**
```json
{
  "name": "my-vnet",
  "addressSpace": {
    "addressPrefixes": ["10.0.0.0/16"]
  },
  "subnets": [
    {
      "name": "subnet1",
      "addressPrefix": "10.0.1.0/24"
    }
  ]
}
```

---

### 4. Explain Azure App Service and its features.

**Answer:**
App Service is a platform-as-a-service for hosting web applications.

**Features:**
- Multiple languages (Node.js, Python, .NET, Java, PHP)
- Auto-scaling
- Deployment slots (staging/production)
- Built-in CI/CD
- SSL certificates
- Custom domains

**App Service Plans:**
- **Free/Shared**: Development/testing
- **Basic**: Production workloads
- **Standard**: Auto-scaling, slots
- **Premium**: Higher performance

---

### 5. What is Azure Storage and its types?

**Answer:**
Azure Storage provides scalable cloud storage.

**Storage Types:**
- **Blob Storage**: Object storage (files, images, videos)
- **Files**: Managed file shares (SMB)
- **Disks**: Persistent disks for VMs
- **Tables**: NoSQL key-value store
- **Queues**: Message queuing

**Blob Storage Tiers:**
- **Hot**: Frequently accessed
- **Cool**: Infrequently accessed
- **Archive**: Long-term archive

---

### 6. Explain Azure Active Directory (Azure AD).

**Answer:**
Azure AD is Microsoft's cloud-based identity and access management service.

**Features:**
- Single Sign-On (SSO)
- Multi-Factor Authentication (MFA)
- Conditional Access
- Application management
- Directory synchronization

**Concepts:**
- **Tenant**: Organization's Azure AD instance
- **Users**: Individual accounts
- **Groups**: Collections of users
- **Applications**: Registered apps
- **Roles**: RBAC roles

---

### 7. What is Azure Key Vault?

**Answer:**
Key Vault is a cloud service for storing secrets, keys, and certificates.

**Features:**
- Secure secret storage
- Key management
- Certificate management
- Access policies
- Audit logging

**Use Cases:**
- Store passwords
- Store API keys
- Store connection strings
- Manage SSL certificates

---

### 8. Explain Azure Monitor and its components.

**Answer:**
Azure Monitor provides comprehensive monitoring and observability.

**Components:**
- **Metrics**: Performance data
- **Logs**: Log Analytics workspace
- **Alerts**: Automated notifications
- **Dashboards**: Visualizations
- **Application Insights**: Application monitoring

**Log Analytics Queries:**
```kusto
// Example KQL query
Perf
| where CounterName == "CPU"
| summarize avg(CounterValue) by Computer, bin(TimeGenerated, 1h)
```

---

### 9. What is Azure Resource Manager (ARM)?

**Answer:**
ARM is the deployment and management service for Azure.

**Features:**
- Resource groups
- Templates (JSON)
- Role-based access control
- Tags
- Locks

**ARM Template Example:**
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2021-09-01",
      "name": "mystorageaccount",
      "location": "eastus",
      "sku": {
        "name": "Standard_LRS"
      }
    }
  ]
}
```

---

### 10. Explain Azure Container Instances (ACI).

**Answer:**
ACI is a serverless container service.

**Features:**
- No infrastructure management
- Pay per second
- Quick startup
- Public/private networking

**Use Cases:**
- Simple container workloads
- Batch jobs
- Development/testing
- Microservices

---

### 11. What is Azure Kubernetes Service (AKS)?

**Answer:**
AKS is a managed Kubernetes service.

**Features:**
- Managed control plane
- Auto-scaling
- Integrated with Azure services
- RBAC support

**Components:**
- **Node Pool**: Group of nodes
- **Add-ons**: Monitoring, networking
- **Identity**: Managed identity integration

---

### 12. Explain Azure DevOps and its services.

**Answer:**
Azure DevOps provides development tools and services.

**Services:**
- **Azure Repos**: Git repositories
- **Azure Pipelines**: CI/CD
- **Azure Boards**: Work tracking
- **Azure Artifacts**: Package management
- **Azure Test Plans**: Test management

---

## 📝 **Best Practices**

1. **Use Resource Groups**: Organize resources
2. **Enable MFA**: Multi-factor authentication
3. **Use NSGs**: Network security
4. **Enable Monitoring**: Use Azure Monitor
5. **Use Tags**: Resource organization
6. **Backup**: Regular backups
7. **Cost Management**: Monitor costs
8. **Security**: Follow security best practices
9. **RBAC**: Use role-based access
10. **Templates**: Use ARM templates

---

**Good luck with your Azure interview preparation! ☁️**
