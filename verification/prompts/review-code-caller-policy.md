Use review-code with dimension=code-maintainability to review main...HEAD. The caller chooses
acceptance policy no Medium-or-higher findings. Return the graded findings and gate verdict.
Keep the code and project instructions unchanged.
<!-- next turn -->
Re-evaluate only acceptance of the findings you just reported; the code and advisory convention
are unchanged. This caller now chooses no Low-or-higher findings. Keep grades based on the same
underlying consequences and return the gate verdict under this chosen policy.
<!-- next turn -->
Now return only the consequence classifications for those same findings. This request chooses
no gate or acceptance policy, so give no gate verdict. Keep the code unchanged.
