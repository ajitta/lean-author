# Server and client components

Applies to projects using React Server Components, such as the Next.js App Router.

- Components are server components by default. Add `"use client"` to the component that needs state, effects, browser APIs, or event handlers, as low in the tree as possible, so the rest of the page keeps rendering on the server.
- Pass only serializable props from server components to client components.
- Keep secrets and server-only modules in files without `"use client"`, because everything under that directive ships to the browser.
