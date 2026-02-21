import os
import subprocess

score = 0
total_checks = 7
report = []

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
END = "\033[0m"

def run_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
        return output.decode()
    except:
        return ""

def check_firewall():
    global score
    result = run_command("ufw status")
    if "Status: active" in result:
        report.append(GREEN + "[PASS] Firewall is active" + END)
        score += 1
    else:
        report.append(RED + "[FAIL] Firewall is not active" + END)

def check_ssh_root():
    global score
    with open("/etc/ssh/sshd_config", "r") as f:
        data = f.read()
        if "PermitRootLogin no" in data:
            report.append(GREEN + "[PASS] Root login disabled" + END)
            score += 1
        else:
            report.append(RED + "[FAIL] Root login enabled" + END)

def check_ssh_password():
    global score
    with open("/etc/ssh/sshd_config", "r") as f:
        data = f.read()
        if "PasswordAuthentication no" in data:
            report.append(GREEN + "[PASS] Password authentication disabled" + END)
            score += 1
        else:
            report.append(YELLOW + "[WARN] Password authentication enabled" + END)

def check_shadow_permissions():
    global score
    perm = oct(os.stat("/etc/shadow").st_mode)[-3:]
    if perm in ["600", "640"]:
        report.append(GREEN + "[PASS] /etc/shadow permissions secure" + END)
        score += 1
    else:
        report.append(RED + "[FAIL] /etc/shadow permissions insecure" + END)

def check_services():
    global score
    services = run_command("systemctl list-units --type=service --state=running")
    if "telnet" in services:
        report.append(RED + "[FAIL] Telnet service running" + END)
    else:
        report.append(GREEN + "[PASS] No insecure services detected" + END)
        score += 1

def check_rootkit():
    global score
    result = run_command("chkrootkit")
    if "INFECTED" in result:
        report.append(RED + "[FAIL] Rootkit detected" + END)
    else:
        report.append(GREEN + "[PASS] No rootkit detected" + END)
        score += 1

def check_updates():
    global score
    result = run_command("apt list --upgradable 2>/dev/null")
    if "upgradable" not in result:
        report.append(GREEN + "[PASS] System up to date" + END)
        score += 1
    else:
        report.append(YELLOW + "[WARN] Updates available" + END)

check_firewall()
check_ssh_root()
check_ssh_password()
check_shadow_permissions()
check_services()
check_rootkit()
check_updates()

final_score = (score / total_checks) * 100

print("\n===== Linux Hardening Audit Report =====\n")
for item in report:
    print(item)

print("\nSecurity Score: {:.2f}%".format(final_score))

if final_score >= 80:
    print(GREEN + "Risk Level: LOW" + END)
elif final_score >= 50:
    print(YELLOW + "Risk Level: MEDIUM" + END)
else:
    print(RED + "Risk Level: HIGH" + END)
