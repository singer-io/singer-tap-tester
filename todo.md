# Things to think about and/or do

1. Add card: Do type/schema modeling (either with `typing` if possible, or `schema`)
2. How to make a good pattern for folks to run this?
3. How to restrict data from being created by tests? We really can't...
   - Other than say that tests should clean up after themselves if they make data
   - DOCUMENT IN README
4. Set pattern for creating a standard "what was tested" report.
   - Print table of streams and rows synced after record validation
   - Maybe even a small viz of state, schema, and record messages?
     - #|||||$|||||$|||||$|||
   - What kind of useful CLI outputs can we make here?\

## Test Writing Standards (Don'ts)

1. Don't import the tap code directly. This is meant to be true black-box integration testing, and importing a client library muddies that up, and may actually make a test ineffective.
2. Don't create or delete data, these should be generic, and should rely on data that already exists to test the tap's features. This is not always possible, but should be for those who are interested in the tap.

## TODO
1. Basic Discovery Test
2. Canary test that selects all and syncs
3. Menagerie-esque assertion on non-discoverable metadata and tap-specific metadata (e.g., `tap-foo.*` should confirm that the tap is actually `tap-foo`)
  - So we do kind of need a "type" or "tap-name", which would match the run command
  - Maybe we should create an object spec or something?
