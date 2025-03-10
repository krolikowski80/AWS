# 📌 AWS S3 – Kompletny Poradnik CLI, Polityki, Montowanie

## 📖 Opis
AWS S3 (Simple Storage Service) to skalowalna usługa przechowywania danych w chmurze. Ten poradnik obejmuje:
- Tworzenie i zarządzanie bucketami S3 w **AWS CLI**.
- **Polityki IAM** do kontroli dostępu.
- **Montowanie S3 jako dysk sieciowy** w **Windows i macOS**.

---

## 🔹 1. Tworzenie i zarządzanie bucketami w AWS CLI

### **🔧 Tworzenie bucketa S3**
```bash
aws s3 mb s3://nazwa-twojego-bucketa --region eu-central-1
```
> 📌 Bucket musi mieć unikalną nazwę globalnie.

### **📜 Lista bucketów**
```bash
aws s3 ls
```

### **📂 Wysyłanie plików**
```bash
aws s3 cp lokalny_plik.txt s3://nazwa-twojego-bucketa/
```

### **📥 Pobieranie plików**
```bash
aws s3 cp s3://nazwa-twojego-bucketa/lokalny_plik.txt .
```

### **🗑️ Usunięcie bucketa**
```bash
aws s3 rb s3://nazwa-twojego-bucketa --force
```

---

## 🔹 2. Polityki IAM dla S3

### **📜 Publiczny dostęp do wszystkich obiektów w bucketach** *(Uwaga: każdy ma dostęp!)*
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::nazwa-twojego-bucketa/*"
        }
    ]
}
```
📌 **Zastosowanie:**
- **AWS Console** → **S3** → **Permissions** → **Bucket Policy**.
- Wklej politykę i **zapisz zmiany**.

### **🔒 Prywatny dostęp tylko dla właściciela**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::nazwa-twojego-bucketa/*"
        }
    ]
}
```
📌 **Blokuje dostęp dla wszystkich poza właścicielem.**

---

## 🔹 3. Montowanie S3 jako dysk w Windows

### **🛠 Metoda 1: Rclone (zalecana)**
#### **1️⃣ Instalacja Rclone**
```bash
winget install Rclone
```
#### **2️⃣ Konfiguracja dostępu do AWS**
```bash
rclone config
```
- Wybierz `New remote`
- Nazwa np. **myS3**
- Typ: **s3**
- Wpisz **AWS Access Key ID** i **Secret Access Key**
- Region: `eu-central-1`

#### **3️⃣ Montowanie bucketa jako dysk X:**
```bash
rclone mount myS3:nazwa-twojego-bucketa X: --vfs-cache-mode full
```
#### **4️⃣ Automatyczne montowanie po restarcie**
Dodaj do **Task Scheduler**:
```bash
rclone mount myS3:nazwa-twojego-bucketa X: --vfs-cache-mode full
```

---

### **🛠 Metoda 2: s3fs + WinFsp**
#### **1️⃣ Instalacja zależności**
```bash
winget install WinFsp
winget install s3fs
```
#### **2️⃣ Konfiguracja pliku z poświadczeniami**
```bash
echo "AWS_ACCESS_KEY_ID:AWS_SECRET_ACCESS_KEY" > C:\Users\TwojeKonto\.passwd-s3fs
icacls C:\Users\TwojeKonto\.passwd-s3fs /grant TwojeKonto:F
```
#### **3️⃣ Montowanie bucketa jako dysk X:**
```bash
s3fs nazwa-twojego-bucketa X: -o passwd_file=C:\Users\TwojeKonto\.passwd-s3fs -o url=https://s3.eu-central-1.amazonaws.com
```

---

## 🔹 4. Montowanie S3 jako dysk w macOS

### **🛠 Metoda 1: Rclone (zalecana)**
#### **1️⃣ Instalacja Rclone**
```bash
brew install rclone
```
#### **2️⃣ Konfiguracja dostępu do AWS**
```bash
rclone config
```
#### **3️⃣ Montowanie S3 jako `/Volumes/S3`**
```bash
mkdir -p /Volumes/S3
rclone mount myS3:nazwa-twojego-bucketa /Volumes/S3 --daemon
```
#### **4️⃣ Automatyczne montowanie po restarcie**
Dodaj do `crontab`:
```bash
@reboot /usr/local/bin/rclone mount myS3:nazwa-twojego-bucketa /Volumes/S3 --daemon
```

---

### **🛠 Metoda 2: s3fs**
#### **1️⃣ Instalacja s3fs**
```bash
brew install s3fs
```
#### **2️⃣ Konfiguracja pliku z poświadczeniami**
```bash
echo "AWS_ACCESS_KEY_ID:AWS_SECRET_ACCESS_KEY" > ~/.passwd-s3fs
chmod 600 ~/.passwd-s3fs
```
#### **3️⃣ Montowanie S3 jako `/Volumes/S3`**
```bash
mkdir -p /Volumes/S3
s3fs nazwa-twojego-bucketa /Volumes/S3 -o passwd_file=~/.passwd-s3fs -o allow_other -o url=https://s3.eu-central-1.amazonaws.com
```

---

## ✅ Podsumowanie
| Metoda | Windows | macOS | Zalety |
|--------|---------|--------|--------|
| **Rclone** | ✅ | ✅ | Proste, szybkie, stabilne |
| **s3fs** | ✅ | ✅ | Pełna integracja z systemem |

📌 **Rekomendacja**: **Użyj Rclone, jeśli potrzebujesz prostego montowania.** Jeśli chcesz pełnej integracji – **s3fs**.