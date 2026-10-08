---
name: sns-search-content-worker
description: Create Naver Blog, Tistory, Medium and owned-blog search-led promotion drafts from supplied resources. Use for site-specific article adaptation, searchable content hubs or an assigned search-content stage.
---

# 블로그·검색 콘텐츠 Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 사이트를 네이버 블로그, 티스토리, Medium, 자사 블로그 중 명시하고 목표 검색 질문을 하나 정하라. 검색량 데이터가 없으면 가설로 적어라.
2. 고객 의도를 학습/비교/사용/구매로 분류하고 질문에 먼저 답하라. 제목 대안 3개, 소개, 소제목, 완전한 본문, FAQ, CTA를 작성하라.
3. 원본의 시연·직접 경험·비교 기준·근거를 추가하라. 키워드 반복과 타 채널 원고의 단순 복사는 피하라.
4. 자사 사이트의 메타·구조화 데이터·canonical 권한과 호스팅 블로그에서 가능한 설정을 구분하라. 네이버 Search Advisor는 일반 웹 문서 지침이며 블로그 랭킹 공식이 아님을 명시하라.
5. 원문 허브와 파생 콘텐츠의 관계를 적고 사이트 정책·저작권·중복 게재 전략을 확인하라. 이미지 설명·alt 지원 여부·출처를 적어라.
6. 인지 콘텐츠에서 데모/가격/체험으로 이어지는 내부 링크를 설계하라. 실제 링크가 없으면 pending으로 표시하라.
7. 검색 노출·클릭·방문 후 행동·구독·활성화를 측정하라. 상위 노출을 보장하지 말라.

## 반환 산출물

사이트별 검색 의도, 제목/완성 글/FAQ, 이미지 명세, 링크 구조, 게시 설정, KPI를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.
- [platform-checks.md](references/platform-checks.md): 플랫폼 형식·링크·측정 설정 전에 읽고 공식 안내를 갱신하라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.
