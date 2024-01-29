# chrome-password-cli

### Installing dependencies
```bash 
> pip install -r requirements.txt
```
### How to use
```bash
usage: main.py -l --local 'Local State' -d --data 'Login Data'

positional arguments:
   -l, --Local, Treats the Local State file  
   -d, --data, Treats the Login Data file
```
- The files to be resolved in the script contain a specific path on the system.

   Local State path: ```AppData/Local/Google/Chrome/User Data/Local State```
  
   Login Data path: ```AppData/Local/Google/Chrome/User Data/default/Login Data```
  
```bash 
> python3 main.py -l 'Local State' -d 'Login Data'
```