# 📚 Smart-TimeTable-Scheduler

## 🚀 How to Run

### 1️⃣ Clone this Repository
```bash 
git clone https://github.com/your-username/your-repo-name.git``
cd your-repo-name
2️⃣ Install Requirements
Make sure Python 3.9+ is installed.
Install the required packages:

bash
Copy code
pip install -r requirements.txt
requirements.txt includes:

nginx
Copy code
Flask
firebase-admin
requests
3️⃣ Firebase Setup
Go to Firebase Console → Project Settings → Service Accounts

Click Generate new private key and download the JSON file

Save the file in your project folder as:

pgsql
Copy code
serviceAccountKey.json
4️⃣ Run the Flask App
bash
Copy code
python app.py
You will see:

csharp
Copy code
 * Running on http://127.0.0.1:5000/
✅ Now open your browser and go to:

Home → http://127.0.0.1:5000/

Register → /register

Login → /login

Forgot Password → /forgot

Admin Dashboard → /admin/dashboard

Faculty Dashboard → /faculty/dashboard

yaml
Copy code
