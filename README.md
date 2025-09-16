# 📚 Smart-TimeTable-Scheduler

## 🚀 How to Run

### 1️⃣ Clone this Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
2️⃣ Install Requirements

Make sure Python 3.9+ is installed.
Install the required packages:
```
pip install -r requirements.txt
```

requirements.txt includes:
```
Flask
firebase-admin
requests
```
3️⃣ Firebase Setup

Go to Firebase Console → Project Settings → Service Accounts

Click Generate new private key and download the JSON file

Save the file in your project folder as:

```
serviceAccountKey.json
```

Run the Flask App
```
python app.py
```
You will see:
```
 * Running on http://127.0.0.1:5000/
```
🌐 Open in Browser

🏠 Home → http://127.0.0.1:5000/

📝 Register → /register

🔑 Login → /login

📩 Forgot Password → /forgot

🛠 Admin Dashboard → /admin/dashboard

🎓 Faculty Dashboard → /faculty/dashboard



