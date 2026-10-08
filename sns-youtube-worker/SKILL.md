---
name: sns-youtube-worker
description: Create YouTube long-form and Shorts promotion packages, scripts, titles, descriptions and next-view journeys from resource evidence. Use for YouTube channel promotion or an assigned YouTube stage; actual video production belongs to production tools.
---

# YouTube 게시·홍보 Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 고객의 검색 질문·보고 싶은 시연·이해에 필요한 깊이를 기준으로 long-form과 Shorts를 구분하라. 유입 Short와 상세 영상의 약속을 연결하라.
2. 제목 3개, 썸네일 문구 2개와 시각 설계, 초반 훅, 완전한 대본을 작성하라. 제목에서 약속한 결과를 영상에서 회수하고 과장된 수치·썸네일은 제외하라.
3. 시간 구간별 narration, 화면/자료, 증거 ID, 자막, CTA를 적어라. 예상 발화 시간을 계산하고 실제 보유 영상과 추가 제작 요청을 나눠라.
4. 설명란, 실제 시간 확정 후 넣을 챕터, 고정 댓글, 후속 관련 영상·재생목록 경로를 작성하라. 챕터 타임코드를 렌더 전 확정값처럼 쓰지 말라.
5. Shorts는 최대 길이·비율·음원 및 Content ID 조건을 공식 안내에서 확인하라. 정책·언어별 페이지가 상충하면 보수적으로 권리가 명확한 자산을 쓰고 충돌을 기록하라.
6. Shorts 설명/댓글의 일반 URL은 클릭되지 않는다는 점을 반영하라. 관련 영상이나 채널 프로필 링크로 실제 전환 경로를 설계하고 필요한 기능 권한을 확인하라.
7. 기존 긴 콘텐츠를 독립적인 Short로 재구성하라. 맥락 없이 중간만 잘라내지 말고 각 Short에 완결된 가치와 다음 행동을 넣어라.
8. long-form은 impressions CTR·시청 유지·다음 영상·전환을, Shorts는 views와 engaged views·계속 시청·전환을 구분하라. 게시물 간 차이만으로 인과관계를 선언하지 말라.

## 반환 산출물

영상 형식/유입 설계, 완성 대본, 제목/썸네일, 설명/댓글, 쇼츠 파생안, 자산 요청, KPI를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.
- [platform-checks.md](references/platform-checks.md): 플랫폼 형식·링크·측정 설정 전에 읽고 공식 안내를 갱신하라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.
