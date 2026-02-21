🔐 Linux Hardening Audit Report

Author: Mohammed Nihal
Platform: Kali Linux (VirtualBox – Oracle VM)
Kernel Version: 6.18.9-kali
Audit Date: 21 Feb 2026

1️⃣ Objective

The objective of this project was to design and implement a Linux Hardening Audit Tool to evaluate system security configuration against CIS-style best practices. The tool audits firewall status, SSH hardening, file permissions, rootkit presence, running services, and system updates, generating a compliance score and risk classification.

2️⃣ Environment Setup

The audit was performed on a Kali Linux virtual machine configured in Oracle VirtualBox. The following security tools were installed and configured:

UFW (Firewall)

OpenSSH Server

chkrootkit

rkhunter

Lynis

auditd

fail2ban

net-tools

All packages were successfully installed and updated using apt.

SSH service was enabled and confirmed running via systemctl status ssh.

3️⃣ Firewall Configuration

The UFW firewall was enabled and configured.

Command executed:

sudo ufw enable
sudo ufw status

Findings:

Firewall status: Active

Port 22 (SSH) allowed

Port 80 denied

Custom deny rule for external IP

Firewall configuration is properly active and enforced.

4️⃣ SSH Security Assessment

SSH configuration file:
/etc/ssh/sshd_config

Current settings identified:

PermitRootLogin yes
PasswordAuthentication yes
Security Impact:

Root login enabled → Security risk

Password authentication enabled → Brute-force risk

SSH service was confirmed running and listening on port 22 via netstat -tulnp.

5️⃣ Rootkit and Malware Scan
chkrootkit Scan

Executed without root privileges initially, then properly audited.

Results:

No rootkits detected

All tested binaries reported “not infected”

rkhunter Installation

Installed successfully

Rootkit Hunter version 1.4.6 configured

No malicious indicators detected.

6️⃣ Lynis System Audit

Lynis version 3.1.6 was executed:

sudo lynis audit system

System identified as:

OS: Kali Linux (Rolling)

Architecture: x86_64

Kernel: 6.18.9-kali

Lynis completed successfully with standard hardening recommendations for SSH and authentication.

7️⃣ Custom Python Audit Tool Results

The developed tool performed automated checks on:

Firewall status

SSH root login

SSH password authentication

File permissions (/etc/shadow)

Insecure services

Rootkit detection

Pending updates

Output:
[PASS] Firewall is active
[FAIL] Root login enabled
[WARN] Password authentication enabled
[PASS] /etc/shadow permissions secure
[PASS] No insecure services detected
[PASS] No rootkit detected
[WARN] Updates available
Security Score:

57.14%

Risk Level:

MEDIUM

8️⃣ Identified Security Gaps
Issue	Risk Level	Recommendation
Root SSH login enabled	High	Set PermitRootLogin no
Password authentication enabled	Medium	Disable & use key-based authentication
Pending updates	Medium	Run full system upgrade
SSH open to all networks	Medium	Restrict allowed IPs
9️⃣ Hardening Recommendations

Disable SSH root login:

PermitRootLogin no

Disable password authentication:

PasswordAuthentication no

Restart SSH:

sudo systemctl restart ssh

Apply pending updates:

sudo apt upgrade -y

Configure Fail2Ban to prevent brute-force attacks.

🔟 Conclusion

The Linux Hardening Audit Tool successfully evaluated system security posture and provided a quantifiable compliance score.

The system currently falls under Medium Risk (57.14%), primarily due to insecure SSH configuration and pending updates.

Firewall configuration and rootkit integrity checks passed successfully, indicating no malware presence and active network protection.

After implementing recommended hardening measures, the expected security score would exceed 80%, placing the system in a Low Risk category.
