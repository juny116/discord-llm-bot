# Discord LLM Bot

Discord 채널의 여러 사용자와 대화하는 언어모델 봇입니다. 작성자와 멘션을 모델 입력에 반영하고, 토큰 예산에 맞춘 대화 이력과 Elasticsearch 검색 메모리로 문맥을 관리합니다.

## 두 버전

| 버전 | 모델 연결 | 실행 모듈 |
|---|---|---|
| v1 | LangChain의 OpenAI 모델, Transformers의 FLAN·Vicuna | `discord_llm.v1.bot` |
| v2 | OpenAI·Gemini SDK 직접 호출 | `discord_llm.v2.bot` |

두 버전은 Discord 이벤트·명령·대화 메모리를 공유합니다. v1은 기존 모델 loader를 사용하고, v2는 직접 API 어댑터의 서로 다른 응답 형식을 공통 대화 인터페이스로 변환합니다.

## 구조

```text
discord_llm/
├── bot.py                  # Discord 대화 이벤트와 명령 처리
├── conversation_memory.py  # 토큰 윈도와 Elasticsearch 검색 메모리
├── message_formatting.py   # 작성자 접두사와 사용자 멘션 변환
├── moderation_bot.py       # 메시지 정리용 보조 봇
├── v1/
│   ├── bot.py              # v1 실행 진입점
│   ├── model_backends.py   # 선택한 모델만 로딩
│   ├── hosted_models.py    # LangChain chat/completion 모델
│   └── local_models.py     # FLAN·Vicuna 모델
└── v2/
    ├── bot.py              # v2 실행 진입점
    ├── conversation_model.py # API 응답을 대화 모델로 연결
    └── providers/          # OpenAI·Gemini 호출과 메시지 변환
```

## 설치와 실행

Python 3.10 이상에서 저장소 루트를 기준으로 실행합니다.

```bash
pip install -r requirements.txt
python -m discord_llm v1 --config-dir /absolute/path/to/conf --config-name config
python -m discord_llm v2 --config-dir /absolute/path/to/conf --config-name config
```

Hydra 설정의 `discord.token`으로 연결합니다. `template.system`은 `member_list`, `current_member`, `additional_prompt`를 받는 시스템 프롬프트입니다. `window_size`, `max_turns`, `save_path`는 대화 길이·응답 횟수·저장 위치를 정합니다. `long_term_memory`를 켜면 `host`, `memory_size`로 Elasticsearch 메모리를 구성합니다.

v1의 `model.type`은 `chatgpt`, `openai`, `flan-ul2`, `flan-t5`, `vicuna` 중 하나입니다. 로컬 모델을 쓰려면 `requirements-local.txt`를 추가 설치하고 모델 경로와 GPU 설정을 지정합니다.

v2의 `model.type`은 `openai` 또는 `google`입니다. `model_name`, `temperature`, `max_tokens`, 선택적인 `api_key`, `max_retry`, `timeout`을 읽습니다. Gemini는 `requirements-gemini.txt`를 추가 설치합니다. v2의 대화 토큰 예산은 `cl100k_base` 토크나이저로 추정합니다.

## 대화와 명령

봇을 멘션하면 응답하고, 다른 채널 대화도 이력에 추가합니다. 생성 작업은 별도 스레드에서 실행하며 메시지 처리는 순서대로 진행합니다.

명령 메시지에도 봇을 멘션합니다.

| 명령 | 기능 |
|---|---|
| `!clear` | 현재 대화 초기화 |
| `!clear long_term` | 검색 메모리도 초기화 |
| `!prompt 내용` | 시스템 프롬프트의 추가 내용 갱신 |
| `!save 이름` | 대화 이력 저장 |
| `!memorize`, `!get 검색어` | 검색 메모리 저장·조회 |
| `!max_turns 숫자` | 최대 응답 횟수 변경 |
| `!max_token 숫자` | 대화 토큰 윈도 변경 |
| `!ping` | 응답 확인 |

검색 메모리 명령은 `long_term_memory`를 켰을 때 사용합니다. 별도 보조 봇은 `python -m discord_llm moderation --config-dir /absolute/path/to/conf`로 실행하며, `!clear`로 채널 메시지를 정리합니다.

## 테스트

```bash
python -m unittest discover -s tests -v
```

두 버전의 진입점, 대화 응답과 명령, API 응답 변환, 멘션 처리, 메모리 저장·복원을 검사합니다.

[이전 파일과 새 모듈 대응표](docs/module-map.md)
