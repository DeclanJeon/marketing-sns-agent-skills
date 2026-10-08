# 관측에서 다음 버전까지

metrics.csv 필드: observation_id, content_id, revision, channel, account, observed_at, window_start, window_end, metric, value, denominator_metric, denominator, definition, source_locator, traffic_type, attribution_window. 알 수 없는 수치는 빈칸으로 남기며 0으로 대체하지 말라. 개별 고객 개인정보는 수집하지 말라.

1. 게시물/실제 URL·revision과 데이터를 매칭하라. 기간·시간대·관측 시점이 다른 값은 분리하라. 동일 observation_id 중복이나 누적 값의 반복 합산을 막아라.
2. 조회·클릭·문의·적합 문의·실제 주문을 구분하라. 원자료가 지표 정의를 지원하지 않으면 해석을 보류하라. 비율은 같은 기간의 분자/분모를 쓰고 0/누락 분모는 계산 불가다.
3. 사전 계획한 관측 시점을 우선하라. 예: 초기 오류 확인, 7일 평가, 14일 후속 평가는 캠페인 가정으로 제시할 수 있으며 플랫폼 권장값이나 최적값으로 단정하지 말라.
4. 가설, 관측, 해석을 따로 보고하라. 유기적 비교의 노출량·시간·대상 차이와 작은 표본을 기록하라. 승자를 찾기 위해 매번 관측 기간을 바꾸지 말라.
5. change_request: request_id, content_id, from_revision, observation_ids, decision=keep/modify/stop/collect_more, variable, rationale, next_owner, review_window, decision_rule. modify면 명확한 문구/CTA/포맷 변경을 한 변수로 제시하라. 데이터가 없으면 observation_ids=[]과 planned를 명시하라.
6. 오케스트레이터는 다음 revision을 만들고 원고/자산/QA 영향 범위만 다시 실행한다. 게시된 원본을 덮어쓰지 말고 관측→변경→새 게시물의 관계를 보존하라. 확대/유료 집행은 예산과 실행 권한 범위 안에서만 진행한다.
