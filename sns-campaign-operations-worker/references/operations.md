# 제작·운영 계약 v1

## 사용 순서
campaign.json은 기존 1.1 규약을 유지한다. 추가 operations.json은 이 문서의 운영 sidecar다. 초안에서는 unresolved를 허용하고 ready/scheduled/published 게시물은 게시 전 검증을 요구한다. 결과를 내기 전에 두 파일을 검증하라. 구조 검사와 의미·실계정 검증을 구분하라.

1. assets/operations-template.json을 복사하고 캠페인 ID와 게시물 revision을 연결하라. 요청되지 않은 실제 제작·유료 생성·외부 게시를 실행하지 말라. 제작 요청이 있으면 기존 권한·예산 안에서 다음 계약으로 라우팅하라.
2. 제작: 총괄이 지정한 content-production-orchestrator(여러 제작 단계의 외부 제작 담당), orchestrating-video-preproduction(텍스트 기획), storyboarding-video(콘티), imagegen(이미지), 실제로 연결된 영상 생성·편집 스킬 중 필요한 것만 사용하라. 이름으로 찾고 부재하면 명세와 남은 작업을 반환하라. 기획·프롬프트를 완성 미디어로 표시하지 말라.
3. 제작 handoff: task_id, content_id/revision, brief_version, source_atom_ids/claim_ids, locked_fields, 목적/고객, 장면별 메시지·자막·CTA, 화면비·목표 길이, 브랜딩, 접근성, 입력 파일, 권리 상태, 예산/시간 상한, 담당 스킬, 완료 기준을 전달하라. 규격은 최신 공식 문서/실제 게시 화면으로 확인하고 임의의 최신 수치를 고정하지 말라.
4. 반환: task_id, 입력 revision, asset_id, 실제 파일 경로, SHA-256, 제작 도구 및 실제 응답 locator, 길이/크기/재생 확인, 캡션/대체텍스트, 권리·잔여 이슈. 제공 파일은 provided 상태로 표시할 수 있지만 생성했다고 주장하지 말라. 실제 자산이 없으면 requested로 유지하라. 출력 경로만 존재한다고 미디어 품질·코덱·권리가 검증된 것은 아니다.
5. 게시 전 검증: content_id/revision, channel/account/surface, 게시 payload 해시, asset hash, checked_at, method, evidence를 묶어라. checked_at은 실제 검토를 수행한 시각을 도구에서 읽어 시간대 포함 값으로 기록하라. 날짜만 알고 자정이나 임의 시각을 채우지 말라. 실제 검사를 수행하지 않았다면 검사 status=unknown을 유지하고 검토 시각을 성공 근거로 쓰지 말라. unknown 계정명은 초안의 미확인 표시일 뿐 게시 가능 계정이 아니다. 공식 문서 기준과 해당 계정 게시 화면을 구분하라. 원고·자산·계정·CTA·규격 변경은 검증을 무효화한다. 규정/계정 기능이 바뀌었거나 게시 시점에 오래된 검사라면 다시 확인하라.
6. 검증 항목은 semantic, channel_fit, accessibility, rights, upload_rules, length, cta_route다. 텍스트 전용에도 적용 여부를 이유와 함께 기록하라. not_applicable은 length나 사실/채널/CTA 검사를 건너뛰는 수단이 아니다. X 실제 길이는 twitter-text 또는 composer의 근거를 남겨라. 댓글 질문 CTA면 클릭 링크가 없어도 답글 기능/목표 행동이 가능함을 확인하라. 외부 링크는 실제 착지 페이지와 요청한 체험/문의 행동까지 확인하라.
7. 실제 실행 시 이미 받은 권한 범위를 재사용하라. 실계정/도구가 없으면 수동 체크리스트와 초안을 전달하라. timeout은 실패/성공으로 단정하지 말고 결과 조회 전 재게시하지 말라. 명시적 실패만 원인 수정 후 재시도한다. 불확실한 실행은 event outcome=unknown으로 기록하고 조회 작업을 남겨라.
8. 캠페인마다 campaign.json, operations.json, 실제 자산, 구조/의미 QA, metrics.csv를 지속 가능한 저장소에 보관하라. 개인 스킬 폴더에 캠페인/고객 데이터·키를 넣지 말라. scripts/campaign_operations.py snapshot으로 변경 시점의 JSON과 자산 해시를 보존하라. 실제 파일은 별도 함께 보관해야 한다. snapshot은 로컬 기록이며 외부 게시/영구 백업이 아니다.
9. 이미 게시된 revision은 보존하고 수정안은 revision+1로 생성하라. 게시 URL·계정·시간·revision·실제 영수증 locator를 execution event와 연결하라. 로그에 토큰·쿠키·개인 메시지 전문을 저장하지 말라.
10. 성과→실험→변경: measurement-worker에 원본 측정 데이터와 metric definition, 게시 revision, 기간, 유료 여부를 전달하라. 변경 요청에는 observation_ids, 대상 content_id/revision, 한 변수, 변경 이유, 성공/중단 기준, 관측 기간과 담당자를 넣어라. 관측이 없으면 실험 계획만 만들라. 다음 버전은 QA와 제작을 영향 범위만 재실행하라.

## 도구
```bash
python3 scripts/campaign_operations.py validate campaign.json operations.json
python3 scripts/campaign_operations.py snapshot campaign.json operations.json campaign-history
```
Python 3.9+, 표준 라이브러리. 자산 경로는 operations.json 부모에 상대적이거나 절대 경로다. 공백 경로는 shell에서 인용하라. snapshot은 전체 JSON과 SHA-256을 담으며 같은 내용 재요청은 기존 파일을 유지한다. 외부 결과의 진위나 검토 품질은 자동 판정하지 않는다.
