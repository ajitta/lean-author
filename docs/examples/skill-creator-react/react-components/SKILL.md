---
name: react-components
description: Build, refactor, and review React components and hooks, covering effects, state, rendering performance, server/client component boundaries, component tests, and accessibility. Use this skill whenever the user is writing or changing React or Next.js UI code, asks about useEffect, useState, useMemo or context, hits a re-render or stale-state bug, adds "use client", writes React Testing Library tests, or asks for a review of a React change, even if they don't say "React" explicitly (for example, they mention a .tsx or .jsx file or a components/ folder).
---

# React Components

This skill helps you write and review React code that fits the project it lives in and follows React's current rules. Most React bugs that reach review come from a small set of patterns (effects used for derived state, unstable keys, misplaced client boundaries), so the workflow below front-loads the project facts that decide which patterns apply, then points you at the reference that covers the change.

## Workflow

### 1. Learn the project before writing code

Read `package.json` and note the React version, the framework (Next.js, Vite, Remix, React Native), the test runner, and the lint and type-check scripts. Then open two existing components that are close to the task and follow their file layout, styling approach, state management, and data fetching. Matching existing conventions matters more than any general best practice, because reviewers judge new code against the code around it.

Also check whether the React Compiler is enabled (`babel-plugin-react-compiler` or the framework's compiler option). It changes the memoization advice in `references/rendering-and-performance.md`.

### 2. Read the reference that matches the change

| Change touches | Read |
|---|---|
| `useEffect`, subscriptions, derived values, state placement, context | `references/effects-and-state.md` |
| Lists and keys, memoization, a slow render | `references/rendering-and-performance.md` |
| Server Components, `"use client"`, Next.js App Router | `references/server-components.md` |
| Component tests, forms, interactive elements | `references/testing-and-accessibility.md` |

Read only the files the change needs; each one is self-contained.

### 3. Implement the smallest change that meets the task

Use the dependencies the project already has. If the task seems to need a new library, a build change, or backend work, say so and let the user decide, since those choices affect more than the component you are editing.

### 4. Verify

Run the type check, the lint, and the tests for the files you touched. If something fails for a reason unrelated to your change, report it rather than working around it, so the user can see the pre-existing problem.

## Reviewing React code

When the user asks for a review rather than a change, don't edit files. Read the diff, apply the same references, and use this structure:

```markdown
## Summary
One or two sentences on the overall state of the change.

## Findings
1. [file:line] What is wrong, why it matters to users, and the fix.

## Verification
Commands run and their results.
```

Order findings by their effect on users, not by file order.

## Examples

**Example 1:**
Input: "The filtered list flashes the old results for a moment after I type in the search box."
Output: Find the `useEffect` that copies filtered results into state, replace it with a value computed during render, and explain that the effect caused an extra render with stale data.

**Example 2:**
Input: "Review this PR that adds a todo list component."
Output: A review in the structure above, flagging for instance `key={index}` on a list that can be reordered, with the fix `key={todo.id}`.

**Example 3:**
Input: "Add a like button to the blog post page" (Next.js App Router project)
Output: A small `LikeButton` client component with `"use client"`, used from the existing server component page, so the rest of the page stays on the server.
