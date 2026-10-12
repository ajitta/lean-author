---
status: draft
revised: 2026-10-13
---

# 별도 repo + 자체 마켓플레이스로 배포하는 방안

입력: [01-discovery.md](./01-discovery.md). 요청(2026-10-12): "이것을 만드는 새로운 repo를 만들어 독립적으로 마켓플에이스에 올리는 방안".

해석: 제작 스킬을 superclaude 저장소 밖의 새 GitHub repo에서 만들고, 그 repo가 자기 `marketplace.json`을 가진다(`ajitta-socratic`에 넣지 않음). Anthropic 디렉터리 제출은 선택 단계(§6 P6)로 둔다.

범위: repo·배포 구조만. 스킬 본문·references·검사기의 구현 계획은 `/sc:plan`의 05-plan이 맡는다.

## 1. discovery에 주는 영향

승인되면 01-discovery에 D20으로 기록하고 아래를 바꾼다.

| 항목 | 지금 | 바뀜 |
|---|---|---|
| NFR-3 배포 | `ajitta-socratic`에 별도 항목, `package.py` 다중 플러그인화 | 새 repo의 자체 마켓플레이스, 플러그인 하나 |
| F-5 / §7 `package.py` 다중 플러그인 구조 | 설계 과제 | 없어짐: 새 repo는 플러그인 하나라 단일 플러그인 전제가 그대로 맞음 |
| reflect G1 (마켓플레이스 이름 불일치) | plan 전 결정 필요 | 해소 |
| NFR-2 독립성 | 같은 저장소 안의 독립 폴더 | 저장소 단위로 독립 |
| superclaude 쪽 | — | 아직 배포한 것이 없으므로 `renames`·이전 안내 불필요 |

## 2. 확인한 사실 (2026-10-12 조회)

| # | 사실 | 출처 |
|---|---|---|
| R-1 | 한 repo가 마켓플레이스이자 플러그인일 수 있다: `.claude-plugin/marketplace.json`에 항목 하나, `source`는 `"./"`, 항목 `name`은 `plugin.json`과 같게 | code.claude.com/docs/en/plugins/publish "Publish through your own marketplace" |
| R-2 | 하위 폴더도 된다: `source`는 `./`로 시작하는 상대 경로, `..` 금지 | plugins/marketplace-reference "Relative path plugin source" |
| R-3 | marketplace 필수 키 `name`·`owner`·`plugins`. 예약 이름(`claude-plugins-official`, `claude-community` 등, `claudeai-*`, `npm`·`pip`·`github`…) 금지. 사용자에게 보이는 이름은 repo 이름이 아니라 `marketplace.json`의 `name` | marketplace-reference "Top-level fields", "Reserved names"; host-marketplace |
| R-4 | 플러그인 이름이 `claude-`·`anthropic-`·`anthropics-`·`cc-plugin-`으로 시작하면 오류. 이름은 영구 식별자(F-9) | plugins/manifest-reference `name` |
| R-5 | `marketplace add`는 `owner/repo`, `owner/repo@ref`, `owner/repo#ref`. 기본은 repo 기본 브랜치. 버전 고정은 `#<ref>` | marketplace-reference "Fields by type"; host-marketplace |
| R-6 | 사용자는 계산된 버전이 바뀔 때만 새 사본을 받음. `plugin.json`의 `version`이 우선. 서드파티 마켓플레이스 자동 업데이트는 기본 꺼짐 | host-marketplace "Release a new version" |
| R-7 | claude.ai: Customize > Plugins > Add > Add marketplace에 repo URL, 또는 Upload plugin에 zip(폴더 하나 또는 내용물 바로) | claude.com/docs/plugins/build |
| R-8 | 디렉터리 제출은 claude.ai/directory/manage, 유료 플랜 필요. `claude-plugins-official`은 제출을 받지 않음. README 40단어 이상 + `LICENSE` 또는 `license` 필드 | plugins/publish "Submit to Anthropic's directory"; claude.com/docs/plugins/build |
| R-9 | `claude plugin validate <dir>`는 marketplace·plugin 매니페스트와 skills·agents·commands를 검사. 둘 다 있으면 둘 다(v2.1.289+). `--strict`로 경고도 실패 | plugins/cli-reference "plugin validate" |
| R-10 | Codex 플러그인(`.codex-plugin/plugin.json`, Codex 마켓플레이스)은 공식 문서를 열지 못해 **미확인**. plain 스킬 폴더 복사(`~/.agents/skills/`)는 socratic에서 쓰는 경로 | `portable-skills/README.md` Install 표 |
| R-11 | 출시 전 점검: `claude plugin validate --strict`, 로컬 마켓플레이스 설치, 플러그인 루트에 `README.md`. `claude plugin eval`이 플러그인 테스트 케이스를 돌려 점수를 낸다. `claude plugin tag`는 `{name}--v{version}` 태그를 만들며, 태그는 다른 플러그인이 버전 범위로 의존할 때만 필요 | plugins/publish "Prepare your plugin for release", "Tag a release" |

## 3. repo 구조

플러그인을 repo 루트가 아닌 하위 폴더에 둔다(R-2).

```
lean-author/
├── .claude-plugin/marketplace.json   항목 하나: { "name": "lean-author", "source": "./plugin" }
├── plugin/                           배포 단위. 이 아래만 설치 캐시·zip에 들어감
│   ├── .claude-plugin/plugin.json
│   ├── README.md                     영어, 사용자에게 보이는 설명 (R-11)
│   └── skills/lean-author/               plain Agent Skill: SKILL.md, references/, scripts/, agents/openai.yaml
├── releases/lean-author.zip             claude.ai Upload용 (커밋)
├── tools/package.py                  검증 + zip + 버전 다이제스트
├── plugin-release.json               현재 버전의 다이제스트 (배포 안 함)
├── tests/                            pytest
├── docs/                             설계 문서 (한글 허용, 배포 안 함)
├── README.md  LICENSE  pyproject.toml  .github/workflows/ci.yml
```

왜 하위 폴더인가:
- 루트 플러그인(`"./"`)이면 `docs/`·`tests/`가 설치 캐시와 claude.ai로 함께 간다. 한글 설계 문서가 배포물에 섞이고, 루트에 `agents/`·`bin/` 같은 이름을 쓰면 플러그인 구성요소로 해석된다.
- 지금 socratic이 쓰는 "plain 소스 → 생성된 `plugins/` 사본" 이중 구조가 필요 없다. `plugin/skills/lean-author/`은 매니페스트를 담지 않은 plain 스킬이라 Codex·`.claude/skills/` 복사 경로에 그대로 쓰이고, 플러그인 폴더는 `plugin/` 자체다. `package.py`의 `write_plugin_dir`가 빠진다.

## 4. 결정 (2026-10-12 대화로 확정)

| # | 질문 | 결정 | 이유 |
|---|---|---|---|
| N1 | 플러그인 이름 (영구) | `lean-author` | 이름이 "무엇을 얻는지(품질)"를 드러내도록 하자는 요청자 선택. lean은 Anthropic의 "Keep the prompt lean"과 같은 결. 앞서 본 skillsmith·pith·laconic·whittle·brevity는 같은 생태계에 이미 있는 이름이라 뺐다. R-4 접두사 규칙과 예약 이름(R-3)에 걸리지 않고, `ajitta/lean-author`는 비어 있음(2026-10-12 확인) |
| N1a | 스킬 구조 | 스킬 하나. 유형(agent·skill·command)은 입력에서 판단하고, 모호하면 묻는다(FR-1). 유형별 내용은 references | 공통 references(형식·플러그인·품질·대상 제약)가 한 벌로 끝남. 한 요청에서 여러 유형을 섞어 만들 수 있음. 자동 발동 description이 하나. discovery FR-3·NFR-1이 이미 이 구조를 전제로 쓰여 있음 |
| N1b | 스킬 이름 | `lean-author` (플러그인과 같음) | Codex에서는 `$lean-author`로 단독 표시돼 겹치지 않는다. Claude Code는 `/lean-author:lean-author`. 스킬 이름은 나중에 바꿀 수 있음 |
| N2 | 마켓플레이스·repo 이름 | 플러그인과 같은 `lean-author`: `ajitta/lean-author`, 설치는 `lean-author@lean-author` | R-1이 항목 이름과 plugin.json 이름을 같게 하라고 함. 기억할 이름이 하나뿐 |
| N3 | 브랜치 | `main` 하나를 릴리스 채널로. 작업은 브랜치에서 하고, 병합이 곧 릴리스. 릴리스마다 `claude plugin tag --push`(`lean-author--v<version>`) | 플러그인 파일이 바뀌면 다이제스트 검사가 버전 올림을 강제하므로 `stable`/`master` 분리가 필요 없음. 고정을 원하는 사용자는 `#lean-author--v1.0.0`(R-5, R-11) |
| N4 | 설계 문서 위치 | 이 폴더를 새 repo `docs/`로 복사하고, 여기 README에 이동 위치를 한 줄 남김. 이력은 superclaude git에 남음 | 이후 결정이 새 repo 코드와 함께 바뀜 |
| N5 | 라이선스 | MIT | socratic과 같음. R-8 제출 요건 |
| N6 | zip 배포 | `releases/lean-author.zip` 커밋 + 재현성 테스트 | 검증된 방식 재사용 |

## 5. superclaude에서 가져가는 것과 두고 오는 것

가져감(복사 후 새 repo가 소유, 이후 동기화 없음):
- `portable-skills/package.py`: `frontmatter`, `validate`(허용 키·200줄·이름=폴더·금지 폴더), `validate_manifest`, 다이제스트·버전 검사, 재현 가능한 zip. `TEXT_SUFFIXES`에 `.py`·`.sh` 추가(F-8)
- `tests/unit/test_portable_skills.py` 중 검증기·zip·다이제스트·한글 검사 테스트. `renames`·"플러그인 하나" 테스트는 새 마켓플레이스 기준으로 다시 씀
- `portable-skills/README.md`의 설치·호출 표 형식

두고 옴:
- 저장소 `.claude/rules/` (NFR-2: 참고만)
- `evals/` 하네스: 새 repo는 `claude plugin eval`(R-11)을 쓴다. v1은 §6 P5 시나리오를 eval 케이스로 옮기는 데서 시작
- superclaude CLI·훅 의존 없음

## 6. 단계

- [x] P0 결정: N1–N6 확정(§4). 01-discovery에 D20–D22 추가, NFR-3·§7 수정
- [x] P1 repo 생성: `gh repo create ajitta/lean-author --public`, §3 구조, `LICENSE`, README(40단어 이상, 설치 표), `.gitignore`(`.venv/`, `.claude/settings.local.json`, `CLAUDE.local.md`, `.claude/superclaude/`), `pyproject.toml`(dev: pytest, pyyaml, ruff)
- [x] P2 도구 이식: §5의 `package.py`·테스트를 `plugin/` 기준으로 고침. CI: `python tools/package.py --check`, `pytest`, `ruff check`
- [x] P3 플러그인 골격: `plugin.json` 0.1.0(`displayName`, `homepage`, `repository`, `license`), `plugin/README.md`, 빈 스킬 하나로 `claude plugin validate . --strict` 통과, `claude plugin marketplace add ./`로 로컬 설치 확인 (R-9, R-11)
- [ ] P4 스킬 구현: `/sc:plan`의 05-plan으로 따로 진행 (이 문서 범위 밖)
- [ ] P5 설치 확인 (1.0.0 태그 전):
  - [x] Claude Code (0.1.0, 2026-10-13): 격리한 `CLAUDE_CONFIG_DIR`에서 `claude plugin marketplace add ajitta/lean-author` → `claude plugin install lean-author@lean-author` → 스킬 로드, `#lean-author--v<ver>` 고정도 확인. `claude plugin eval` 실행
  - [ ] claude.ai: Add marketplace와 Upload plugin(zip) 두 경로 (요청자 확인)
  - [ ] Codex: `plugin/skills/lean-author`를 `~/.agents/skills/`에 복사 → `$lean-author` 호출
- [ ] P6 선택: claude.ai/directory/manage 제출 (R-8, 유료 플랜)
- [x] P7 superclaude 정리: N4대로 superclaude 쪽 README에 이동 위치 기록. superclaude README·Pages에 링크를 넣을지는 따로 묻는다

## 7. 위험과 미확인

- N1을 잘못 정하면 되돌릴 수 없다. P1에서 repo를 공개하기 전에 확정.
- Codex 플러그인(R-10) 미확인: v1은 복사 경로만 안내. `.codex-plugin/`은 discovery §6대로 범위 밖.
- CI에서 `claude plugin validate`를 인증 없이 돌릴 수 있는지 미확인. 안 되면 로컬 검사 + PR 체크리스트로.
- claude.ai Add marketplace가 `source: "./plugin"` 하위 폴더를 읽는지 미확인(socratic은 `./portable-skills/plugins/socratic`이라 하위 폴더 자체는 동작 사례 있음). P5에서 확인.
- SuperClaude 규칙이 바뀌어도 새 repo의 references는 따라가지 않는다. NFR-2가 받아들인 비용.
- 새 repo에서 `/sc:*` 명령을 쓰려면 그 repo에 `superclaude install --scope local`이 필요. 먼저 `superclaude doctor --scope local`로 확인(gotcha `sync-scope-creates`). 설치물은 P1의 `.gitignore`가 가린다.

## 8. 완료 기준

- 격리한 설정에서 `marketplace add ajitta/lean-author` → `install` → 스킬 로드 확인
- `claude plugin validate . --strict` 통과, CI(검증·pytest·ruff) green
- claude.ai zip 업로드 성공 (요청자 확인)
- 01-discovery에 D20 반영

## Deviations

- P1–P3 (2026-10-13, `301d3dc`, `a27c83e`): repo는 `ajitta/lean-author`, 로컬 폴더는 `C:\Users\ajitta\Repos\ajitta\lean-author`(요청자 지정).
- `tools/package.py`: socratic 버전에서 `write_plugin_dir`를 뺐다(하위 폴더 구조라 생성 사본이 없음). `validate_manifest`를 `validate_plugin`으로 바꾸고 `license` 필수, `plugin/bin/` 금지, `plugin/SKILL.md` 금지, 스킬 없음 검사를 더했다. `TEXT_SUFFIXES`에 `.py`·`.sh`(F-8).
- `claude plugin validate plugin --strict`의 권고에 따라 `plugin/README.md`에 한 단계 설치 줄(`/plugin install lean-author --marketplace ajitta/lean-author`)을 넣었다.
- CI 첫 실행이 ubuntu에서 ruff EXE001(shebang 있는데 실행 비트 없음)로 실패 → `git update-index --chmod=+x tools/package.py`로 수정, 두 OS green.
- CI 경고: `actions/checkout@v4`·`astral-sh/setup-uv@v6`가 Node 20 대상(강제로 Node 24에서 실행됨). 실패는 아니라 그대로 둠.
- `claude plugin validate`는 CI에 넣지 않았다(인증 없이 도는지 미확인). 로컬에서 `.`과 `plugin` 둘 다 `--strict` 통과.
- GitHub 설치 캐시에는 `plugin/` 내용만 들어감을 확인(`.claude-plugin`, `skills`, `README.md`).

