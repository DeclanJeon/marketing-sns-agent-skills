---
name: sns-threads-worker
description: Write Threads-native conversational posts and follow-up promotion from supplied resources. Use for Threads copy, community conversations or an assigned Threads stage.
---

# Threads 게시·홍보 Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 원본에서 실제로 겪은 상황, 깨달음, 고객의 문제, 직접 해본 과정을 선택하라. X 문장을 그대로 옮기지 말고 대화의 맥락을 추가하라.
2. 첫 문장에 구체적 상황을, 본문에 경험 또는 증거를, 끝에 실제 답변 가능한 질문이나 작은 CTA를 적어라. 억지 논쟁이나 내용 없는 댓글 유도는 피하라.
3. 단일 게시물 또는 짧은 연결 게시물로 완성하라. 긴 텍스트 첨부를 사용할 경우 계정 기능을 확인하고 메인 글만 읽어도 가치가 남도록 하라.
4. 관련 주제 태그와 검색 대화를 선택하라. 특정 태그가 무조건 노출을 올린다고 단정하지 말라.
5. 게시 후 예상 질문 3개와 답글 원고, 다음 날 후속 글을 제공하라. 고객 학습 질문은 과거 행동·기존 해결 방법을 묻고 구매 가정을 유도하지 말라.
6. 필요하면 미디어에 짧은 맥락 설명과 대체 텍스트를 붙여라. 외부 링크는 제공된 URL만 사용하고 클릭 경로와 제공되는 Insights를 확인하라.
7. 질문에 성실히 답하는 운영 시간을 일정에 반영하라. 일방적인 홍보 글 수만 늘리지 말라.
8. 답글의 내용·잠재 고객 대화·링크 클릭·구독을 측정하라. 답글 수를 수요 검증으로 단정하지 말라.

## 반환 산출물

완성 포스트, 주제/형식 선택, 답글 3개, 후속 글, 링크 경로, 대화 학습과 KPI를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.
- [platform-checks.md](references/platform-checks.md): 플랫폼 형식·링크·측정 설정 전에 읽고 공식 안내를 갱신하라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.
