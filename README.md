# Diesis q/kdb+ SDK

q/kdb+ event schemas, tables, and lossless decoding through abi-typegen-runtime. This target does not provide RPC or transaction submission.

Includes bindings for 29 public system contracts and `canonical.json` with chain
configuration and addresses. Generated with exact **abi-typegen 0.9.3**.

## Regenerate

Install [abi-typegen 0.9.3](https://github.com/doublesharp/abi-typegen/releases/tag/v0.9.3)
and compile the Diesis contracts. From this repository:

```sh
DIESIS_CONTRACTS_DIR=/path/to/diesis-contracts python3 scripts/generate.py
DIESIS_CONTRACTS_DIR=/path/to/diesis-contracts python3 scripts/generate.py --check
```

The full Diesis workspace uses `../../diesis-core/diesis/contracts` by default.
Set `ABI_TYPEGEN` to select a binary explicitly. Other versions are rejected.
`generation.json` pins the contracts revision, compiler, and generator release.
Generation verifies the compiler version and ABI hash for each selected contract.
`canonical.json` is vendored from `diesis-js`; refresh it when chain configuration changes.

## Use

Compile `generated/abi_typegen_q.c` as a shared library using the official `k.h`
and `libabi_typegen_runtime` from abi-typegen-runtime 0.9.3. Load a generated `.q` module, then
call its `loadBridge` function with the shared-library path before decoding.
For example, `IWrappedDS.q` uses namespace `.atgIWrappedDS`. Integer values are
lossless 32-byte ABI words, not q long or floating-point values.


## Validation

Run `python3 scripts/generate.py --check` to verify the checked-in bindings against
the pinned contract artifacts.

For a build stored outside the source checkout, set `DIESIS_ARTIFACTS_DIR`
to the compiled artifact directory. The generator uses it instead of `out/`.
