# Diesis q/kdb+ SDK

q/kdb+ event schemas, tables, and lossless decoding through abi-typegen-runtime. This target does not provide RPC or transaction submission.

Includes bindings for 29 public system contracts and `canonical.json` with chain
configuration and addresses. Generated with exact **abi-typegen 0.8.0**.

## Regenerate

Install [abi-typegen 0.8.0](https://github.com/doublesharp/abi-typegen/releases/tag/v0.8.0)
and compile the Diesis contracts. From this repository:

```sh
DIESIS_CONTRACTS_DIR=/path/to/diesis-contracts python3 scripts/generate.py
DIESIS_CONTRACTS_DIR=/path/to/diesis-contracts python3 scripts/generate.py --check
```

The full Diesis workspace uses `../../diesis-core/diesis/contracts` by default.
Set `ABI_TYPEGEN` to select a binary explicitly. Other versions are rejected.
`generation.json` records the contract selection and exact generator version.
`canonical.json` is vendored from `diesis-js`; refresh it when chain configuration changes.

## Use

Compile `generated/abi_typegen_q.c` as a shared library using the official `k.h`
and the matching `libabi_typegen_runtime`. Load a generated `.q` module, then
call its `loadBridge` function with the shared-library path before decoding.
For example, `IWrappedDS.q` uses namespace `.atgIWrappedDS`. Integer values are
lossless 32-byte ABI words, not q long or floating-point values.


## Validation

All generated modules passed local compilation or loading. Codec checks cover
large integers and representative Diesis ABI values; all 221 event definitions
passed independent fixtures in q. These checks do not establish live Diesis RPC
qualification. See the parent workspace's SDK validation reports for full evidence.
