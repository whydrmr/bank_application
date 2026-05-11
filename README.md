# Bank Account & Budget Management System Application

A Python-based banking application for managing multiple accounts, transactions, and budgets with Caesar cipher encryption for data security.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/whydrmr/bank_application.git
cd bank_application
cd bank
```


### 2. Create a virtual environment (recommended)


**Linux/macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```
**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```


### 3. Install dependencies
```bash
pip install -r requirements.txt
```

**GUI Version (tkinter required):** 

tkinter is part of Python's standard library but may need system-level installation: 

**Linux:**
```bash
# Ubuntu/Debian/Mint
sudo apt-get install python3-tk

# Arch/Manjaro
sudo pacman -S tk

# Fedora/RHEL/CentOS
sudo dnf install python3-tkinter
```
**macOS/Windows:** tkinter is included with Python from python.org 

**Verify installation:**
```bash
python -m tkinter
```

### 4. Structure

```bash
bank/
│
├── core/              
├── ui/                           
└── requirements.txt
```

### 5. Account File Encryption

Before running the application, the account file must be encrypted.

The project uses a simple Caesar cipher system for educational purposes.

## Expected File Format

Replace a file named:

```bash
bank/core/compte.txt
```

Each line must follow this format:

```txt
IDENTIFIANT*MOTDEPASSE*NOM*CLE
```

Example:

```txt
1234*5678*Thomas*4321
9876*1111*Alice*8765
```

---

## Encrypt the File

Run the encryption script:

```bash
python cryptage.py
```

This will generate:

```bash
bank/core/compte_crypte.txt
```

The encrypted file is the one used by the application.

### 6. Run the program in /bank_application directory:
```bash
python -m bank.ui.main
```
