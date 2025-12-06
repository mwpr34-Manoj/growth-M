# HashiCorp Vault Interview Questions & Answers

## 🔐 **Vault Fundamentals**

### 1. What is HashiCorp Vault and what are its key features?

**Answer:**
Vault is a tool for securely storing and accessing secrets.

**Key Features:**
- **Secret Management**: Store and access secrets
- **Dynamic Secrets**: Generate secrets on-demand
- **Encryption as a Service**: Encrypt/decrypt data
- **Access Control**: Fine-grained access policies
- **Audit Logging**: Track all access

**Use Cases:**
- Store API keys
- Store database credentials
- Manage certificates
- Encrypt application data

---

### 2. How do you install and configure Vault?

**Answer:**
**Installation:**
```bash
# Download
wget https://releases.hashicorp.com/vault/1.15.0/vault_1.15.0_linux_amd64.zip
unzip vault_1.15.0_linux_amd64.zip
sudo mv vault /usr/local/bin/

# Verify
vault version
```

**Configuration:**
```hcl
# config.hcl
storage "file" {
  path = "/var/lib/vault/data"
}

listener "tcp" {
  address = "127.0.0.1:8200"
  tls_disable = 1
}
```

**Start Vault:**
```bash
vault server -config=config.hcl
```

---

### 3. How do you use Vault for secret management?

**Answer:**
**Initialization:**
```bash
# Initialize Vault
vault operator init

# Unseal Vault
vault operator unseal <key>
```

**Storing Secrets:**
```bash
# Write secret
vault kv put secret/myapp username=admin password=secret123

# Read secret
vault kv get secret/myapp

# List secrets
vault kv list secret/
```

**Using Secrets:**
```bash
# Get secret value
vault kv get -field=password secret/myapp
```

---

### 4. What are Vault policies and how do you create them?

**Answer:**
Policies define what a user can access.

**Policy Example:**
```hcl
# policy.hcl
path "secret/data/myapp/*" {
  capabilities = ["read"]
}

path "secret/data/myapp" {
  capabilities = ["read", "list"]
}
```

**Apply Policy:**
```bash
# Create policy
vault policy write my-policy policy.hcl

# Assign to user
vault write auth/userpass/users/alice \
  password=password \
  policies=my-policy
```

---

### 5. How do you use Vault with dynamic secrets?

**Answer:**
Dynamic secrets are generated on-demand.

**Enable Database Secrets Engine:**
```bash
# Enable database secrets engine
vault secrets enable database

# Configure database
vault write database/config/mydb \
  plugin_name=postgresql-database-plugin \
  allowed_roles="readonly" \
  connection_url="postgresql://{{username}}:{{password}}@db:5432/mydb" \
  username="vault" \
  password="vaultpass"

# Create role
vault write database/roles/readonly \
  db_name=mydb \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';" \
  default_ttl="1h" \
  max_ttl="24h"
```

**Get Dynamic Secret:**
```bash
vault read database/creds/readonly
```

---

## 📝 **Best Practices**

1. **Unseal Keys**: Store unseal keys securely
2. **Policies**: Use least privilege
3. **Audit Logging**: Enable audit logs
4. **Rotation**: Rotate secrets regularly
5. **Backup**: Regular backups
6. **High Availability**: Use HA setup
7. **Encryption**: Use TLS
8. **Access Control**: Proper authentication

---

**Good luck with your Vault interview preparation! 🔐**
