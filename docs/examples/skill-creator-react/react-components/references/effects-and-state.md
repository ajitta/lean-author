# Effects and state

## Effects

Effects are for synchronizing with systems outside React. Most other uses add a render and a moment of stale UI.

- **Derived values:** compute them during render from props and state. Syncing them through an effect shows stale data for one render.
- **User actions:** handle submits and clicks in the event handler, not in an effect that watches state.
- **Dependencies:** list every reactive value the effect reads. When a dependency changes too often, move the value inside the effect or out of the component instead of leaving it out of the array.
- **Cleanup:** return a cleanup function for every subscription, timer, or listener the effect starts.
- **Data fetching:** use the project's data layer (framework loader, TanStack Query, SWR) when one exists. A raw fetch in an effect needs cancellation for out-of-order responses.

## State

- Keep state in the lowest component that reads it; lift it only to the nearest common parent of its readers.
- Store the minimal state and derive the rest during render.
- Use context for values many distant components read and that change rarely, because every consumer re-renders when the value changes.
- Reset a component's state by changing its `key` rather than copying props into state with an effect.
