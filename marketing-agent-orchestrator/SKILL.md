---
name: marketing-agent-orchestrator
description: Be the single orchestrator for extensible marketing and SNS worker skills. Select and compose workers for research, branding, pricing, cash sales, product/code promotion, channel-native content production, distribution, publishing and measurement. Use for end-to-end marketing, multi-channel SNS promotion, goals requiring multiple workers, or a marketing team. Discover installed capabilities and build only the needed dependency graph; direct narrow tasks may use a worker.
---

# 마케팅·SNS 통합 오케스트레이터

마케팅 12개와 SNS 15개 워커를 조합하는 유일한 총괄이다. 기존 SNS 총괄은 `sns-campaign-operations-worker` 운영 워커로 전환했다. 워커를 하나 더 늘릴 때 총괄을 추가하지 말고 capability registry를 확장한다.

## 실행
1. 사용자 요구를 goal·deliverables·고객/제품·리소스·단계·요청 채널·기한·현금/예산/시간·계정·도구·권한·기존 산출물로 정규화하라. `assets/task-template.json`으로 brief/evidence ledger를 만들고 미확인은 가설로 남겨라. 기본 ko/Asia/Seoul은 사용자 맥락에 맞춰 가정으로 표시한다. 중요한 누락만 묻고 독립 준비는 계속한다.
2. [references/composition-design.md](references/composition-design.md)를 읽고 설치된 워커를 frontmatter 이름과 worker-capability로 발견하라. 예제 registry는 snapshot이며 실제 목록을 대신하지 않는다. 관련 미등록 스킬은 계약 등록 제안으로 남기고 자동 설치·수정하지 않는다.
3. [references/synergy-playbooks.md](references/synergy-playbooks.md)의 12개 recipe 중 목표에 맞는 최소 흐름을 고르고 조건부/새 기능은 extra_capabilities로 추가하라. 최소안/균형안/확장안을 자원·근거·목표 행동·현금·도구·위험으로 비교한다. 이미 있는 검증 산출물은 artifact/revision별로 재사용하고 중복 전략을 만들지 않는다.
4. `assets/composition-job-template.json`을 작업 위치로 복사하고 `scripts/compose_workers.py`로 필요한 워커·입력 의존성·병렬 그룹·충돌/누락·유효 조합 수를 검사하라. --count 수는 레시피×채널 부분집합이며 성공이 입증된 전략 수가 아니다. 공수 미확인은 unknown으로 남기고 요청 채널을 몰래 삭제하지 않는다.
5. 모든 워커의 worker-interface 계약으로 campaign_id/plan_id/task_id·brief_version·입력 artifact/근거·locked_fields·범위·완료 기준을 전달하라. 증거와 약속을 잠그고 의존 입력을 먼저 확정한다. 독립 채널 워커만 병렬 가능하다. 별도 에이전트는 요청/런타임이 허용할 때 적용하고 없으면 순차 적용한다.
6. [references/strategy-conflicts.md](references/strategy-conflicts.md)로 책의 상충 처방을 조건별 비교하라. 책은 고객 사실·효능의 증거가 아니다. 참/거짓 의미 판정은 marketing-decision-judge로 공급자/모델을 명시 선택하고 미설정/미교정은 review로 남긴다. 산술·허용 목록·권한·날짜는 코드와 실제 요청으로 확인한다.
7. [references/channel-production-distribution.md](references/channel-production-distribution.md)와 선택 채널 SKILL.md로 완성 원고·대본·페이지/컷·CTA·접근성·제작 명세를 만들라. 동일 약속을 유지하되 채널별 원고를 재작성한다. marketing-social-campaign은 캠페인 방향, SNS 채널 워커는 원고를 담당한다.
8. distribution은 시간대·담당자·클릭/주문 경로·2주 일정을 연결하고 judge/quality는 주장·채널·CTA를 검토한다. 운영 워커가 campaign/operations 규약으로 정규화하고 실제 제작 요청이면 지정된 제작 담당에 인계한다. 초기 QA는 원고 사전 검토다. 제작 반환 후에는 실제 자산/해시에 연결된 최종 quality 검토와 필요한 judge 검토를 다시 수행하라. 실제 자산·권리·길이·계정 규격·CTA·버전별 최종 검토 이후만 ready로 둔다.
9. 실제 게시·예약·발송·집행이 요청되고 기존 승인 범위와 연결 도구가 맞으면 운영 워커로 실행한다. 매번 재승인을 요구하지 않는다. 요청 없는 유료 생성/게시를 실행하지 않으며 도구/자산 부재는 완성 수동 패키지와 blocked 사유를 제공한다. 실제 URL/ID/응답·시간만 기록하고 timeout은 조회 전 재시도하지 않는다.
10. SNS measurement→business measurement로 지표 정의·원자료·비용·실입금/활성화/유지를 연결한다. 결과 없으면 측정 계획만 반환한다. 수정은 한 변수·관측 근거·다음 revision·담당자를 지정하고 영향받는 워커만 재실행한다. 검토 수정 최대 2회 뒤 unresolved를 보고한다.

## 반환
선택/제외 워커와 이유, 후보 조합 비교, 실행 DAG, 근거/조건/가설, locked brief, 채널별 완성 원고와 실제/미제작 자산 구분, 제작·배포 일정, QA/blocked/실제 실행 기록, 측정·다음 수정 계획을 반환한다. 짧은 업무는 해당 범위 결과만 제공한다. plan 완료와 실제 게시 완료를 구분한다.

## 자료
- [references/composition-design.md](references/composition-design.md): 확장 발견·조합 수·DAG·선택·재사용.
- [references/synergy-playbooks.md](references/synergy-playbooks.md): 12개 목표별 시너지·인계·충돌.
- [references/channel-production-distribution.md](references/channel-production-distribution.md): 채널 제작·배포·피드백.
- [references/unified-acceptance.md](references/unified-acceptance.md): 통합 수락 기준.
- `assets/combination-recipes.json`, `assets/composition-job-template.json`, `assets/worker-registry.example.json`, `assets/worker-capability.example.json`: 조합 계약·레시피·snapshot·확장 양식.
- `scripts/compose_workers.py`, `scripts/test_compose_workers.py`: 현재 등록 워커 발견·조합/공수/의존성 검사 및 회귀 테스트. 외부 실행 도구가 아니다.
- [references/routing.md](references/routing.md), [references/operational-playbooks.md](references/operational-playbooks.md): 분야별 선택과 광고/CRM 등 추가 운영.
- [references/source-review.md](references/source-review.md), [references/strategy-conflicts.md](references/strategy-conflicts.md), [references/review-limitations.md](references/review-limitations.md): 책 기반 프레임과 미완료 검토 범위.
- [references/examples.md](references/examples.md), [references/acceptance-scenarios.md](references/acceptance-scenarios.md): 기존 업무 수락 기준.
- `assets/task-template.json`, `assets/agent-task-template.json`, `assets/campaign-operations-template.json`: 기존 작업·운영 계약.
- `assets/source-catalog.json`, `assets/source-coverage.json`: 원본 검토 수준. 통합 후에도 장별·원칙별 검증 미완료를 유지한다.
