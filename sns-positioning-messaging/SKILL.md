---
name: sns-positioning-messaging
description: Define an evidence-grounded audience, positioning, content angle and promotion message from supplied resources. Use for assigned SNS messaging work, hooks, value propositions or creator/product promotion; avoid triggering for unrelated general brand work.
---

# SNS 포지셔닝·메시지 Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 실제 고객 대안을 먼저 적어라: 다른 제품, 수작업, 아무것도 하지 않기. 대안 대비 확인된 차별점 → 고객 가치 → 가장 잘 맞는 고객 → 이해하기 쉬운 범주 순서로 정리하라.
2. 고객을 주인공으로 두고 원하는 결과, 외적·내적 문제, 가이드로서의 근거, 작은 실행 계획, CTA, 현실적인 성공 상태를 작성하라. 없는 고객 후기·경력을 만들지 말라.
3. 전체 캠페인을 설명하는 핵심 문장 한 개와 메시지 3개를 결정하라. 전문용어를 고객의 구체적인 상황·행동으로 바꾸고 기획자의 관점과 고객이 얻는 가치를 연결하라.
4. 콘텐츠의 독특한 관점(content tilt)을 정의하라. 정보 자체가 평범하면 독자적 시연, 과정, 비교 기준 또는 경험을 요구하라.
5. 훅 3개를 작성하라: 구체적 문제, 예상 밖의 검증된 발견, 직접 보여줄 결과. 각각 근거와 본문에서 반드시 회수할 약속을 기록하라.
6. 공유 동기를 1~2개만 선택하라: 유용함, 표현하고 싶은 정체성, 일상적 계기, 감정, 관찰 가능한 행동, 이야기를 통해 전달되는 효용. 조회수 보장을 쓰지 말라.
7. CTA를 고객 여정에 맞춰 하나씩 지정하라. 인지 단계에는 배움·저장·관련 자료, 의도 단계에는 체험·구독·구매를 제안하라.

8. references/messaging-canvas.md를 사용해 해당 캠페인에 필요한 항목을 실행하고 메시지·공유 계기·고객 학습·포지셔닝 갱신을 명시적인 산출물로 반환하라.

## 반환 산출물

positioning brief, 핵심 문장, 훅 3개, 메시지/근거 매핑, CTA ladder, 금지 주장를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.

- [messaging-canvas.md](references/messaging-canvas.md): 자료의 핵심 개념을 캠페인 실행 항목으로 바꿀 때 읽어라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.
