# 공통 작업 계약

## 입력
campaign_id, brief_version, resource_ids, claim_ledger, content_atoms, audience, goal, offer, brand_voice, selected_channels, budget, time_budget, accounts, language, timezone, supplied_urls, permissions, constraints를 받으라. 필수 입력이 누락되면 assumed 또는 unknown으로 표시하고 확인된 범위에서 진행하라.

## 근거
claim에는 claim_id, text, source_id, locator, status(verified/user_reported/hypothesis/unknown), conditions를 기록하라. verified는 원본을 실제 확인한 경우이며 사용자 주장 자체가 객관적 증명이 되지 않는다. 조사 자료의 사례 수치와 홍보 제품의 수치를 혼동하지 말라. URL/타임코드/문서 절·문단/코드 파일로 추적 가능하게 하라.

## Worker 반환
worker_name, campaign_id, brief_version, status(done/partial/blocked), assumptions, evidence_ids, deliverables, asset_requests, open_questions, next_owner를 반환하라. 참고 문헌 링크는 독자용 완성 원고와 분리할 수 있으나 원고의 필요한 사실 출처는 유지하라.

## 채널 게시 패키지
content_id, revision, channel, surface, audience, goal, angle, source_atom_ids, claim_ids, format, hook, body_or_script, caption_or_description, title_cover, asset_specs, alt_text_or_captions, cta, link_path, supplied_url, utm, publish_at, timezone, promotion_actions, primary_kpi, diagnostic_metrics, experiment, qa_status, length_check, feature_checks, publication_status를 채워라. 해당 없는 필드는 null 또는 not_applicable로 표시하라. 미확인 링크·규격은 unknown/pending으로 적어라. 영상·이미지 설계와 실제 렌더 파일을 구분하라.

## 상태와 권한
전략 작성은 게시 권한이 아니다. draft → reviewed → ready 순으로 원고 상태를 유지하고 실제 게시/예약 응답이 있을 때만 published/scheduled를 기록하라. final revision, 계정, 채널, 시간, 예산이 승인 범위와 맞는지 확인하라. 이미 승인된 범위는 반복 확인하지 말라. 실패·타임아웃에는 결과 조회 후 재시도하고 content_id 기반 중복 방지를 적용하라.

## 최신성과 품질
글자 수·비율·길이·링크·태그·예약·음원·광고 공개는 공식 안내와 계정/도구 상태로 확인하라. 조회 일자·공식 URL·확인 범위를 적어라. 캐시된 문서는 출발점이며 새 캠페인에서 재확인하라. 확인 실패는 규격 검증 대기이며 전략·초안 작성은 계속하라. 알고리즘 가중치·최적 게시시간·보장 조회수는 추정하지 말라.
