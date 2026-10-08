---
name: sns-instagram-worker
description: Create Instagram-specific Reels, carousel, Stories and caption promotion packages from supplied evidence. Use for Instagram promotion or an assigned Instagram stage; do not claim media was produced when only a brief exists.
---

# Instagram 게시·홍보 Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 목표와 리소스에 따라 Reels(직접 시연·발견), carousel(저장할 설명·체크리스트), Stories(관계·후속 행동)에서 적합한 형식을 선택하라. 선택 이유를 설명하라.
2. 원본 리소스에서 실제로 확보 가능한 장면·화면으로 훅 → 증거/과정 → 요점 → CTA를 구성하라. 외부 플랫폼 워터마크가 있는 재업로드 대신 원본 마스터에 맞춰 편집하라.
3. Reels는 시간 구간별 화면, 내레이션, 화면 글자, 컷 연결, 캡션·커버 문구를 작성하라. carousel은 표지와 각 페이지의 문구·시각 요소·마지막 CTA까지 완성하라. Stories는 순서·스티커·후속 경로를 적어라.
4. 캡션의 첫 문장은 콘텐츠의 약속과 일치시켜라. 관련 검색어·태그만 사용하고 태그 수나 특정 음원을 성공 공식으로 단정하지 말라.
5. CTA에 실제로 사용할 수 있는 링크 위치를 적어라. 프로필 링크·Story 링크·기타 기능의 계정 사용 가능성을 확인하고 캡션 URL 클릭 가능성을 가정하지 말라.
6. 시각장애인용 설명, 자막, 모바일 가독성, UI에 가려질 영역을 검토하라. 제작 크기·비율·길이는 최신 공식 가이드와 실제 업로드 경로에서 재확인하라.
7. 첫 게시 후 관련 댓글 응답, 질문에서 후속 carousel/Reels 제작, 협업 가능한 창작자 유형을 제안하라. 자동 DM·협업 메시지 전송은 별도 승인 범위에서만 수행하라.
8. 계정 Insights로 저장·공유·도달·프로필 행동·실제 전환을 각각 측정하라. trial 기능은 계정에서 확인된 경우만 계획에 넣어라.

## 반환 산출물

선택 형식의 완성 원고, 커버/컷·페이지 설계, 캡션, CTA 경로, 게시 후 홍보, KPI를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.
- [platform-checks.md](references/platform-checks.md): 플랫폼 형식·링크·측정 설정 전에 읽고 공식 안내를 갱신하라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.
