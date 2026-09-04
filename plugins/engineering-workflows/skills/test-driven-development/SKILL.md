---
name: test-driven-development
description: Use only when the user explicitly requests TDD, test-first development, or a red-green-refactor workflow for executable behavior.
---

<!-- Derived from Superpowers by Jesse Vincent (MIT). See THIRD_PARTY_NOTICES.md. -->

# Test-Driven Development

Apply strict red-green-refactor to one behavior at a time.

1. **Red:** Write the smallest test that expresses the required behavior. Run it and confirm it fails because that behavior is missing, not because the test is broken.
2. **Green:** Write only enough production code to pass. Run the focused test, then the smallest relevant regression suite.
3. **Refactor:** Improve structure without changing behavior. Keep the tests green.
4. Repeat for the next behavior.

Do not write or retain the implementation for a requested behavior before observing its test fail. If exploration is needed, keep it disposable and restart the production change from the failing test. Prefer real code over mocks; mock only an unavoidable boundary.

Generated artifacts, documentation, metadata, and non-executable configuration are outside this workflow. Verify them with the smallest relevant check instead.

Completion evidence must include the observed failing test, the passing test after implementation, and the final relevant suite.
