# 공급자 선택

| profile | 모델 | API | 키 환경 변수 |
|---|---|---|---|
| openrouter-jev | typesafe/jev-1.13 | https://openrouter.ai/api/alpha/decisions | OPENROUTER_API_KEY |
| typesafe-jev | jev-latest | https://api.typesafe.ai/v1/systemone | TYPESAFE_API_KEY |
| openrouter-judge-llm | 사용자가 선택한 구조화 출력 모델 | https://openrouter.ai/api/v1/chat/completions | OPENROUTER_API_KEY |
| custom-judge-llm | 제공자 모델 ID | 사용자가 제공한 HTTPS chat/completions | CUSTOM_JUDGE_API_KEY |

OpenRouter Jev는 chat/completions가 아닌 Decisions API로 호출한다. TypeSafe 직접 API도 state/questions/answers를 사용하지만 모델 ID와 엔드포인트가 다르다.
선택은 `--profile`로 한다. 공급자 자체를 선택하려면 TypeSafe 직접 profile 또는 OpenRouter profile을 사용하라. OpenRouter 안의 실제 추론 제공자 제한은 provider_routing.only/order에 모델이 지원하는 현재 제공자 slug를 넣어라. slug는 현재 모델의 endpoints 정보와 공급자 문서로 확인하며 추측하지 말라. only와 allow_fallbacks=false로 지정 목록 밖 제공자 전환을 막을 수 있다. actual_provider를 결과에서 확인하라. TypeSafe 직접 호출에는 OpenRouter routing 옵션을 전송하지 말라.

대체 LLM은 strict JSON schema를 지원하는 API만 사용한다. 설정의 REPLACE 값을 실제 모델 ID로 교체해야 한다. API와 같은 출력 기능을 가진다는 것이 Jev와 같은 교정·정확도·속도를 뜻하지 않는다. LLM이 보고한 확률은 미교정 값으로 취급하고 별도로 정답 표본으로 평가한다. 공급자 기능이 다르면 새로운 어댑터를 작성하고 계약 테스트를 추가해야 한다.

현재 어댑터는 명시 선택된 하나의 profile만 호출한다. 자동 fallback은 하지 않는다. 고정 입력·질문·모델 버전·정책 해시를 평가 기록에 남겨 모델 변경 전후를 비교하라. 실제 API 호출은 입력 데이터를 선택한 외부 공급자에 전송한다. 민감한 고객 정보를 최소화하고 API 키는 파일·로그·응답에 쓰지 않는다.
