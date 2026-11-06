Use handoff to prepare continuation of ./manifest.md and ./decisions.md on another host.
That host cannot access this scratch filesystem or the original conversation. It can access the
versioned public format specification at https://example.invalid/spec/v2 (a reference only;
do not fetch it). It needs to continue the pending local work under the same authority.
Write the payload in the supplied records directory and give its path. Do not execute work
or contact external services.
