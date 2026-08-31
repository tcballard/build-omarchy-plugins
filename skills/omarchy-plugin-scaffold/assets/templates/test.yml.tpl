name: Test

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  portable:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.4.0
      - uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5.6.0
        with:
          python-version: "3.12"
      - run: ./tests/run
