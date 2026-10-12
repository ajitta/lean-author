# Rendering and performance

- **Keys:** give list items a stable key from the data. Index keys attach item state to the wrong row when the list is reordered, filtered, or prepended.
- **Memoization with the React Compiler:** leave memoization to the compiler and write plain components.
- **Memoization without the compiler:** add `useMemo`, `useCallback`, or `memo` for a measured slow render, or for a value passed to a memoized child or a dependency array. Memoizing everything adds code and comparison cost without a measured benefit.
- **Component definitions:** define components at module level. A component defined inside another gets a new type on each render, which remounts its subtree and drops its state.
