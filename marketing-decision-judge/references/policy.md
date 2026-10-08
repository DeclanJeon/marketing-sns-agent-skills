# 판단 정책과 교정

## 상태
- noul은 true의 확률이다. 초기 제안 임계값은 p≥0.90 true, p≤0.10 false, 그 사이는 review다. 이 수치는 성능 보장이 아니다.
- 초기 설정 calibrated=false이면 높은 확률도 review로 반환한다. 실제 목표 도메인에서 표본 평가와 기준 합의가 완료되어야 분기를 활성화한다.
- 근거 상태가 sufficient가 아니면 확률과 무관하게 review다. 빈 근거는 false가 아니다. 충분하다는 표시는 에이전트가 출처·범위·시점과 반례를 검토해서 입력한다.
- choice/score는 confidence와 확률 분포를 함께 본다. confidence는 승자 확률과 같은 값이 아니고 정확도 보장도 아니다.
- 질문의 의미와 실행 조건을 구분한다. “주장이 근거와 일치하는가”, “브랜드 톤과 맞는가”, “추가금이 투명한가”를 따로 평가한다. 승인 범위는 코드·사용자 요청으로 확인한다.

## 목표 도메인 평가
1. 실제 업무의 명확한 긍정·부정·모호·상충·인젝션 사례를 모으고 담당자가 근거와 정답을 작성한다.
2. 질문·기준을 조정하는 개발 표본과 최종 평가 표본을 분리한다. 같은 사례를 반복 튜닝하고 평가 성능이라고 발표하지 않는다.
3. FP/FN, precision/recall, review 비율, 검토 제외된 자동 분기 오류율을 계산한다. noul은 Brier score와 구간별 교정 오차도 검토한다. 표본 수와 불확실성을 함께 보고한다.
4. 잘못 승인할 비용과 잘못 거절할 비용을 정하고 임계값을 선택한다. 표본이 부족하면 review를 유지한다.
5. calibration_record에 데이터 버전·평가 시점·모델·공급자·질문 해시·정책·표본수·평가 지표·승인자를 기록한다. calibrated=true는 이 기록에 해당하는 설정에서만 사용한다.
6. 공급자·모델·기준·도메인 변화 또는 오류 증가 때 다시 calibrated=false로 전환하고 평가한다.

## 인계
최종 출력은 사실 증명서가 아닌 입력 근거에 대한 모델 판단이다. 질문별 근거 ID, 질문 정의, 확률, true/false/review, 오류·검토 이유를 남긴다. deterministic hard-rule failure와 semantic model judgment를 같은 boolean으로 섞지 않는다. 공개 전에는 실제 게시 권한·가격 최신성·고객 조건을 확인한다.

## 교정 기록의 실행 계약
`domain_id`와 근거 ID를 입력에 포함하라. 근거가 충분하다는 표시에는 `evidence_ids` 또는 질문별 `evidence_refs`가 필요하다. 모델은 근거가 충분한 질문만 호출하며 전부 누락·상충이면 호출 없이 review로 반환한다.

calibration_record는 다음 값을 요구한다: configuration_hash, sample_count, evaluation_id, actual_models(평가된 실제 버전 목록), actual_providers(평가된 실제 공급자 목록), valid_until(시간대 포함 ISO 시각). configuration_hash는 `scripts/judge.py`의 `calibration_fingerprint(config, profile, job)`로 계산한다. 엔드포인트·어댑터·모델·공급자 라우팅·질문·업무 도메인·임계값·정책 버전이 달라지면 무효화한다. 응답의 실제 모델·공급자가 교정 목록과 다르거나 유효기간이 지나면 review다. TypeSafe 직접 연결의 공급자 표기는 `direct:api.typesafe.ai`다. 버전 별칭이 같은 문자열이어도 실제 응답 버전이 바뀌면 다시 평가한다.

`python3 scripts/evaluate.py --input /absolute/path/labeled.json --output /absolute/path/evaluation.json`으로 noul 평가 기록을 집계하라. 입력은 id, p_true, label(true/false/null)를 가진 레코드 배열이다. Brier score·ECE·오탐·미탐·검토율을 함께 읽고, 검토된 긍정 사례까지 포함하는 positive_capture_all_labeled를 확인하라. 표본 통계만으로 자동 운영을 승인하지 않는다. 실제 정답 자료가 없으면 실정확도는 미측정이다. 이 스크립트는 calibrated를 활성화하지 않는다.
