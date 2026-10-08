# 확장 가능한 조합 설계 v2

## 총괄과 역할
유일한 진입점은 marketing-agent-orchestrator다. 마케팅 12개 + SNS 15개 워커를 필요에 따라 선택한다. sns-promotion-orchestrator는 sns-campaign-operations-worker로 전환됐다. SNS 전체 팀을 별도 총괄로 호출하거나 워커가 총괄을 재호출하는 순환을 만들지 않는다. 콘텐츠 제작 전용 스킬은 실제 제작이 요청될 때만 외부 제작 담당으로 연결한다.

## 발견과 확장
1. 설치된 SKILL.md의 frontmatter 이름과 assets/worker-capability.json을 읽어 후보 목록을 갱신한다. 폴더 ID와 고정 sibling 경로에 의존하지 않는다. 스킬 이름·설명·role·provides·requires·phase·채널·충돌·버전을 함께 확인한다.
2. descriptor가 없는 새 스킬도 설명에서 관련 후보로 찾을 수 있지만 모델이 실제 입출력을 확인해 임시 capability 계약을 작업 위치의 extra-registry.json에 작성한다. 실제 설치 이름·스킬 본문과 입출력을 확인하고 --extra-registry로 해당 캠페인에만 합친다. 확인할 수 없으면 capability_gap으로 남긴다. 캠페인 중 설치된 스킬을 자동 수정하지 않는다. 실행 가능한 조합에는 검토된 계약을 갖는 워커만 등록한다.
3. 새 워커의 capability가 기존 것과 같으면 후보 간 근거·공수·품질·제약을 비교하고 provider_overrides로 명시 선택한다. 코드가 이름 순으로 임의 선택하지 않는다. requires/provides 및 phase 순환·충돌을 검사한다.
4. 단일 워커 추가는 새 channel_package capability 또는 extra_capabilities로 조합에 연결할 수 있다. 새로운 사업 목표는 레시피를 추가한다. 기능 등록만으로 새 목표 전략이나 시너지가 입증되지는 않는다.

## 선택 절차
사용자 요청을 primary_goal, secondary_goals, deliverables, product/resource type, lifecycle stage, requested_channels, audience evidence, deadline, cash/budget/time, accounts/tools, existing_artifacts, authorization_scope로 정규화한다. goals를 조회수 대신 고객 행동으로 쓴다. 의미 분류/적합성 true/false는 decision-judge와 근거 원장을 사용하고 미설정은 review다. 산술/허용 목록/의존성 검사는 코드로 한다.

12개 레시피 중 최소 하나를 기본으로 선택하고 secondary goal은 extra_capabilities로 합친다. 관심 고객 자료가 없으면 조사, 선지출·정산 제약이면 가격/현금, 서비스 위험이면 CX를 조건부 추가한다. 이미 검증된 산출물이 있으면 artifact_id/revision/근거를 확인해 available_capabilities로 재사용한다. 브랜드와 SNS 메시지는 새로 서로 다른 약속을 만들지 않고 같은 locked brief에서 파생한다.

최소안 / 균형안 / 확장안의 2~3개 후보를 비교한다. 항목: 목표 기여 경로, 근거, 준비된 자산, 제작·운영 시간, 선지출과 정산, 실행 도구, 검토 비용, 예상 시너지와 위험. 근거 없는 점수를 확률/성과로 쓰지 않는다. 시간 추정은 사용자 제공 또는 측정 기반이며 없으면 unknown이다. 시간/예산 상한을 넘으면 요청 채널을 몰래 삭제하지 않고 일정 분산·재사용·단계 확장 대안을 제안한다.

## 의존성·병렬·재사용
brief/evidence_ledger → 리소스 atom → 필요한 조사/전략/오퍼 → 캠페인 메시지 → 채널 선택 → 채널별 원고 → 배포 일정 → 의미/채널 QA → 제작/게시 운영 → 채널 측정 → 사업 지표 순서다. 일부 사업 단계는 요청/재사용에 따라 생략한다. locked brief가 확정된 이후 독립 채널 워커는 같은 병렬 그룹이다. 전략·가격 변경 전에 downstream 원고를 확정하지 않는다.

compile 도구는 입력 capability와 recipe를 의존성 DAG로 바꾸고 phase 순서로 게이트를 둔다. phase는 작업 순서 제약이며 자동 사실성/시간/권한 검증이 아니다. 같은 phase가 병렬 가능해도 실제 별도 에이전트 실행은 사용자 요청·런타임 범위에 따른다. 도구가 없으면 계약 순서로 동일 에이전트가 수행한다.

재사용 master는 사실·가격·CTA 약속·금지 주장만 공통이다. 원고/훅/길이/장면/링크 위치/규격/음원은 채널별로 재작성·검증한다. 캠페인 측정은 신규 유입·활성화·실입금·유지 등 동일 business goal로 연결하되 플랫폼 조회수는 합산 비교하지 않는다.

## 조합 수의 정의
scripts/compose_workers.py --count가 현재 registry에서 가능한 레시피×채널 부분집합과 중복 제거 워커 집합을 산출한다. 현재 8개 채널군(Instagram, X, Threads, YouTube, TikTok, LinkedIn, 커뮤니티, 블로그/검색), SNS 필요 레시피 8개, 채널 없는 레시피 4개다. 명목 수는 8×(2^8−1)+4=2,044개이며 도구가 누락/중복/순환으로 실패하는 변형은 유효 수에서 제외한다. 독립적인 의미의 마케팅 전략 2,044개나 성공이 입증된 시너지 2,044개가 아니다. optional stage, 세부 형식, 사이트/게시판, 언어, 내용 변형은 이 수에 포함하지 않는다.

새 채널군 n이면 기본식 8×(2^n−1)+4이며 registry/recipe 변경 후 실제 유효 수와 unique_worker_sets를 다시 계산한다. 모든 워커의 2^27개 무작위 조합은 설계하지 않는다. 동일 capability/worker 조합이 레시피 이름만 다르면 unique_worker_sets에서는 하나로 센다.

## 실행과 완료
계획 DAG 완료와 실제 캠페인 완료를 구분한다. 실제 제작/게시가 요청되면 채널 워커의 제작 명세를 운영 워커에 넘기고 요청 범위의 제작 스킬로 실제 자산을 확보한다. 실제 미디어·CTA·계정·규격·권리·최종 버전 검토가 ready 게이트다. 승인된 실행 범위가 있고 연결 도구가 있으면 게시하며 URL/ID/실제 응답을 기록한다. 연결이 없으면 완성 수동 패키지와 blocked 이유를 제공한다.

도구 명령(스킬 설치 경로 기준):
```bash
python3 scripts/compose_workers.py --skills-root /absolute/installed-skills --recipes assets/combination-recipes.json --job /absolute/job.json --output /absolute/plan.json
python3 scripts/compose_workers.py --skills-root /absolute/installed-skills --recipes assets/combination-recipes.json --count
```
설치본이 스킬 이름 폴더인 ZIP 구조와 skill-ID 폴더인 환경을 모두 지원한다. 새 워커를 추가할 때 worker-capability.example.json 규약을 사용하고 테스트를 실행한다. 본문을 읽어 생성한 임시 계약은 {"workers":[계약]} 형식으로 저장하고 --extra-registry /absolute/extra-registry.json을 추가한다. 설치 이름이 없는 허구 워커와 중복 이름은 거부한다.
