---
name: sns-campaign-operations-worker
description: Normalize channel deliverables into a campaign package, hand off authorized media production, validate preflight and record real publishing outcomes. Use for a marketing-agent-orchestrator assigned SNS operations stage or direct campaign execution preparation. Do not select the overall marketing worker team.
---

# SNS 제작·배포 운영 워커

총괄은 `marketing-agent-orchestrator` 한 개다. 기존 SNS 총괄의 운영 자료와 도구를 이 워커가 이어받는다. 예전 `sns-promotion-orchestrator` 호출은 통합 총괄로 안내하며 다시 총괄 루프를 시작하지 않는다.

## 실행
1. [references/worker-interface.md](references/worker-interface.md), [references/contract.md](references/contract.md)를 읽고 승인된 brief·선택 채널 완성 패키지·배포 일정·QA를 받으라. 전체 워커 선택은 다시 수행하지 않는다.
2. [references/intake.md](references/intake.md)와 [references/input-fallbacks.md](references/input-fallbacks.md)로 누락·접근 불가 입력을 기록하라. default ko/Asia/Seoul은 가정이며 모든 게시 일정에 시간대를 유지하라.
3. [references/validation.md](references/validation.md)로 `assets/campaign-schema.json` 규약에 완성 패키지를 정규화하라. `assets/campaign-template.json`을 복사하고 원문 atom·claim ID·채널 revision을 보존하라. 템플릿·전략을 완성 원고로 표시하지 말라.
4. [references/operations.md](references/operations.md)를 읽고 `assets/operations-template.json`으로 제작 handoff·실제 자산·게시 전 검증·실제 실행 이벤트를 연결하라. 제작이 요청되었으면 총괄이 정한 제작 담당에게 전달하고 scope 밖 유료 생성은 실행하지 말라.
5. 실제 미디어 반환 파일·해시·권리·자막·CTA·업로드 검사를 content_id/revision별로 확인하라. 초기 원고 QA를 실제 미디어 QA로 재사용하지 말라. 제작 반환 후 실제 파일/해시에 연결된 최종 quality·필요한 judge 재검토를 총괄에 요청하고 통과 전에는 draft로 유지한다. 원고/자산/계정/시간 변경은 해당 검사를 무효화한다. 구조 검사와 의미·계정 확인을 구분하라.
6. `scripts/validate_campaign.py` 및 `scripts/campaign_operations.py validate`로 campaign과 operations를 검사하라. 모든 blocker를 수정하거나 draft/blocked로 남기고 준비물은 반환하라. ready로 꾸미기 위해 unknown을 pass로 바꾸지 말라.
7. 실제 게시·예약이 요청되고 연결 도구와 기존 권한 범위가 맞으면 배포 일정의 정확한 payload로 실행하라. 실제 URL/ID·시간·응답 locator만 기록한다. timeout은 unknown이며 결과 조회 전 재시도하지 않는다. 도구 부재는 수동 게시 패키지+blocked다.
8. 스냅샷과 변경 요청을 보존하고 실제 성과 원자료를 총괄/measurement 워커에 인계하라. 실행 결과와 미해결 담당자를 반환하라. 전체 전략·채널 우선순위는 변경 제안만 하고 총괄이 결정한다.

## 명령
설치 경로를 기준으로 실행하라. 캠페인 파일은 작업 위치에 두고 개인 스킬 폴더에 고객 데이터·키를 저장하지 말라.
```bash
python3 scripts/validate_campaign.py campaign.json
python3 scripts/campaign_operations.py validate campaign.json operations.json
python3 scripts/campaign_operations.py snapshot campaign.json operations.json campaign-history
```

## 참조
- [references/source-to-action.md](references/source-to-action.md), [references/principles.md](references/principles.md), [references/source-map.json](references/source-map.json): 검토 자료와 실행 매핑.
- [references/acceptance-cases.md](references/acceptance-cases.md): 운영 수락 사례.
- `assets/example-campaign.json`, `assets/example-operations.json`: 합성 예제, 실제 제작·게시 결과가 아니다.
- `scripts/test_validate_campaign.py`, `scripts/test_campaign_operations.py`: 구조·운영 회귀 검증.
- `assets/worker-capability.json`: 운영 역할의 입출력 기능.
