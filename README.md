# 🔐 Merkle Tree Based Transaction Storage System

A secure transaction storage system built using **Merkle Trees** and **cryptographic hashing** to ensure data integrity and detect tampering.

## 🚀 Features

* Implements Merkle Tree for transaction verification
* Custom SHA-256 hashing (no external libraries)
* SQLite database for storing transactions
* Detects and highlights tampered data
* Simple web interface using Flask

## 🛠️ Tech Stack

Python, Flask, SQLite, HTML/CSS

## ▶️ Run the Project

```bash
pip install -r requirements.txt
python app.py
```

Open in browser: http://127.0.0.1:5000/

## 📌 Description

Transactions are hashed and organized into a Merkle Tree. The root hash acts as a secure reference. Any change in transaction data alters the root, allowing quick detection of tampering.

## 🔮 Future Scope

* Blockchain integration
* REST API support
* User authentication
