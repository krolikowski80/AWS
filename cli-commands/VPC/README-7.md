# 🌍 Instalacja serwera WWW na EC2

W tym kroku skonfigurowałem instancję EC2 jako serwer WWW.

---

## **8️⃣ Instalacja i konfiguracja serwera WWW**  

> **Apache HTTP Server** to popularny serwer WWW, który pozwala na hostowanie stron internetowych.

📌 **Co zrobiłem w tym kroku?**  
- Zainstalowałem **Apache HTTP Server**.  
- Skonfigurowałem **automatyczne uruchamianie serwera** po restarcie.  
- Dodałem **stronę testową**, aby sprawdzić działanie.  

---

### **🖥️ Aktualizacja pakietów i instalacja Apache**
```bash
sudo yum update -y

sudo yum install -y httpd
```
✅ **Aktualizuję pakiety i instaluję Apache HTTP Server.**  

---

### **🖥️ Uruchomienie serwera Apache**
```bash
sudo systemctl start httpd

sudo systemctl enable httpd
```
✅ **Uruchamiam serwer WWW i włączam jego automatyczne uruchamianie.**  

---

### **🖥️ Tworzenie testowej strony internetowej**
```bash
echo "<h1>Serwer WWW działa poprawnie!</h1>" | sudo tee /var/www/html/index.html
```
✅ **Tworzę stronę testową w katalogu `/var/www/html`.**  

---

### **🖥️ Sprawdzanie statusu serwera Apache**
```bash
sudo systemctl status httpd
```
✅ **Upewniam się, że serwer działa poprawnie.**  

---

### **🖥️ Testowanie dostępu do strony WWW**
```bash
curl http://localhost
```
✅ **Sprawdzam, czy strona testowa jest dostępna lokalnie.**  

---

## **✅ Co dalej?**
1. **Sprawdzam, czy strona jest dostępna z przeglądarki, wpisując `http://PUBLIC_IP`.**  
2. **Jeśli wszystko działa, serwer WWW jest gotowy do użycia!**  
3. **W kolejnym kroku zabezpieczę serwer i zoptymalizuję jego konfigurację.**  

🚀 **Serwer WWW działa na EC2!**  

