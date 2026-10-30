# UI decision comparisons

Use the comparison relevant to the current ambiguity; these are not fixed replacement strings.

| Context | Decision | Function that must survive |
| --- | --- | --- |
| A Save button has a tooltip saying “Click Save to save your changes”; the tooltip has no other information or behavior. | Delete the tooltip and its obsolete description reference during a fix. In an audit, report the issue without editing. | Save's accessible name, keyboard submission, and other useful descriptions. |
| The same form announces Saving, then Saved, or a verified failure with a retry action. | Keep these states. They answer whether the operation is pending, completed, or needs recovery. | Honest feedback, retained input where supported, and usable retry. |
| A mobile email input uses only the placeholder “Work email”; only a specified company domain is accepted. | Add a persistent visible label and the verified visible domain condition. More text is necessary here. | Programmatic label association, validation, and guidance available before submission. |
| Delete workspace opens a dialog explaining permanent loss of all files and no undo. A second sentence merely explains that this is a confirmation dialog. | Remove the dialog-purpose sentence; keep the consequential warning and confirmation. | Named and described modal, Cancel, safe initial focus, dismissal, and return focus. |
| A project card says “Open your project by selecting Open project” beside that link. An Export card describes which fields its CSV contains. | Remove the repeated instruction; keep the useful export contents. | Distinct card information that affects a choice. |
| An empty collection says “No projects yet” and offers New project; filtered results say “No projects match your filters” and offer Clear filters. | Remove a greeting that repeats the action, but retain each state's meaning and appropriate action. | Distinction from loading and load failure, with feedback and recovery. |
| A game objective requires all three lanterns before the north gate opens; an eerie keeper narration was requested. | Keep the objective's quantity and order and the requested narration. Remove “Your objective is shown in the Objective section.” | Playable mission, progress, accessible controls, and story purpose. |
