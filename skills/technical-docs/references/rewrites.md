# Before and after

Pairs taken from real documentation passes. The left column is not wrong
English; it is the wrong stance for a technical document.

## Procedure that isn't a procedure

> Upload `config.json` to the server root over SFTP and restart the server.
> Settings apply at start.

> The server writes `config.json` at first start and reads it again at every
> start, so a change takes effect at the next restart.

The first tells someone how the writer got the file there. The second tells
every reader when their change lands, whether they used SFTP, the panel, or a
deploy script.

## A setting explained by its consequence

> Set `cookie_secret` to a random string. Without it, sessions are signed with a
> fresh key at every start.

> `cookie_secret` holds the key that signs sessions. Left out, each start
> invents a new one, and everyone signed in at the time signs out.

Name what the setting is, then what follows from leaving it out. The reader
decides whether that consequence matters to them.

## A prohibition rewritten as behavior

> Don't put the login config in the data directory.

> The server refuses a config it finds in the data directory, because the reader
> can write there and could edit its own login away.

A prohibition invites the question "or what". Behavior plus reason answers it in
the same sentence.

## An automatic decision that was leaking as a knob

> The panel's port closes. Set `bind` to `0.0.0.0` to keep it open as well.

> The panel's port closes, because the tunnel is already a way in and leaving
> both open would publish the map twice over.

The first sentence hands the reader an override for a decision the system made
deliberately. Document the decision. Leave the escape hatch to the operator
reference, if it belongs anywhere.

## An operator command in a user guide

> Check a config before restarting:
> ```bash
> docker run --rm -e SELFTEST=1 -v /path/to/config.json:/app/config.json:ro image:latest
> ```

> (removed from the user guide; kept in the operator README)

Someone reading the panel documentation has no Docker daemon and no image. The
block is accurate and useless to them.

## An example that hid the shape

> ```json
> { "users": { "admin": "a-long-password" } }
> ```

> ```json
> {
>   "users": {
>     "admin": "a-long-password",
>     "coach": "env:COACH_PASSWORD",
>     "analyst": "another-long-password"
>   }
> }
> ```

One entry reads as a scalar with decoration. Three entries show that the field
is a map, that values resolve individually, and that names are free-form. This
is the difference that made a reader ask whether the field took a list.

## A heading that ordered the reader around

> ## Fix a rejected config

> ## What the server reports

The section describes where output goes and what refusals look like. Naming it
after a repair implies the reader arrived broken.

## Vague attribution replaced by the source

> The system may reject some provider names.

> `provider` accepts any name oauth2-proxy accepts, among them `google`,
> `github`, `gitlab`, `entra-id`, `oidc`, and `keycloak-oidc`. The two OIDC
> names also want `oidc_issuer_url`.

"May" is what a writer says when they haven't read the parser.
