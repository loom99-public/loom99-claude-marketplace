```
Boris from the Claude Code team here. We also love output styles -- calling it "deprecated" is a miss on our part, and makes the change sound scarier than it is.
Output styles are now more powerful, and easier to customize. You can add the same instructions you previously put in your output style to your CLAUDE.md, or use hooks to inject them at each turn, or use --system-prompt, --append-system-prompt, or --append-system-prompt-file to append to or fully swap out the system prompt.
Roughly, in order from weakest prompting to strongest prompting:
Append instructions to the system prompt with --append-system-prompt or --append-system-prompt-file
Add instructions to your CLAUDE.md
Inject instructions with a SessionStart hook
Swap out the system prompt with --system-prompt
Inject instructions before every turn with a UserPromptSubmit hook, or after every turn with a Stop hook
For most use cases 1 or 2 are sufficient, but if you want really strong adherence, 3-5 will give even better results.
```
