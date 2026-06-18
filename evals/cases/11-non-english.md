---
id: 11-non-english
mode: readable
aggressiveness: conservative
should_trigger: true
---

## Prompt

Compress this paragraph. Keep it in its original language.

## Input

我想在这里非常诚恳地、认认真真地告诉大家一件其实说起来也并不算特别复杂的事情，那就是
我们这个新版本的应用程序，在经过了很长很长一段时间的反复打磨和不断优化之后，终于把大家
一直以来都非常期待、也反复提到过很多次的离线模式功能正式地、完整地加入进来了，从现在开始
即使在完全没有网络连接的情况下，你也依然可以正常地、顺畅地使用这个应用。

## Rubric

- [ ] Output remains in Chinese (does not translate to another language)
- [ ] Preserves the core facts: the new app version adds an offline mode; it works with no network connection
- [ ] Removes filler/intensifiers ("非常诚恳地、认认真真地", "很长很长", "正式地、完整地", "正常地、顺畅地")
- [ ] Output is markedly shorter than the input
- [ ] Reads as fluent Chinese prose (readable mode), no broken fragments
- [ ] Reports an estimated size reduction
