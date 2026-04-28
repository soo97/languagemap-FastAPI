# AI Coaching 기능 외부 API 및 환경 변수 가이드

AI Coaching 기능에서 사용하는 외부 API 연동을 위해 환경 변수 설정이 필요합니다.  
로컬 개발 및 협업 시 아래 내용을 참고하여 설정해주세요.

---

## 환경 변수 설정

프로젝트 실행 전, FastAPI 프로젝트 루트 경로에 `.env` 파일을 생성한 뒤  
`.env.example` 파일을 참고하여 각 환경 변수를 입력해주세요.

```env
OPENAI_API_KEY=
AZURE_SPEECH_KEY=
AZURE_SPEECH_REGION=
AZURE_SPEECH_ENDPOINT=
YOUTUBE_API_KEY=
```

## 환경 변수 설명

| 변수명                   | 설명                    | 사용 목적             |
|-----------------------|-----------------------|-------------------|
| OPENAI_API_KEY        | OpenAI API 인증 키       | AI 대화 생성, 피드백 생성  |
| AZURE_SPEECH_KEY      | Azure Speech 인증 키     | 음성 인식(STT),발음 평가       |
| AZURE_SPEECH_REGION   | Azure Speech 리전 정보    | 예: `koreacentral` |
| AZURE_SPEECH_ENDPOINT | Azure Speech 엔드포인트    | Speech API 호출 주소  |
| YOUTUBE_API_KEY       | YouTube Data API 인증 키 | 학습 콘텐츠 추천, 영상 검색  |

---

## 보안 및 업로드 정책

실제 API Key가 포함된 `.env` 파일은 민감 정보에 해당하므로  
GitHub 저장소에 업로드하지 않습니다.

`.gitignore`에 `.env` 파일이 포함되어 있는지 반드시 확인해주세요.

저장소에는 샘플 템플릿 파일인 `.env.example`만 업로드합니다.

---

## 협업 가이드

유료 API Key는 비용 및 보안 이슈로 인해 직접 공유하지 않고 서버 환경 변수로 관리합니다.

팀원들은 아래 방식으로 협업합니다.

### 로컬 개발

각자 `.env` 파일을 생성하여 필요한 값을 직접 입력 후 실행합니다.

### 공용 서버 개발

배포 서버 또는 공용 개발 서버에서는 환경 변수로 별도 관리합니다.

### 기능 테스트

API Key가 없는 팀원은 외부 API 호출 기능을 제외한 일반 API, 프론트 연동, UI 개발이 가능합니다.

---

## 참고 사항

외부 API 호출량에 따라 비용이 발생할 수 있으므로  
개발 단계에서는 불필요한 반복 호출을 지양하고, 테스트용 요청만 사용해주세요.