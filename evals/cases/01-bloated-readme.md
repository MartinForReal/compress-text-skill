---
id: 01-bloated-readme
mode: readable
aggressiveness: conservative
should_trigger: true
---

## Prompt

Compress this README section. Keep it readable for humans.

## Input

It is important to note that, basically, in order to get started with the project,
you will first need to make sure that you have installed all of the required
dependencies. As mentioned above, the dependencies are required. Once you have
installed the dependencies (which are required), you can then proceed to run the
build command, which builds the project. After the build command has finished
building the project, you can run the start command in order to start the server
on port 3000. The server runs on port 3000.

## Rubric

- [ ] Output is shorter than the input (target: at least 40% fewer words)
- [ ] Preserves: install dependencies → build → start server on port 3000
- [ ] Keeps the verbatim fact "port 3000"
- [ ] Removes filler ("it is important to note that", "basically", "as mentioned above") and the repeated "dependencies are required" / "port 3000" statements
- [ ] Stays fluent prose (readable mode), no telegraphic fragments
- [ ] Reports an estimated size reduction
