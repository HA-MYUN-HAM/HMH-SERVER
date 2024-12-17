# HMH-SERVER

AWS-EC2 이용 
public ip 주소: http://43.202.43.140/

# **NORI - 내부 행사 관리 플랫폼**

---

## **프로젝트 개요**
**NORI**는 단체 내부 행사를 쉽고 효율적으로 **생성, 홍보, 신청 및 관리**할 수 있는 웹 플랫폼입니다.  
대형 동아리, 학회, 대학 동창회 등 다양한 단체의 행사 기획부터 참여까지 **모든 과정을 통합**하여 제공합니다.

---

## **기능 소개**

### **관리자 기능**
1. **행사 생성**
   - 행사 정보를 입력하면 자동으로 **홍보 페이지**와 **신청 페이지**가 생성됩니다.
2. **AI 홍보물 생성**
   - OpenAI API를 활용해 행사에 적합한 홍보 이미지를 자동으로 생성합니다.
3. **참석자 관리**
   - 신청자 명단을 조회하고 관리할 수 있습니다.

### **회원 기능**
1. **행사 목록 조회**
   - 등록된 행사 정보를 한눈에 확인할 수 있습니다.
2. **행사 신청**
   - 원클릭 신청 기능을 통해 간편하게 행사 참여를 할 수 있습니다.
3. **티켓 발급**
   - 신청 후 **디지털 티켓**이 발급되어 행사 정보를 쉽게 확인할 수 있습니다.

---

## **기술 스택**

### **프론트엔드**
- React + TypeScript  
- Axios (백엔드와의 통신)  

### **백엔드**
- Django (백엔드 서버 및 API 구축)  
- MySQL (데이터베이스)  
- AWS EC2 (서버 호스팅)  
- Nginx + uWSGI (서버 요청 처리 및 배포)

### **AI 이미지 생성**
- OpenAI API를 사용하여 행사 정보를 바탕으로 자동 홍보물 이미지 생성  

---

## **프로젝트 구조**

```bash
HMH/
├── HMH-SERVER/                # Django 백엔드
│   ├── be/                 # 프로젝트 설정
│   ├── events/             # 행사 관련 앱
│   ├── accounts/           # 사용자 인증 앱
│   ├── ai/                  # ai 관련 앱
│   ├── admins/            # 관리자 설정 앱 
│   └── requirements.txt    # Python 라이브러리 목록
└── README.md               # 프로젝트 설명 파일
```

#### **1.1. 가상 환경 설정 및 패키지 설치**  
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**1.1. 가상 환경 설정 및 패키지 설치**  
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
**1.2. 데이터베이스 설정 및 마이그레이션** 

```
python manage.py makemigrations
python manage.py migrate
```

1.3. 서버 실행
```
python manage.py runserver
```
백엔드 서버는 http://localhost:8000 에서 확인할 수 있습니다.

## Open Source & API 

python: https://www.python.org<br>
django: https://www.djangoproject.com<br>
OpenAI: https://openai.com<br>
kakao dev (login API): https://developers.kakao.com<br>
mysql: https://www.mysql.com
aws ec2: https://aws.amazon.com/ko/ec2/?trk=bc3c5de1-7376-43c7-ad4f-f0f3f8248023&sc_channel=ps&ef_id=CjwKCAiA34S7BhAtEiwACZzv4YFoSe68M_6VcFQcU-zIxZCcCSniNMaW0TrSN3_9D7eTnAg76c4LEhoCcbAQAvD_BwE:G:s&s_kwcid=AL!4422!3!588924203019!e!!g!!aws%20ec2!16390049454!133992834459&gbraid=0AAAAADjHtp_5rmuMkJrgwP3TqxMM7EyCw&gclid=CjwKCAiA34S7BhAtEiwACZzv4YFoSe68M_6VcFQcU-zIxZCcCSniNMaW0TrSN3_9D7eTnAg76c4LEhoCcbAQAvD_BwE<br>
nginx: https://nginx.org <br>
uwsgi: https://uwsgi-docs.readthedocs.io/en/latest/
