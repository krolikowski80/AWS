# 🔒 Zabezpieczenie i optymalizacja serwera WWW

W tym kroku zabezpieczyłem serwer Apache i zoptymalizowałem jego działanie.

---

## **9️⃣ Zabezpieczenie i optymalizacja serwera**  

> **Dobre praktyki bezpieczeństwa** pomagają chronić serwer przed atakami i optymalizują jego wydajność.

📌 **Co zrobiłem w tym kroku?**  
- Skonfigurowałem **firewalla**, aby ograniczyć dostęp do serwera.  
- Usunąłem **zbędne moduły** Apache.  
- Skonfigurowałem **limit zasobów**, aby zwiększyć wydajność.  

---

### **🖥️ Konfiguracja firewalla**
```bash
sudo yum install -y firewalld

sudo systemctl start firewalld

sudo systemctl enable firewalld

sudo firewall-cmd --permanent --add-service=http

sudo firewall-cmd --permanent --add-service=https

sudo firewall-cmd --reload
```
✅ **Włączam firewalla i zezwalam tylko na ruch HTTP i HTTPS.**  

---

### **🖥️ Usunięcie zbędnych modułów Apache**
```bash
sudo sed -i 's/^LoadModule status_module/#LoadModule status_module/' /etc/httpd/conf/httpd.conf

sudo sed -i 's/^LoadModule autoindex_module/#LoadModule autoindex_module/' /etc/httpd/conf/httpd.conf

sudo systemctl restart httpd
```
✅ **Wyłączam zbędne moduły, aby zwiększyć bezpieczeństwo.**  

---

### **🖥️ Optymalizacja konfiguracji Apache**
```bash
echo "KeepAlive On" | sudo tee -a /etc/httpd/conf/httpd.conf

echo "MaxKeepAliveRequests 100" | sudo tee -a /etc/httpd/conf/httpd.conf

echo "KeepAliveTimeout 5" | sudo tee -a /etc/httpd/conf/httpd.conf

sudo systemctl restart httpd
```
✅ **Włączam `KeepAlive`, aby zmniejszyć liczbę połączeń HTTP i poprawić wydajność.**  

---

## **✅ Co dalej?**
1. **Sprawdzam, czy firewall działa poprawnie (`sudo firewall-cmd --list-all`).**  
2. **Testuję stronę WWW, aby upewnić się, że optymalizacja nie wpłynęła negatywnie na jej działanie.**  
3. **W kolejnym kroku przygotuję instrukcję czyszczenia zasobów AWS.**  

🚀 **Serwer WWW jest teraz zabezpieczony i zoptymalizowany!**  

