---
name: sns-quality-reviewer
description: Review drafted SNS campaigns for claim support, channel fit, CTA feasibility and operational readiness. Use for assigned SNS QA or pre-publication review; semantic judgments do not replace source verification.
---

# SNS 사실·채널 QA Worker

공통 계약을 먼저 읽고 할당된 단계의 산출물을 완성하라. 작업 언어는 사용자 지정에 따르고 기본은 한국어이다.

## 실행

1. 원고와 resource/claim ledger를 비교하라. 모든 수치·효능·비교·경험담·인용·후기는 근거와 조건을 확인하라. 출처가 불명확하면 삭제·완화·추가 자료 요청을 선택하라.
2. 핵심 메시지, 고객 가치, 훅의 약속과 본문 회수, 채널의 문체·형식·가독성, 접근성, CTA의 실현 가능성을 점검하라.
3. 링크·계정 기능·길이·미디어 규격·광고 공개·음원/이미지 권리는 공식 근거 또는 실제 업로드 경로로 확인하라. 모르면 unknown을 쓰고 게시 가능을 선언하지 말라.
4. 검사 결과는 check_id, 대상 content_id, pass/fail/unknown, evidence_ids, 이유, severity, 수정안을 포함하라. 숫자 계산·길이 검사는 결정적 도구로 먼저 수행하라.
5. 선택적으로 사용자가 지정한 판단 모델/프로바이더가 실제 사용 가능할 때만 semantic judge에 원고·판정 기준·근거를 전달하라. Jev 또는 호환 모델의 존재·endpoint를 추정하지 말라. 모델 판정은 증거 확인 후 보조 검토에만 쓰라. 외부 전송 권한과 민감 데이터 범위를 확인하라.
6. judge가 boolean만 반환하면 입력 근거가 충분한 경우에만 true/false를 평가하라. 근거 누락·응답 오류·타임아웃은 true로 처리하지 말고 unknown으로 반환하라. provider, model, 기준, 판정 시간을 기록하라.
7. 치명적인 오류는 해당 게시물만 owner Worker로 반환하라. 최대 2회 수정 후 unresolved를 보고하고 다른 사용 가능한 원고는 제공하라. 원고 해시/버전이 바뀌면 기존 QA·게시 승인 적용 여부를 재평가하라.
8. 게시 성공은 연결 도구의 실제 응답으로만 확인하라. 이 검토는 게시·메시지·광고 집행 권한을 부여하지 않는다.

9. 오케스트레이터가 정규화한 패키지의 구조 검사 결과와 의미 검토 결과를 따로 보고하라. 구조 통과를 사실 검증으로 대체하지 말라. ready는 QA passed, 자산 확보, 기능·길이 검사 완료 조건을 모두 만족해야 한다. final 전달본과 실제 게시 상태를 구분하라.

## 반환 산출물

검사표, blocker/수정안, content별 ready/draft 상태, judge 사용 여부·한계, 최종 버전를 제공하라. 작업 계약에 맞춰 assumptions, evidence_ids, 미확인 사항, 다음 담당자를 함께 반환하라. 채널 전략은 완성 게시 원고·대본을 대체하지 않는다.

## 리소스

- [contract.md](references/contract.md): 실행 전 입력·출력·근거·권한 계약을 읽어라.
- [principles.md](references/principles.md): 메시지·실험을 설계할 때 자료에서 도출한 원칙을 적용하라.
- [source-map.json](references/source-map.json): 자료 출처·locator·해시를 확인할 때 읽어라.

## 운영 검토

[semantic-preflight.md](references/semantic-preflight.md)를 읽고 구조·의미·실계정 검증을 각각 보고하라. 오케스트레이터의 운영 계약에 맞춰 revision/payload/asset hash별 preflight를 반환하라. 미확인 항목은 draft로 남기고 수정 책임자를 지정하라.

## 통합 워커 역할
[references/worker-interface.md](references/worker-interface.md)를 읽고 총괄의 작업 계약·입력 버전·완료 기준을 따른다. 역할과 입출력 기능은 `assets/worker-capability.json`으로 제공한다. 단일 업무는 직접 수행할 수 있으나 통합 캠페인 워커 선택은 `marketing-agent-orchestrator`에 반환한다.

통합 실행에서는 의미 참/거짓 판정은 marketing-decision-judge의 결과를 사용한다. 미설정 review는 unknown으로 매핑하고 원문 대조와 채널 검토는 계속 수행한다. 최종 campaign 구조 검사는 sns-campaign-operations-worker가 수행한다.
