echo \" <<'POWERSHELL_SCRIPT' >/dev/null # " | Out-Null
# ===== PowerShell Script Begin =====
venv\Scripts\activate
pip install -qr requirements.txt
flask --app web_app\webapp.py db upgrade
flask --app web_app\webapp.py --debug run
# ====== PowerShell Script End ======
while ( ! $MyInvocation.MyCommand.Source ) { $input_line = Read-Host }
exit
<#
POWERSHELL_SCRIPT


set +o histexpand 2>/dev/null
# ===== Bash Script Begin =====
. venv/bin/activate
pip install -qr requirements.txt
flask --app web_app/webapp.py db upgrade
flask --app web_app/webapp.py --debug run
# ====== Bash Script End ======
case $- in *"i"*) cat /dev/stdin >/dev/null ;; esac
exit
#>