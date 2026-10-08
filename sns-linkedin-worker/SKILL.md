---
name: sns-linkedin-worker
description: Write LinkedIn-native professional posts, document/carousel concepts and B2B promotion based on supplied resources. Use for LinkedIn content promotion or an assigned LinkedIn stage.
---

# LinkedIn 게시·홍보 Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 독자를 직무·책임·해결 과제로 정의하라. 개발 도구라면 실제 사용자와 구매 승인자의 관심을 구분하라.
2. 구체적인 업무 문제 → 수행한 과정 → 근거 있는 결과 → 적용 방법 → CTA 순으로 완성 포스트를 작성하라. 수치를 증명할 수 없으면 관찰된 변화로 표현하라.
3. 경험형 포스트, 문서/슬라이드, 데모 영상 중 선택하고 이유를 제시하라. 문서형은 페이지별 원고와 도표에 필요한 데이터를 적어라.
4. 제품 기능을 비용·시간·품질·위험 감소로 연결하되 ROI를 발명하지 말라. 조직·고객의 기밀은 동의를 확인한 범위에서 사용하라.
5. 관련 직무의 대화에 넣을 답글과 파트너에게 보낼 소개 초안을 제공하라. 무단 태그·대량 연결 요청·메시지 전송은 하지 말라.
6. 개인 계정과 회사 Page의 분석·권한을 구분하라. 채널 지표와 적합한 리드·상담·활성화·구매를 연결하라.

## 반환 산출물

직무별 가치, 완성 포스트, 선택 형식의 자산 명세, 답글/소개 초안, 리드 KPI를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.
- [platform-checks.md](references/platform-checks.md): 플랫폼 형식·링크·측정 설정 전에 읽고 공식 안내를 갱신하라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.
