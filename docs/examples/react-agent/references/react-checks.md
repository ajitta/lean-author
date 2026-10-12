# React checks

One section per topic. Read only the sections the change touches.

<effects>
- Compute values derived from props or state during render. Syncing them through an effect adds a render and a moment where the UI shows stale data.
- Handle user-triggered work (submits, clicks) in the event handler, not in an effect that watches state.
- List every reactive value the effect reads in its dependency array. When a dependency changes too often, move the value inside the effect or out of the component.
- Return a cleanup function for every subscription, timer, or listener the effect starts.
- Fetch data through the project's data layer (framework loader, TanStack Query, SWR) when one exists. A raw fetch in an effect needs cancellation for out-of-order responses.
</effects>

<state>
- Keep state in the lowest component that reads it; lift it only to the nearest common parent of its readers.
- Store the minimal state and derive the rest during render.
- Use context for values that many distant components read and that change rarely. Every consumer re-renders when the context value changes.
- Reset a component's state by changing its `key`, so props are never copied into state by an effect.
</state>

<rendering>
- Give list items a stable key from the data. Index keys attach item state to the wrong row when the list is reordered, filtered, or prepended.
- With the React Compiler enabled, leave memoization to the compiler and write plain components. Without it, add `useMemo`, `useCallback`, or `memo` for a measured slow render, or for a value passed to a memoized child or a dependency array.
- Define components at module level. A component defined inside another gets a new type on each render, which remounts its subtree and drops its state.
</rendering>

<server-client>
- Components are server components by default. Add `"use client"` to the component that needs state, effects, browser APIs, or event handlers, as low in the tree as possible.
- Pass only serializable props from server components to client components.
- Keep secrets and server-only modules in files without `"use client"`.
</server-client>

<testing>
- Use the project's test runner, and Testing Library when present. Query by role and accessible name first (`getByRole`), then by label text; use test ids when no accessible query exists.
- Simulate input with `userEvent` and await each call.
- Assert what the user sees or what the component calls, not internal state.
- Wait for asynchronous UI with `findBy*` or `waitFor`.
</testing>

<accessibility>
- Use the native element for the role: `button` for actions, `a` with `href` for navigation, a `label` tied to each form control.
- Give icon-only controls an accessible name (`aria-label` or visually hidden text).
- Keep every interactive element reachable and operable by keyboard, with a visible focus state.
</accessibility>
