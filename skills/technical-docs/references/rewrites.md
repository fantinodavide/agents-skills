# Worked documentation examples

Each example uses the hypothetical source facts stated with it.
These are illustrations, not claims about this repository or commands for it.
The document follows those facts; a rewrite must not add implementation behavior.

## Recommendation and enforcement

Source facts: the loader accepts any readable JSON file path. No caller
restricts its directory. Deployment guidance recommends a separate
configuration directory to keep configuration apart from uploaded files.

A draft says: "The loader rejects configuration files in the upload directory."

The supported description is:

> Deployment guidance recommends a separate configuration directory so
> configuration and uploaded files stay apart. The loader accepts any readable
> JSON file path; it does not enforce that directory choice.

If a later implementation rejects that location, the document can describe
the rejection after the check and its error are verified.
A recommendation alone cannot support that claim.

## Defaults and meaningful variations

Source facts: `retention_days` defaults to 14 when absent. A value of 0 disables
automatic deletion. Positive integers set the retention period in days.
Negative values fail validation. The worker reads this setting at startup.

A complete reference section is:

> ## File retention
>
> `retention_days` controls automatic deletion.
>
> | Value | Behavior |
> |---|---|
> | Omitted | Delete files after 14 days. |
> | `0` | Keep files without automatic deletion. |
> | Positive integer | Delete files after that many days. |
>
> Negative values fail validation. The worker reads the setting at startup,
> so a change takes effect after a restart.

Both supported forms can deserve an example when the audience needs the syntax:

```json
{"retention_days": 14}
```

```json
{"retention_days": 0}
```

The second example distinguishes disabled deletion from the default period.
The source facts do not establish cleanup frequency or a particular error
string, so neither belongs in the section.

## Failure and preserved state

Source facts: a reload reads and validates a candidate routing file before
replacing active routes. Validation failure leaves the active routes unchanged
and returns `routes must be a list`. The reload action remains available.

A troubleshooting section is:

> ## Rejected route reload
>
> `routes must be a list` means the candidate file contains a `routes` value
> with the wrong type. The reload leaves the active routes unchanged.
>
> The `routes` value needs a JSON list. After the file is corrected, the reload
> action reads and validates it again before replacing the active routes.

The description distinguishes rejection of the new input from loss of the
working configuration. It makes no promise about behavior after a restart,
because that behavior is outside the supplied facts.

## Audience and automatic behavior

Source facts: the panel has a relay switch. Enabling it closes the direct
listener, and the panel has no override for that behavior. Operators also have
a host diagnostic command. Panel users have no access to host commands.

The panel guide can say:

> Enabling the relay closes the direct listener. The panel provides no control
> for keeping both connections active.

The host diagnostic command belongs in the operator documentation.
The source facts do not explain why both connections cannot remain active,
so the guide must not invent a security or performance rationale.

## Procedure with a verifiable outcome

Source facts: a hypothetical tool named `profilectl` is installed on the host.
Its `check PATH` command validates a candidate without changing the active
profile. Its `apply PATH` command validates again, replaces the active profile,
and prints `Profile applied`. An invalid candidate leaves the active profile
unchanged. This section is for an operator.

A procedure can say:

> ## Profile replacement
>
> The candidate profile is a local JSON file. `profilectl` must be installed
> on the host.
>
> 1. Run `profilectl check candidate.json`.
> 2. Run `profilectl apply candidate.json` after validation succeeds.
> 3. Confirm that the command prints `Profile applied`.
>
> An invalid candidate leaves the active profile unchanged.

The commands belong because the document describes an ordered operator task.
The confirmation comes from the supplied command behavior. A short section
needs no additional sentences to satisfy a minimum length.
