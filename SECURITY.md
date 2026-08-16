# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Report responsibly via a private GitHub security advisory.

Include description, reproduction steps, and impact (risk bypass, leverage override, oracle spoof).

## Security model

- RiskGuardian is fail-closed
- Max leverage hard-capped at 5x (prefer 2-3x)
- Dual-leg margin + gap buffers required
- Oracle health gates
- Default path is offline/mock (no live keys or network required for verify)
- Live mode requires explicit progressive unlock and kill switches
