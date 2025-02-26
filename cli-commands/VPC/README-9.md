# 🧹 Usuwanie zasobów AWS

W tym kroku usunąłem wszystkie zasoby AWS, aby nie ponosić zbędnych kosztów.

---

## **🔄 Usuwanie instancji EC2**  
```bash
aws ec2 terminate-instances   --instance-ids $INSTANCE_ID
```
✅ **Zatrzymuję i usuwam instancję EC2.**  

---

## **🔄 Usuwanie Security Groups**  
```bash
aws ec2 delete-security-group   --group-id $SEC_GROUP_WEB_ID

aws ec2 delete-security-group   --group-id $SEC_GROUP_PRIVATE_ID
```
✅ **Usuwam Security Groups, które były przypisane do instancji.**  

---

## **🔄 Usuwanie klucza SSH**  
```bash
aws ec2 delete-key-pair   --key-name $KEY_NAME

rm -f ${KEY_NAME}.pem
```
✅ **Usuwam klucz SSH z AWS i lokalnego systemu.**  

---

## **🔄 Usuwanie tablic routingu**  
```bash
aws ec2 delete-route-table   --route-table-id $ROUTE_TABLE_PUBLIC_ID

aws ec2 delete-route-table   --route-table-id $ROUTE_TABLE_PRIVATE_ID
```
✅ **Usuwam tablice routingu.**  

---

## **🔄 Odłączenie i usunięcie Internet Gateway**  
```bash
aws ec2 detach-internet-gateway   --internet-gateway-id $IGW_ID   --vpc-id $VPC_ID

aws ec2 delete-internet-gateway   --internet-gateway-id $IGW_ID
```
✅ **Odłączam i usuwam Internet Gateway.**  

---

## **🔄 Usuwanie subnetów**  
```bash
aws ec2 delete-subnet   --subnet-id $SUBNET_PUBLIC_ID

aws ec2 delete-subnet   --subnet-id $SUBNET_PRIVATE_ID
```
✅ **Usuwam subnety w VPC.**  

---

## **🔄 Usuwanie VPC**  
```bash
aws ec2 delete-vpc   --vpc-id $VPC_ID
```
✅ **Usuwam całą VPC i wszystkie pozostałe zasoby.**  

---

## **✅ AWS został wyczyszczony!**  
Wszystkie zasoby zostały usunięte, aby uniknąć dodatkowych kosztów.  

🚀 **Projekt zakończony!**  

