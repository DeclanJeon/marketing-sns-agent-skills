# 패키지 정규화와 검증

## 규약
최종 산출물을 assets/campaign-schema.json의 캠페인 형식으로 정규화하라. 기존 Worker의 텍스트 반환은 오케스트레이터가 병합한다. resources[].resource_id, claim_ledger[].claim_id, content_atoms[].atom_id를 각각 구분하고 body_or_script에는 독자가 쓸 완성 원고를 넣어라. 참고 문헌·검토 설명을 원고와 분리하라.

Worker 결과는 jobs[]에 worker_name, status, brief_version, evidence_ids, deliverables, assumptions, open_questions, next_owner로 기록하라. 모든 Worker가 실제 실행된 것처럼 기록하지 말라. 형식상 jobs[]는 실행 기록의 표현이며 도구 실행을 증명하는 로그가 아니다.

schema_version=1.1. bootstrap은 초기 템플릿이고 최종 원고가 아니다. draft는 미확인 항목을 포함한 완성 초안, final은 선택 채널별 패키지가 존재하는 최종 전달본이다. final도 실제 게시 상태 ready/published를 뜻하지 않는다. 1.0의 텍스트 length_check를 1.1에서는 {status,evidence}로, feature_checks를 {name,status,evidence} 배열로 바꾸라. 적용 불가 항목은 not_applicable을 쓰고 왜 적용 불가인지 evidence로 남겨라.

## 실행
Python 3.9+가 있으면 다음 명령을 실행하라. 외부 패키지와 네트워크가 필요 없다.

```bash
python3 scripts/validate_campaign.py assets/example-campaign.json
python3 scripts/validate_campaign.py campaign.json --require-posts
```

스킬 폴더 안에서 실행하라. 다른 위치에서는 실제 스크립트/JSON의 절대 경로를 사용하라. exit 0은 구조·참조·상태 검사 통과, exit 1은 실패이다. 상세 errors와 warnings를 출력한다. 테스트 입력에 사용하는 example-campaign.json은 합성 예제이며 실제 게시/성과 데이터가 아니다.

## ready 게이트
주장·자산·기능·글자 수 검증이 완료되고 QA passed인 경우만 ready로 올려라. 검증 결과 passed에는 어떤 검사를 했는지 evidence를 남겨라. X의 가중 길이는 공식 parser/작성기로 확인해야 한다. 이 스크립트는 길이를 재계산하지 않으며 문구의 사실성·저작권·정책의 최신성을 증명하지 않는다.

scheduled/published는 실제 실행 receipt와 해당 버전·계정·채널·시간에 맞는 허가 scope가 있어야 한다. ready는 게시 권한을 부여하지 않는다. 실제 승인 범위가 이미 정해져 있으면 반복 승인 요청하지 말라. 시간대는 캠페인과 게시 패키지 전체에 동일하게 유지하라.

## 회귀 확인
scripts/test_validate_campaign.py로 합성 입력의 양성/음성 경계 사례를 확인하라. 이 검사는 SNS API·음원·실제 계정 접근을 수행하지 않는다. Python이 없으면 동일 체크 항목을 수동으로 검토하고 자동 검사 미실행을 표시하라.
