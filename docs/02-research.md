---
status: draft
revised: 2026-10-12
---

# 기존 제작 도구와 지시문 서식 근거 — research

입력: [00-intent.md](./00-intent.md), [01-discovery.md](./01-discovery.md). 조회일 2026-10-12.

요청자 질문: "만연체로 늘어지는 지시문의 나열과 마크다운의 지나치게 중첩되는 헤딩과 강조같은 장식들이야. 아무 효과가 없다는 것을 알고 있다. 그리고, xml로 내용을 구분할 수 있게하고 compaction되었을때 문단이 잘리지 않게 하는 거야."

완료 기준: 질문 다섯 갈래(장황함, 헤딩, 강조, XML, compaction)마다 독립 출처 2곳 이상, 기존 도구 5개 이상 비교, 요청자 믿음과 반대되는 근거 별도 기록.

앞선 저장소 조사(다시 하지 않음): [XML vs Markdown 토큰](../../research/xml-vs-markdown-tokens-research-ajitta-2026-05-09.md) — XML이 Claude 토크나이저로 약 11% 더 비쌈, [Claude Code 잘림 한도](../../research/claude-code-truncation-thresholds-ajitta-2026-05-05.md).

## 1. 결론

| 갈래 | 요청자 믿음 "아무 효과가 없다" | 근거가 말하는 것 | 확신 |
|---|---|---|---|
| 만연체 지시문 나열 | 반박됨 | 효과가 **있고 대부분 해롭다**: 지시가 많고 길수록 지켜지는 비율이 떨어진다. 없애라는 결론은 맞다 | 높음 |
| 헤딩 중첩 | 근거 없음 | 헤딩 깊이를 따로 잰 연구는 없다. 확인된 효과는 프롬프트의 마크다운이 출력 문체로 옮겨 가는 것 | 낮음–중간 |
| 강조(굵게, 대문자, CRITICAL/MUST) | 일부 맞음 | 남발하면 이득이 없고 최신 Claude에서는 과잉 발동을 부른다. 한두 줄에만 쓰면 우선순위를 올린다 | 중간 |
| XML로 내용 구분 | — | 지시·맥락·예시·입력 같은 **내용 종류를 나누는 데** 효과가 있다는 데 두 회사(Anthropic, OpenAI)가 일치 | 높음 |
| compaction 때 문단 잘림 | — | 잘림은 문단·태그가 아니라 **토큰 수** 기준: 스킬 본문은 앞 5,000 토큰만 다시 붙는다. 본문을 그보다 짧게 쓰면 잘리지 않는다 | 높음 |

요약: 장식과 장황함은 "효과 없음"이 아니라 "비용이 있고 이득이 없음"이다. 지우는 결론은 같지만 이유가 다르다.

## 2. 만연체 지시문 나열

- IFScale, "How Many Instructions Can LLMs Follow at Once?" (arXiv 2507.11538, 2025, preprint): 지시 10개에서 claude-sonnet-4 100%, 250개 77.2%, 500개 42.9%. 앞쪽 지시를 더 잘 지키는 primacy bias.
- Claude Code best practices (code.claude.com/docs/en/best-practices, 공식): "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!", "If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise." 처방: "Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook."
- Anthropic, "Effective context engineering for AI agents" (2025-09-29, 공식): "the smallest possible set of high-signal tokens". 엣지 케이스를 줄줄이 나열하는 것은 권하지 않는다.
- Chroma, "Context Rot" (2025-07-14, 업계 보고서, 18개 모델): 입력이 길수록 성능이 꾸준히 떨어진다.
- OpenAI GPT-5-Codex 가이드 (공식): "less is more". GPT-5 가이드: 모순되거나 모호한 지시는 모델이 그것을 맞추느라 추론을 쓰게 만든다.
- 반대 근거: 같은 Anthropic 글 "minimal does not necessarily mean short". 긴 프롬프트 끝에 짧게 다시 말해 주라는 권고(Opus 5 가이드, 하위 조사 보고. 원문 미확인)와 GPT-4.1 가이드의 "both the beginning and end". 같은 규칙을 **필요한 위치에** 다시 두는 것은 잡음이 아니다.

## 3. 헤딩 중첩

- He et al., "Does Prompt Formatting Have Any Impact on LLM Performance?" (arXiv 2411.10541, 2024, preprint): 평문·마크다운·JSON·YAML 사이 GPT-3.5 성능 차이 최대 40%, GPT-4는 덜 민감. 헤딩 깊이는 재지 않음.
- Sclar et al., FormatSpread (ICLR 2024, 동료 심사): 서식만 바꿔 LLaMA-2-13B에서 최대 76점 차이. 오래된 공개 모델, few-shot 분류.
- Anthropic 글: "the exact formatting of prompts is likely becoming less important as models become more capable."
- Anthropic 프롬프팅 가이드 (platform.claude.com, 공식, 원문 확인): "The formatting style used in your prompt may influence Claude's response style … removing markdown from your prompt can reduce the volume of markdown in the output." → 무거운 마크다운은 지시 준수가 아니라 **출력 문체**에 효과가 있다.
- 반대 근거: OpenAI GPT-4.1 가이드는 "deeper hierarchy, to H4+"까지 권한다.
- 도구 쪽: 깊이 규칙을 둔 도구는 하나도 없다. Pocock은 헤딩을 "개념 하나의 정의·규칙·주의를 한 헤딩 아래" 모으는 용도로 쓰고, Anthropic은 100줄 넘는 참고 파일에 목차를 권한다(부분 읽기에서도 범위가 보이도록).

## 4. 강조 (굵게, 대문자, CRITICAL / MUST)

- Anthropic 프롬프팅 가이드 (공식, 원문 확인): "these models may now overtrigger. The fix is to dial back any aggressive language. Where you might have said "CRITICAL: You MUST use this tool when...", you can use more normal prompting". 같은 페이지: "NEVER use ellipses"보다 이유를 적은 지시가 낫다.
- Claude Code best practices (공식, 원문 확인): "If Claude keeps skipping one instruction, add emphasis such as "IMPORTANT" to that line alone. If you emphasize many lines, none of them stands out." → 강조는 **한 줄에만 쓰는 예산**.
- skill-creator (anthropics/skills): "explain to the model why things are important in lieu of heavy-handed musty MUSTs", 대문자 ALWAYS/NEVER는 "yellow flag".
- "Attention is Case-Sensitive" (arXiv 2608.03711, 2026, preprint): 대문자화가 비추론 모델에서 최대 +8.95pp, 추론(thinking) 모델에서는 효과가 줄어듦.
- GUIDE (arXiv 2409.19001, 2024, preprint): 대문자나 'Important'로 눈에 띄는 개선 없음(Mistral, Gemma).
- "Control Illusion" (arXiv 2502.15851): "You must always follow this constraint"를 붙여도 준수율은 최고 63.8%(GPT-4o).
- 금지형 역효과 (arXiv 2511.12381, 2025, preprint, 20B 이하 공개 모델): "X를 말하지 마라" 뒤 X가 더 나온다. Pocock: "steering by prohibition drags the forbidden behaviour into context".
- 반대 근거: superpowers writing-skills는 규율형 스킬에 "YOU MUST" 같은 권위 언어를 **권한다**(`persuasion-principles.md`). 근거로 든 Meincke et al. 2025는 위험 요청 순응(jailbreak) 연구라 지시 준수 근거로는 약하다. 같은 스킬이 모양이 틀린 출력에는 금지보다 긍정 레시피가 낫다는 자체 실험도 적었다.

## 5. XML로 내용 구분

- Anthropic 프롬프팅 가이드 (공식, 원문 확인): "XML tags help Claude parse complex prompts unambiguously, especially when your prompt mixes instructions, context, examples, and variable inputs. Wrapping each type of content in its own tag … reduces misinterpretation."
- OpenAI GPT-4.1 가이드 (공식): 긴 맥락 시험에서 XML이 잘 동작, JSON은 나쁨. GPT-5 가이드(Cursor 사례): `<[instruction]_spec>` 같은 XML 명세가 지시 준수를 높임.
- 반대·제약:
  - Anthropic 글은 "XML tagging or Markdown headers"를 동등하게 둔다. XML 비용은 약 11% 더 많은 토큰(앞선 조사).
  - 스킬 frontmatter(`name`, `description`)에는 XML 꺾쇠 금지: skill-creator `quick_validate.py`, Anthropic best practices "Cannot contain XML tags".
  - 기존 제작 도구 7개 중 **본문 XML을 권하거나 금하는 곳은 없다**. agentskills.io 명세: "There are no format restrictions."
  - plugin-dev는 2026-02-05 커밋에서 에이전트 description의 `<example>` 블록을 산문으로 바꿨지만 `agent-creator.md`는 아직 `<example>`을 가르친다(자기모순).

## 6. compaction과 잘림

| 무엇 | compaction 뒤 | 출처 |
|---|---|---|
| 실행한 스킬 본문 | 가장 최근 실행본을 다시 붙임. 스킬마다 **앞 5,000 토큰**, 모두 합쳐 25,000 토큰. 최근 실행 순으로 채우고 오래된 스킬은 통째로 빠짐 | code.claude.com/docs/en/skills "Skill content lifecycle"; /docs/en/context-window |
| 스킬 목록(description) | 다시 넣지 않음 | /docs/en/context-window |
| Read로 읽은 파일(references 포함) | 원문은 사라지고 요약에 흡수. 최근 **수정한** 파일 최대 5개만 다시 읽음 | /docs/en/context-window |
| CLAUDE.md, 시스템 프롬프트, 메모리 | 다시 로드 | /docs/en/context-window, /docs/en/how-claude-code-works |
| subagent 본문 | 서브에이전트의 시스템 프롬프트가 됨. 대화 기록이 아니므로 compaction 대상이 아님(추론, 문서에 명시 없음). subagent도 같은 규칙으로 자체 compaction | /docs/en/sub-agents |
| 훅 | 문맥이 아니라 코드로 실행되므로 영향 없음 | /docs/en/skills Troubleshooting |

공식 처방 (skills 문서 "Claude stops following a skill"):
- "put the most important instructions near the top of `SKILL.md`"
- 매번 지켜야 하는 규칙은 "move the rule into a hook … define the hook in the skill's `hooks` frontmatter"
- 판단이 필요한 지침은 과제 전체에 걸리게 쓴다: "Run the tests after every edit"

잘리는 단위: 토큰 수 기준이라는 것만 문서에 있다. 문단·XML 경계를 지켜서 자른다는 언급은 없다. 2차 출처(handbook.reopt.ai)도 같은 수치를 적는다.

## 7. 기존 제작 도구 비교

| 도구 | 장황함 | 헤딩·강조 | 본문 XML | 길이 | compaction | 훅·스크립트 생성 |
|---|---|---|---|---|---|---|
| anthropics/skills skill-creator | "Keep the prompt lean", 기록을 읽고 낭비 부분 삭제 | MUST 남발 반대, 대문자는 "yellow flag". 헤딩 언급 없음 | 언급 없음 (description에 `<>` 금지) | 본문 500줄 미만 | 없음 | 훅 없음. 자체 eval·검증·패키징 스크립트 |
| obra/superpowers writing-skills | 단어 목표 150/200/500 | 규율형에는 "YOU MUST" 권장, 모양 문제에는 긍정 레시피 | 언급 없음 | 단어 수 | 없음 | 없음 (그래프 렌더 스크립트만) |
| claude-plugins-official plugin-dev | 1,500–2,000단어 | 스킬은 명령형, 에이전트는 2인칭. 굵게·헤딩 자유 | 에이전트 description `<example>` 제거했으나 일부 남음 | 본문 5k단어 미만, 에이전트 1만 자 미만 | PreCompact 훅만 | **있음**: 훅 작성 + 검증·테스트 스크립트 |
| Anthropic skill best practices | "context window is a public good", "Claude is already very smart" | 반대 규칙 없음, 용어 일관 | frontmatter 금지, 본문 언급 없음 | 500줄 미만, 참고 1단계, 100줄 넘으면 목차 | 없음 | 스크립트 동봉 권장 |
| agentskills.io 명세 | — | — | "no format restrictions" | 5,000 토큰, 500줄 미만 권장 | 없음 | — |
| openai/skills skill-creator (Codex) | Anthropic 문구 이식 | 명령형만 | 언급 없음 | 500줄 미만 | 없음 | 초기화·yaml 생성·검증 스크립트 |
| mattpocock/skills writing-for-agents | 가장 강함: 문장 단위로 no-op 제거, "Sprawl" | 금지 대신 긍정, 개념당 헤딩 하나 | 언급 없음 | 계층 보호용 점진 공개 | 없음 | 없음 |
| Claude Code skills 문서 | 본문 간결, "every line is a recurring token cost" | — | — | 500줄 미만, description+when_to_use 1,536자 | **앞 5,000 토큰 / 합계 25,000** | 훅을 스킬 frontmatter에 두라고 안내 |

빈 곳: 본문 XML 사용 규칙, compaction에서 문단을 지키는 방법, 헤딩 깊이 규칙을 다루는 도구는 없다. 훅까지 생성하는 도구는 plugin-dev 하나다.

## 8. 설계 단계로 넘기는 근거

결정이 아니라 근거에서 바로 나오는 사실만 적는다.
- 스킬 본문이 5,000 토큰 이하이면 compaction 뒤에도 잘리지 않는다. 그보다 길면 뒤가 잘리고, 그때 열린 XML 태그가 닫히지 않을 수 있다. portable 규칙의 본문 200줄 상한(`package.py:52`)이 5,000 토큰 안에 드는지는 실측해야 한다.
- references는 compaction 뒤 원문이 남지 않는다. compaction 뒤에도 지켜야 할 규칙은 SKILL.md 앞쪽이나 훅에 있어야 한다. 이는 01-discovery D1·D5(제작물에 훅 생성)와 같은 방향이다.
- 제작물이 플러그인이면 생성된 스킬마다 같은 5,000 토큰 규칙이 걸린다. 제작 스킬의 검사기가 잴 수 있는 항목이다.
- 강조는 예산: 이유를 적은 평문이 기본, 강조는 반복해서 빠지는 한 줄에만.
- 금지문보다 원하는 동작을 적는 긍정문.
- XML은 내용 종류(지시, 예시, 입력, 경계)를 나누는 데 근거가 있고, 중첩 구조를 만드는 데에는 근거가 없다.
- 길이 단위가 출처마다 다르다(줄, 단어, 토큰). 하나를 골라야 한다.
- description은 compaction 뒤 다시 들어가지 않고 1,536자에서 잘린다. 핵심 용도를 맨 앞에 둔다.

## 9. 반대 근거, 미확인, 위험

- 반대 근거: Claude Code 문서는 한 줄 강조를 권한다. superpowers는 권위 언어를 권한다. OpenAI GPT-4.1은 H4 이상의 깊은 헤딩을 권한다. 형식 민감도 연구(Sclar, He)는 효과가 크다고 보고한다(오래된·작은 모델 중심).
- 미확인:
  - 헤딩 깊이·굵게 표시를 최신 Claude에서 따로 잰 연구 없음.
  - compaction에서 XML과 마크다운 중 어느 쪽이 더 잘 남는지 시험한 곳 없음. 필요하면 `evals/tasks.yaml` 프로브로 직접 잰다.
  - claude.ai·Codex의 compaction 규칙은 확인하지 못함(Claude Code만 문서화).
  - "긴 프롬프트 끝의 짧은 리마인더"(Opus 5 가이드)는 하위 조사 보고로만 있고 원문을 대조하지 못함.
  - 2608.03711은 최근 preprint, 검색 요약만 읽음.
- 위험:
  - IFScale은 키워드 포함 같은 가벼운 제약을 센다. 실제 스킬 지시는 더 무거워서 곡선이 다를 수 있다.
  - superpowers에 동봉된 Anthropic best practices 사본은 현재 문서와 약 800줄 다르다. 현재 페이지를 인용할 것.
  - plugin-dev 안의 모순(`agent-creator.md`와 2026-02-05 커밋). 한쪽을 베끼면 표류를 함께 가져온다.

## 10. skill·agent의 필수 요소

요청: "agent, skill 이 가져야할 필수 요소를 조사하라". 하위 조사 결과를 원문과 대조함(대조한 것은 "원문 확인" 표시).

### 10.1 skill 메타데이터

| 환경 | 필수 | 제약 | 빠지거나 모르는 필드 |
|---|---|---|---|
| Agent Skills 명세 | `name`, `description` | name 1–64자, `a-z0-9-`, 폴더 이름과 같아야 함. description 1–1024자 | 명세에 없음 |
| Claude Code | 없음: "All fields are optional" (원문 확인) | description+when_to_use 1,536자에서 잘림 | 모르는 필드는 오류 없이 무시. name이 없으면 폴더 이름 |
| claude.ai 업로드·Skills API | `name`, `description` | 허용 키 6개(`name, description, license, compatibility, metadata, allowed-tools`), XML 꺾쇠 금지, name에 "anthropic"·"claude" 금지 | 허용 밖 키는 "packaging or upload fails with a hard error" (원문 확인, skills 문서) |
| Codex | `description` (name은 폴더 이름으로 대체) | name 64자, description 1024자. 플러그인 안에서는 `plugin:name`이 64자 이내 | 잘못된 SKILL.md는 시작 시 경고 후 건너뜀 (GitHub issue, 미대조) |

### 10.2 agent 메타데이터

| 환경 | 필수 | 형식·제약 | 빠지거나 모르는 필드 |
|---|---|---|---|
| Claude Code subagent | "Only `name` and `description` are required." (원문 확인) | 마크다운, 본문이 시스템 프롬프트 | name 없음 → 문서로 보고 건너뜀. name만 있고 description 없음 → 건너뛰고 debug 로그 |
| Claude Code 플러그인 agent | 같음 | "plugin subagents don't support the `hooks`, `mcpServers`, or `permissionMode` frontmatter fields" (원문 확인) | name이 없거나 YAML이 깨져도 파일 이름으로 로드 (원문 확인) |
| claude.ai | — | "Agents and hooks load in Cowork and Claude Code; chat ignores them without an error." (원문 확인, claude.com/docs/plugins/build) | chat에서는 조용히 무시 |
| Codex custom agent | `name`, `description`, `developer_instructions` (원문 확인) | **TOML**, `~/.codex/agents/` 또는 `.codex/agents/`. "the `name` field is the source of truth" | 생략한 선택 필드는 부모 세션 값을 물려받음 |

claude.ai 명령: "In chat, a command loads as a skill, and Claude applies it when the task fits." (원문 확인). 01-discovery D9와 같은 결과다.

### 10.3 본문에 들어갈 요소

skill 본문:

| 요소 | 요구(R)·권장(r)한 출처 |
|---|---|
| 한 가지 일(목적·범위 한 줄) | r: Codex 문서 "Keep each skill focused on one job", Anthropic best practices |
| 절차: 명령형, 순서 있는 단계, 각 단계의 완료 조건 | r: 명세 "Step-by-step instructions"(원문 확인), Anthropic, OpenAI skill-creator, Pocock "Every step ends on a completion criterion" |
| 입력·출력 또는 출력 형식 | r: 명세 "Examples of inputs and outputs"(원문 확인), Codex |
| 구체적 예시 | r: 명세, Anthropic "Examples are concrete, not abstract" |
| 경계 사례와 제약 | r: 명세 "Common edge cases"(원문 확인) |
| 품질이 중요한 일의 검증 반복 | r: Anthropic "Feedback loops included for quality-critical tasks"(원문 확인) |
| references 가리키기: 파일마다 언제 읽을지, 한 단계 깊이 | r: 명세, Anthropic, OpenAI skill-creator, claude.com how-to |
| 넣지 않는 것: 본문의 "언제 쓰나" 절(description에 둠), README·변경 이력, 시간에 따라 바뀌는 정보 | r: 두 skill-creator(원문 확인), Anthropic |

agent 본문(시스템 프롬프트):

| 요소 | 권장한 출처 |
|---|---|
| 역할 한 줄(2인칭 "You are …") | plugin-dev agent-development(원문 확인), agent-creator |
| 맡는 일과 맡지 않는 일 | plugin-dev, Codex "instructions that keep it from drifting into adjacent work"(원문 확인) |
| 절차 | plugin-dev, system-prompt-design.md |
| 품질 기준과 자체 검증 | plugin-dev, agent-creator |
| 출력 형식(부모에게 돌려줄 내용) | plugin-dev, agent-creator, Claude Code 문서 |
| 경계 사례, 막혔을 때의 대안 | plugin-dev, agent-creator |
| 도구 범위(`tools`/`disallowedTools`, Codex `sandbox_mode`) | Claude Code, Codex |
| 필요한 프로젝트 규칙 재진술: subagent는 Claude Code 시스템 프롬프트를 받지 않음 | Claude Code 문서 |

### 10.4 출처끼리 다른 점, 미확인

- skill `name`: 명세·claude.ai는 필수, Claude Code·Codex는 폴더 이름으로 대체. 생성기는 항상 쓰는 쪽이 안전하다.
- agent 필드: plugin-dev는 `model`·`color`를 필수로, name을 3–50자로 둔다. Claude Code 문서는 name·description만 필수.
- "언제 쓰나": 두 skill-creator는 본문에 두지 말라고 하고, superpowers 템플릿에는 `## When to Use` 절이 있다.
- claude.ai description 한도: 하위 조사에 따르면 support.claude.com 문서 하나가 200자라고 적었고 나머지는 1024자다. 미대조.
- 미확인: claude.ai **플러그인** 업로드가 안에 든 스킬 frontmatter를 단독 스킬 업로드만큼 엄격하게 검사하는지(Claude Code 전용 키를 넣은 시험 플러그인을 올려 봐야 앎). Codex 플러그인이 agent를 실을 수 있는지. Codex custom agent에서 필수 키가 빠졌을 때의 동작.
- 01-discovery와 걸리는 점: 제작물이 claude.ai 대상(D6)이면 agent는 chat에서 동작하지 않는다. 같은 agent를 Codex용으로 쓰려면 TOML로 따로 만들어야 한다(§6 범위 밖의 Codex 생성과 연결).

## 출처

| 출처 | 등급 |
|---|---|
| platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | 공식 (원문 대조) |
| platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | 공식 |
| code.claude.com/docs/en/{skills, context-window, how-claude-code-works, sub-agents, best-practices, hooks} | 공식 (원문 대조) |
| anthropic.com/engineering/effective-context-engineering-for-ai-agents (2025-09-29) | 공식 |
| developers.openai.com cookbook: GPT-5, GPT-5-Codex, GPT-4.1 prompting guides | 공식 (타사) |
| agentskills.io/specification | 명세 |
| github.com/anthropics/skills skills/skill-creator | 공식 도구 (원문 대조) |
| github.com/anthropics/claude-plugins-official plugins/plugin-dev | 공식 도구 (원문 대조) |
| github.com/openai/skills skills/.system/skill-creator | 공식 도구 (타사) |
| github.com/obra/superpowers skills/writing-skills | 커뮤니티 (원문 대조) |
| github.com/mattpocock/skills skills/productivity/writing-for-agents | 커뮤니티 (원문 대조) |
| Sclar et al., arXiv 2310.11324 (ICLR 2024) | 동료 심사 |
| He et al. 2411.10541; IFScale 2507.11538; GUIDE 2409.19001; Control Illusion 2502.15851; 2511.12381; 2608.03711 | preprint |
| trychroma.com/research/context-rot (2025-07-14) | 업계 보고서 |
| handbook.reopt.ai/en/books/claude-code-advanced/context | 2차 |
| claude.com/docs/plugins/build, claude.com/docs/skills/how-to | 공식 (build 원문 대조) |
| developers.openai.com/codex/subagents, /codex/skills | 공식 (타사, subagents 원문 대조) |
| github.com/openai/codex `codex-rs/core-skills/src/loader.rs`, issues #25042 #26066 | 소스·이슈 (미대조) |
