---
name: sns-community-worker
description: Plan rule-aware promotion for Reddit, Naver Cafe, Discord, developer communities and Product Hunt from supplied resources. Use for community seeding, developer-tool launches or an assigned community stage; messages remain drafts unless sending is authorized.
---

# 커뮤니티·출시 사이트 Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 고객이 실제로 모이는 커뮤니티·게시판·출시 사이트를 선택하라. 사이트 이름만으로 허용 규칙을 추정하지 말고 해당 게시판의 현행 자기홍보·링크·가입/활동 요건을 확인하라.
2. 독자가 얻는 가치와 게시자/제품의 관계를 밝히라. 해결 방법·재현 가능한 데모·실험 결과·다운로드 가능한 유틸리티를 먼저 제공하라.
3. 네이버 카페는 게시판 맥락·운영자 규칙, Reddit은 subreddit 규칙, Discord는 채널 규칙과 알림 관행, 개발자 커뮤니티는 기술 근거와 동작 조건을 반영하라.
4. Product Hunt는 출시 가능 상태·작동하는 제품·등록 자산·실제 참여 가능 시간을 점검하라. 순위·추천 확보를 위해 투표 거래·가짜 계정·조작을 제안하지 말라.
5. 선택 사이트별 완성 글, 제목, 데모/링크 위치, 관계 공개 문장, FAQ 응답을 작성하라. 규칙 미확인 사이트는 draft로 유지하라.
6. 개발 프로그램은 실행 방법, 지원 환경, 라이선스, 데모 상태·한계를 사실대로 적어라. 아카이브/코드 링크를 발명하지 말라.
7. 투입 시간, 적합한 대화, 유입, 활성 사용자·피드백·구매를 측정하라. 협업·DM·운영자 문의는 초안과 전송을 구분하라.

## 반환 산출물

사이트/게시판 선정 근거, 규칙 확인 기록, 완성 게시글, 공개/FAQ, 출시 자산·일정, KPI를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.
- [platform-checks.md](references/platform-checks.md): 플랫폼 형식·링크·측정 설정 전에 읽고 공식 안내를 갱신하라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.
