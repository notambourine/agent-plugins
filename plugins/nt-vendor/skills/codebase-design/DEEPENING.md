# Deepening

Classify the dependencies of the modules you plan to deepen. The category decides how
the deepened module is tested.

| Category | Example | Strategy |
| --- | --- | --- |
| In-process | Pure computation, in-memory state | Merge the modules and test the new interface directly. No adapter. |
| Local-substitutable | A database with a local stand-in | Test with the stand-in. Keep the seam internal. |
| Remote, owned | Your own service over the network | Inject a port. Production uses a transport adapter and tests use an in-memory one. |
| External | A third-party service | Inject a port. Tests use a mock adapter. |

- Add a port only when two adapters are justified, usually production and test. A seam
  with one adapter is only indirection.
- Keep internal seams out of the external interface, even when tests use them.
- Once tests exist at the deepened module's interface, delete the old unit tests on the
  shallow modules.
- Assert on outcomes seen through the interface. A test that has to change when the
  implementation changes is testing past the interface.
