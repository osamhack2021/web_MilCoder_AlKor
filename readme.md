# MilCoder
![title](https://user-images.githubusercontent.com/13505734/138091450-3ce87032-e182-4fa3-aede-223e4391b69d.png)


## 프로젝트 소개
미래 국방비전 2050, 각군의 스마트 부대 육성 등 군의 스마트화, 디지털화에 대한 움직임이 활발히 진행되고 있습니다. 국가 차원에서도 4차산업혁명 관련 인력육성을 위해 <전국민 AI/SW교육 확산방안>과 같은 연구를 진행한 사실에서 알 수 있듯이, 군 역시 이런 패러다임 변화에 맞춰 군 인력에 대한 체계적인 소프트웨어 기초역량 강화방안을 필요로 합니다.

군 역시 각군 교육사령부를 통해 AI, SW 인력 양성교육을 수행하고 있지만, 소집교육이 종료된 후에는 국방망(내부망)이라는 환경적 제약으로 인해 쌓은 지식들에 대해 충분한 복습기회를 제공받지 못하고 쉽게 내용을 망각하게 됩니다.

![forget-curve-short](https://user-images.githubusercontent.com/13505734/138091478-dd85cd50-6148-4f6a-a074-e398b4c37bbf.png)

이를 해결하기 위해 저희는 **국방망 내 문제풀이 기반 프로그래밍 학습체계를 구축해 국방 실무자들이 ①손쉽게, ②꾸준히 실력향상을 꾀할 수 있도록 하자**는 목표와 함께 <**Mil Coder**> 프로젝트를 제안합니다.

## 기능 설명

- Docker 기반 배포, 간편한 설치
- C/C++, JAVA, Python 채점 가능
- 게시판을 통한 질문/답변
- 사용자 및 조직별 랭킹
- 교육과정 등에 활용할 수 있는 그룹 기능 및 그룹 별 연습세션


## 컴퓨터 구성 / 필수 조건 안내 (Prerequisites)

- ECMAScript 6 지원 브라우저 사용
- 권장: Google Chrome 버전 77 이상


## 기술 스택 (Technique Used)

### OJ Server (back-end)
- Django
- redis
- postgreSQL

### Front-end
- 주 프레임워크: Vue.js
- 디자인 UI: Element-UI / iView
- 그 외 UI: Golden Layout, Monaco Editor 등

### Judge Server
- Flask

### Judge Sandbox
- seccomp

## 설치 안내 (Installation Process)
```shell
scripts/dev_setup.sh
```

필요한 패키지와 추후 추가될 설치 과정은 위 스크립트 수정 또는 새로 추가헤서 관리 

## 프로젝트 사용법 (Getting Started)
```shell
python3 manage.py runserver # API
npm run dev # FRONT
```


## 팀 정보 (Team Information)

- Lee Woncheol (wclee2265\@naver.com), GitHub ID: wclee2265
- Kim Minchul (k.minchul95\@gmail.com), GitHub ID: nyan101
- Kim Jehyung (arlawpgud2\@gmail.com), GitHub ID: 0xrgb


## 저작권 및 사용권 정보 (Copyleft / End User License)

MIT, GPL 3.0. 자세한 정보는 [license.md](license.md)에서 확인하세요.


## 참조 (Reference)

- https://github.com/QingdaoU/OnlineJudge 
- https://github.com/judge0/judge0
- https://github.com/egoist/vue-monaco
