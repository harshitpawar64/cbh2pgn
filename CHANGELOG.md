# Changelog

## [0.2.0](https://github.com/harshitpawar64/cbh2pgn/compare/v0.1.0...v0.2.0) (2026-09-10)


### Features

* **cli:** report game decoding errors in convert command ([463c7c7](https://github.com/harshitpawar64/cbh2pgn/commit/463c7c732c6218b9e20b617d12503a7524eef272))
* **database:** integrate CBGReader to decode game moves ([249826d](https://github.com/harshitpawar64/cbh2pgn/commit/249826d6a84f0c75b82e23570e41c1d1721450d9))
* **models:** add moves, fen, and error fields to GameMetadata ([47640a3](https://github.com/harshitpawar64/cbh2pgn/commit/47640a3fee79517135bd8c7dc38cc83a6c6ff389))
* **project:** support Python &gt;=3.10 ([05a9278](https://github.com/harshitpawar64/cbh2pgn/commit/05a927874f5a6aa8b0cc90d61f9411c01eee9ad5))
* **readers:** add cbg binary reader to decode moves to SAN ([5473caf](https://github.com/harshitpawar64/cbh2pgn/commit/5473cafc031e8e86a52e1a1c8e8e85134e67118c))


### Refactor

* **readers:** use explicit byteorder and bitwise mask for deleted games ([b05749b](https://github.com/harshitpawar64/cbh2pgn/commit/b05749b2bd4a21e2d6928bcec6f6d78de9164dca))

## [0.1.0](https://github.com/harshitpawar64/cbh2pgn/compare/v0.0.1...v0.1.0) (2026-09-03)


### Features

* **cli:** add convert command supporting file and stdout output ([7cb5b7a](https://github.com/harshitpawar64/cbh2pgn/commit/7cb5b7ad59539f1511cc97be60c19cf7eeb501af))
* **database:** implement CBHDatabase to aggregate metadata from readers ([69f1eb9](https://github.com/harshitpawar64/cbh2pgn/commit/69f1eb9ff63377aced28a3d44494c21ad8427864))
* **models:** add data models for cbh records and pgn metadata ([ab3007d](https://github.com/harshitpawar64/cbh2pgn/commit/ab3007d36471172e86c1d921a2ac9aa57cd27f82))
* **models:** add to_pgn method to GameMetadata ([2c0eb87](https://github.com/harshitpawar64/cbh2pgn/commit/2c0eb873c47a27f0cd90e260df7c4782fba2013e))
* **readers:** add cbh binary reader for game header records ([269c554](https://github.com/harshitpawar64/cbh2pgn/commit/269c5547aa46e1edf26105e137b38a59d32c3efb))
* **readers:** add cbp binary reader for player data ([d6f937b](https://github.com/harshitpawar64/cbh2pgn/commit/d6f937b1640d4b79bbbf8b960b16c37acd0a5c03))
* **readers:** add cbt binary reader for tournament data ([70b9ecb](https://github.com/harshitpawar64/cbh2pgn/commit/70b9ecb270fdaae213698f1842c4ba807834e65d))

## 0.0.1 (2026-08-29)


### Features

* **cli:** add initial cli entrypoint and project scaffolding ([370a5a3](https://github.com/harshitpawar64/cbh2pgn/commit/370a5a359681384a7dc4bae85a9302d0ddcf0beb))
