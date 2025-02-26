# 🔗 Połączenie z instancją EC2 przez SSH

W tym kroku połączę się do mojej instancji EC2 za pomocą **SSH**.

---

## **7️⃣ Połączenie do EC2 przez SSH**  

> **SSH (Secure Shell)** umożliwia bezpieczne zdalne zarządzanie instancją EC2.

📌 **Co zrobiłem w tym kroku?**  
- Sprawdziłem **publiczny adres IP** instancji.  
- Połączyłem się do instancji za pomocą **SSH i klucza `.pem`**.  

---

### **🖥️ Pobranie publicznego IP instancji**
```bash
PUBLIC_IP=$(aws ec2 describe-instances   --instance-ids $INSTANCE_ID   --query 'Reservations[0].Instances[0].PublicIpAddress'   --output text)

echo "PUBLIC_IP=$PUBLIC_IP" >> .env

echo "Instancja EC2 jest dostępna pod adresem: $PUBLIC_IP"
```
✅ **Pobieram publiczny adres IP instancji EC2 i zapisuję go do `.env`.**  

---

### **🖥️ Połączenie przez SSH**
```bash
ssh -i ${KEY_NAME}.pem ec2-user@$PUBLIC_IP
```
✅ **Łączę się do instancji EC2 jako użytkownik `ec2-user`.**  

---

### **🖥️ Sprawdzanie, czy instancja działa**
```bash
aws ec2 describe-instance-status   --instance-ids $INSTANCE_ID   --query 'InstanceStatuses[*].[InstanceId, InstanceState.Name, SystemStatus.Status, InstanceStatus.Status]'   --output table
```
✅ **Sprawdzam status instancji (`running` oraz `ok`).**  

---

## **✅ Co dalej?**
1. **Upewniam się, że mogę zalogować się do instancji EC2 przez SSH.**  
2. **Jeśli połączenie działa, mogę skonfigurować dodatkowe usługi na instancji.**  
3. **W kolejnym kroku przygotuję instancję do działania jako serwer WWW.**  

🚀 **Połączenie SSH do instancji EC2 działa!**  

