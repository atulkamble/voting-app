1. **A basic voting app** — simple Python Flask backend with HTML UI
2. **Dockerfile** — to containerize it
3. **Kubernetes manifests** — Deployment & Service
4. Instructions to **host on a Kubernetes cluster (EKS/Minikube)**

---

## 📦 1️⃣ App Code: `app.py`

```python
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

votes = {"Python": 0, "Java": 0, "Go": 0}

@app.route('/')
def index():
    return render_template('index.html', votes=votes)

@app.route('/vote', methods=['POST'])
def vote():
    language = request.form.get('language')
    if language in votes:
        votes[language] += 1
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset_votes():
    for key in votes:
        votes[key] = 0
    return redirect(url_for('index'))

@app.route('/data')
def data():
    return jsonify(votes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 🖥️ 2️⃣ HTML UI: `templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Voting App by atulkamble</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: #333;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 40px;
        }
        .container {
            background: #fff;
            border-radius: 16px;
            padding: 30px;
            max-width: 800px;
            width: 100%;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        h1 {
            margin-top: 0;
            font-size: 2.5rem;
            color: #444;
        }
        .buttons {
            margin: 20px 0;
        }
        button {
            padding: 14px 30px;
            margin: 10px;
            font-size: 18px;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            transition: 0.3s;
        }
        .vote-btn {
            background-color: #4CAF50;
            color: white;
        }
        .vote-btn:hover {
            background-color: #45a049;
        }
        .reset-btn {
            background-color: #f44336;
            color: white;
        }
        .reset-btn:hover {
            background-color: #d32f2f;
        }
        .logout-btn {
            background-color: #333;
            color: white;
        }
        .logout-btn:hover {
            background-color: #222;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            color: #333;
            text-decoration: none;
            font-size: 16px;
        }
        a:hover {
            color: #000;
            font-weight: bold;
        }
        canvas {
            margin-top: 30px;
            border-radius: 10px;
            background: #f9f9f9;
            padding: 20px;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Vote for Your Favorite Programming Language</h1>

        <form method="POST" action="/vote" class="buttons">
            <button type="submit" name="language" value="Python" class="vote-btn">🐍 Python</button>
            <button type="submit" name="language" value="Java" class="vote-btn">☕ Java</button>
            <button type="submit" name="language" value="Go" class="vote-btn">🐹 Go</button>
        </form>

        {% if logged_in %}
        <form method="POST" action="/reset" class="buttons">
            <button type="submit" class="reset-btn">🔄 Reset Votes (Admin)</button>
        </form>
        <a href="/logout">🚪 Logout</a>
        {% else %}
        <a href="/login">🔐 Admin Login</a>
        {% endif %}

        <canvas id="voteChart" width="600" height="400"></canvas>
    </div>

    <script>
        const ctx = document.getElementById('voteChart').getContext('2d');
        let chart;

        function fetchData() {
            fetch('/data')
                .then(response => response.json())
                .then(data => {
                    const labels = Object.keys(data);
                    const votes = Object.values(data);

                    if (chart) {
                        chart.data.labels = labels;
                        chart.data.datasets[0].data = votes;
                        chart.update();
                    } else {
                        chart = new Chart(ctx, {
                            type: 'bar',
                            data: {
                                labels: labels,
                                datasets: [{
                                    label: 'Votes',
                                    data: votes,
                                    backgroundColor: ['#4CAF50', '#2196F3', '#FF9800'],
                                    borderRadius: 8
                                }]
                            },
                            options: {
                                responsive: true,
                                scales: {
                                    y: {
                                        beginAtZero: true,
                                        ticks: {
                                            precision: 0
                                        }
                                    }
                                },
                                plugins: {
                                    legend: {
                                        labels: {
                                            font: {
                                                size: 14
                                            }
                                        }
                                    }
                                }
                            }
                        });
                    }
                });
        }

        setInterval(fetchData, 1000);
        fetchData();
    </script>

</body>
</html>
```

---

**run this voting app locally on your machine without Docker/Kubernetes**:

---

## 📦 1️⃣ Project Structure (locally)

```
voting-app/
├── app.py
├── requirements.txt
└── templates/
    └── index.html
```

---

## 🐍 2️⃣ Install Python & Dependencies

If you haven't already:

```bash
python3 --version
pip3 --version
```

---

### Install virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Install Flask

Create `requirements.txt`:

```
Flask
```

Then run:

```bash
pip3 install -r requirements.txt
```

---

## 🏃 3️⃣ Run the App

From your project directory:

```bash
python3 app.py
```

You’ll see:

```
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

---

## 🌐 4️⃣ Access in Browser

Open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

✔️ You should see your voting app UI.

---

## 📌 Optional: Run without Virtualenv

If you prefer globally:

```bash
pip3 install Flask
python3 app.py
```

---

✅ Done — your voting app is now running locally!


## 🐳 3️⃣ Dockerfile

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

**requirements.txt**

```
Flask
```

---

## 📦 4️⃣ Build & Push Docker Image

```bash
docker build -t atuljkamble/voting-app:latest .
docker push atuljkamble/voting-app:latest
```

---

## ☸️ 5️⃣ Kubernetes YAML Manifests

**voting-app-deployment.yaml**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: voting-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: voting-app
  template:
    metadata:
      labels:
        app: voting-app
    spec:
      containers:
      - name: voting-app
        image: atulkamble/voting-app:latest
        ports:
        - containerPort: 5000
```

**voting-app-service.yaml**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: voting-app-service
spec:
  selector:
    app: voting-app
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
```

---

## 📤 6️⃣ Deploy to Kubernetes

### Create Deployment and Service

```bash
kubectl apply -f voting-app-deployment.yaml
kubectl apply -f voting-app-service.yaml
```

---

## 🔍 7️⃣ Get LoadBalancer/NodePort URL

```bash
kubectl get svc
```

👉 If you're using **Minikube**:

```bash
minikube service voting-app-service
```

---

## ✅ Done — Voting App hosted in Kubernetes 🎉

---

## 📁 GitHub Repo Structure:

```
voting-app/
├── app.py
├── Dockerfile
├── requirements.txt
├── templates/
│   └── index.html
├── voting-app-deployment.yaml
└── voting-app-service.yaml
```
# ec2-amazon linux
```
sudo apt install snap -y 
sudo apt install python3-pip -y
sudo yum install git -y 
git --version
git config --global user.name "Atul Kamble"
git config --global user.email "atul_kamble "
git config --list 
git clone https://github.com/atulkamble/voting-app.git
cd voting-app
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install flask 
python app.py 
```
# ubuntu 
```
sudo apt update -y 
sudo apt install tree -y 
sudo apt install python-is-python3
sudo apt update -y
sudo apt install python3-pip -y
sudo apt install git -y
git clone https://github.com/atulkamble/voting-app.git
cd voting-app/
sudo pip3 install flask 
sudo apt install python3.12-venv -y
sudo apt install pipx -y 
python3 -m venv venv
source venv/bin/activate 
pip install flask -y 
python app.py 
```
# linux hosting
let’s deploy this Flask voting app on a **Linux server (Ubuntu/RHEL-based)**.
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

---
