# Agent Workflow

Use this skill when a user asks for a Python scientific figure.

1. Inspect the data shape or ask for the expected columns.
2. Pick a template from the catalog.
3. Generate a runnable Matplotlib script.
4. Export PNG and SVG unless the user asks for another format.
5. Explain what the figure shows and what it does not prove.
6. Run the repository checks before suggesting that output is ready for public
   docs or a release.

Keep private data out of examples. If the user provides sensitive data, work
with a small synthetic sample that preserves the shape but not the values.
