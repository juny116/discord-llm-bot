# Discord LLM Bot

Discord 채널에서 여러 사용자와 대화하는 언어모델 봇입니다. 메시지의 작성자와 멘션을 처리하고, 대화 이력을 모델에 전달해 문맥에 맞는 응답을 생성합니다.

## 주요 기능

- Discord 메시지·멘션 처리와 모델 응답 전송
- 토큰 길이에 맞춘 대화 context window 관리
- Elasticsearch에 저장한 과거 대화 검색
- 대화 이력 초기화·저장과 시스템 메시지 갱신
- OpenAI API 및 Transformers 기반 모델 연결

## 코드 구조

| 경로 | 역할 |
|---|---|
| `llmbot.py` | Discord 이벤트, 명령 처리와 대화 흐름 |
| `models.py` | LangChain 및 Transformers 기반 모델 loader |
| `memory.py` | 토큰 단위 대화 윈도와 Elasticsearch 장기 메모리 |
| `utils.py` | 사용자 이름·멘션과 모델 프롬프트 변환 |
| `utilbot.py` | 보조 봇 기능 |
| `api_adapters/` | OpenAI·Gemini 직접 호출용 모델 어댑터 |

## 동작 흐름

`LLMBot`이 Discord 메시지를 받으면 작성자 정보를 정리하고 대화 이력에 추가합니다. 메모리 모듈이 모델에 전달할 문맥을 구성하고, `models.py`에서 불러온 모델이 생성한 답안을 Discord로 보냅니다.

`ChatMessageHistoryWithContextWindow`는 토큰 예산 안의 메시지를 선택합니다. `ChatMessageHistoryWithLongTerm`은 Elasticsearch에서 관련 대화를 찾아 문맥에 추가합니다.

## 실행 구성

진입점은 `llmbot.py`이며 Hydra의 `conf/config`를 읽습니다. Discord 연결 정보, 사용할 모델, 대화 메모리와 시스템 프롬프트를 설정합니다. 주요 의존성은 discord.py, LangChain, Hydra/OmegaConf, Transformers, PyTorch와 Elasticsearch 클라이언트입니다.
