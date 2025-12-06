# Chef Interview Questions & Answers

## 🚀 **Chef Fundamentals**

### 1. What is Chef and how does it work?

**Answer:**
Chef is a configuration management and automation platform that uses a "desired state" model. It allows you to define infrastructure as code and automatically configure systems to match that desired state.

**Key Components:**
- **Chef Server**: Central repository for cookbooks, policies, and node data
- **Chef Workstation**: Development machine where you write cookbooks
- **Chef Client (Node)**: Runs on managed nodes, applies configurations
- **Cookbooks**: Collection of recipes, attributes, templates, etc.
- **Recipes**: Sets of instructions for configuring resources
- **Resources**: Desired state declarations (package, service, file, etc.)

**How It Works:**
1. Write cookbooks on workstation
2. Upload cookbooks to Chef Server
3. Chef Client runs periodically on nodes
4. Client pulls cookbooks from server
5. Client applies configurations to achieve desired state
6. Client reports back to server

---

### 2. What is the difference between Chef and Ansible?

**Answer:**

| Feature | Chef | Ansible |
|---------|------|---------|
| **Architecture** | Client-server (or Chef Solo) | Agentless (SSH) |
| **Language** | Ruby DSL | YAML |
| **Learning Curve** | Steeper (Ruby knowledge helps) | Easier (YAML) |
| **Idempotency** | Built-in | Built-in |
| **Push/Pull** | Pull (client pulls from server) | Push (control node pushes) |
| **State Management** | Strong (convergence) | Good |
| **Enterprise Features** | Strong (compliance, reporting) | Good |

**When to Use Chef:**
- Large-scale infrastructure
- Need for compliance and reporting
- Complex state management
- Team familiar with Ruby

**When to Use Ansible:**
- Simpler setup (no server required)
- Quick automation tasks
- Team prefers YAML
- Agentless requirement

---

### 3. How do you install and configure Chef?

**Answer:**
**Chef Workstation Installation:**

**Linux:**
```bash
# Download and install
wget https://packages.chef.io/files/stable/chef-workstation/22.10.1013/ubuntu/20.04/chef-workstation_22.10.1013-1_amd64.deb
sudo dpkg -i chef-workstation_22.10.1013-1_amd64.deb

# Verify
chef --version
```

**macOS:**
```bash
brew install chef-workstation
```

**Chef Client Installation (on nodes):**
```bash
# Using bootstrap script
curl -L https://www.chef.io/chef/install.sh | sudo bash

# Or using package manager
# Ubuntu/Debian
wget https://packages.chef.io/files/stable/chef/17.10.0/ubuntu/20.04/chef_17.10.0-1_amd64.deb
sudo dpkg -i chef_17.10.0-1_amd64.deb
```

**Configuration:**
```ruby
# ~/.chef/config.rb (workstation)
current_dir = File.dirname(__FILE__)
log_level                :info
log_location             STDOUT
node_name                'your-username'
client_key               "#{current_dir}/your-username.pem"
chef_server_url          'https://chef-server.example.com/organizations/myorg'
cookbook_path            ["#{current_dir}/../cookbooks"]
```

---

### 4. What are Chef cookbooks and how do you create them?

**Answer:**
Cookbooks are the fundamental unit of configuration in Chef. They contain recipes, attributes, templates, files, and metadata.

**Creating a Cookbook:**
```bash
# Generate cookbook
chef generate cookbook cookbooks/myapp

# Structure
cookbooks/myapp/
  ├── .delivery/
  ├── .kitchen.yml
  ├── CHANGELOG.md
  ├── LICENSE
  ├── README.md
  ├── attributes/
  │   └── default.rb
  ├── files/
  │   └── default/
  ├── libraries/
  ├── metadata.rb
  ├── recipes/
  │   └── default.rb
  ├── spec/
  │   ├── spec_helper.rb
  │   └── unit/
  │       └── recipes/
  │           └── default_spec.rb
  ├── templates/
  │   └── default/
  └── test/
      └── integration/
          └── default/
              └── default_test.rb
```

**Basic Recipe:**
```ruby
# recipes/default.rb
package 'nginx' do
  action :install
end

service 'nginx' do
  action [:enable, :start]
end

template '/etc/nginx/nginx.conf' do
  source 'nginx.conf.erb'
  variables(
    port: node['nginx']['port'],
    workers: node['nginx']['workers']
  )
  notifies :restart, 'service[nginx]'
end
```

---

### 5. What are Chef resources and what are the common ones?

**Answer:**
Resources represent the desired state of a part of the system.

**Common Resources:**

**1. Package Resource:**
```ruby
package 'nginx' do
  action :install
  version '1.18.0'
end

# Multiple packages
package %w(nginx mysql-server redis-server)
```

**2. Service Resource:**
```ruby
service 'nginx' do
  action [:enable, :start]
  supports restart: true, reload: true
end
```

**3. File Resource:**
```ruby
file '/etc/nginx/nginx.conf' do
  content 'server { listen 80; }'
  mode '0644'
  owner 'root'
  group 'root'
  action :create
end

# Create directory
directory '/var/www/html' do
  owner 'www-data'
  group 'www-data'
  mode '0755'
  recursive true
end
```

**4. Template Resource:**
```ruby
template '/etc/nginx/nginx.conf' do
  source 'nginx.conf.erb'
  variables(
    port: 80,
    server_name: 'example.com'
  )
  notifies :restart, 'service[nginx]'
end
```

**5. User Resource:**
```ruby
user 'deploy' do
  comment 'Deployment user'
  home '/home/deploy'
  shell '/bin/bash'
  password '$1$salt$hashedpassword'
end
```

**6. Execute/Command Resource:**
```ruby
execute 'run script' do
  command '/usr/bin/script.sh'
  creates '/path/to/result'
  action :run
end
```

---

### 6. How do you use attributes in Chef?

**Answer:**
Attributes define configuration data for nodes.

**Attribute Precedence (lowest to highest):**
1. Default (in cookbook)
2. Force default (in cookbook)
3. Normal (set on node)
4. Override (in cookbook)
5. Force override (in cookbook)
6. Automatic (Ohai facts)

**Defining Attributes:**
```ruby
# attributes/default.rb
default['myapp']['port'] = 80
default['myapp']['workers'] = 4
default['myapp']['user'] = 'www-data'

# Using in recipe
node['myapp']['port']
```

**Setting Attributes:**
```ruby
# In recipe
node.default['myapp']['port'] = 8080
node.override['myapp']['port'] = 9000
node.normal['myapp']['port'] = 80
```

**Role Attributes:**
```ruby
# roles/webserver.rb
name "webserver"
description "Web server role"
run_list "recipe[nginx]"
default_attributes(
  "nginx" => {
    "port" => 80
  }
)
```

---

### 7. How do you use templates in Chef?

**Answer:**
Templates use ERB (Embedded Ruby) to generate files dynamically.

**Template Example:**
```erb
# templates/default/nginx.conf.erb
server {
    listen <%= @port %>;
    server_name <%= @server_name %>;
    
    <% if @ssl_enabled -%>
    listen 443 ssl;
    ssl_certificate <%= @ssl_cert_path %>;
    <% end -%>
    
    location / {
        root <%= @web_root %>;
        index index.html;
    }
    
    <% @backends.each do |backend| -%>
    location <%= backend['path'] %> {
        proxy_pass http://<%= backend['host'] %>:<%= backend['port'] %>;
    }
    <% end -%>
}
```

**Using Template:**
```ruby
template '/etc/nginx/nginx.conf' do
  source 'nginx.conf.erb'
  variables(
    port: node['nginx']['port'],
    server_name: node['nginx']['server_name'],
    ssl_enabled: node['nginx']['ssl_enabled'],
    ssl_cert_path: node['nginx']['ssl_cert_path'],
    web_root: node['nginx']['web_root'],
    backends: node['nginx']['backends']
  )
  notifies :restart, 'service[nginx]'
end
```

---

### 8. What are Chef notifications and subscriptions?

**Answer:**
Notifications and subscriptions allow resources to trigger actions on other resources.

**Notifications (notifies):**
```ruby
template '/etc/nginx/nginx.conf' do
  source 'nginx.conf.erb'
  notifies :restart, 'service[nginx]', :immediately
  # or
  notifies :reload, 'service[nginx]', :delayed
end

service 'nginx' do
  action :nothing
end
```

**Subscriptions (subscribes):**
```ruby
service 'nginx' do
  action :nothing
  subscribes :restart, 'template[/etc/nginx/nginx.conf]', :immediately
end
```

**Timing:**
- `:immediately`: Run at end of resource execution
- `:delayed`: Run at end of Chef run (default)
- `:before`: Run before resource execution

---

### 9. How do you use Chef roles and environments?

**Answer:**
Roles and environments help organize and manage infrastructure.

**Creating a Role:**
```ruby
# roles/webserver.rb
name "webserver"
description "Web server role"
run_list(
  "recipe[nginx]",
  "recipe[myapp::web]"
)
default_attributes(
  "nginx" => {
    "port" => 80
  }
)
override_attributes(
  "myapp" => {
    "environment" => "production"
  }
)
```

**Using Roles:**
```bash
# Apply role to node
knife node run_list add node1.example.com "role[webserver]"
```

**Creating an Environment:**
```ruby
# environments/production.rb
name "production"
description "Production environment"
cookbook_versions(
  "nginx" => "1.0.0",
  "myapp" => "2.0.0"
)
default_attributes(
  "myapp" => {
    "environment" => "production"
  }
)
override_attributes(
  "nginx" => {
    "workers" => 8
  }
)
```

**Using Environments:**
```bash
# Set environment for node
knife node environment set node1.example.com production
```

---

### 10. How do you test Chef cookbooks?

**Answer:**
Multiple testing tools available for Chef.

**1. ChefSpec (Unit Testing):**
```ruby
# spec/unit/recipes/default_spec.rb
require 'chefspec'

describe 'myapp::default' do
  let(:chef_run) { ChefSpec::SoloRunner.new.converge(described_recipe) }

  it 'installs nginx' do
    expect(chef_run).to install_package('nginx')
  end

  it 'starts nginx service' do
    expect(chef_run).to enable_service('nginx')
    expect(chef_run).to start_service('nginx')
  end

  it 'creates nginx config' do
    expect(chef_run).to create_template('/etc/nginx/nginx.conf')
  end
end
```

**2. Test Kitchen (Integration Testing):**
```yaml
# .kitchen.yml
---
driver:
  name: vagrant

provisioner:
  name: chef_solo

platforms:
  - name: ubuntu-20.04
  - name: centos-8

suites:
  - name: default
    run_list:
      - recipe[myapp::default]
    attributes:
```

**Running Tests:**
```bash
# Run ChefSpec
chef exec rspec

# Run Test Kitchen
kitchen test
kitchen converge
kitchen verify
```

---

### 11. How do you use Chef with Chef Server vs Chef Solo?

**Answer:**
**Chef Server (Client-Server):**
- Centralized management
- Node data stored on server
- Search functionality
- Better for large infrastructures

**Chef Solo / Local Mode:**
- No server required
- All data local
- Simpler setup
- Good for development/testing

**Using Chef Solo:**
```bash
# Run with chef-solo
chef-solo -c solo.rb -j node.json

# solo.rb
file_cache_path "/tmp/chef-solo"
cookbook_path ["/path/to/cookbooks"]
role_path ["/path/to/roles"]
```

**Using Chef Local Mode:**
```bash
# Run with chef-client in local mode
chef-client --local-mode --runlist 'recipe[myapp]'
```

---

### 12. How do you manage data bags in Chef?

**Answer:**
Data bags store global data (passwords, API keys, etc.) in JSON format.

**Creating Data Bag:**
```bash
# Create data bag
knife data bag create users

# Create data bag item
knife data bag create users alice
# Edit in editor, then save
```

**Data Bag Item:**
```json
{
  "id": "alice",
  "username": "alice",
  "password": "$1$salt$hashed",
  "groups": ["sudo", "docker"]
}
```

**Using Data Bag:**
```ruby
# In recipe
user_data = data_bag_item('users', 'alice')

user user_data['username'] do
  password user_data['password']
  groups user_data['groups']
end
```

**Encrypted Data Bags:**
```bash
# Create secret
openssl rand -base64 512 > secret_key

# Create encrypted data bag
knife data bag create --secret-file secret_key users alice
```

```ruby
# In recipe
user_data = data_bag_item('users', 'alice', IO.read('/path/to/secret_key'))
```

---

### 13. How do you use Chef search?

**Answer:**
Search allows querying node data from Chef Server.

**Search Examples:**
```ruby
# Search for all nodes
nodes = search(:node, '*:*')

# Search by attribute
web_servers = search(:node, 'role:webserver')

# Search with query
db_servers = search(:node, 'role:database AND chef_environment:production')

# Use in recipe
search(:node, 'role:webserver').each do |web_node|
  puts "Web server: #{web_node['fqdn']}"
end
```

**Search from Command Line:**
```bash
# Search nodes
knife search node "role:webserver"

# Search with query
knife search node "chef_environment:production AND role:database"
```

---

## 📝 **Best Practices**

1. **Use version control**: Keep cookbooks in git
2. **Test cookbooks**: Use ChefSpec and Test Kitchen
3. **Follow naming conventions**: Use descriptive names
4. **Use attributes**: Make cookbooks configurable
5. **Idempotency**: Ensure recipes are idempotent
6. **Documentation**: Add README and comments
7. **Use roles and environments**: Organize infrastructure
8. **Security**: Use encrypted data bags for secrets
9. **Version cookbooks**: Use semantic versioning
10. **Code review**: Review cookbooks before deployment

---

**Good luck with your Chef interview preparation!**
