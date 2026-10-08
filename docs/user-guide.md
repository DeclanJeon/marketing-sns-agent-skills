# 마케팅·SNS 통합 스킬 v2.0

2026-10-08 · 오케스트레이터 1개 + 워커 27개

## 가장 쉬운 사용법

전체 스킬 폴더를 구조 그대로 설치한 뒤 다음처럼 요청하세요.

> $marketing-agent-orchestrator로 이 제품을 홍보해줘. 목표는 유료 구매이고 Instagram·Threads를 사용하려 한다. 예산은 0원, 주당 2시간이다. 제공 자료의 사실만 사용하고 워커 조합을 비교한 뒤 채널별 원고·제작 명세·배포 일정·측정 계획을 만들어줘.

개발자/콘텐츠 제작자는 이렇게 쓸 수 있습니다.

> $marketing-agent-orchestrator로 첨부한 프로그램과 시연 자료를 X·YouTube·개발자 커뮤니티에 홍보해줘. 목표는 실제 활성 사용자다. 공개 URL·지원 환경·라이선스는 제공 자료를 기준으로 확인하고, 없는 정보는 미확인으로 두어라.

실제 제작·게시까지 원하면 사용할 계정·채널·콘텐츠/제작 범위·시점·예산을 요청에 포함하세요. 계정/연결 도구나 필수 자산이 없으면 완성된 수동 패키지와 재개 조건을 제공합니다. 초안과 실제 게시 완료를 구분합니다.

## 구조

유일한 총괄: marketing-agent-orchestrator.

- 마케팅 워커 12개: 조사, 브랜드, 크리에이티브, 캠페인, 판매, 가격/현금, CX, 고객 성공, 채널/리테일, 혁신/제휴, 측정, Jev 판단.
- SNS 워커 15개: 리소스 분석, 메시지, 채널 선택, Instagram, X, Threads, YouTube, TikTok, LinkedIn, 커뮤니티, 블로그/검색, 배포, QA, 제작·게시 운영, 측정.
- 기존 sns-promotion-orchestrator는 sns-campaign-operations-worker로 전환했습니다. 이전 호출은 통합 총괄로 바꾸세요. 별도의 SNS 총괄을 중첩 호출하지 않습니다.
- 실제 영상/이미지 제작 스킬은 요청과 설치된 도구가 있을 때 외부 제작 담당으로 연결합니다. 이 패키지가 모든 제작 도구나 SNS 계정 연결을 제공하는 것은 아닙니다.

## 조합과 시너지

12개 목표 레시피를 기본으로 필요한 워커만 선택합니다. 후보 최소안/균형안/확장안을 고객 근거·자산·현금·시간·도구·위험으로 비교합니다. 기존 산출물은 근거와 버전을 확인해 재사용합니다. 전체 워커를 매번 실행하지 않습니다.

8개 채널군 × SNS 레시피 8개 + 채널 없는 레시피 4개에서 현재 유효 조합은 2,044개입니다. 이는 레시피별 비어 있지 않은 채널 부분집합을 센 값이고, 입증된 전략/매출 성공의 개수가 아닙니다. 선택적 단계·세부 형식·내용 변형은 제외했습니다. 실제 채널 적합성·예산·권한·계정은 별도로 검토합니다.

시너지 설계와 조건은 총괄의 references/synergy-playbooks.md, 조합 선택/확장은 references/composition-design.md, 채널별 제작/배포는 references/channel-production-distribution.md를 참고하세요.

## 새 워커를 더할 때

스킬은 frontmatter 이름으로 찾습니다. 새 워커의 assets/worker-capability.json에 role, provides, requires, phase, channels, conflicts_with를 기록하면 다음 discovery에서 자동 후보가 됩니다. 같은 기능을 두 워커가 제공하면 비교 후 명시 선택하고 이름 순으로 임의 선택하지 않습니다.

descriptor가 없지만 관련 있는 새 설치 스킬은 본문을 읽어 입출력을 확인한 뒤 작업 위치의 임시 extra-registry.json으로 연결할 수 있습니다. 스킬 자체는 자동 수정하지 않습니다. 설치되지 않은 이름·중복·의존 순환은 거부합니다. 새 사업 목표에는 레시피를 추가하며 새 기능을 등록한 것만으로 시너지가 입증되지는 않습니다.

## 조합 도구 예시

ZIP을 푼 폴더에서 실행하세요. 입력 파일은 스킬 폴더 밖 작업 위치에 보관합니다.

```bash
python3 marketing-agent-orchestrator/scripts/compose_workers.py --skills-root . --recipes marketing-agent-orchestrator/assets/combination-recipes.json --count
python3 marketing-agent-orchestrator/scripts/compose_workers.py --skills-root . --recipes marketing-agent-orchestrator/assets/combination-recipes.json --job /absolute/job.json --output /absolute/plan.json
```

composition-job-template.json은 예제입니다. 목표 recipe_id와 요청 channels, 기존 artifact ID, 추가 기능, 제약 플래그를 채웁니다. plan은 워커 계획이며 실제 호출·제작·게시를 자동 실행하는 서버가 아닙니다. 공수 unknown은 0분 작업을 뜻하지 않습니다.

## 제작·배포 흐름

근거 원장/atom → 필요한 사업 전략·오퍼 → locked message → 채널 선택 → 채널별 완성 원고 → 일정 → 의미/채널 QA → 실제 제작/게시 운영 → 채널/사업 측정 → 다음 revision.

각 채널은 훅·본문·장면/페이지·자막·CTA 위치·규격/음원 검토가 다릅니다. 동일 master의 사실과 약속만 공유하고 같은 글을 전 채널에 복제하지 않습니다. 제작 명세만 있으면 미제작, URL/계정/권리/최종 검사가 없으면 draft/blocked입니다. timeout은 결과 조회 전 재게시하지 않습니다.

## Jev와 공급자

marketing-decision-judge의 providers.example.json을 작업 위치에 복사하고 OpenRouter/TypeSafe 직접/호환 구조화 모델 중 profile을 명시 선택합니다. 키는 지정 환경 변수로만 제공합니다. 실제 정답 표본 평가와 설정별 교정이 없으면 review를 유지합니다. 산술·날짜·권한 검사는 모델이 아닌 결정적 검사로 수행합니다.

## 검증과 남은 범위

통합 조합 25개, SNS 구조/운영 44개, judge/평가 54개 총 123개 코드 테스트를 통과했습니다. 2,044개 조합의 DAG 검사와 베개/CSV 프로그램의 독립 모의 실행 2건을 검토했습니다. 실제 API·미디어 생성·SNS 게시·정산은 검증하지 않았습니다. 기존 책 152개 원칙의 원문 구절 연결과 장별 전수 검토는 계속 미완료입니다. 자세한 결과는 unified-qa.html에 있습니다.
