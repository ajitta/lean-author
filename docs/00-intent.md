---
status: approved-for-plan
revised: 2026-10-12
---

# Intent: superclaude를 참조하지만 독립적으로 AGENT, SKILL, COMMAND를 제작하는 스킬

Author: ajitta.

원문 요청:
> suerclaude를 참조하지만 돌립적으로 AGENT,SKILL, COMMNAND를 제작하는 스킬을 만들고자 한다.
> 제작요청을 받으면 마크다운 파일과 reference 문서 스크립트를 훅을 제작한다.
> 기본적으로 마크다운 형식을을 따라가지만, 내부적으로 xml 테크를 병용한다.

## Problem
"1,2 문제, 그리고 장황한 문제, 핵심 지시사항, 그리고 최적화되지 않는 마크다운 문서."
- 1 (선택): agent·skill·command를 만들면 형식 없이 만들어진다
- 2 (선택): 마크다운만 만들고 reference·스크립트·훅까지 함께 만드는 수단이 없다

## Proposed outcome
"제작요청을 받으면 마크다운 파일과 reference 문서 스크립트를 훅을 제작한다."
"기본적으로 마크다운 형식을을 따라가지만, 내부적으로 xml 테크를 병용한다."

## Affected users and systems
- "SC 미설치 사용자도" — SuperClaude를 설치하지 않은 Claude Code 사용자도 쓸 수 있음 (선택)
- "portable-skills에 추가한다" / "포터블 스킬이 싱글 스킬이 아니가 마켓플레이스에 합쳐져 있다."
- 마켓플레이스 안의 배포 단위: "별도의 플러그인으로."

## Constraints
- "superclaude를 참조하지만 독립적으로"
- 참조 대상: "SUPERCLAUDE rule에 xml, agent, command, skill등에 대한 authoring이 있어" — 현재 `.claude/rules/`에 있는 것: `xml-prose-format.md`, `agent-authoring.md`, `command-authoring.md`, `output-style-authoring.md`, `mode-authoring.md`, `mcp-authoring.md`, `content-quality.md`, `schemas.yaml` (`skill-authoring.md`는 없음, 2026-10-12 기준)
- 기존 `authoring-skill`(`sc-author`, `feature/authoring-skill` worktree)과의 관계: "기존 authoring-skill 설계는 참조할 수 있지만 다른 방향이다. (superclaude와 독립적으로 설치하는 것이다)"
- 그 밖의 제약: "따로 없음"

## Open questions
- 제작하는 스크립트·훅이 할 일: not stated
  - 요청자 메모: "skill에는 바로 훅스크립트를 넣을 수 있는 것으로 알고 있다."
