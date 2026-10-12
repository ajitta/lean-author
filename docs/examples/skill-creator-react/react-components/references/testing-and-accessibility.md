# Testing and accessibility

## Testing

- Use the project's test runner, and Testing Library when present.
- Query by role and accessible name first (`getByRole`), then by label text; use test ids when no accessible query exists. Role queries test what users and assistive technology see.
- Simulate input with `userEvent` and await each call.
- Assert what the user sees or what the component calls, not internal state.
- Wait for asynchronous UI with `findBy*` or `waitFor`.

## Accessibility

- Use the native element for the role: `button` for actions, `a` with `href` for navigation, a `label` tied to each form control.
- Give icon-only controls an accessible name (`aria-label` or visually hidden text).
- Keep every interactive element reachable and operable by keyboard, with a visible focus state.
