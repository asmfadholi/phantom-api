# Verification checklist

Apply checks proportionate to the change and the repository's scripts.

## Automated checks

- Test the default path with no active scenario.
- Test every added scenario's status, headers, and payload shape.
- Test exact parsing so similarly named keys cannot collide.
- Test mutually exclusive groups and preset replacement behavior.
- Test Clear/reset behavior.
- Test route matching, especially specific routes before wildcards.
- Test that both panel and adapter are disabled in production and other disallowed modes.
- Run typecheck and focused lint/tests before a full build.

For server handlers, construct requests with the same cookie/header/query signal used by the UI. For MSW, test handled and pass-through requests. For client adapters, test both forced and normal behavior.

## Browser checks

When the application can run locally:

1. Navigate to the target route and confirm only relevant scenarios appear.
2. Activate the scenario through the control panel.
3. Confirm the requested UI branch, actions, copy, and status.
4. Reload and confirm the chosen persistence behavior.
5. Clear all scenarios and confirm the normal UI returns.
6. Check console and network panels for unexpected failures.
7. Confirm keyboard access and focus behavior for the panel.
8. Confirm the trigger tooltip contains no controls and the interactive popover is non-modal.
9. Confirm click, Enter, and Space open the popover; Escape and outside click close it; focus returns predictably.
10. Test at 320px and 375px widths, at 200% zoom, in both themes, and with reduced motion enabled.
11. Confirm every interactive target is at least 44 by 44 CSS pixels and active state is not conveyed by color alone.
12. Confirm the popover flips or shifts near viewport edges without horizontal overflow or hiding its actions.

## Completion report

Report:

- implemented scenario keys and presets;
- server, MSW, client, or combined adapter choice and why;
- how another developer or QA tester activates and clears the case;
- automated and browser checks run;
- any pre-existing failure that prevented verification.
