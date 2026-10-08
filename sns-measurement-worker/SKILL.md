---
name: sns-measurement-worker
description: Analyze social promotion results and plan evidence-grounded iteration. Use for assigned SNS measurement, channel experiments, attribution or content-performance analysis; never infer sales from views alone.
---

# SNS 성과·실험 Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 실제 지표 데이터·기간·게시물 버전·채널·유료/자연 유입·측정 이벤트·지표 정의를 받으라. 데이터가 없으면 측정 계획만 작성하라.
2. 목표 KPI와 진단 지표를 분리하라: 발견은 도달, 반응은 유지/저장/대화, 획득은 적합한 방문·구독·활성화, 수익은 실제 구매·환불 반영 수익.
3. 공식 지표 정의를 확인하라. YouTube Shorts views와 engaged views, 노출과 순 방문, 링크 클릭과 랜딩 세션은 서로 같지 않다. 플랫폼 간 조회수 단순 비교를 피하라.
4. 비율은 분자·분모·기간을 함께 표시하고 분모가 0이면 계산 불가로 처리하라. CAC에는 명시한 비용 범위와 고객 수를 포함하라. 시간 비용은 별도 기준으로 공개하라.
5. UTM, 채널 내 행동, 실제 전환 이벤트를 연결하라. dark social·교차 기기·중복 전환·귀속 기간·데이터 누락을 기록하라.
6. 다음 실험은 한 가지 주요 변수, 가설, 대조 조건, 관측 기간, 필요한 표본, 결정 기준으로 작성하라. 유기적 게시물 비교는 랜덤 A/B가 아님을 밝히라.
7. 작은 표본에서는 우승을 단정하지 말고 추가 관측 또는 질적 인터뷰를 제안하라. 질문은 과거 행동·실제 대안·투입한 시간/돈으로 구성하라.
8. 결과를 유지·확대·수정·중단으로 분류하고 content atom, 메시지, 채널 우선순위의 변경을 근거와 함께 오케스트레이터에 반환하라.

## 반환 산출물

지표 정의/계산표, 귀속 한계, 가설과 결과, 다음 실험, Worker 수정 요청를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.

## 반복 운영

[feedback-loop.md](references/feedback-loop.md)에 따라 원자료→관측→해석→변경 요청을 분리하라. [metrics-template.csv](assets/metrics-template.csv)로 실제 데이터와 정의를 수집하라. 변경 요청은 오케스트레이터가 다음 revision과 재검토 작업으로 연결하도록 반환하라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.
