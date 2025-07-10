1. **A basic voting app** — simple Python Flask backend with HTML UI
2. **Dockerfile** — to containerize it
3. **Kubernetes manifests** — Deployment & Service
4. Instructions to **host on a Kubernetes cluster (EKS/Minikube)**

---

## 📦 1️⃣ App Code: `app.py`

```python
from flask import Flask, render_template, request, redirect, url_for

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 🖥️ 2️⃣ HTML UI: `templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Simple Voting App</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        button { padding: 10px 20px; margin: 10px; font-size: 16px; }
    </style>
</head>
<body>
    <h1>Vote for your Favorite Language</h1>
    <form method="POST" action="/vote">
        <button type="submit" name="language" value="Python">Python</button>
        <button type="submit" name="language" value="Java">Java</button>
        <button type="submit" name="language" value="Go">Go</button>
    </form>
    <h2>Current Results:</h2>
    <ul>
        {% for lang, count in votes.items() %}
        <li><strong>{{ lang }}</strong>: {{ count }} votes</li>
        {% endfor %}
    </ul>
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

## 📁 Suggested GitHub Repo Structure:

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
---
