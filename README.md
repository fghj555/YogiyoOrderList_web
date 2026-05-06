## 프로젝트 설명

- 요기요 웹에 위치기반 가게검색 구현

## 실행 방법

### 1. Conda 환경 준비

최초 1회만 실행합니다.

```powershell
conda create -n yogiyo-api python=3.8 -y
conda activate yogiyo-api
python -m pip install "setuptools==57.5.0"
python -m pip install -r requirements.txt
```

이미 `yogiyo-api` 환경을 만들어 둔 경우에는 아래처럼 활성화만 하면 됩니다.

```powershell
conda activate yogiyo-api
```

### 2. PostgreSQL 실행

Docker Desktop을 먼저 실행한 뒤, 프로젝트 루트에서 아래 명령을 실행합니다.

```powershell
cd docker
docker compose up -d db
cd ..
```

`.env` 파일 기준으로 Django는 `localhost:5432`의 PostgreSQL을 사용합니다.

### 3. Django 실행

`manage.py`는 루트가 아니라 `yogiyo` 폴더 안에 있습니다.

```powershell
cd yogiyo
python manage.py check
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

실행 후 브라우저에서 접속합니다.

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/swagger/
```

## 종료 방법

Django 서버는 터미널에서 `Ctrl + C`로 종료합니다.

PostgreSQL 컨테이너를 끄려면 프로젝트 루트에서 실행합니다.

```powershell
cd docker
docker compose down
```
