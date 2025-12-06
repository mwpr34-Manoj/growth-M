# Linux Interview Questions & Answers

## 🐧 **Linux Fundamentals**

### 1. What is Linux and what are its key features?

**Answer:**
Linux is an open-source, Unix-like operating system kernel created by Linus Torvalds. It's the foundation for many operating systems (distributions).

**Key Features:**
- **Open Source**: Free and modifiable
- **Multi-user**: Multiple users can use the system simultaneously
- **Multi-tasking**: Can run multiple processes concurrently
- **Security**: User permissions, file permissions, SELinux
- **Stability**: Reliable and stable
- **Flexibility**: Highly customizable
- **Command-line**: Powerful CLI tools
- **Package Management**: Easy software installation (apt, yum, dnf)

**Popular Distributions:**
- **Ubuntu**: User-friendly, Debian-based
- **CentOS/RHEL**: Enterprise-focused, Red Hat-based
- **Debian**: Stable, community-driven
- **Fedora**: Cutting-edge, Red Hat-sponsored
- **Arch Linux**: Minimal, rolling release

---

### 2. What is the Linux file system hierarchy?

**Answer:**
Linux follows the Filesystem Hierarchy Standard (FHS).

**Key Directories:**
```
/                    # Root directory
├── /bin             # Essential binaries (ls, cp, mv)
├── /sbin            # System binaries (fdisk, ifconfig)
├── /boot             # Boot loader files
├── /dev              # Device files
├── /etc              # Configuration files
├── /home             # User home directories
├── /lib              # Shared libraries
├── /opt              # Optional software
├── /proc             # Process information (virtual)
├── /root             # Root user home
├── /run              # Runtime data
├── /tmp              # Temporary files
├── /usr              # User programs
│   ├── /usr/bin      # User binaries
│   ├── /usr/lib      # User libraries
│   └── /usr/local    # Local software
└── /var              # Variable data (logs, cache)
    ├── /var/log      # Log files
    └── /var/cache    # Cache files
```

---

### 3. What are Linux file permissions and how do you manage them?

**Answer:**
Linux uses a permission system with three types: read (r), write (w), execute (x).

**Permission Types:**
- **Owner (u)**: File owner permissions
- **Group (g)**: Group permissions
- **Others (o)**: Everyone else permissions

**Permission Values:**
- **Read (r)**: 4
- **Write (w)**: 2
- **Execute (x)**: 1

**Viewing Permissions:**
```bash
ls -l file.txt
# Output: -rw-r--r-- 1 user group 1024 Jan 1 12:00 file.txt
#         ^  ^  ^
#         |  |  |
#         |  |  +-- Others: r--
#         |  +----- Group: r--
#         +-------- Owner: rw-
```

**Changing Permissions:**
```bash
# Using chmod with numbers
chmod 755 file.txt    # rwxr-xr-x
chmod 644 file.txt    # rw-r--r--
chmod 700 file.txt    # rwx------

# Using chmod with symbols
chmod u+x file.txt    # Add execute for owner
chmod g-w file.txt    # Remove write for group
chmod o+r file.txt    # Add read for others
chmod a+x file.txt    # Add execute for all (a=all)

# Recursive
chmod -R 755 directory/
```

**Changing Ownership:**
```bash
# Change owner
chown user file.txt

# Change owner and group
chown user:group file.txt

# Recursive
chown -R user:group directory/
```

---

### 4. What are the essential Linux commands?

**Answer:**
**File Operations:**
```bash
# List files
ls                    # List files
ls -l                 # Long format
ls -a                 # Include hidden files
ls -lh                # Human-readable sizes

# Change directory
cd /path/to/dir       # Change directory
cd ~                  # Home directory
cd -                  # Previous directory
cd ..                 # Parent directory

# Create/remove directories
mkdir dirname         # Create directory
mkdir -p dir1/dir2    # Create with parents
rmdir dirname         # Remove empty directory
rm -rf dirname        # Remove directory and contents

# Copy/move files
cp file1 file2       # Copy file
cp -r dir1 dir2       # Copy directory
mv file1 file2       # Move/rename file

# Remove files
rm file.txt           # Remove file
rm -f file.txt        # Force remove
rm -rf directory/     # Remove directory recursively

# View files
cat file.txt          # Display file content
less file.txt         # Page through file
head file.txt         # First 10 lines
tail file.txt         # Last 10 lines
tail -f file.txt      # Follow file (logs)
```

**Text Processing:**
```bash
# Search
grep "pattern" file.txt
grep -r "pattern" directory/
grep -i "pattern" file.txt    # Case insensitive

# Find
find /path -name "*.txt"
find /path -type f -name "*.log"
find /path -mtime -7          # Modified in last 7 days

# Sort and filter
sort file.txt
uniq file.txt
cut -d: -f1 file.txt          # Cut by delimiter
awk '{print $1}' file.txt     # Print first column
sed 's/old/new/g' file.txt    # Replace text
```

**System Information:**
```bash
# System info
uname -a                      # Kernel info
hostname                     # Hostname
whoami                       # Current user
id                           # User and group IDs

# Process management
ps                           # Running processes
ps aux                       # All processes
top                          # Interactive process viewer
htop                         # Enhanced top
kill PID                     # Kill process
killall process_name         # Kill by name

# System resources
free -h                      # Memory usage
df -h                        # Disk usage
du -sh directory/            # Directory size
lscpu                        # CPU information
uptime                       # System uptime
```

---

### 5. How do you manage processes in Linux?

**Answer:**
**Process Management:**
```bash
# View processes
ps                           # Current processes
ps aux                       # All processes (BSD style)
ps -ef                       # All processes (Unix style)
ps aux | grep process_name   # Find specific process

# Interactive process viewer
top                          # Default top
htop                         # Enhanced version (install separately)

# Process information
pgrep process_name           # Find process ID
pidof process_name           # Get PID
pstree                       # Process tree

# Kill processes
kill PID                     # Send TERM signal
kill -9 PID                  # Force kill (SIGKILL)
killall process_name         # Kill by name
pkill process_name           # Kill by pattern

# Background processes
command &                    # Run in background
nohup command &              # Run in background, survive logout
jobs                         # List background jobs
fg %1                        # Bring job to foreground
bg %1                        # Send job to background
```

**Process Signals:**
```bash
# Common signals
SIGHUP (1)   # Hangup
SIGINT (2)   # Interrupt (Ctrl+C)
SIGQUIT (3)  # Quit
SIGKILL (9)  # Kill (cannot be caught)
SIGTERM (15) # Terminate (default)
```

---

### 6. How do you manage users and groups in Linux?

**Answer:**
**User Management:**
```bash
# Create user
useradd username
useradd -m -s /bin/bash username    # With home directory and shell
useradd -g groupname username       # With primary group

# Delete user
userdel username
userdel -r username                 # Remove home directory

# Modify user
usermod -aG groupname username      # Add to group
usermod -s /bin/zsh username        # Change shell
usermod -L username                  # Lock account
usermod -U username                  # Unlock account

# Change password
passwd username                      # Change password
passwd -l username                   # Lock password

# User information
id username                          # User ID and groups
whoami                               # Current user
w                                    # Who is logged in
last                                 # Last logged in users
```

**Group Management:**
```bash
# Create group
groupadd groupname

# Delete group
groupdel groupname

# Modify group
groupmod -n newname oldname          # Rename group
groupmod -g 1001 groupname           # Change GID

# Add user to group
usermod -aG groupname username
gpasswd -a username groupname

# Remove user from group
gpasswd -d username groupname

# Group information
groups username                      # User's groups
getent group groupname               # Group information
```

---

### 7. How do you manage packages in Linux?

**Answer:**
**Debian/Ubuntu (apt):**
```bash
# Update package list
sudo apt update

# Upgrade packages
sudo apt upgrade
sudo apt full-upgrade

# Install package
sudo apt install package_name

# Remove package
sudo apt remove package_name
sudo apt purge package_name          # Remove with config

# Search packages
apt search keyword

# Package information
apt show package_name
apt list --installed

# Clean
sudo apt clean
sudo apt autoremove
```

**RHEL/CentOS/Fedora (yum/dnf):**
```bash
# Update packages
sudo yum update
sudo dnf update

# Install package
sudo yum install package_name
sudo dnf install package_name

# Remove package
sudo yum remove package_name
sudo dnf remove package_name

# Search packages
yum search keyword
dnf search keyword

# Package information
yum info package_name
dnf info package_name

# Clean
sudo yum clean all
sudo dnf clean all
```

---

### 8. How do you manage services in Linux?

**Answer:**
**systemd (Modern Linux):**
```bash
# Service status
systemctl status service_name

# Start/stop/restart
sudo systemctl start service_name
sudo systemctl stop service_name
sudo systemctl restart service_name
sudo systemctl reload service_name

# Enable/disable (start on boot)
sudo systemctl enable service_name
sudo systemctl disable service_name

# List services
systemctl list-units --type=service
systemctl list-units --type=service --state=running

# Service information
systemctl show service_name
```

**SysV init (Legacy):**
```bash
# Service management
sudo service service_name start
sudo service service_name stop
sudo service service_name restart
sudo service service_name status

# Enable/disable
sudo chkconfig service_name on
sudo chkconfig service_name off
```

---

### 9. How do you manage disk space and partitions?

**Answer:**
**Disk Usage:**
```bash
# Disk usage
df -h                    # Human-readable disk usage
df -h /                  # Specific mount point
du -h                    # Directory usage
du -sh directory/        # Summary of directory
du -h --max-depth=1      # One level deep

# Find large files
find / -type f -size +100M    # Files larger than 100MB
find / -type f -size +1G      # Files larger than 1GB
```

**Partition Management:**
```bash
# List partitions
lsblk                    # Block devices
fdisk -l                 # Partition table
parted -l                # Partition information

# Mount/Unmount
mount /dev/sda1 /mnt
umount /mnt
mount -a                 # Mount all in /etc/fstab

# Filesystem
mkfs.ext4 /dev/sda1      # Create ext4 filesystem
fsck /dev/sda1           # Check filesystem
```

**fstab Configuration:**
```bash
# /etc/fstab
/dev/sda1  /mnt  ext4  defaults  0  2
# Device  Mount  FS    Options  Dump  Pass
```

---

### 10. How do you manage networking in Linux?

**Answer:**
**Network Configuration:**
```bash
# Interface information
ip addr show              # Show IP addresses
ip link show             # Show network interfaces
ifconfig                 # Legacy command

# Network configuration
ip addr add 192.168.1.10/24 dev eth0
ip link set eth0 up
ip link set eth0 down

# Routing
ip route show             # Show routes
ip route add default via 192.168.1.1
ip route del default

# Network connectivity
ping google.com
traceroute google.com
netstat -tulpn            # Network connections
ss -tulpn                 # Modern netstat
```

**Firewall (iptables/firewalld):**
```bash
# iptables
sudo iptables -L          # List rules
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# firewalld
sudo firewall-cmd --list-all
sudo firewall-cmd --add-port=80/tcp --permanent
sudo firewall-cmd --reload
```

---

### 11. How do you manage logs in Linux?

**Answer:**
**Log Locations:**
```bash
/var/log/syslog           # System log
/var/log/messages          # General messages
/var/log/auth.log         # Authentication
/var/log/kern.log         # Kernel log
/var/log/apache2/         # Apache logs
/var/log/nginx/           # Nginx logs
```

**Viewing Logs:**
```bash
# System logs
journalctl                # systemd logs
journalctl -u service_name
journalctl -f             # Follow logs
journalctl --since "1 hour ago"

# Log files
tail -f /var/log/syslog
less /var/log/syslog
grep "error" /var/log/syslog
```

**Log Rotation:**
```bash
# /etc/logrotate.d/
# Configure log rotation
/var/log/app/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

### 12. How do you use cron for scheduling tasks?

**Answer:**
**Cron Syntax:**
```
* * * * * command
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, Sunday = 0 or 7)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

**Examples:**
```bash
# Every minute
* * * * * command

# Every hour
0 * * * * command

# Daily at midnight
0 0 * * * command

# Weekly on Sunday
0 0 * * 0 command

# Monthly on 1st
0 0 1 * * command

# Every 5 minutes
*/5 * * * * command
```

**Managing Cron:**
```bash
# Edit crontab
crontab -e                # Edit user crontab
crontab -l                # List crontab
crontab -r                # Remove crontab

# System cron
sudo nano /etc/crontab
sudo nano /etc/cron.d/custom
```

---

### 13. How do you secure a Linux system?

**Answer:**
**Security Practices:**
```bash
# User management
# - Use strong passwords
# - Limit sudo access
# - Disable root login (SSH)

# SSH Security
# /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no    # Use keys only
Port 2222                    # Change default port

# Firewall
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp

# SELinux/AppArmor
getenforce                   # Check SELinux status
setenforce 1                 # Enable SELinux

# File permissions
chmod 600 ~/.ssh/id_rsa      # Private keys
chmod 644 ~/.ssh/id_rsa.pub  # Public keys

# Updates
sudo apt update && sudo apt upgrade
```

---

## 📝 **Best Practices**

1. **Regular updates**: Keep system updated
2. **User management**: Use least privilege
3. **Backup**: Regular backups
4. **Monitoring**: Monitor system resources
5. **Logging**: Review logs regularly
6. **Security**: Follow security best practices
7. **Documentation**: Document configurations
8. **Testing**: Test changes in non-production
9. **Automation**: Use scripts for repetitive tasks
10. **Version control**: Track configuration changes

---

**Good luck with your Linux interview preparation!**
