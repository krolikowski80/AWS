# 📌 Zadanie: Baza Studentów na AWS RDS z Python

## 📖 Opis

Ten projekt zawiera skrypty w Pythonie do tworzenia i zarządzania bazą danych **MySQL na AWS RDS**.

- `create_database.py` – tworzy bazę MySQL na AWS RDS i zapisuje jej endpoint do pliku `.env`.
- `students.py` – umożliwia dodawanie studentów, ocen i ich wyświetlanie, korzystając z bazy na AWS.
- `.env` – przechowuje dane konfiguracyjne bazy i Security Group.

---

> 📌 Zainstaluję odpowiednie pakiety:
>
> ```bash
> pip install boto3 mysql-connector-python python-dotenv
> ```

---

## 📂 Struktura projektu

```
/aws_rds_project
│── .env                  # Plik z danymi konfiguracyjnymi
│── create_database.py     # Tworzy bazę MySQL na AWS RDS i zapisuje endpoint do .env
│── students.py            # Program do zarządzania studentami (korzysta z .env)
```

---

## 🔹 1. Konfiguracja `.env`

Najpierw utworzę plik `.env`, który będzie przechowywał dane konfiguracyjne:
<details>
  <summary>📜 .env`</summary>

> ```bash
> AWS_REGION=us-east-1
> DB_INSTANCE_IDENTIFIER=student-database
> DB_NAME=student_db
> DB_USERNAME=admin
> DB_PASSWORD=SuperTajneHaslo123
> DB_INSTANCE_CLASS=db.t3.micro
> DB_STORAGE=20
> DB_ENGINE=mysql
> DB_VERSION=8.0
> DB_ENDPOINT=
> SECURITY_GROUP_ID=
> ```
</details>
---

## 🔹 2. Tworzenie Security Group dla RDS

> 📌 Aby utworzyć Security Group:
>
> ```bash
> SECURITY_GROUP_ID=$(aws ec2 create-security-group \
      --group-name rds-access-sg \
      --description "Security Group dla RDS" \
      --vpc-id \
          $(aws ec2 describe-vpcs \
          --query "Vpcs[0].VpcId" \
          --output text) \
      --query "GroupId" \
      --output text)
> echo "SECURITY_GROUP_ID=$SECURITY_GROUP_ID" >> .env
> ```

> 📌 Dodaje regułę dla MySQL (port 3306, dostęp z internetu):
>
> ```bash
> aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 3306 \
    --cidr 0.0.0.0/32
> ```

---

## 🔹 3. Tworzenie bazy danych na AWS RDS

Sskrypt `create_database.py` utworzy instancję MySQL na AWS i zapisze jej **endpoint** do `.env`.
>
> ```bash
> python create_database.py
> ```
>
> Skrypt:
>
> - Tworzy bazę na AWS RDS.
> - Czeka na jej gotowość.
> - Aktualizuje plik `.env` o `DB_ENDPOINT`.

🔎 Po zakończeniu w `.env` pojawi się `DB_ENDPOINT=student-database.xxxx.us-east-1.rds.amazonaws.com`.

---

## 🔹 4. Korzystanie z bazy: `students.py`

Program `students.py` umożliwia zarządzanie studentami i ocenami w bazie.

> 📌 Uruchomienie:
>
> ```bash
> python students.py
> ```
>
> Wybierz opcję:
> 1️⃣ Dodaj studenta
> 2️⃣ Dodaj ocenę
> 3️⃣ Wyświetl studentów
> 4️⃣ Wyjście

---

## 🔹 5. Sprawdzenie bazy MySQL w AWS CLI

Aby sprawdzić listę baz w MySQL RDS:

> 📌 Połącz się do MySQL przez CLI:
>
> ```bash
> mysql -h your-db-endpoint.rds.amazonaws.com -u admin -p
> ```
>
> Jakie mamy tablice:
>
> ```sql
> SHOW DATABASES;
> ```

---

## 🔹 6. Usunięcie bazy RDS

Aby usunąć bazę MySQL w AWS RDS:

> ```bash
> aws rds delete-db-instance \
    --db-instance-identifier student-database \
    --skip-final-snapshot
> ```