# Web access and interaction

Apply the relevant standard with its level, units and exceptions. The values below are WCAG 2.2 reference points, not a complete conformance test or universal styling rules. The brief and platform determine which requirements apply.

## Measurements that need their context

| Property | Requirement and boundary |
|---|---|
| Text contrast, AA | At least 4.5:1 for normal text; 3:1 for large text—24 CSS px, or 18⅔ CSS px bold. Compare the unrounded ratio against the actual background. Secondary and placeholder text are not exempt; inactive controls, incidental text and logotypes have exceptions. |
| Non-text contrast and color | Required control/state and graphical distinctions need applicable non-text contrast. Meaning must not depend on color alone. Inspect the actual states and paint, including alpha, images and gradients. |
| Target size, AA | 24×24 CSS px, with spacing, equivalent-control, inline, user-agent and essential exceptions. The enhanced 44×44 criterion is AAA, not the AA threshold. Platform pt/dp and CSS px are not interchangeable. |
| Text resizing and reflow | Check 200% text resizing without loss. Vertical-scrolling web content reflows at 320 CSS px; horizontal-scrolling content uses 256 CSS px height. Necessary two-dimensional content has exceptions; surrounding content still reflows. |

Unsupported paint and untested states remain unverified. A 390px screenshot, a size formula or an automated pass cannot establish these requirements.

## Behavior to exercise

- **Keyboard and focus:** suitable native controls, meaningful names, visible labels, reading/focus order and a visible focus indicator that is not fully obscured by the surrounding interface (AA). Test the actual path, including dynamic changes; a `:focus-visible` selector is not evidence.
- **Dialogs:** focus enters the dialog, stays within a modal, and returns appropriately on dismissal. Test the supported dismissal path and a sensible initial focus, especially for consequential actions.
- **State and recovery:** distinguish pending, empty, failed and completed work where applicable. Preserve input through errors and retries; show determinate progress only when progress is measurable. Explain recovery beside the relevant action or field. Verify announcements with the required browser/assistive technology rather than inferring them from ARIA attributes.
- **Motion and input alternatives:** preserve meaning and feedback when motion is reduced. Check applicable autoplay pause/stop and flash requirements. Essential hover or drag behavior needs an accessible alternative; inspect that path. A reduced-motion media query alone does not establish it.
- **Commitment and forms:** make irreversible effects clear before commitment and provide useful undo where possible. Preserve password-manager, paste and relevant autocomplete behavior. Apply authentication and redundant-entry requirements with their exceptions; routine confirmations and extra fields are not automatic safeguards.

## Language and equivalent access

Direction is not right alignment. Use appropriate language/direction markup and isolate mixed-direction runs; test actual strings, fonts, punctuation and focus order in supported languages. Layout mirroring does not decide whether a particular icon or chart should mirror.

Meaningful images and graphics need equivalents suited to the task, not merely an alt-text attribute. `figures.md` covers relationships, quantitative information and interactive states. Verify the delivered reading order and meaning; source inspection can locate defects but does not prove assistive use.
