# Change Log
## v1.0.0

* Drop Python 2.7 support
* Convert workflows to mistral using orquestaconvert

## v0.2.0

- Add find_mac and find_ip actions, aliases, and tests
- Updated format of changelog for formatting consistancy

## v0.1.6

- Minor linting fix

## V0.1.5
- version updated with 4 actions

## V0.1.4

- Version bump to fix tagging issues

## V0.1.3

- Update to pack name to match reference

## V0.1.2

- Missed a validation path and that results in ssl_verify being unset. Added default of `ssl_verify = True`

## V0.1.1

- Add validation around the `defaults:ssl:verify` config entry, allowing for a string value set converting to boolean if needed

## V0.1.0

- Pack creation and base actions
