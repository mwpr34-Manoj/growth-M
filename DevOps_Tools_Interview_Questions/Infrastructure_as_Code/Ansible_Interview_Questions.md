# Ansible Interview Questions & Answers

## 🚀 **Ansible Fundamentals**

### 1. What is Ansible and how does it work?

**Answer:**
Ansible is an open-source automation tool for configuration management, application deployment, and task automation. It uses a simple, agentless architecture and YAML-based playbooks.

**Key Features:**
- **Agentless**: No agents required on target machines
- **Idempotent**: Running the same playbook multiple times produces the same result
- **Simple**: YAML-based syntax, easy to learn
- **Powerful**: Can manage thousands of servers
- **Extensible**: Large collection of modules and plugins

**How It Works:**
1. Ansible connects to target machines via SSH (Linux) or WinRM (Windows)
2. Pushes modules to target machines
3. Executes modules and removes them
4. Returns results to control node
5. No persistent agent required

**Architecture:**
- **Control Node**: Machine running Ansible
- **Managed Nodes**: Servers being managed
- **Inventory**: List of managed nodes
- **Playbooks**: Automation scripts (YAML)
- **Modules**: Units of work (copy, file, service, etc.)

---

### 2. How do you install and configure Ansible?

**Answer:**
**Installation:**

**On Linux (Control Node):**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ansible

# RHEL/CentOS
sudo yum install ansible
# or
sudo dnf install ansible

# Using pip
pip3 install ansible
```

**On macOS:**
```bash
brew install ansible
```

**Configuration:**
```bash
# Create ansible.cfg
mkdir -p ~/ansible
cd ~/ansible
cat > ansible.cfg <<EOF
[defaults]
inventory = ./inventory
remote_user = ansible
private_key_file = ~/.ssh/id_rsa
host_key_checking = False
roles_path = ./roles
EOF

# Or use system-wide config
sudo nano /etc/ansible/ansible.cfg
```

**Verify Installation:**
```bash
ansible --version
ansible all -m ping
```

---

### 3. What is an Ansible inventory and how do you create one?

**Answer:**
Inventory is a list of hosts that Ansible manages.

**Basic Inventory (INI format):**
```ini
# inventory.ini
[webservers]
web1.example.com
web2.example.com

[dbservers]
db1.example.com
db2.example.com

[all:vars]
ansible_user=ansible
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

**YAML Format Inventory:**
```yaml
# inventory.yml
all:
  children:
    webservers:
      hosts:
        web1.example.com:
          ansible_host: 192.168.1.10
        web2.example.com:
          ansible_host: 192.168.1.11
      vars:
        http_port: 80
    dbservers:
      hosts:
        db1.example.com:
          ansible_host: 192.168.1.20
      vars:
        db_port: 5432
    production:
      children:
        webservers:
        dbservers:
      vars:
        environment: production
```

**Dynamic Inventory:**
```bash
# AWS EC2 dynamic inventory
ansible-inventory -i aws_ec2.yml --list

# Using plugins
ansible-inventory -i inventory.yml --list
```

**Using Inventory:**
```bash
# List all hosts
ansible-inventory --list

# List specific group
ansible-inventory --host web1.example.com

# Test connectivity
ansible webservers -m ping
```

---

### 4. What are Ansible playbooks and how do you write them?

**Answer:**
Playbooks are YAML files that define automation tasks.

**Basic Playbook:**
```yaml
# playbook.yml
---
- name: Install and configure Nginx
  hosts: webservers
  become: yes
  vars:
    http_port: 80
    max_clients: 200
  tasks:
    - name: Install Nginx
      apt:
        name: nginx
        state: present
        update_cache: yes
      when: ansible_os_family == "Debian"

    - name: Start and enable Nginx
      systemd:
        name: nginx
        state: started
        enabled: yes

    - name: Configure Nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: restart nginx

  handlers:
    - name: restart nginx
      systemd:
        name: nginx
        state: restarted
```

**Running Playbooks:**
```bash
# Run playbook
ansible-playbook playbook.yml

# Run with specific inventory
ansible-playbook -i inventory.yml playbook.yml

# Run with extra variables
ansible-playbook playbook.yml -e "http_port=8080"

# Run with tags
ansible-playbook playbook.yml --tags "install"

# Check mode (dry-run)
ansible-playbook playbook.yml --check

# Verbose output
ansible-playbook playbook.yml -v
ansible-playbook playbook.yml -vvv
```

---

### 5. What are Ansible modules and how do you use them?

**Answer:**
Modules are units of work that Ansible executes on target hosts.

**Common Modules:**

**1. File Management:**
```yaml
- name: Create directory
  file:
    path: /opt/myapp
    state: directory
    mode: '0755'

- name: Copy file
  copy:
    src: /local/file.txt
    dest: /remote/file.txt
    mode: '0644'

- name: Create file with content
  copy:
    content: "Hello World\n"
    dest: /tmp/hello.txt
```

**2. Package Management:**
```yaml
- name: Install package (Debian/Ubuntu)
  apt:
    name: nginx
    state: present
    update_cache: yes

- name: Install package (RHEL/CentOS)
  yum:
    name: nginx
    state: present

- name: Install multiple packages
  apt:
    name:
      - nginx
      - mysql-server
    state: present
```

**3. Service Management:**
```yaml
- name: Start service
  systemd:
    name: nginx
    state: started
    enabled: yes

- name: Restart service
  systemd:
    name: nginx
    state: restarted
```

**4. User Management:**
```yaml
- name: Create user
  user:
    name: ansible
    groups: sudo
    append: yes
    shell: /bin/bash

- name: Add SSH key
  authorized_key:
    user: ansible
    state: present
    key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
```

**5. Command Execution:**
```yaml
- name: Run command
  command: /usr/bin/command arg1 arg2
  args:
    creates: /path/to/file

- name: Run shell command
  shell: |
    echo "Hello"
    echo "World"
  register: result

- name: Display result
  debug:
    var: result.stdout
```

---

### 6. What are Ansible roles and how do you create them?

**Answer:**
Roles are reusable, organized collections of playbooks, variables, and files.

**Role Structure:**
```
roles/
  nginx/
    tasks/
      main.yml
    handlers/
      main.yml
    templates/
      nginx.conf.j2
    files/
      default.conf
    vars/
      main.yml
    defaults/
      main.yml
    meta/
      main.yml
    README.md
```

**Creating a Role:**
```bash
# Create role structure
ansible-galaxy init nginx
```

**Role Tasks (roles/nginx/tasks/main.yml):**
```yaml
---
- name: Install Nginx
  apt:
    name: nginx
    state: present

- name: Configure Nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: restart nginx

- name: Start Nginx
  systemd:
    name: nginx
    state: started
    enabled: yes
```

**Using Roles:**
```yaml
# playbook.yml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  roles:
    - nginx
    - role: mysql
      vars:
        db_name: myapp
        db_user: appuser
```

**Installing Roles from Galaxy:**
```bash
# Install role
ansible-galaxy install geerlingguy.nginx

# Install from requirements file
ansible-galaxy install -r requirements.yml
```

---

### 7. How do you use variables in Ansible?

**Answer:**
Variables allow dynamic configuration in playbooks.

**Variable Precedence (lowest to highest):**
1. Command line values (`-e`)
2. Role defaults (`roles/role/defaults/main.yml`)
3. Inventory file or script group vars
4. Inventory group_vars/all
5. Playbook group_vars/all
6. Inventory group_vars/group_name
7. Playbook group_vars/group_name
8. Inventory host_vars/hostname
9. Playbook host_vars/hostname
10. Host facts
11. Play vars
12. Play vars_prompt
13. Play vars_files
14. Role vars (`roles/role/vars/main.yml`)
15. Block vars
16. Task vars
17. Include vars
18. Set_facts / registered vars
19. Role (and include_role) params
20. Include params
21. Extra vars (`-e`)

**Defining Variables:**
```yaml
# In playbook
- name: Configure server
  hosts: webservers
  vars:
    http_port: 80
    max_clients: 200
  tasks:
    - name: Use variable
      debug:
        msg: "Port is {{ http_port }}"
```

**Using Variable Files:**
```yaml
# playbook.yml
- name: Configure server
  hosts: webservers
  vars_files:
    - vars/main.yml
    - vars/secrets.yml
```

**Group Variables:**
```yaml
# group_vars/webservers.yml
http_port: 80
nginx_workers: 4
```

**Host Variables:**
```yaml
# host_vars/web1.yml
http_port: 8080
```

**Facts (Gathered automatically):**
```yaml
- name: Display facts
  debug:
    var: ansible_facts

- name: Use fact
  debug:
    msg: "OS is {{ ansible_facts['os_family'] }}"
```

---

### 8. How do you use templates in Ansible?

**Answer:**
Templates use Jinja2 templating to generate files dynamically.

**Template Example:**
```jinja2
# templates/nginx.conf.j2
server {
    listen {{ http_port }};
    server_name {{ server_name }};
    
    {% if ssl_enabled %}
    listen 443 ssl;
    ssl_certificate {{ ssl_cert_path }};
    {% endif %}
    
    location / {
        root {{ web_root }};
        index index.html;
    }
    
    {% for backend in backends %}
    location {{ backend.path }} {
        proxy_pass http://{{ backend.host }}:{{ backend.port }};
    }
    {% endfor %}
}
```

**Using Templates:**
```yaml
- name: Configure Nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    mode: '0644'
  notify: restart nginx
  vars:
    http_port: 80
    server_name: example.com
    ssl_enabled: true
    backends:
      - path: /api
        host: api.example.com
        port: 8080
```

**Template Filters:**
```jinja2
{{ variable | upper }}
{{ variable | lower }}
{{ variable | default('default_value') }}
{{ list | join(',') }}
{{ path | basename }}
```

---

### 9. What are Ansible handlers and when do you use them?

**Answer:**
Handlers are tasks that run only when notified by other tasks.

**Example:**
```yaml
---
- name: Configure Nginx
  hosts: webservers
  tasks:
    - name: Update Nginx config
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: restart nginx

    - name: Update SSL certificate
      copy:
        src: cert.pem
        dest: /etc/nginx/cert.pem
      notify:
        - restart nginx
        - reload nginx

  handlers:
    - name: restart nginx
      systemd:
        name: nginx
        state: restarted

    - name: reload nginx
      systemd:
        name: nginx
        state: reloaded
```

**Handler Characteristics:**
- Run only when notified
- Run at the end of play, even if notified multiple times
- Run in the order listed, not order notified
- Only run if notifying task changed something

**Flushing Handlers:**
```yaml
- name: Some task
  template:
    src: file.j2
    dest: /etc/file.conf
  notify: restart service

- name: Flush handlers
  meta: flush_handlers

- name: Another task
  command: /usr/bin/command
```

---

### 10. How do you implement conditionals and loops in Ansible?

**Answer:**
Ansible supports conditionals and loops for dynamic task execution.

**Conditionals:**
```yaml
- name: Install package on Debian
  apt:
    name: nginx
    state: present
  when: ansible_os_family == "Debian"

- name: Install package on RHEL
  yum:
    name: nginx
    state: present
  when: ansible_os_family == "RedHat"

- name: Deploy to production
  command: /usr/bin/deploy
  when:
    - environment == "production"
    - deploy_enabled | bool
```

**Loops:**
```yaml
# Simple loop
- name: Create users
  user:
    name: "{{ item }}"
    state: present
  loop:
    - alice
    - bob
    - charlie

# Loop with dictionary
- name: Create users with details
  user:
    name: "{{ item.name }}"
    groups: "{{ item.groups }}"
    shell: "{{ item.shell }}"
  loop:
    - name: alice
      groups: sudo
      shell: /bin/bash
    - name: bob
      groups: docker
      shell: /bin/zsh

# Loop with list
- name: Install packages
  apt:
    name: "{{ item }}"
    state: present
  loop: "{{ packages }}"
  vars:
    packages:
      - nginx
      - mysql-server
      - redis-server
```

**Combining Conditionals and Loops:**
```yaml
- name: Create directories
  file:
    path: "{{ item.path }}"
    state: directory
  loop: "{{ directories }}"
  when: item.create | default(true)
```

---

### 11. How do you manage secrets in Ansible?

**Answer:**
Multiple approaches for managing sensitive data.

**1. Ansible Vault:**
```bash
# Encrypt file
ansible-vault create secrets.yml

# Encrypt existing file
ansible-vault encrypt secrets.yml

# Edit encrypted file
ansible-vault edit secrets.yml

# View encrypted file
ansible-vault view secrets.yml

# Decrypt file
ansible-vault decrypt secrets.yml
```

**Using Vault:**
```yaml
# secrets.yml (encrypted)
db_password: secret123
api_key: key456
```

```yaml
# playbook.yml
- name: Configure app
  hosts: webservers
  vars_files:
    - secrets.yml
  tasks:
    - name: Use secret
      debug:
        msg: "Password is {{ db_password }}"
```

**Running with Vault:**
```bash
# Prompt for password
ansible-playbook playbook.yml --ask-vault-pass

# Use password file
ansible-playbook playbook.yml --vault-password-file ~/.vault_pass

# Use environment variable
export ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass
ansible-playbook playbook.yml
```

**2. External Secret Managers:**
```yaml
- name: Get secret from HashiCorp Vault
  community.hashi_vault.vault_read:
    secret: secret/data/myapp
  register: vault_secret

- name: Use secret
  debug:
    msg: "{{ vault_secret.data.data.password }}"
```

---

### 12. How do you implement error handling in Ansible?

**Answer:**
Multiple strategies for handling errors.

**1. Ignore Errors:**
```yaml
- name: Try to remove file
  file:
    path: /tmp/file.txt
    state: absent
  ignore_errors: yes
```

**2. Failed When:**
```yaml
- name: Check service status
  command: systemctl status myservice
  register: result
  failed_when: "'active' not in result.stdout"
```

**3. Rescue Blocks:**
```yaml
- name: Attempt deployment
  block:
    - name: Deploy application
      command: /usr/bin/deploy
    - name: Verify deployment
      uri:
        url: http://localhost/health
        status_code: 200
  rescue:
    - name: Rollback
      command: /usr/bin/rollback
    - name: Notify failure
      mail:
        to: admin@example.com
        subject: "Deployment failed"
  always:
    - name: Cleanup
      file:
        path: /tmp/deploy
        state: absent
```

**4. Retry Logic:**
```yaml
- name: Wait for service
  uri:
    url: http://localhost/health
    status_code: 200
  register: result
  until: result.status == 200
  retries: 5
  delay: 10
```

---

### 13. How do you use Ansible for Windows?

**Answer:**
Ansible can manage Windows machines using WinRM.

**Prerequisites:**
- WinRM enabled on Windows hosts
- Python installed on control node
- pywinrm package

**Configuration:**
```yaml
# inventory.yml
windows:
  hosts:
    win1.example.com:
      ansible_host: 192.168.1.10
      ansible_user: Administrator
      ansible_password: Password123
      ansible_connection: winrm
      ansible_winrm_transport: ntlm
```

**Windows Modules:**
```yaml
- name: Install IIS
  win_feature:
    name: IIS-WebServerRole
    state: present

- name: Start service
  win_service:
    name: Spooler
    state: started

- name: Create user
  win_user:
    name: ansible
    password: Password123
    groups: Administrators

- name: Copy file
  win_copy:
    src: /local/file.txt
    dest: C:\temp\file.txt
```

---

### 14. How do you optimize Ansible performance?

**Answer:**
**Optimization Strategies:**

1. **Use Pipelining:**
```ini
# ansible.cfg
[defaults]
pipelining = True
```

2. **Enable Fact Caching:**
```ini
# ansible.cfg
[defaults]
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
```

3. **Use Async Tasks:**
```yaml
- name: Long running task
  command: /usr/bin/long-task
  async: 3600
  poll: 10
  register: result
```

4. **Parallel Execution:**
```bash
# Run with forks
ansible-playbook playbook.yml -f 10
```

5. **Use Tags:**
```yaml
- name: Install packages
  apt:
    name: nginx
  tags: install

- name: Configure
  template:
    src: config.j2
    dest: /etc/config
  tags: config
```

```bash
# Run only tagged tasks
ansible-playbook playbook.yml --tags "install"
```

---

## 📝 **Best Practices**

1. **Use roles**: Organize playbooks into reusable roles
2. **Idempotency**: Ensure tasks are idempotent
3. **Use handlers**: For service restarts and reloads
4. **Version control**: Keep playbooks in git
5. **Use vault**: Encrypt sensitive data
6. **Documentation**: Add comments and README files
7. **Testing**: Test playbooks in check mode first
8. **Inventory management**: Use dynamic inventories when possible
9. **Error handling**: Implement proper error handling
10. **Performance**: Use fact caching and pipelining

---

**Good luck with your Ansible interview preparation!**
