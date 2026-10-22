---
feature: portable-authoring-skill
phase: discovery
owner: ajitta
created: 2026-10-12
updated: 2026-10-12
---

# portable 제작 스킬

SuperClaude를 참조하되 독립적으로 agent·skill·command를 제작하는 스킬을 만들려는 요청. 제작 요청을 받으면 마크다운 파일과 reference 문서, 스크립트, 훅을 만든다(초기 버전은 마크다운과 references만, 스크립트·훅은 그 다음). 형식은 마크다운을 기본으로 하고 내부에 XML 태그를 함께 쓴다. SuperClaude를 설치하지 않은 사용자도 쓸 수 있도록 portable-skills 마켓플레이스에 별도 플러그인으로 배포한다. 기존 `authoring-skill`(`sc-author`) 설계는 참조만 하고 방향은 다르다.

## Documents

- [00-intent.md](./00-intent.md) — 의도 기록: 요청자 표현 그대로의 문제, 원하는 결과, 대상, 제약, 미결 질문 (approved-for-plan)
- [01-discovery.md](./01-discovery.md) — 요구사항 discovery: 결정 D1–D22, 자체 리뷰 기록, 확인한 사실, 요구사항, sc-author와 다른 점 (approved-for-plan)
- [02-research.md](./02-research.md) — 기존 제작 도구 7종 비교, 장황함·헤딩·강조·XML의 효과 근거, compaction 때 스킬 본문이 잘리는 방식, skill·agent 필수 요소 (draft)
- [03-analysis.md](./03-analysis.md) — 제작 가이드 초안: 길이·배치, frontmatter, 본문 요소, 문체, XML, compaction, 검사 항목. references와 검사기 설계의 입력, react 예시 두 개 비교 (draft)
- [05a-plan-standalone-repo.md](./05a-plan-standalone-repo.md) — 새 GitHub repo가 자기 마켓플레이스로 배포하는 방안: repo 구조(`plugin/` 하위 폴더), 결정 N1–N6(이름 `lean-author`, 스킬 하나), discovery 영향(NFR-3 대체), 단계 P0–P7 (draft)
- [examples/](./examples/) — 같은 React 범위를 가이드(agent)와 skill-creator 규칙(skill)으로 만든 예시 두 개
- [sc-author/](./sc-author/) — superclaude v4.34.3의 sc-author 원본(SKILL.md와 references 8개). 이 프로젝트의 입력 자료이며 동작하는 skill이 아님. 출처는 [ORIGIN.md](./ORIGIN.md)
