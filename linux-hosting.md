Excellent idea, Atul — let’s deploy this Flask voting app on a **Linux server (Ubuntu/RHEL-based)**.
I’ll give you a clean step-by-step guide to:

* Install dependencies
* Run it as a background service (so it stays running)
* Expose it via your Linux server’s public IP on port `5000` or via Nginx reverse proxy on port `80`

---

## 📦 1️⃣ Upload/Clone Your App on Linux

SSH into your Linux server:

```bash
ssh ubuntu@<server-ip>
```

Clone your repo or copy files via SCP:

```bash
scp -r voting-app/ ubuntu@<server-ip>:~
```

---

## 🐍 2️⃣ Install Python3 and pip3 (if not installed)

For Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

For RHEL/CentOS:

```bash
sudo yum install python3 python3-pip -y
```

---

## 📄 3️⃣ Install Required Python Modules

Navigate to your project directory:

```bash
cd voting-app
```

Then install Flask:

```bash
pip3 install -r requirements.txt
```

---

## 🏃 4️⃣ Run the App

```bash
python3 app.py
```

You’ll see:

```
* Running on http://0.0.0.0:5000/
```

---

## 🔒 5️⃣ Open Firewall Port (if needed)

For **Ubuntu with UFW**:

```bash
sudo ufw allow 5000/tcp
```

For **firewalld (CentOS/RHEL)**:

```bash
sudo firewall-cmd --add-port=5000/tcp --permanent
sudo firewall-cmd --reload
```

---

## 🖥️ 6️⃣ Access the App in Browser

Open:

```
http://<server-ip>:5000
```

✔️ You should see your voting app.

---

## 🎛️ (Optional) Run as Background Service (using `nohup`)

To keep it running even after closing SSH:

```bash
nohup python3 app.py > app.log 2>&1 &
```

Check running processes:

```bash
ps aux | grep app.py
```

---

## 🔄 (Optional) Serve via Nginx on Port 80

If you want it on `http://<server-ip>`:

### Install Nginx

```bash
sudo apt install nginx -y
```

### Create Reverse Proxy Config:

```bash
sudo nano /etc/nginx/sites-available/voting-app
```

**Config:**

```
server {
    listen 80;
    server_name <server-ip>;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Enable and Restart Nginx

```bash
sudo ln -s /etc/nginx/sites-available/voting-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Now, access:

```
http://<server-ip>
```

---

✅ Done — your voting app is now hosted on a Linux server!
