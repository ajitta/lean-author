---
status: approved-for-plan
revised: 2026-10-12
---

# portable 제작 스킬 — discovery

입력: [00-intent.md](./00-intent.md). 참조만 하고 방향은 다른 것: 저장소 `.claude/rules/`의 authoring 규칙, `feature/authoring-skill` worktree의 `sc-author` 설계(`docs/features/authoring-skill/04-design.md`).

## 1. Intent coverage

| Intent 항목 | discovery에서 구체화된 것 |
|---|---|
| Problem — "1,2 문제, 그리고 장황한 문제, 핵심 지시사항, 그리고 최적화되지 않는 마크다운 문서." | 형식 없음 → 유형별 references + 형식 규칙(FR-3, FR-4). 훅·스크립트 없음 → 제작물 플러그인에 훅·스크립트 생성, 둘 다 초기 버전 이후(D16, D18, FR-5). 장황함·핵심 지시사항·최적화 → 체크리스트 자가 점검 + 검사 스크립트(FR-7) |
| Proposed outcome — "마크다운 파일과 reference 문서 스크립트를 훅을 제작한다", "마크다운 형식 + xml 태그 병용" | 출력은 플러그인 폴더(D3). 환경별 전달은 D19. 형식은 헤딩 골격 + 일부 블록만 XML(D4) |
| Affected users and systems — "SC 미설치 사용자도", portable-skills 마켓플레이스, "별도의 플러그인으로." | 제작 스킬은 portable 규칙 그대로 모든 환경(claude.ai, Claude Code, Codex)에서 동작(D2). 새 repo의 자체 마켓플레이스로 배포(D20). 처음 intent의 "portable-skills에 추가"를 대체 |
| Constraints — "superclaude를 참조하지만 독립적으로", authoring 규칙 참조, sc-author는 "참조할 수 있지만 다른 방향" | references는 독립 작성, 저장소 rules와 import 관계 없음(NFR-2). sc-author와 다른 점은 §5 |
| Open questions — 스크립트·훅이 할 일, 훅 위치 | 훅·스크립트는 제작물의 것(D1). 제작물 훅은 `hooks/hooks.json` 기본, frontmatter는 예외(D5). 제작 스킬 자신은 검사 스크립트만, 훅 없음(D10). 스크립트·훅이 할 일은 정하지 않고 둘 다 초기 버전에서 제외(D16, D18) |

## 2. 결정 (Resolved Decisions)

모두 2026-10-12 세션에서 답함. D12·D14·D16·D20은 요청자 진술, D18·D19는 리뷰 후 선택지 문자, D15는 요청자 판단, 나머지는 선택지 문자 → confirmed.

| # | 질문 | 결정 | mode |
|---|---|---|---|
| D1 | 스크립트·훅은 누구의 것인가 | [a] 제작물(사용자가 만드는 agent·skill·command)에 들어갈 훅·스크립트를 스킬이 생성 | confirmed |
| D2 | 플러그인이 동작할 곳 | [b] 모든 환경 + Claude Code 추가 기능: 스킬 본체는 claude.ai·Codex에서도 동작, 훅은 Claude Code에서만 | confirmed |
| D3 | 제작물 형태 | [b] 플러그인 폴더 (`.claude-plugin/plugin.json` + `skills/` + `agents/` + `hooks/hooks.json` + `scripts/`) | confirmed |
| D4 | XML 병용 모양 | [a] `##` 헤딩 골격 + 예시·제약·경계 같은 일부 블록만 XML 태그 | confirmed |
| D5 | 제작물 훅 위치 | [a] `hooks/hooks.json` 기본. 특정 스킬을 쓴 뒤에만 필요한 훅만 skill frontmatter | confirmed |
| D6 | 제작물 설치 대상 | [c] 요청마다 선택: Claude Code 전용 / claude.ai 업로드 가능 | confirmed |
| D7 | 품질 검사 방법 | [c] 둘 다: references 체크리스트 자가 점검(항상) + 검사 스크립트(코드 실행 가능할 때) | confirmed |
| D8 | COMMAND 파일 | [a] `skills/<name>/SKILL.md` + `disable-model-invocation: true` | confirmed |
| D9 | claude.ai 대상에서 COMMAND | [b] `disable-model-invocation` 없이 일반 스킬로 만들고 description을 좁게, 명시 호출 전용이 아님을 알림 | confirmed |
| D10 | 제작 스킬 자신이 갖는 것 | [a] 검사 스크립트만, 훅 없음 | confirmed |
| D11 | 제작 스킬 자신의 발동 | [a] description으로 자동 발동 허용, 이웃 스킬과 구분되는 발동 조건 | confirmed |
| D12 | 본문 품질 기준 | "matt pocock의 아이디어도 나와 같다." → 문장 단위 no-op 제거, 장황함(sprawl) 제거, 금지보다 긍정문 ([02-research.md](./02-research.md) §7). SC `content-quality.md`도 같은 출처에서 나옴 | confirmed (요청자 진술) |
| D13 | 본문 작성 규칙 출처 | "본문을 어떻게 쓸지는 SUPERCLAUDE의 RULE를 참조" → [a] 문체 규칙만 참조, 구조는 D4 유지 | confirmed |
| D14 | SKILL.md와 references 분리 | "SKILL의 5000토큰을 지키는 수준에서 skill.md를만들고 다른 추가 요소는 REFEFENCE로 필요할 때 불러오는 형태" → SKILL.md 본문은 5,000 토큰 이하(compaction 뒤 다시 붙는 한도, [02-research.md](./02-research.md) §6), 나머지는 references에서 필요할 때 읽음. 제작 스킬 자신과 제작물 스킬 모두 | confirmed (요청자 진술) |
| D15 | references 형식 | "문서에서 부분 읽기가 xml이 유리할 것이라는 것이 나의 판단이다." → references는 XML 태그로 구간을 나눠 부분 읽기. 이 판단을 직접 재거나 반박한 출처는 없음(02-research §9) | confirmed (요청자 판단) |
| D16 | 초기 버전 범위 | "훅은 초기 버전을 만들때에는제외" → 제작물 훅 생성(D1의 훅, D5, FR-5)을 초기 버전에서 뺌. 스크립트 생성은 유지 | confirmed (요청자 진술) |
| D17 | 제작물 언어 | "특별한 지시가 있지 않는한 영어로 작성하고 만약 해당 언어의 특별한 맥락이 필요하면 reference 파일로 따로 처리" → [a] 제작물에만 적용. 제작 스킬 자신은 지금처럼 전부 영어(F-7 한글 금지 테스트 유지) | confirmed |
| D18 | 초기 버전의 스크립트 (리뷰 I1) | [b] 초기 버전에서 스크립트 생성도 제외. 초기 버전 제작물은 마크다운 + references만. D16의 "스크립트 생성은 유지"를 대체 | confirmed |
| D19 | 환경별 결과 전달 (리뷰 I2) | [a] Claude Code·Codex는 작업 폴더에 플러그인 폴더를 쓴다. claude.ai chat은 업로드할 수 있는 zip 파일로 내려받게 한다 | confirmed |
| D20 | 배포 단위 | "이것을 만드는 새로운 repo를 만들어 독립적으로 마켓플에이스에 올리는 방안" → 새 GitHub repo `ajitta/lean-author`가 자체 마켓플레이스를 가짐. `ajitta-socratic`에 넣지 않음. 구조·절차는 [05a-plan-standalone-repo.md](./05a-plan-standalone-repo.md). NFR-3을 대체 | confirmed (요청자 진술) |
| D21 | 스킬 구조 | 플러그인 안에 스킬 하나. 유형은 입력에서 판단하고 유형별 내용은 references (05a N1a) | confirmed |
| D22 | 이름 | 플러그인·마켓플레이스·repo·스킬 모두 `lean-author`. 이름이 "무엇을 얻는지(품질)"를 드러내도록 요청자가 정함 (05a N1, N1b, N2) | confirmed |

D1과 D7·D10의 관계: D1은 훅·스크립트를 생성물로 정했고, D7 [c]가 제작 스킬 자신의 검사 스크립트를 더했다. D10으로 "자신은 검사 스크립트만"으로 확정. D16·D18로 초기 버전의 생성물은 마크다운 + references만. 제작 스킬 자신의 검사 스크립트(D10)는 그대로.

## 3. 확인한 사실

| # | 사실 | 출처 |
|---|---|---|
| F-1 | skill frontmatter 훅은 스킬 호출 시 등록되어 **세션 끝까지** 동작. `once: true`면 첫 성공 후 제거 (`once`는 skill frontmatter에서만 유효) | code.claude.com/docs/en/hooks "Hooks in skills and agents" (2026-10-12 조회) |
| F-2 | 플러그인 `hooks/hooks.json`은 플러그인이 켜져 있는 동안 동작. 파일은 최상위 `"hooks"` 래퍼 필요. 경로는 `"${CLAUDE_PLUGIN_ROOT}"` | code.claude.com/docs/en/plugins-reference (같은 날) |
| F-3 | 스킬 폴더의 `scripts/`는 "executed, not loaded". `${CLAUDE_SKILL_DIR}`로 참조, `allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/x.sh *)`로 무확인 실행 | code.claude.com/docs/en/skills (같은 날) |
| F-4 | claude.ai·Cowork는 최상위 `bin/`이 있는 플러그인을 설치하지 않음. 새 플러그인은 `commands/`보다 `skills/` 권장 | plugins-reference "Standard layout" |
| F-5 | `package.py`는 단일 플러그인 전제: `plugin-manifest.json`·`plugin-release.json`·`plugins/<name>`이 하나씩 | `portable-skills/package.py:41-42`, `:152` |
| F-6 | portable 스킬 frontmatter 허용 키: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. 본문 200줄 상한. 스킬 폴더에 `skills/`·`bin/`·`.claude-plugin/`·`.codex-plugin/` 금지 | `portable-skills/package.py:43-56` |
| F-7 | claude.ai **단독 스킬** 업로드는 허용 키 6개 밖의 키(`disable-model-invocation`, `argument-hint`, `when_to_use` …)에서 실패. **플러그인** 업로드가 안의 스킬을 같은 기준으로 검사하는지는 미확인(02-research §10.4, §7로 넘김). 배포 파일에 한글이 있으면 테스트 실패 | `portable-skills/README.md` "Layout" 절, code.claude.com/docs/en/skills |
| F-8 | zip 바이트 재현성을 위한 LF 정규화 대상 확장자에 `.py`·`.sh`가 없음 | `portable-skills/package.py:57` `TEXT_SUFFIXES` |
| F-9 | 플러그인 이름이 `claude-`·`anthropic-`로 시작하면 `claude plugin validate` 오류. 플러그인 `name`은 영구 식별자: "never change it after release" | plugins-reference `name` 절, claude.com/docs/plugins/build |
| F-10 | claude.ai 업로드 zip은 `.claude-plugin/plugin.json`이 zip 최상위나 최상위 폴더 하나 안에 있어야 함. claude.ai chat은 agent를 오류 없이 무시. 플러그인 agent는 `hooks`·`mcpServers`·`permissionMode`를 무시 | claude.com/docs/plugins/build, code.claude.com/docs/en/sub-agents (02-research §10.2) |

## 4. 요구사항

기능:
- FR-1 입력: 제작 요청(유형 `agent` | `skill` | `command`, 목적, 설치 대상 D6). 대상이 안 정해졌으면 묻는다.
- FR-2 출력: 플러그인 폴더(D3). 필요한 것만 만든다. 초기 버전은 `hooks/`와 `scripts/`를 만들지 않는다(D16, D18).
- FR-2a 전달(D19): Claude Code·Codex에서는 작업 폴더에 플러그인 폴더를 쓴다. claude.ai chat에서는 업로드할 수 있는 zip으로 내려받게 한다(F-10의 zip 구조).
- FR-3 유형별 references: skill, agent, command(= 명시 호출 스킬, D8), plugin 구조. 제작 스킬은 요청 유형의 reference만, 필요한 구간만 읽는다(D14, D15).
- FR-3a 생성하는 스킬도 같은 구조: SKILL.md 본문 5,000 토큰 이하, 매번 필요한 절차와 compaction 뒤에도 지켜야 할 규칙은 본문 앞쪽, 나머지는 XML 구간으로 나눈 references(D14, D15).
- FR-3b 제작물 언어(D17): 사용자가 따로 지시하지 않으면 영어로 쓴다. 특정 언어 맥락(예: 그 언어의 발동 문구, 용어)이 필요하면 제작물의 별도 reference 파일에 둔다.
- FR-4 형식: 마크다운 헤딩 골격 + 일부 블록만 XML(D4). 어떤 블록을 XML로 감쌀지는 형식 reference 한 곳에서 정한다.
- FR-5 훅 생성 — 초기 버전 이후(D16): 기본 `hooks/hooks.json`(D5), 스킬 사용 후에만 필요한 훅은 그 스킬 frontmatter. 훅 명령은 `scripts/`의 스크립트를 `"${CLAUDE_PLUGIN_ROOT}"`로 부른다(F-2).
- FR-6 설치 대상별 제약(D6): claude.ai 대상이면 `bin/` 금지, 스킬 frontmatter는 공통 키만, COMMAND는 D9, agent는 chat에서 동작하지 않고 Cowork·Claude Code에서만 동작한다고 알린다(F-10). (훅이 들어오면 `hooks/hooks.json`에만)
- FR-6a 플러그인 agent에는 무시되는 필드(`hooks`, `mcpServers`, `permissionMode`)를 쓰지 않는다(F-10).
- FR-7 품질 검사(D7): references의 체크리스트(장황함, 핵심 지시사항, 마크다운 최적화)로 항상 자가 점검 + 코드 실행이 되면 제작 스킬 `scripts/`의 검사기 실행(frontmatter, SKILL.md 본문 5,000 토큰 상한(D14), XML 짝, 플러그인 구조).
- FR-8 대상이 플러그인이면 `claude plugin validate`가 있는 환경에서 그것도 실행 안내.

비기능:
- NFR-1 portable 규칙 준수(D2, D11): 제작 스킬 자신의 frontmatter는 F-6 허용 키만, 본문 200줄 이하, 배포 파일 영어(사용자 언어로 응답), 훅 없음(D10).
- NFR-2 독립성: SuperClaude 설치·파일·CLI에 의존하지 않는다. 저장소 `.claude/rules/`는 작성 시 참고만, import·복사 관계 없음.
  - 참고하는 것(D13): `content-quality.md` 전체(삭제 테스트, 강한 용어, 절차·참고 분리), `xml-prose-format.md`의 문체 규칙(Design Goals, Content Inside Tags의 목록 형태, `<example>`, 표, 속성 규칙)
  - 참고하지 않는 것: `xml-prose-format.md`의 Root Structure(루트 XML 하나)와 본문 헤딩 금지. 구조는 D4
- NFR-3 배포 (D20): 새 repo `ajitta/lean-author`의 자체 마켓플레이스, 플러그인 하나(`lean-author@lean-author`). 검증·패키징·버전 다이제스트는 새 repo의 `tools/package.py`가 맡음 (05a §5).
- NFR-4 검사 스크립트는 claude.ai·Codex·사용자 PC에서 돌도록 추가 패키지 없이 실행.

## 5. sc-author와 다른 점

| | sc-author (참조) | 이 스킬 |
|---|---|---|
| 배포 | `superclaude install`의 `skills` 컴포넌트 | 별도 repo `ajitta/lean-author`의 자체 마켓플레이스 (D20) |
| 발동 | 명시 호출만 (`disable-model-invocation`) | description 자동 발동 (D11) |
| 형식 | `--md` 또는 `--xml` 중 선택 | 마크다운 + 일부 XML 병용 하나 (D4) |
| 유형 | skill, agent, command, output-style, memory | agent, skill, command |
| 출력 | 단일 파일 작성·수정 | 플러그인 폴더 + references (훅·스크립트는 초기 버전 이후, D16·D18) |
| 검사 | `superclaude author-check` CLI | 동봉 스크립트 + 체크리스트 |
| 훅 | 범위 밖 | 제작물에 생성 (초기 버전 이후, D16) |

## 6. 범위 밖

- output style, CLAUDE.md·rules 같은 memory 문서: intent가 AGENT, SKILL, COMMAND만 지정
- 기존 파일 감사·수정: intent는 "제작요청"만 지정 (설계에서 필요하면 다시 묻는다)
- 제작 스킬 자신의 훅 (D10)
- 초기 버전: 제작물 훅·스크립트 생성 (D16, D18). FR-5와 D5는 다음 버전용으로 남겨 둠. 스크립트가 할 일은 그때 정한다
- Codex용 플러그인(`.codex-plugin/`) 생성: 제작물 대상은 Claude Code / claude.ai (D6)

## 7. 설계로 넘기는 것

- description 문구 (이웃: `skill-creator`, `plugin-authoring` 등과 구분, D11). 이름은 D22로 정함
- 검사 스크립트 언어와 `TEXT_SUFFIXES`에 스크립트 확장자 추가 여부 (F-8, NFR-4)
- 5,000 토큰을 추가 패키지 없이 재는 방법(근사치 기준과 여유분), 그리고 portable 본문 200줄 상한(F-6)과의 관계 (D14, NFR-4)
- references의 XML 구간 규칙: 태그 이름, 부분 읽기 방법(검색 후 범위 읽기), 큰 파일의 목차. D15 판단을 확인할 측정 방법(예: 같은 references를 XML 구간판과 헤딩판으로 만들어 부분 읽기 정확도 비교)
- references 목록과 각 파일의 로드 조건, 본문 200줄 안에 들어갈 절차
- XML로 감쌀 블록 목록 (D4, FR-4)
- 검증 방법: 대상별 제작 시나리오(Claude Code / claude.ai)와 `claude plugin validate` 결과. 초기 버전 합격 시나리오 예: Claude Code 대상 skill 요청 → 생성된 플러그인이 `claude plugin validate` 통과, SKILL.md 본문 5,000 토큰 이하
- claude.ai 플러그인 업로드가 안의 스킬 frontmatter를 단독 업로드만큼 검사하는지 (F-7). Claude Code 전용 키 하나를 넣은 시험 플러그인 업로드로 확인
- claude.ai chat에서 zip을 만드는 방법과 그 전제(코드 실행 기능이 켜져 있어야 하는지) (D19)

## Self-Review Iteration Log

- v1 → v2 (2026-10-12, `/sc:review`, 작성자 자체 리뷰라 독립 리뷰 아님): Critical 0, Important 5, Suggestion 6
  - I1 스크립트가 할 일 미정 → D18: 초기 버전에서 스크립트 생성 제외
  - I2 환경별 전달 미정 → D19, FR-2a
  - I3 agent 조사 결과 미반영 → F-10, FR-6 보강, FR-6a
  - I4 F-7 과대 일반화 → 단독 스킬 업로드로 한정, 플러그인 업로드는 §7에서 확인
  - I5 03-analysis의 "길이 단위는 토큰"과 200줄 상한 충돌 → 03-analysis §1 수정
  - S1·S2 README 요약과 §5 출력 행을 D16·D18에 맞춤. S3 03-analysis §6의 미확인 예외 삭제. S4 플러그인 이름 영구성 F-9·§7. S5 합격 시나리오 예를 §7에. S6 이 절
