---
name: sns-channel-strategist
description: Select and prioritize SNS channels and sites for resource-based content promotion. Use for assigned channel strategy, audience-channel fit or traction experiments across social, search and communities.
---

# SNS 채널 전략 Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 목표를 인지도, 구독, 체험, 구매 중 하나로 좁혀라. 예산·주간 작업 시간·계정 상태·기존 팔로워·보유 자산·지역·언어를 기록하라.
2. 요청 채널은 모두 평가하라. 각 채널의 고객 존재 근거, 구매/관심 의도, 리소스와 형식 적합성, 제작 비용, 클릭 경로, 계정 제약을 비교하라. 인기가 있다는 이유만으로 채널을 추천하지 말라.
3. Bullseye를 적용해 후보 넓히기 → 우선순위 → 작은 실험 → 작동하는 채널 집중 순서로 계획하라. 채널 점수는 의사결정 가설이며 실제 데이터가 아님을 명시하라.
4. 기본은 주력 1~2개와 보조 1개로 제안하라. 사용자가 전 채널을 요구하면 전 채널 산출물을 제공하되 동시에 운영 가능한 최소 일정과 확장 순서를 나눠라.
5. 채널별 역할을 발견, 관계, 증거/설명, 전환, 재방문으로 정하고 구독 가능한 자사 허브를 연결하라. 외부 링크가 제공되지 않으면 발명하지 말라.
6. 예산·시간을 반영한 2주 실험을 설계하라. 채널마다 가설, 대상, 게시물 유형, 수량, 비용 상한, 주 KPI, 최소 관측 조건, 확대/수정/중단 기준을 사전에 적어라.
7. 게시 시간·빈도는 계정 데이터 없이는 실험 가설로 표시하라. 추천 점수와 날짜별 일정을 구분하라.

## 반환 산출물

채널 비교표, 선택/제외 이유, 채널 역할, 2주 실험 계획, Worker 작업 목록를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.
