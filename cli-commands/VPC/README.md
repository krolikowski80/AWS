# 🌐 Konfiguracja VPC w AWS
## **1️⃣ Tworzenie VPC**

> VPC (Virtual Private Cloud) to prywatna sieć w AWS, w której będę umieszczać swoje zasoby.

📌 **Parametry VPC:**  
- **CIDR:** `10.0.0.0/16` (przestrzeń adresowa, pozwala na 65 536 adresów)  
- **Nazwa:** `"MyVPC"`  
- **Włączę DNS Hostnames**, aby instancje EC2 mogły uzyskać nazwy domenowe  

### **🖥️ Tworzenie VPC**
```bash
VPC_ID=$(aws ec2 create-vpc \
--cidr-block 10.0.0.0/16 \
--query 'Vpc.VpcId' \
--output text)

echo "VPC_ID=$VPC_ID" >> .env
```
✅ **Tworzę VPC i zapisuję jego ID do pliku `.env` dla przyszłego użycia.**  

### **🖥️ Nadanie nazwy VPC**
```bash
aws ec2 create-tags \
--resources $VPC_ID \
--tags Key=Name,Value="MyVPC"
```
✅ **Nadaję VPC nazwę `"MyVPC"`, aby łatwo je znaleźć w AWS Console.**  

### **🖥️ Włączenie obsługi DNS hostnames**
```bash
aws ec2 modify-vpc-attribute \
--vpc-id $VPC_ID \
--enable-dns-hostnames
```
✅ **Włączam obsługę DNS hostnames, aby EC2 mogły mieć nazwy domenowe.**  

---

## **2️⃣ Usunięcie domyślnej tablicy routingu i utworzenie własnych**

> AWS automatycznie tworzy domyślną tablicę routingu. Ponieważ chcę pełną kontrolę, usuwam ją i tworzę własne.

### **🖥️ Sprawdzam domyślną tablicę routingu**
```bash
ROUTE_TABLE_MAIN_ID=$(aws ec2 describe-route-tables \
--filters "Name=vpc-id,Values=$VPC_ID" "Name=association.main,Values=true" \
--query 'RouteTables[0].RouteTableId' \
--output text)

echo "ROUTE_TABLE_MAIN_ID=$ROUTE_TABLE_MAIN_ID"
```
✅ **Pobieram ID domyślnej tablicy routingu.**  

### **🖥️ Tworzę własne tablice routingu**
```bash
# Publiczna tablica routingu
ROUTE_TABLE_PUBLIC_ID=$(aws ec2 create-route-table \
--vpc-id $VPC_ID \
--query 'RouteTable.RouteTableId' \
--output text)

echo "ROUTE_TABLE_PUBLIC_ID=$ROUTE_TABLE_PUBLIC_ID" >> .env

aws ec2 create-tags \
--resources $ROUTE_TABLE_PUBLIC_ID \
--tags Key=Name,Value="MyPublicRouteTable"

# Prywatna tablica routingu
ROUTE_TABLE_PRIVATE_ID=$(aws ec2 create-route-table \
--vpc-id $VPC_ID \
--query 'RouteTable.RouteTableId' \
--output text)

echo "ROUTE_TABLE_PRIVATE_ID=$ROUTE_TABLE_PRIVATE_ID" >> .env

aws ec2 create-tags \
--resources $ROUTE_TABLE_PRIVATE_ID \
--tags Key=Name,Value="MyPrivateRouteTable"
```
✅ **Tworzę dwie tablice routingu: `"MyPublicRouteTable"` i `"MyPrivateRouteTable"`.**  

### **🖥️ Przypisuję subnety do tablic routingu**
```bash
aws ec2 associate-route-table \
--route-table-id $ROUTE_TABLE_PUBLIC_ID \
--subnet-id $SUBNET_PUBLIC_ID

aws ec2 associate-route-table \
--route-table-id $ROUTE_TABLE_PRIVATE_ID \
--subnet-id $SUBNET_PRIVATE_ID
```
✅ **Publiczny subnet korzysta teraz z `"MyPublicRouteTable"`, a prywatny z `"MyPrivateRouteTable"`.**  

### **🖥️ Usuwam domyślną tablicę routingu**
```bash
aws ec2 delete-route-table \
--route-table-id $ROUTE_TABLE_MAIN_ID
```
✅ **Usuwam domyślną tablicę routingu, ponieważ mam już własne.**  

---

## **3️⃣ Sprawdzam konfigurację**

### **🖥️ Sprawdzam wszystkie tablice routingu**
```bash
aws ec2 describe-route-tables   --query 'RouteTables[*].[RouteTableId, Associations[*].SubnetId, Tags]'   --output table
```
✅ **Upewniam się, że subnety są poprawnie przypisane.**  

---
<br><br>

# 🌐 Konfiguracja Internet Gateway (IGW) w AWS

W tym kroku dodałem **Internet Gateway (IGW)** do mojej VPC, aby umożliwić instancjom w publicznym subnecie dostęp do Internetu.

---

## **3️⃣ Tworzenie Internet Gateway (IGW)**  

> **Internet Gateway (IGW)** umożliwia instancjom w **publicznym subnecie** dostęp do Internetu oraz odbieranie połączeń z sieci publicznej.

- Utworzyłem **Internet Gateway**  
- Przypisałem go do **VPC**  
- Skonfigurowałem **trasę do Internetu** w publicznej tablicy routingu  

---

### **🖥️ Tworzenie Internet Gateway**
```bash
IGW_ID=$(aws ec2 create-internet-gateway \
--query 'InternetGateway.InternetGatewayId' \
--output text)

echo "IGW_ID=$IGW_ID" >> .env
```
✅ **Tworzę IGW i zapisuję jego ID do pliku `.env` do dalszego użycia.**  

---

### **🖥️ Nadanie nazwy Internet Gateway**
```bash
aws ec2 create-tags \
--resources $IGW_ID \
--tags Key=Name,Value="MyInternetGateway"
```
✅ **Nadaję IGW nazwę `"MyInternetGateway"`**, aby łatwo je znaleźć w AWS Console.  

---

### **🖥️ Przypisanie IGW do VPC**
```bash
aws ec2 attach-internet-gateway \
--internet-gateway-id $IGW_ID \
--vpc-id $VPC_ID
```
✅ **Przypisuję IGW do VPC**, aby umożliwić dostęp do Internetu.  

---

### **🖥️ Konfiguracja trasy do Internetu**
> Muszę dodać trasę `0.0.0.0/0 → IGW_ID` w publicznej tablicy routingu.

```bash
aws ec2 create-route \
--route-table-id $ROUTE_TABLE_PUBLIC_ID \
--destination-cidr-block 0.0.0.0/0 \
--gateway-id $IGW_ID
```
✅ **Dodaję trasę dla całego ruchu (`0.0.0.0/0`) do Internet Gateway.**  

---

### **🖥️ Sprawdzam trasę w tablicy routingu**
```bash
aws ec2 describe-route-tables   --route-table-id $ROUTE_TABLE_PUBLIC_ID   --query 'Routes'   --output table
```
✅ **Sprawdzam, czy tablica `"MyPublicRouteTable"` zawiera trasę do Internet Gateway.**  

---

🚀 **VPC jest teraz połączone z Internetem!**  

# 🔐 Konfiguracja Security Groups w AWS

W tym kroku utworzyłem **Security Groups (SG)**, które kontrolują ruch sieciowy do i z instancji EC2.

---

## **4️⃣ Tworzenie Security Groups**  

> **Security Groups (SG)** określają, jakie połączenia są dozwolone do instancji EC2.  
> Tworzę dwie grupy:  
> - `MyWebSG` → dla serwera webowego w **publicznym subnecie** (HTTP + SSH)  
> - `MyPrivateSG` → dla instancji w **prywatnym subnecie** (tylko ruch wewnętrzny)  

📌 **Reguły Security Groups**  
| Security Group | Porty | Źródło |
|---------------|-------|--------|
| `MyWebSG` | `80 (HTTP)` | `0.0.0.0/0` (Internet) |
| `MyWebSG` | `22 (SSH)` | **Mój IP** (zalecane, nie `0.0.0.0/0`) |
| `MyPrivateSG` | `ALL` | `10.0.0.0/16` (tylko wewnętrzny ruch w VPC) |

---

### **🖥️ Tworzenie Security Group dla serwera webowego**
```bash
SEC_GROUP_WEB_ID=$(aws ec2 create-security-group \
--group-name "MyWebSG" \
--description "Security Group for Web Server"  \
--vpc-id $VPC_ID \
--query 'GroupId' \
--output text)

echo "SEC_GROUP_WEB_ID=$SEC_GROUP_WEB_ID" >> .env
```
✅ **Tworzę Security Group `MyWebSG` dla instancji w publicznym subnecie.**  

---

### **🖥️ Zezwolenie na ruch HTTP (port 80)**
```bash
aws ec2 authorize-security-group-ingress \
--group-id $SEC_GROUP_WEB_ID \
--protocol tcp \
--port 80 \
--cidr 0.0.0.0/0
```
✅ **Zezwalam na dostęp HTTP z dowolnego adresu (`0.0.0.0/0`).**  

---

### **🖥️ Zezwolenie na SSH (port 22) tylko z mojego IP**
```bash
MY_IP=$(curl -s http://checkip.amazonaws.com)

aws ec2 authorize-security-group-ingress \
--group-id $SEC_GROUP_WEB_ID \
--protocol tcp \
--port 22 \
--cidr ${MY_IP}/32
```
✅ **Zezwalam na SSH tylko z mojego IP (zalecane).**  

---

### **🖥️ Tworzenie Security Group dla prywatnej instancji**
```bash
SEC_GROUP_PRIVATE_ID=$(aws ec2 create-security-group \
--group-name "MyPrivateSG" \
--description "Security Group for Private Instance" \
--vpc-id $VPC_ID \
--query 'GroupId' \
--output text)

echo "SEC_GROUP_PRIVATE_ID=$SEC_GROUP_PRIVATE_ID" >> .env
```
✅ **Tworzę Security Group `MyPrivateSG` dla instancji w prywatnym subnecie.**  

---

### **🖥️ Zezwolenie na ruch wewnętrzny w VPC**
```bash
aws ec2 authorize-security-group-ingress \
--group-id $SEC_GROUP_PRIVATE_ID \
--protocol -1 \
--cidr 10.0.0.0/16
```
✅ **Pozwalam na cały ruch wewnętrzny w obrębie VPC.**  

---

# 🔑 Tworzenie klucza SSH do logowania na EC2
---

## **5️⃣ Tworzenie klucza SSH**  

> **Klucz SSH** jest wymagany do bezpiecznego logowania się do instancji EC2 w AWS.

---

### **🖥️ Tworzenie klucza SSH**
```bash
KEY_NAME="MyAWSKey"

aws ec2 create-key-pair \
--key-name $KEY_NAME \
--query 'KeyMaterial' \
--output text > ${KEY_NAME}.pem
```
✅ **Tworzę klucz SSH o nazwie `"MyAWSKey"` i zapisuję go do pliku `.pem`.**  

---

### **🖥️ Nadanie odpowiednich uprawnień do pliku klucza**
```bash
chmod 400 ${KEY_NAME}.pem
```
✅ **Ustawiam uprawnienia, aby plik klucza był bezpieczny (`chmod 400`).**  

---

### **🖥️ Zapisywanie nazwy klucza w `.env` do dalszego użycia**
```bash
echo "KEY_NAME=$KEY_NAME" >> .env
```
✅ **Zapisuję nazwę klucza do `.env`, aby móc go później wykorzystać.**  

---

### **🖥️ Sprawdzanie, czy klucz został utworzony**
```bash
aws ec2 describe-key-pairs \
--query 'KeyPairs[*].KeyName' \
--output table
```
✅ **Sprawdzam, czy klucz `"MyAWSKey"` został dodany do AWS.**  

---
# 🖥️ Tworzenie instancji EC2
---

## **6️⃣ Tworzenie instancji EC2**  

> **EC2 (Elastic Compute Cloud)** to usługa AWS umożliwiająca uruchamianie maszyn wirtualnych.

---

### **🖥️ Pobranie ID najnowszego Amazon Linux 2 AMI**
```bash
AMI_ID=$(aws ec2 describe-images \
--owners amazon \
--filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" \
          "Name=state,Values=available" \
--query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' \
--output text)
echo "AMI_ID=$AMI_ID" >> .env
```
✅ **Pobieram ID najnowszego Amazon Linux 2 AMI dla t2.micro i zapisuję go do `.env`.**  

---

### **🖥️ Tworzenie instancji EC2**
```bash
INSTANCE_ID=$(aws ec2 run-instances \
--image-id $AMI_ID \
--instance-type t2.micro \
--key-name $KEY_NAME \
--security-group-ids $SEC_GROUP_WEB_ID \
--subnet-id $SUBNET_PUBLIC_ID \
--query 'Instances[0].InstanceId' \
--output text)

echo "INSTANCE_ID=$INSTANCE_ID" >> .env
```
✅ **Tworzę instancję EC2 (`t2.micro`) i zapisuję jej ID do `.env`.**  

---

### **🖥️ Nadanie nazwy instancji**
```bash
aws ec2 create-tags \
--resources $INSTANCE_ID \
--tags Key=Name,Value="MyPublicEC2"
```
✅ **Nadaję instancji nazwę `"MyPublicEC2"` w AWS Console.**  

---

### **🖥️ Sprawdzanie statusu instancji**
```bash
aws ec2 describe-instances \
--instance-ids $INSTANCE_ID \
--query 'Reservations[*].Instances[*].[InstanceId, State.Name, PublicIpAddress]' \
--output table
```
✅ **Sprawdzam, czy instancja działa oraz jaki ma publiczny adres IP.**  

---
