<div align="center">

# 🚀 End-to-End MLOps Capstone Project

### Production-Ready Machine Learning Pipeline with DVC • MLflow • Docker • GitHub Actions • AWS ECR • Amazon EKS • Prometheus • Grafana

<p align="center">
<img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/Flask-Web_App-black?style=for-the-badge&logo=flask">
<img src="https://img.shields.io/badge/MLflow-Experiment_Tracking-blue?style=for-the-badge&logo=mlflow">
<img src="https://img.shields.io/badge/DVC-Data_Versioning-purple?style=for-the-badge">
<img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker">
<img src="https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?style=for-the-badge&logo=githubactions">
<img src="https://img.shields.io/badge/AWS-EKS_&_ECR-FF9900?style=for-the-badge&logo=amazonaws">
<img src="https://img.shields.io/badge/Prometheus-Monitoring-E6522C?style=for-the-badge&logo=prometheus">
<img src="https://img.shields.io/badge/Grafana-Dashboards-F46800?style=for-the-badge&logo=grafana">

</p>

---

### ⚠️ Project Goal

> **This project focuses on implementing an industry-style MLOps workflow rather than building a highly accurate machine learning model.**

The primary objective is to demonstrate the complete operational lifecycle of an ML project, including:

**Experiment Tracking → Data Versioning → Automated Training → Model Registry → Docker → CI/CD → AWS ECR → Amazon EKS → Monitoring**

</div>

---

# 📌 Project Architecture

---
```mermaid
flowchart TD

subgraph group_training["Training Pipeline"]
  node_dvc{{"DVC pipeline<br/>orchestrator<br/>[dvc.yaml]"}}
  node_params["Run parameters<br/>[params.yaml]"]
  node_dvc_state["DVC state<br/>pipeline state<br/>[dvc.lock]"]
  node_s3[("S3 data remote<br/>AWS storage")]
  node_ingestion["Data ingestion<br/>pipeline stage<br/>[data_ingestion.py]"]
  node_data_connections["AWS connections<br/>data access<br/>[s3_connection.py]"]
  node_preprocessing["Preprocessing<br/>pipeline stage"]
  node_features["Feature engineering<br/>pipeline stage"]
  node_training_stage["Model training<br/>pipeline stage<br/>[model_building.py]"]
  node_evaluation["Model evaluation<br/>pipeline stage"]
  node_mlflow[("MLflow / Dagshub<br/>experiment tracking")]
  node_registration["Model registration<br/>pipeline stage<br/>[register_model.py]"]
  node_promotion["Model promotion<br/>operations script<br/>[promote_model.py]"]
end

subgraph group_serving["Inference Service"]
  node_flask_app{{"Flask API<br/>HTTP inference runtime<br/>[app.py]"}}
  node_processing["Request processing<br/>serving utility"]
  node_ui["Browser interface<br/>HTML template<br/>[index.html]"]
end

subgraph group_delivery["Delivery"]
  node_docker["Service image<br/>container build"]
  node_ci{{"GitHub Actions<br/>CI/CD workflow<br/>[ci.yaml]"}}
  node_ecr[("Amazon ECR<br/>container registry")]
  node_eks{{"Amazon EKS<br/>Kubernetes runtime<br/>[deployment.yaml]"}}
end

node_prometheus[("Prometheus<br/>metrics collection")]
node_grafana["Grafana<br/>dashboards"]

node_params -->|"configures stages"| node_dvc
node_dvc_state -->|"locks runs"| node_dvc
node_dvc -->|"runs"| node_ingestion
node_s3 -->|"source data"| node_ingestion
node_data_connections -->|"accesses"| node_s3
node_ingestion -->|"raw data"| node_preprocessing
node_preprocessing -->|"prepared data"| node_features
node_features -->|"features"| node_training_stage
node_training_stage -->|"trained model"| node_evaluation
node_training_stage -->|"artifacts"| node_mlflow
node_evaluation -->|"metrics"| node_mlflow
node_evaluation -->|"validated model"| node_registration
node_registration -->|"registered model"| node_promotion
node_promotion -.->|"selected model"| node_flask_app
node_ui -->|"requests"| node_flask_app
node_flask_app -->|"delegates inputs"| node_processing
node_docker -->|"packages"| node_flask_app
node_ci -.->|"validates pipeline"| node_dvc
node_ci -->|"builds image"| node_docker
node_docker -->|"publishes image"| node_ecr
node_ci -->|"deploys"| node_eks
node_ecr -->|"image pull"| node_eks
node_eks -->|"hosts"| node_flask_app
node_prometheus -.->|"scrapes metrics"| node_flask_app
node_grafana -->|"queries metrics"| node_prometheus

click node_dvc "https://github.com/rajdeep712/mlops-capstone-project/blob/main/dvc.yaml"
click node_params "https://github.com/rajdeep712/mlops-capstone-project/blob/main/params.yaml"
click node_dvc_state "https://github.com/rajdeep712/mlops-capstone-project/blob/main/dvc.lock"
click node_ingestion "https://github.com/rajdeep712/mlops-capstone-project/blob/main/src/data/data_ingestion.py"
click node_data_connections "https://github.com/rajdeep712/mlops-capstone-project/blob/main/src/connections/s3_connection.py"
click node_preprocessing "https://github.com/rajdeep712/mlops-capstone-project/blob/main/src/data/data_preprocessing.py"
click node_features "https://github.com/rajdeep712/mlops-capstone-project/blob/main/src/features/feature_engineering.py"
click node_training_stage "https://github.com/rajdeep712/mlops-capstone-project/blob/main/src/model/model_building.py"
click node_evaluation "https://github.com/rajdeep712/mlops-capstone-project/blob/main/src/model/model_evaluation.py"
click node_registration "https://github.com/rajdeep712/mlops-capstone-project/blob/main/src/model/register_model.py"
click node_promotion "https://github.com/rajdeep712/mlops-capstone-project/blob/main/scripts/promote_model.py"
click node_flask_app "https://github.com/rajdeep712/mlops-capstone-project/blob/main/flask_app/app.py"
click node_processing "https://github.com/rajdeep712/mlops-capstone-project/blob/main/flask_app/processing_utility.py"
click node_ui "https://github.com/rajdeep712/mlops-capstone-project/blob/main/flask_app/templates/index.html"
click node_docker "https://github.com/rajdeep712/mlops-capstone-project/blob/main/Dockerfile"
click node_ci "https://github.com/rajdeep712/mlops-capstone-project/blob/main/.github/workflows/ci.yaml"
click node_eks "https://github.com/rajdeep712/mlops-capstone-project/blob/main/deployment.yaml"

classDef toneNeutral fill:#f8fafc,stroke:#334155,stroke-width:1.5px,color:#0f172a
classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
classDef toneMint fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef toneRose fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337
classDef toneIndigo fill:#e0e7ff,stroke:#4f46e5,stroke-width:1.5px,color:#312e81
classDef toneTeal fill:#ccfbf1,stroke:#0f766e,stroke-width:1.5px,color:#134e4a
class node_dvc,node_params,node_dvc_state,node_s3,node_ingestion,node_data_connections,node_preprocessing,node_features,node_training_stage,node_evaluation,node_mlflow,node_registration,node_promotion toneBlue
class node_flask_app,node_processing,node_ui toneAmber
class node_docker,node_ci,node_ecr,node_eks toneMint
class node_prometheus,node_grafana toneNeutral
```

# ✨ Key Features

## 📦 Complete MLOps Pipeline

- Modular ML pipeline
- Automated preprocessing
- Feature engineering
- Model training
- Evaluation metrics
- Model registration
- Production inference API

---

## 📊 MLflow Experiment Tracking

✔ Track experiments

✔ Compare multiple runs

✔ Store metrics

✔ Store parameters

✔ Store artifacts

✔ Register best model

✔ Integrated with **Dagshub**

---

## 📂 Data Version Control (DVC)

- Data versioning
- Pipeline versioning
- Pipeline reproducibility
- Automatic dependency tracking
- S3 Remote Storage

Commands used:

```bash
dvc repro
dvc status
dvc push
```

---

## ☁️ AWS Cloud Integration

The project integrates multiple AWS services.

| Service    | Purpose               |
| ---------- | --------------------- |
| Amazon S3  | DVC Remote Storage    |
| Amazon ECR | Docker Image Registry |
| Amazon EKS | Kubernetes Deployment |
| IAM        | Authentication        |
| EC2        | Monitoring Servers    |

---

## 🐳 Dockerized Application

The Flask application is fully containerized.

Features:

- Lightweight image
- Production ready
- Environment variable support
- Easy deployment
- Portable runtime

---

## ⚙️ GitHub Actions CI/CD

Automatic pipeline executes on every push.

Pipeline includes:

- Checkout repository
- Setup Python
- Install dependencies
- Run tests
- Execute DVC pipeline
- Build Docker Image
- Push Docker Image to ECR
- Deploy to Amazon EKS

---

## ☸ Kubernetes Deployment (Amazon EKS)

Deployment features:

- Managed Kubernetes Cluster
- Replica management
- Rolling updates
- Service exposure
- LoadBalancer deployment
- Production-ready container orchestration

---

## 📈 Monitoring Stack

### Prometheus

Collects metrics from the Flask application.

Tracks:

- HTTP requests
- Request latency
- API health
- Custom application metrics

---

### Grafana

Beautiful dashboards for:

- Request statistics
- Traffic monitoring
- System health
- Live metrics visualization

---

# 🏗 Project Structure

```text
MLOPS-Capstone-Project/
│
├── .dvc/                          # DVC configuration for data version control
│   ├── .gitignore
│   └── config
│
├── .github/
│   └── workflows/
│       └── ci.yaml                # CI/CD pipeline configuration
│
├── docs/                          # Project documentation (Sphinx)
│   ├── Makefile
│   ├── commands.rst
│   ├── conf.py
│   ├── getting-started.rst
│   ├── index.rst
│   └── make.bat
│
├── flask_app/                     # Flask web application for model serving
│   ├── app.py
│   ├── load_model_test.py
│   ├── processing_utility.py
│   ├── requirements.txt
│   └── templates/
│       └── index.html
│
├── models/                        # Trained model artifacts
│   └── .gitkeep
│
├── notebooks/                     # Exploratory analysis & experiments
│   ├── IMDB.csv
│   ├── data.csv
│   ├── exp1.ipynb
│   ├── exp2_bow_vs_tfidf.py
│   └── exp3_lor_bow_hp.py
│
├── references/                    # Data dictionaries, manuals, reference material
│   └── .gitkeep
│
├── reports/                       # Generated analysis reports
│   ├── .gitignore
│   ├── .gitkeep
│   └── figures/
│       └── .gitkeep
│
├── scripts/
│   └── promote_model.py           # Model promotion utility
│
├── src/                           # Source code for use in this project
│   ├── __init__.py
│   │
│   ├── connections/                # External service connections
│   │   ├── __init__.py
│   │   ├── config.json
│   │   ├── s3_connection.py
│   │   └── ssms_connection.py
│   │
│   ├── data/                       # Data ingestion & preprocessing
│   │   ├── .gitkeep
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   └── data_preprocessing.py
│   │
│   ├── features/                   # Feature engineering
│   │   ├── .gitkeep
│   │   ├── __init__.py
│   │   └── feature_engineering.py
│   │
│   ├── logger/                     # Logging utility
│   │   └── __init__.py
│   │
│   ├── model/                      # Model building, evaluation & registration
│   │   ├── .gitkeep
│   │   ├── __init__.py
│   │   ├── model_building.py
│   │   ├── model_evaluation.py
│   │   └── register_model.py
│   │
│   └── visualization/              # Visualization utilities
│       ├── .gitkeep
│       ├── __init__.py
│       └── visualize.py
│
├── tests/                         # Unit & integration tests
│   ├── test_flask_app.py
│   └── test_model.py
│
├── .dvcignore
├── .gitignore
├── Dockerfile                     # Container image definition
├── LICENSE
├── Makefile                       # Convenience commands (setup, train, etc.)
├── README.md
├── deployment.yaml                # Kubernetes deployment manifest
├── dvc.lock                       # DVC pipeline lock file
├── dvc.yaml                       # DVC pipeline stages
├── params.yaml                    # Pipeline hyperparameters/config
├── requirements.txt                # Project dependencies
├── setup.py                        # Package setup
├── test_environment.py            # Environment sanity check
└── tox.ini                        # Test automation config
```

---

# 🛠 Tech Stack

## Machine Learning

- Python
- Scikit-Learn
- Pandas
- NumPy

---

## Experiment Tracking

- MLflow
- Dagshub

---

## Data Versioning

- DVC
- Amazon S3

---

## Backend

- Flask

---

## Containerization

- Docker

---

## CI/CD

- GitHub Actions

---

## Cloud

- AWS IAM
- AWS S3
- AWS ECR
- AWS EKS
- EC2

---

## Monitoring

- Prometheus
- Grafana

---

# 🚀 CI/CD Pipeline

```text
Push Code
     │
     ▼
GitHub Actions
     │
     ▼
Run Unit Tests
     │
     ▼
Build Docker Image
     │
     ▼
Push Image to AWS ECR
     │
     ▼
Deploy to Amazon EKS
     │
     ▼
Application Live
```

---

# 📊 Monitoring Pipeline

```text
Flask API
     │
     ▼
Prometheus Metrics
     │
     ▼
Grafana Dashboards
```

# ⚡ Local Setup

Clone repository

```bash
git clone https://github.com/yourusername/project.git
```

Create environment

```bash
conda create -n atlas python=3.10
conda activate atlas
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run pipeline

```bash
dvc repro
```

Run application

```bash
python flask_app/app.py
```

---

# 📦 Deployment Stack

| Stage               | Tool       |
| ------------------- | ---------- |
| Version Control     | Git        |
| Experiment Tracking | MLflow     |
| Data Versioning     | DVC        |
| Remote Storage      | Amazon S3  |
| Containerization    | Docker     |
| Registry            | Amazon ECR |
| Orchestration       | Amazon EKS |
| Monitoring          | Prometheus |
| Dashboard           | Grafana    |

---

# 🎯 Learning Outcomes

This project demonstrates practical knowledge of:

- Building modular ML pipelines
- Experiment tracking with MLflow
- Data versioning using DVC
- Reproducible ML workflows
- Docker containerization
- GitHub Actions automation
- AWS cloud deployment
- Kubernetes fundamentals
- Production model deployment
- Monitoring ML applications
- Infrastructure automation

---

# 📚 Future Improvements

- Model retraining pipeline
- Hyperparameter optimization
- Canary deployments
- Blue-Green deployment
- Helm Charts
- Terraform Infrastructure
- ArgoCD GitOps
- Autoscaling
- Logging with ELK Stack
- AlertManager integration

---

# 🤝 Contributing

Contributions, issues and feature requests are welcome!

Feel free to fork the repository and submit a Pull Request.

---

# ⭐ If you found this project useful

Please consider giving the repository a ⭐

It motivates me to build more production-grade Machine Learning and MLOps projects.

---

<div align="center">

### Built with ❤️ to learn Production MLOps Engineering

**From Model Training → Cloud Deployment → Monitoring**

</div>
