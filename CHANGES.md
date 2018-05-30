# Change Log

## V0.1.3

Update to pack name to match reference

## V0.1.2

Missed a validation path and that results in ssl_verify being unset. Added default of `ssl_verify = True`

## V0.1.1

Add validation around the `defaults:ssl:verify` config entry, allowing for a string value set converting to boolean if needed

## V0.1.0

Pack creation and base actions
