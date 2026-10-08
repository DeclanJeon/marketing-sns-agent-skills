# 작업 라우팅

| 요청 | 적용 스킬 |
|---|---|
| 시장·고객 조사 | `marketing-market-research` |
| 브랜드 전략 | `marketing-brand-strategy` |
| 광고·메시지 설계 | `marketing-creative-messaging` |
| SNS·홍보 캠페인 | `marketing-social-campaign` |
| 판매·전환 설계 | `marketing-sales-conversion` |
| 가격·수익 설계 | `marketing-pricing-profit` |
| 고객 경험·서비스 | `marketing-customer-experience` |
| 고객 성공·구독 | `marketing-customer-success` |
| 유통·리테일 | `marketing-channel-retail` |
| 신사업·제휴 기획 | `marketing-innovation-partnerships` |
| 성과 측정·실험 | `marketing-measurement-experiments` |
| 참·거짓, 적합성, 주장 근거 검수 | `marketing-decision-judge` |

SNS 판매: research(고객 자료가 없을 때) → pricing(가격 요청 시) → creative → social/sales → judge → 승인된 게시 → measurement.
구독 유지: success → cx(마찰 확인 시) → measurement.
신제품: research → innovation → brand → pricing → 필요한 콘텐츠 → measurement.
이미 충분한 전략 자료가 있으면 이를 재사용하고 전 단계를 반복하지 말라. 인계에는 근거 ID·전제·미결 질문·완성 산출물을 포함하라.

추가 운영: 유료 광고→creative/social/measurement/pricing, 검색 콘텐츠→research/creative/measurement, CRM 후속→sales/success/cx, 댓글·청취→social/cx/research, 채널 재설계→channel-retail/research/pricing. 각 흐름은 operational-playbooks를 먼저 읽고 요청 범위에 필요한 단계만 수행하라.

단일 상품·무광고 예산·빠른 현금 회수: sales의 single-product-sales → pricing의 cash-timing → 필요한 channel-retail → 완성 판매 자료 → 실제 주문·입금·이행 점검. 신뢰·노출 목표와 주문·현금 목표를 구분하되 이분법으로 고정하지 말라. 유명인·체험단·SNS는 구매 연결과 선지출·정산이 있을 때 판매 후보로 비교한다. 채널 추천에 정산일·선지출·공헌이익·공급 능력·근거 수준을 붙여라. 재고를 맡기거나 구매 의사를 받은 것을 실현 매출로 세지 말라.

## SNS 통합 v2
SNS 캠페인 요청은 별도 총괄을 부르지 않고 composition-design과 synergy-playbooks로 직접 워커 DAG를 만든다. 모든 채널별 제작/배포 규약은 channel-production-distribution을 따른다. SNS 제작/정규화/검증/실행 기록의 담당자는 sns-campaign-operations-worker다. marketing-social-campaign은 필요할 때 전체 캠페인 방향/PR을 담당하고 채널 원고를 중복 생성하지 않는다.
