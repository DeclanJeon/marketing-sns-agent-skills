---
name: sns-shortvideo-worker
description: Adapt supplied resources into TikTok-first short-video posting and promotion plans. Use for TikTok or assigned short-video adaptation; route YouTube and Instagram native packaging to their workers.
---

# TikTok·숏폼 홍보 Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 고객 상황과 실제 시연으로 시작하는 주제를 선택하라. TikTok을 쓰는 타깃 근거가 없으면 채널 적합성을 가설로 표시하라.
2. hook → 보여주기 → 결과/배움 → CTA 구조로 1개의 완성 대본과 훅 대안 2개를 작성하라. 검색 의도를 포함한 자연스러운 말·화면 글자·캡션을 구성하라.
3. 시간 구간별 화면, 말, 자막, 시연 자산, 전환을 적어라. 플랫폼용 원본 마스터를 만들고 음원 라이선스를 다른 채널로 자동 확장하지 말라.
4. 계정의 Search Insights 또는 검색 제안에서 확인한 질문을 기록하라. 확인하지 않은 검색량·트렌드를 만들지 말라. 유행은 제품 가치와 연결될 때만 사용하라.
5. 댓글 질문에 답하는 후속 영상 2개를 제안하라. 제작자의 진짜 경험이 없으면 경험담 대신 시연·분석의 관점으로 쓰라.
6. 길이·비율·링크·상업용 음악·브랜디드 콘텐츠 설정은 공식 도움말 및 계정 기능을 확인하라. 기능 확인 실패 시 수동 업로드 패키지를 제공하라.
7. 시청 유지·완주·공유·프로필 방문과 고객 행동을 각각 측정하라. 반복 재생만을 고객 확보 성과로 해석하지 말라.

## 반환 산출물

완성 숏폼 대본, 훅 2개, 캡션/커버, 후속 영상, 음원/업로드 확인 항목, KPI를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.
- [platform-checks.md](references/platform-checks.md): 플랫폼 형식·링크·측정 설정 전에 읽고 공식 안내를 갱신하라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.
