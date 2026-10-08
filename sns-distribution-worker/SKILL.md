---
name: sns-distribution-worker
description: Build promotion, repurposing, launch sequences and posting calendars across selected channels. Use for assigned SNS distribution, promotion calendars or launch coordination; do not publish or buy ads solely from a drafting request.
---

# SNS 배포·런칭 Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 각 channel package를 받아 주력 콘텐츠·파생 콘텐츠·자사 허브의 연결을 점검하라. 같은 문장 복제 대신 각 채널 독자가 얻는 다른 가치를 유지하라.
2. 2주 일정을 현지 시간대와 담당자·작업 시간에 맞춰 작성하라. 게시 시작 전 자산 제작, 링크 테스트, QA 시간을 포함하라.
3. 리소스의 목적에 따라 제작 과정 공개 → 문제 설명/유용한 자료 → 실제 시연 → 체험/출시 → 질문·반론 대응 → 후속 사례 순서를 조합하라. 모든 캠페인을 판매 런칭으로 만들지 말라.
4. 랜딩/구독/체험/구매까지 클릭 경로를 점검하라. UTM으로 channel, campaign, content_id를 식별하되 URL이 없는 경우 임시 URL을 실제처럼 만들지 말라.
5. 댓글 응답·질문 수집·관련 커뮤니티 기여·협업 후보·자사 뉴스레터를 운영 작업으로 계획하라. DM·이메일·실제 포스팅은 승인 범위와 도구 권한을 확인하라.
6. 판매 런칭은 제공 조건·가격·실제 기한·환불/지원 등 사용자에게 제공된 조건만 쓰라. 가짜 희소성·가짜 후기·실적 과장을 제외하라.
7. 유료 홍보는 별도 예산과 승인 범위가 있을 때만 실행하라. 계획에는 타깃, 크리에이티브, 착지 페이지, 비용 상한, 중단 기준을 포함하라.
8. 게시 전에 final_version과 계정·채널·시간·허용 행동을 확정하라. 재시도 전에 결과를 조회해 중복 게시를 방지하라. 삭제·수정도 승인 범위를 따른다.
9. 실제 결과가 없으면 ready/draft/pending 상태를 사용하라. 게시 URL·예약 ID·성공 지표를 발명하지 말라.

## 반환 산출물

2주 캘린더, 작업·재사용 관계, UTM/클릭 경로, 게시 후 운영, 런칭/협업/광고 초안, 실행 상태를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.

## 실행 결과·재시도

게시별 content_id/revision, 계정, 실제 게시 시각, URL 또는 예약 ID, 연결 도구 응답 locator, outcome을 운영 이벤트에 반환하라. 실패 원인과 다음 조회/수정 담당자를 남겨라. timeout/응답 유실은 unknown으로 기록하고 실제 계정에서 결과를 조회하기 전 재실행하지 말라. 게시 전 QA는 정확한 payload와 자산 버전에 연결되어야 한다. 댓글·문의 운영 시간을 캘린더에 포함하고 실행하지 않은 응답을 완료로 표시하지 말라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.
