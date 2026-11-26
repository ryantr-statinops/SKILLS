# Skill evaluation checklist

- The description activates for the intended outcome and excludes nearby work.
- The procedure is actionable, bounded, and does not duplicate generic facts.
- References are loaded only when they affect the evaluated task.
- Scripts, if present, are deterministic and their failures are observable.
- Expected artifacts, failure behavior, and validation are externally checkable.
- Safety boundaries lead to safe behavior in both representative and boundary cases.
- Separate static contract checks (`validate_skills.py`) from observed runtime behavior; never describe static checks as behavioral proof.
