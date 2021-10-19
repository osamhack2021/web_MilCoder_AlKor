# MilCoder

## 프로젝트 소개
- 자기주도적으로 문제를 풀며 SW 프로그래밍을 학습할 수 있는 온라인저지 시스템입니다.

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

### Front-end
- React.js, Vue.js 등 사용한 front-end 프레임워크 
- UI framework
- 기타 사용한 라이브러리

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
