---
name: sns-x-worker
description: Write X-specific posts, threads and conversation-based promotion from resource evidence. Use for X/Twitter copy or an assigned X stage, including Korean weighted-length validation.
---

# X 게시·홍보 Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 원본에서 하나의 명확한 주장과 시연·근거를 뽑아라. 단일 포스트와 연속 포스트 중 정보량에 맞는 형식을 골라라.
2. 첫 포스트에 고객 문제 또는 발견과 구체적 결과를 넣어라. thread의 각 포스트를 독립적으로 이해 가능하게 하고 근거·한계·CTA까지 완성하라. 이어지는 번호도 길이 계산에 포함하라.
3. 일반 포스트의 가중 길이 한도를 확인하라. 한글은 보통 가중치 2, URL은 감지된 링크당 23으로 계산된다. 정확한 검사는 공식 twitter-text 또는 게시 작성기의 검사를 사용하라. Python len만으로 통과를 선언하지 말라. 긴 포스트 기능은 계정별 사용 가능성을 확인하라.
4. 도구가 없으면 짧고 보수적인 초안을 만들되 length_check=unverified로 표시하라. 링크·이모지·멘션·번호를 포함한 최종 문자열을 검증하라.
5. 데모 GIF·스크린샷·코드 결과가 있으면 설명과 대체 텍스트를 함께 제공하라. 코드 스크린샷에 키·고객 정보가 섞이지 않게 하라.
6. 본문 링크와 후속 답글 링크를 테스트 후보로 비교하라. 외부 링크 페널티를 확인되지 않은 법칙처럼 말하지 말라.
7. 관련 대화에 추가할 가치 있는 답글 2개와 후속 포스트 1개를 작성하라. 무관한 인기 글에 링크를 반복하거나 같은 답글을 대량 전송하지 말라.
8. 계정에서 얻을 수 있는 조회·답글·프로필 행동과 UTM 전환을 구분해 기록하라.

## 반환 산출물

완성 단일/연속 포스트, 훅 대안, 이미지 설명, 길이 검증 상태, 답글/후속 원고, KPI를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.
- [platform-checks.md](references/platform-checks.md): 플랫폼 형식·링크·측정 설정 전에 읽고 공식 안내를 갱신하라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.
