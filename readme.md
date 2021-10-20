# MilCoder
![title](https://user-images.githubusercontent.com/13505734/138091450-3ce87032-e182-4fa3-aede-223e4391b69d.png)


## 프로젝트 소개
미래 국방비전 2050, 각군의 스마트 부대 육성 등 군의 스마트화, 디지털화에 대한 움직임이 활발히 진행되고 있습니다. 국가 차원에서도 4차산업혁명 관련 인력육성을 위해 <전국민 AI/SW교육 확산방안>과 같은 연구를 진행한 사실에서 알 수 있듯이, 군 역시 이런 패러다임 변화에 맞춰 군 인력에 대한 체계적인 소프트웨어 기초역량 강화방안을 필요로 합니다.

군 역시 각군 교육사령부를 통해 AI, SW 인력 양성교육을 수행하고 있지만, 소집교육이 종료된 후에는 국방망(내부망)이라는 환경적 제약으로 인해 쌓은 지식들에 대해 충분한 복습기회를 제공받지 못하고 쉽게 내용을 망각하게 됩니다.

<img src="https://user-images.githubusercontent.com/13505734/138091478-dd85cd50-6148-4f6a-a074-e398b4c37bbf.png"  style="display:block;"/>

이를 해결하기 위해 저희는 **국방망 내 문제풀이 기반 프로그래밍 학습체계를 구축해 국방 실무자들이 ①손쉽게, ②꾸준히 실력향상을 꾀할 수 있도록 하자**는 목표와 함께 <**Mil Coder**> 프로젝트를 제안합니다. QingdaoU 온라인저지 프레임워크를 기반으로, 국방망 환경에 적합하도록 실시간 웹 IDE 추가와 함께 커뮤니티 기능을 강화해 국방인력들의 소프트웨어 역량 향상에 기여하고자 합니다.

## 기능 설명

### 프로그래밍 문제 채점
<div style="display:flex;flex-wrap:wrap;align-items:stretch;">
 <img src="https://user-images.githubusercontent.com/13505734/138108549-f009f604-0e84-4edb-a8af-8e8232d119a1.png"  style="width:500px"/>
 <img src="https://user-images.githubusercontent.com/13505734/138108588-884eab18-ce33-4069-82bb-c6334d83cc02.png"  style="width:500px"/>
 <img src="https://user-images.githubusercontent.com/13505734/138108594-4084d69c-bd46-43e2-8872-d1fa7dddffca.png"  style="width:500px"/>
 <img src="https://user-images.githubusercontent.com/13505734/138108602-973b9b91-2083-4c4a-8e6d-da699c6e0faf.png"  style="width:500px"/>
</div>

- 알고리즘 문제해결 기반 프로그래밍 학습을 지원합니다
- C/C++, JAVA, Python 등 주요 프로그래밍 언어를 모두 지원합니다
- 제출한 코드에 대한 정답 여부를 실시간으로 확인할 수 있습니다

### 실시간 웹 IDE 실습환경
<div style="display:flex;flex-wrap:wrap;align-items:stretch;">
 <img src="https://user-images.githubusercontent.com/13505734/138109583-06d0af64-7c33-4ecf-94df-f8b15c0b092b.png"  style="width:500px"/>
 <img src="https://user-images.githubusercontent.com/13505734/138109608-a3493ec7-b063-4d75-9520-ad9e95726066.png"  style="width:500px"/>
 <img src="https://user-images.githubusercontent.com/13505734/138109621-30fd64b4-75d4-429a-84cd-7450a76c4eb6.png"  style="width:500px"/>
</div>
- 별도의 프로그램 설치 없이도 웹브라우저에서 실시간으로 코드 작성 및 실행이 가능합니다
- 입력(`stdin`)에 대한 코드 실행결과(`stdout`, `stderr`)를 눈으로 바로 확인할 수 있어 손쉬운 디버깅이 가능합니다

### 사용자 커뮤니티

* KaTeX와 마크다운 문법을 통해 복잡한 수식, 표, 이미지가 포함된 게시글을 작성할 수 있습니다
* 키워드별, 문제 ID별 검색을 통해 특정 주제에 대한 질문 작성 및 필터링이 가능합니다
* 게시글별 댓글을 통해 사용자들 간 자유롭게 의견을 교류할 수 있습니다

### 순위표, 경연대회 개최

* 현재 다른 사용자들이 어떤 문제를 풀고 있는지, 정답 여부를 확인할 수 있습니다
* 문제풀이 수를 통해 순위표를 구성하고 이를 통해 성취욕을 자극할 수 있습니다
* 체계를 통해 내부 경연대회를 개최함으로써, 선의의 경쟁을 통해 학습의욕을 고취시킬 수 있습니다


## 컴퓨터 구성 / 필수 조건 안내

- ECMAScript 6 지원 브라우저 사용
- 권장: Google Chrome 버전 77 이상


## 소스코드 구성 및 기술 스택 

### Front-End

* `OnlineJudgeFE` :  웹사이트 프론트엔드 구성
  * Vue.js 기반
  * Golden Layout, Monaco Editor를 이용한 IDE UI 구성
  * ElementUI, iView를 이용한 UI 컴포넌트 디자인

### Back-End

* `OnlineJudge` : 웹사이트 백엔드 구성
  * Python Django 기반
  * redis, postgreSQL을 이용한 DB관리
* `JudgeServer` : 문제에 대한 채점서버 API 구성
  * Python Flask 기반
  * seccomp 기반 샌드박스 구성
* `IdeServer` : 웹 IDE 실습환경에 대한 API 구성
  * judge0 기반



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
