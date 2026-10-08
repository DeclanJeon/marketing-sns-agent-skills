# 공식 인터페이스 확인 기록

확인일: 2026-10-02 KST.

- OpenRouter Decisions reference: https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request — alpha endpoint, model/state/questions/provider, answers 계약.
- TypeSafe API: https://docs.typesafe.ai/api — /v1/systemone, jev-latest, noul/choice/score 질문·응답.
- TypeSafe models: https://docs.typesafe.ai/models — 모델 ID는 직접 공급자와 게이트웨이에서 다를 수 있음.
- OpenRouter provider routing: https://openrouter.ai/docs/guides/routing/provider-selection — only/order/allow_fallbacks/require_parameters.
- OpenRouter Jev example: https://openrouter.ai/blog/tutorials/how-to-use-jev/ — 산술은 코드, 의미 판단은 모델, 실패 시 검토, 도메인 표본으로 임계값 조정.

API 접근·가격·모델·제공자 목록은 실행 시 다시 확인한다. 이번 개발에서는 실제 키를 사용한 유료 API 호출을 수행하지 않았으며 모의 응답 계약과 dry-run만 검증한다. 문서 확인이 실호출 성공을 의미하지 않는다.
