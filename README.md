# Currency-Calculator

# 💱 Currency Converter App

A simple desktop-based Currency Converter built using **Streamlit**, **Python**, and **MySQL**.

It allows users to:
- Convert currencies using real-time exchange rates via API.
- View conversion history.
- Store data in a MySQL database.

## 🚀 Features

- 🔁 Real-time currency conversion
- 🧾 Conversion history tracking
- 💾 MySQL database integration
- 🌐 Clean and intuitive Streamlit UI
- 🔐 Environment variable support using `.env`

## 🖼️ Demo

*(Add a screenshot here if you have one)*

## 🛠️ Tech Stack

- Python 3.11+
- Streamlit
- Pandas
- SQLAlchemy
- PyMySQL / MySQL-Connector
- dotenv
- Exchange Rate API (Free or Paid)


## 🧰 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
````

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the root directory (or copy from `.env.example`) with the following:

```env
# .env
DATABASE_URL="mysql+pymysql://your_user:your_password@localhost:3306/your_db_name"
API_KEY="your_currency_api_key"
```

> ⚠️ **Never share your actual `.env` file. Only share `.env.example`**

---

## 🗃️ Database Setup

Create the MySQL database and required tables (if not auto-created).

Example:

### 🛠️ Database Setup

Run the following SQL script:

```bash
mysql -u your_username -p < setup.sql

Or let SQLAlchemy create it on first run.

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Access at: [http://localhost:8501](http://localhost:8501)

---

## 📂 Project Structure

```
├── .streamlit/
│   └── config.toml
├── .gitignore
├── app.py
├── requirements.txt
├── setup.sql         👈
├── .env.example
├── README.md
```

---

## 🧾 Sample .env File

```env
# .env.example
DATABASE_URL="mysql+pymysql://your_user:your_password@localhost:3306/your_db_name"
API_KEY="your_currency_api_key"
```

---

## ❗ Troubleshooting

* Ensure MySQL is running and credentials are correct.
* Check if API key is valid and not over quota.
* Use correct port and database name in `DATABASE_URL`.

---

## 📃 License

This project is licensed under the MIT License. See `LICENSE` for more info.

---

## 🤝 Contributing

Pull requests are welcome! Feel free to fork the repo and submit your improvements.

---

## 👨‍💻 Author

Developed during the **RISE Tamizhan Internship**
Maintained by [Nishant Dharukar](https://github.com/Nishant-stack19/)

```