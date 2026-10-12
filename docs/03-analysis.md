---
status: draft
revised: 2026-10-12
---

# 제작 가이드 초안 — skill · agent · command

입력: [01-discovery.md](./01-discovery.md)(결정 D#), [02-research.md](./02-research.md)(근거 §#). 이 문서는 제작 스킬의 references와 검사기를 설계할 때 쓰는 규칙 목록이다. 규칙마다 근거를 붙였고, 근거가 판단뿐인 것은 "판단"으로 표시했다. 배포용 references는 이 초안을 영어로 다시 쓴다(NFR-1).

## 1. 길이와 배치

- SKILL.md 본문은 5,000 토큰 이하. compaction 뒤 다시 붙는 한도라서 이 안이면 잘리지 않는다 (§6, D14).
- 매번 필요한 절차와 compaction 뒤에도 지켜야 할 규칙을 본문 맨 앞에 둔다. 넘치면 뒤부터 잘린다 (§6).
- 가끔 필요한 내용은 references로 뺀다. Read로 읽은 내용은 compaction 뒤 원문이 남지 않으므로, 계속 지켜야 할 규칙은 references에 두지 않는다 (§6).
- 본문에서 reference를 가리킬 때마다 언제 읽을지를 함께 적는다. 깊이는 한 단계 (§10.3).
- reference는 XML 태그로 구간을 나눠 필요한 구간만 읽게 한다 (D15, 판단 — 측정 근거 없음 §9). 100줄을 넘으면 목차를 둔다 (§3, §10.3).
  - 다른 방식: 분야별로 파일을 나누면 XML 없이 파일 단위로 골라 읽는다(skill-creator 예시, §11). D15를 잴 때 XML 구간판·헤딩판·분야별 파일판 세 가지를 비교한다.
- agent의 reference: agent에는 자기 폴더가 없으므로 플러그인 루트의 `references/`에 두고 본문에서 `${CLAUDE_PLUGIN_ROOT}/references/…`로 가리킨다. 문서상 agent 본문에서 치환되지만 실행 중 동작은 미확인 (02-research §10.2, react-agent 예시).
- 제작물의 길이 단위는 토큰으로 통일한다. 출처마다 줄·단어·토큰이 섞여 있다 (§8). 제작 스킬 자신은 portable 본문 200줄 상한(`package.py:52`)과 5,000 토큰을 둘 다 지킨다 (NFR-1).

## 2. skill frontmatter

| 규칙 | 근거 |
|---|---|
| `name`을 항상 쓴다: 1–64자, `a-z0-9-`, 폴더 이름과 같게, "anthropic"·"claude" 금지 | §10.1, §10.4 |
| `description` 1–1024자, 무엇을 하는지와 언제 쓰는지, 핵심 용도를 맨 앞에, 3인칭 | §10.1, §8 (목록에서 1,536자에서 잘리고 compaction 뒤 다시 들어가지 않음) |
| `name`·`description`에 XML 꺾쇠(`<` `>`) 금지 | §5, §10.1 |
| claude.ai 대상이면 키는 `name, description, license, compatibility, metadata, allowed-tools`만. 그 밖의 키는 업로드가 실패한다 | §10.1, D6 |
| Claude Code 대상이면 Claude Code 전용 키를 써도 된다. 모르는 키는 조용히 무시되므로 철자를 검사기로 확인한다 | §10.1 |
| description은 이웃 skill과 구분되게 쓴다(D11). skill-creator는 덜 발동하는 문제를 막으려고 공격적으로 쓰라고 하지만, 최신 Claude는 과잉 발동 쪽 근거가 있다(§4). 어느 쪽이 맞는지는 발동 평가로 잰다(§11) | D11, §4, skill-creator |

## 3. skill 본문 요소

빠지면 안 되는 것:
- 한 가지 일. 범위를 한 줄로.
- 절차: 명령형, 순서 있는 단계, 단계마다 끝났다고 판단하는 조건.
- 입력과 출력, 또는 출력 형식.

필요할 때 넣는 것:
- 구체적 예시 (추상적 설명 대신). 특히 모호한 요청을 어떻게 해석할지 보여 주는 입력·출력 예시 2–3개 (skill-creator 예시, §11).
- 경계 사례와 제약.
- 품질이 중요한 일에는 검증 → 수정 → 반복.
- reference 가리키기 (§1).

넣지 않는 것:
- 본문의 "언제 쓰나" 절. description에 둔다 (§10.4: superpowers는 반대).
- README, 변경 이력, 시간이 지나면 틀려지는 정보.
- 모델이 시키지 않아도 하는 일을 다시 말하는 문장 (§7 Pocock, D12).

## 4. command

- `skills/<name>/SKILL.md` + `disable-model-invocation: true` (D8). 새 플러그인은 `commands/`보다 `skills/` 권장 (01 F-4).
- claude.ai 대상이면 `disable-model-invocation`을 쓸 수 없다. 일반 스킬로 만들고 description을 좁게 쓴 뒤, 명시 호출 전용이 아니라고 사용자에게 알린다 (D9). claude.ai chat에서는 command도 "Claude applies it when the task fits" (§10.2).

## 5. agent

| 규칙 | 근거 |
|---|---|
| frontmatter 필수: `name`, `description`. description은 언제 맡길지를 짧게 | §10.2 |
| 본문 = 시스템 프롬프트. subagent는 Claude Code 시스템 프롬프트를 받지 않으므로 필요한 프로젝트 규칙을 본문에 다시 적는다 | §10.3 |
| 플러그인 agent에는 `hooks`·`mcpServers`·`permissionMode`를 쓰지 않는다. 무시된다 | §10.2 |
| claude.ai 대상이면 agent가 chat에서 조용히 무시된다고 사용자에게 알린다. Cowork와 Claude Code에서는 동작 | §10.2, FR-6 |
| Codex용 agent는 TOML(`name`, `description`, `developer_instructions`)로 따로 만든다. 지금은 범위 밖 | §10.2, 01 §6 |

본문 요소:
- 역할 한 줄 (2인칭).
- 맡는 일과 맡지 않는 일.
- 절차.
- 품질 기준과 자체 검증.
- 부모에게 돌려줄 출력 형식.
- 경계 사례와 막혔을 때의 대안.
- 도구 범위 (`tools` / `disallowedTools`).
- 필요할 때: 모호한 위임을 어떻게 해석할지 보여 주는 예시 (react-agent 예시에서 빠졌던 것, §11).

## 6. 문체

- 삭제 테스트: 지워도 결과가 같은 문장은 지운다. 단어를 줄이지 말고 문장을 지운다 (§7 Pocock, SC `content-quality.md`, D12·D13).
- 모델이 아는 개념은 용어 하나로 쓴다 (SC `content-quality.md` §3).
- 금지보다 원하는 동작을 적는다. 금지문은 금지한 행동을 문맥에 끌어온다 (§4).
- 이유를 한 구절 붙인다. 이유 있는 지시가 대문자 금지보다 낫다 (§4).
- 강조(굵게, IMPORTANT, MUST, 대문자)는 기본으로 쓰지 않는다. 반복해서 빠지는 한 줄에만 쓴다. 많이 쓰면 아무것도 두드러지지 않고, 최신 Claude에서는 과잉 발동한다 (§4).
- 선언형·명령형으로 쓴다. "should", "might", "consider"는 선택 사항으로 읽힌다 (SC `xml-prose-format.md` Design Goals, D13).
- 헤딩은 골격용 `##` 한 단계를 기본으로 한다 (D4). 깊은 중첩은 근거가 없고, 프롬프트의 마크다운은 출력 문체로 옮겨 간다 (§3, 판단 포함).
- 같은 규칙을 두 곳에 쓰지 않는다.

## 7. XML 사용

- XML은 내용 종류를 나눌 때 쓴다: 예시, 제약, 경계, 입력 템플릿 (§5, D4).
- 태그를 구조 장식으로 중첩하지 않는다. 중첩 구조에는 근거가 없다 (§5, §8).
- 태그 안의 목록·표·`<example>` 형태는 SC `xml-prose-format.md`의 문체 규칙을 따른다 (D13). 루트 XML 하나와 본문 헤딩 금지는 따르지 않는다.
- frontmatter와 description에는 쓰지 않는다 (§2).
- 비용: Claude 토크나이저로 마크다운보다 약 11% 많다 (02-research 서두에 링크한 앞선 조사). 나누는 효과가 있을 때만.

## 8. compaction 대응

- 본문 5,000 토큰 이하 + 중요 규칙은 앞쪽 (§1).
- 매번 지켜야 하는 규칙은 지시문이 아니라 훅으로 강제하는 것이 공식 처방이다 (§6). 제작물 훅 생성은 초기 버전 이후 (D16).
- 판단이 필요한 지침은 과제 전체에 걸리게 쓴다: "편집할 때마다 테스트 실행" (§6).

## 9. 기계로 검사할 수 있는 항목

검사 스크립트 후보 (FR-7). 근거는 위 각 절.

| 항목 | 대상 |
|---|---|
| frontmatter가 YAML로 파싱되는가 | skill, agent |
| `name` 형식, 폴더 이름 일치, 예약어 | skill |
| `description` 길이, 꺾쇠 없음 | skill |
| claude.ai 대상일 때 허용 키 6개만 | skill |
| SKILL.md 본문 추정 토큰 ≤ 5,000 | skill |
| XML 태그 짝 맞음 | skill, agent, reference |
| 본문에서 가리킨 reference 파일이 있는가 | skill |
| 100줄 넘는 reference에 목차가 있는가 | reference |
| 플러그인 agent에 무시되는 필드가 있는가 | agent |
| 최상위 `bin/`이 없는가(claude.ai 대상) | plugin |
| 강조 표기(굵게, 대문자 MUST 등) 개수 — 경고만 | skill, agent |

검사기가 판단할 수 없는 것(삭제 테스트, 용어 선택, 긍정문)은 체크리스트로 자가 점검한다 (D7).

## 10. 효과 시험

기계 검사(§9)는 형식만 본다. 제작물이 실제로 결과를 바꾸는지는 따로 잰다.
- 초안 직후 실제 사용자가 할 법한 테스트 프롬프트 2–3개를 만든다. 근거: Anthropic best practices "Create evaluations BEFORE writing extensive documentation", skill-creator의 `evals/evals.json`.
- 같은 프롬프트를 제작물이 있을 때와 없을 때로 실행해 비교한다. 차이가 없는 문장은 삭제 테스트(§6)로 지운다.
- description은 발동해야 하는 요청과 비슷하지만 발동하면 안 되는 요청을 섞어 발동률을 잰다(skill-creator `run_loop.py`).
- 초기 버전에서 이 시험을 제작 스킬이 직접 돌릴지, 사용자에게 프롬프트만 넘길지는 설계에서 정한다.

## 11. 예시와 비교

같은 범위(React 구현·리뷰)를 두 방식으로 만든 예시: [examples/react-agent](./examples/react-agent/) (이 가이드, agent), [examples/skill-creator-react](./examples/skill-creator-react/react-components/) (skill-creator 규칙, skill). 둘 다 각자의 검사기 통과(`claude plugin validate`, `quick_validate.py`).

| | 가이드 react-agent | skill-creator react-components |
|---|---|---|
| description | 241자, 구분 위주 | 556자, 공격적 |
| 본문 / reference | 약 700 / 720 토큰 | 약 850 / 840 토큰 |
| 헤딩 `##`/`###`, 굵게 | 7/0, 0 | 10/4, 12 |
| reference | 파일 1개, XML 구간 6개 | 분야별 파일 4개 |
| 단계 완료 조건 | 3 | 0 |
| 예시 | 0 | 입력·출력 3개 |
| 효과 시험 | 없음 | 테스트 프롬프트 3개 |

이 비교에서 가이드에 반영한 것: §1 분야별 파일 방식과 agent reference 위치, §2 description 방향, §3·§5 예시, §10 효과 시험. 토큰은 글자 수 ÷ 4 추정.
