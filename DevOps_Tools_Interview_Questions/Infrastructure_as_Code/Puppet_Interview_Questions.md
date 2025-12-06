# Puppet Interview Questions & Answers

## 🚀 **Puppet Fundamentals**

### 1. What is Puppet and how does it work?

**Answer:**
Puppet is a configuration management tool that uses a declarative language to describe the desired state of infrastructure. It follows a client-server (agent-master) model.

**Key Components:**
- **Puppet Master/Server**: Central server that stores manifests and catalogs
- **Puppet Agent**: Runs on managed nodes, applies configurations
- **Manifests**: Puppet code files (.pp) that describe desired state
- **Modules**: Reusable collections of manifests, templates, files
- **Facter**: System information gathering tool
- **Hiera**: Hierarchical data lookup system

**How It Works:**
1. Write manifests on Puppet Master
2. Agent connects to Master (pull model)
3. Master compiles catalog for agent
4. Agent applies catalog to achieve desired state
5. Agent reports back to Master
6. Process repeats (default: every 30 minutes)

**Architecture:**
- **Pull Model**: Agents pull configurations from Master
- **Idempotent**: Running multiple times produces same result
- **Declarative**: Describe what you want, not how to get it

---

### 2. How do you install and configure Puppet?

**Answer:**
**Puppet Master Installation:**

**On Linux:**
```bash
# Download Puppet repository
wget https://apt.puppet.com/puppet7-release-focal.deb
sudo dpkg -i puppet7-release-focal.deb
sudo apt-get update

# Install Puppet Server
sudo apt-get install puppetserver

# Configure
sudo nano /etc/puppetlabs/puppet/puppet.conf

# Start service
sudo systemctl start puppetserver
sudo systemctl enable puppetserver
```

**Puppet Agent Installation:**
```bash
# On managed nodes
sudo apt-get install puppet-agent

# Configure agent
sudo nano /etc/puppetlabs/puppet/puppet.conf
[agent]
server = puppet-master.example.com

# Start agent
sudo systemctl start puppet
sudo systemctl enable puppet
```

**Configuration File:**
```ini
# /etc/puppetlabs/puppet/puppet.conf
[main]
certname = node1.example.com
server = puppet-master.example.com
environment = production

[agent]
runinterval = 30m
```

---

### 3. What are Puppet manifests and how do you write them?

**Answer:**
Manifests are Puppet code files that describe the desired state.

**Basic Manifest:**
```puppet
# /etc/puppetlabs/code/environments/production/manifests/site.pp
node 'web1.example.com' {
  package { 'nginx':
    ensure => present,
  }

  service { 'nginx':
    ensure => running,
    enable => true,
    require => Package['nginx'],
  }

  file { '/etc/nginx/nginx.conf':
    ensure  => file,
    content => template('nginx/nginx.conf.erb'),
    notify  => Service['nginx'],
    require => Package['nginx'],
  }
}
```

**Resource Syntax:**
```puppet
resource_type { 'title':
  attribute => value,
  attribute => value,
}
```

**Common Resources:**
```puppet
# Package
package { 'nginx':
  ensure => present,
}

# Service
service { 'nginx':
  ensure => running,
  enable => true,
}

# File
file { '/etc/nginx/nginx.conf':
  ensure => file,
  source => 'puppet:///modules/nginx/nginx.conf',
  mode   => '0644',
}

# User
user { 'deploy':
  ensure => present,
  home   => '/home/deploy',
  shell  => '/bin/bash',
}

# Group
group { 'www-data':
  ensure => present,
}
```

---

### 4. What are Puppet modules and how do you create them?

**Answer:**
Modules are reusable collections of manifests, templates, files, and facts.

**Module Structure:**
```
modules/
  nginx/
    manifests/
      init.pp
      config.pp
    templates/
      nginx.conf.erb
    files/
      default.conf
    lib/
      facter/
    spec/
    tests/
    README.md
    metadata.json
```

**Creating a Module:**
```bash
# Generate module
puppet module generate myorg-nginx

# Or manually
mkdir -p modules/nginx/{manifests,templates,files}
```

**Module Manifest:**
```puppet
# modules/nginx/manifests/init.pp
class nginx (
  String $package_name = 'nginx',
  String $service_name = 'nginx',
  Integer $worker_processes = 4,
  Integer $port = 80,
) {
  package { $package_name:
    ensure => present,
  }

  service { $service_name:
    ensure => running,
    enable => true,
    require => Package[$package_name],
  }

  file { '/etc/nginx/nginx.conf':
    ensure  => file,
    content => template('nginx/nginx.conf.erb'),
    notify  => Service[$service_name],
    require => Package[$package_name],
  }
}
```

**Using Module:**
```puppet
# In site.pp or other manifest
include nginx

# Or with parameters
class { 'nginx':
  port => 8080,
  worker_processes => 8,
}
```

---

### 5. How do you use variables and facts in Puppet?

**Answer:**
Variables store data, facts provide system information.

**Variables:**
```puppet
# Define variable
$http_port = 80
$server_name = 'example.com'

# Use variable
file { '/etc/nginx/nginx.conf':
  content => "listen ${http_port};",
}

# Class parameters
class nginx ($port = 80) {
  file { '/etc/nginx/nginx.conf':
    content => "listen ${port};",
  }
}
```

**Facts (from Facter):**
```puppet
# Use facts
file { '/etc/hostname':
  content => $facts['hostname'],
}

# Operating system
if $facts['os']['family'] == 'Debian' {
  package { 'nginx':
    ensure => present,
  }
} elsif $facts['os']['family'] == 'RedHat' {
  package { 'nginx':
    ensure => present,
  }
}

# Network
$ip_address = $facts['networking']['ip']
```

**Custom Facts:**
```ruby
# lib/facter/myfact.rb
Facter.add(:myfact) do
  setcode do
    'myvalue'
  end
end
```

---

### 6. How do you use templates in Puppet?

**Answer:**
Templates use ERB (Embedded Ruby) to generate files dynamically.

**Template Example:**
```erb
# modules/nginx/templates/nginx.conf.erb
worker_processes <%= @worker_processes %>;

events {
    worker_connections 1024;
}

http {
    server {
        listen <%= @port %>;
        server_name <%= @server_name %>;
        
        <% if @ssl_enabled -%>
        listen 443 ssl;
        ssl_certificate <%= @ssl_cert_path %>;
        <% end -%>
        
        location / {
            root <%= @web_root %>;
        }
    }
}
```

**Using Template:**
```puppet
class nginx (
  Integer $worker_processes = 4,
  Integer $port = 80,
  String $server_name = 'localhost',
  Boolean $ssl_enabled = false,
  String $ssl_cert_path = '/etc/ssl/cert.pem',
  String $web_root = '/var/www/html',
) {
  file { '/etc/nginx/nginx.conf':
    ensure  => file,
    content => template('nginx/nginx.conf.erb'),
    notify  => Service['nginx'],
  }
}
```

**Template Functions:**
```erb
<%= @variable %>
<%= @array.join(',') %>
<%= @hash['key'] %>
<% if condition -%>
<% end -%>
```

---

### 7. How do you use conditionals and loops in Puppet?

**Answer:**
Puppet supports conditionals and iteration.

**Conditionals:**
```puppet
# If/else
if $facts['os']['family'] == 'Debian' {
  package { 'nginx':
    ensure => present,
  }
} elsif $facts['os']['family'] == 'RedHat' {
  package { 'nginx':
    ensure => present,
  }
} else {
  fail("Unsupported OS: ${facts['os']['family']}")
}

# Case statement
case $facts['os']['family'] {
  'Debian': {
    package { 'nginx': ensure => present }
  }
  'RedHat': {
    package { 'nginx': ensure => present }
  }
  default: {
    fail("Unsupported OS")
  }
}

# Selector
$package_name = $facts['os']['family'] ? {
  'Debian' => 'nginx',
  'RedHat' => 'nginx',
  default  => 'nginx',
}
```

**Loops:**
```puppet
# Each (iteration)
['nginx', 'mysql', 'redis'].each |$package| {
  package { $package:
    ensure => present,
  }
}

# Hash iteration
{
  'user1' => { 'home' => '/home/user1', 'shell' => '/bin/bash' },
  'user2' => { 'home' => '/home/user2', 'shell' => '/bin/zsh' },
}.each |$user, $config| {
  user { $user:
    home  => $config['home'],
    shell => $config['shell'],
  }
}
```

---

### 8. How do you manage relationships and dependencies in Puppet?

**Answer:**
Puppet uses metaparameters to define relationships.

**Metaparameters:**
```puppet
# require (dependency)
package { 'nginx':
  ensure => present,
}

service { 'nginx':
  ensure  => running,
  require => Package['nginx'],  # Service requires package
}

# before
package { 'nginx':
  ensure => present,
  before => Service['nginx'],  # Package before service
}

# notify (triggers refresh)
file { '/etc/nginx/nginx.conf':
  ensure  => file,
  content => template('nginx/nginx.conf.erb'),
  notify  => Service['nginx'],  # File change notifies service
}

# subscribe (subscribes to changes)
service { 'nginx':
  ensure    => running,
  subscribe => File['/etc/nginx/nginx.conf'],  # Service subscribes to file
}

# Chaining
Package['nginx'] -> File['/etc/nginx/nginx.conf'] ~> Service['nginx']
# -> creates dependency, ~> creates notification
```

---

### 9. How do you use Hiera for data management?

**Answer:**
Hiera provides hierarchical data lookup.

**Hiera Configuration:**
```yaml
# /etc/puppetlabs/puppet/hiera.yaml
version: 5
defaults:
  datadir: data
  data_hash: yaml_data
hierarchy:
  - name: "Per-node data"
    path: "nodes/%{trusted.certname}.yaml"
  - name: "Per-environment data"
    path: "environments/%{::environment}.yaml"
  - name: "Common data"
    path: "common.yaml"
```

**Hiera Data:**
```yaml
# data/common.yaml
nginx::port: 80
nginx::worker_processes: 4

# data/environments/production.yaml
nginx::port: 80
nginx::worker_processes: 8

# data/nodes/web1.example.com.yaml
nginx::port: 8080
```

**Using Hiera in Manifests:**
```puppet
# Automatic lookup
class { 'nginx':
  # Parameters automatically looked up from Hiera
}

# Manual lookup
$port = lookup('nginx::port', Integer, 'first', 80)
```

---

### 10. How do you use Puppet environments?

**Answer:**
Environments allow different code versions for different node groups.

**Environment Structure:**
```
/etc/puppetlabs/code/environments/
  production/
    manifests/
      site.pp
    modules/
    data/
  staging/
    manifests/
      site.pp
    modules/
    data/
  development/
    manifests/
      site.pp
    modules/
    data/
```

**Setting Environment:**
```puppet
# In puppet.conf
[agent]
environment = production

# Or via fact
$environment = $facts['environment']
```

**Environment Configuration:**
```ini
# /etc/puppetlabs/puppet/puppet.conf
[main]
environmentpath = $codedir/environments

[production]
modulepath = $environmentpath/production/modules
```

---

### 11. How do you test Puppet code?

**Answer:**
Multiple testing tools available.

**1. Puppet-lint:**
```bash
# Install
gem install puppet-lint

# Run
puppet-lint manifests/
```

**2. rspec-puppet (Unit Testing):**
```ruby
# spec/classes/nginx_spec.rb
require 'spec_helper'

describe 'nginx' do
  it { is_expected.to compile }
  it { is_expected.to contain_package('nginx') }
  it { is_expected.to contain_service('nginx') }
end
```

**3. Beaker (Integration Testing):**
```ruby
# spec/acceptance/nginx_spec.rb
require 'spec_helper_acceptance'

describe 'nginx' do
  it 'should work without errors' do
    pp = <<-EOS
      class { 'nginx': }
    EOS

    apply_manifest(pp, catch_failures: true)
  end
end
```

---

### 12. How do you use Puppet Forge modules?

**Answer:**
Puppet Forge is a repository of pre-built modules.

**Installing Modules:**
```bash
# Install from Forge
puppet module install puppetlabs-nginx

# Install specific version
puppet module install puppetlabs-nginx --version 1.0.0

# Install to specific directory
puppet module install puppetlabs-nginx --target-dir /path/to/modules
```

**Using Forge Modules:**
```puppet
# In manifest
include nginx

# Or with parameters
class { 'nginx':
  package_ensure => 'present',
  service_ensure => 'running',
}
```

**Module Dependencies:**
```json
# metadata.json
{
  "name": "myorg-nginx",
  "dependencies": [
    {
      "name": "puppetlabs-stdlib",
      "version_requirement": ">= 4.0.0"
    }
  ]
}
```

---

## 📝 **Best Practices**

1. **Use modules**: Organize code into reusable modules
2. **Use Hiera**: Separate data from code
3. **Idempotency**: Ensure manifests are idempotent
4. **Version control**: Keep manifests in git
5. **Testing**: Use rspec-puppet and Beaker
6. **Documentation**: Add README and comments
7. **Follow conventions**: Use Puppet style guide
8. **Use facts**: Leverage Facter for system information
9. **Environment management**: Use environments properly
10. **Security**: Use encrypted Hiera for secrets

---

**Good luck with your Puppet interview preparation!**
