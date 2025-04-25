# Changelog

## [0.9.5](https://github.com/tiborsimko/reana-job-controller/compare/v0.9.4...0.9.5) (2025-04-25)


### Build

* **certificates:** update expired CERN Grid CA certificate ([#440](https://github.com/tiborsimko/reana-job-controller/issues/440)) ([8d6539a](https://github.com/tiborsimko/reana-job-controller/commit/8d6539a94af035aca1191c9a6a7ff43791a3c930)), closes [#439](https://github.com/tiborsimko/reana-job-controller/issues/439)
* **deps:** update reana-auth-vomsproxy to 1.3.0 ([#466](https://github.com/tiborsimko/reana-job-controller/issues/466)) ([72e9ea1](https://github.com/tiborsimko/reana-job-controller/commit/72e9ea1442d2b6cf7d466d0701e269fda1e15b22))
* **deps:** update reana-auth-vomsproxy to 1.3.1 ([#486](https://github.com/tiborsimko/reana-job-controller/issues/486)) ([dacbfa0](https://github.com/tiborsimko/reana-job-controller/commit/dacbfa03490d0374701664e77dbaf70a8a00e3fc))
* **docker:** non-editable submodules in "latest" mode ([#416](https://github.com/tiborsimko/reana-job-controller/issues/416)) ([3bdda63](https://github.com/tiborsimko/reana-job-controller/commit/3bdda6367d9a4682028a2a7df7268e4c9b42ef6c))
* **docker:** pin setuptools 70 ([#465](https://github.com/tiborsimko/reana-job-controller/issues/465)) ([c593d9b](https://github.com/tiborsimko/reana-job-controller/commit/c593d9bc84763f142573396be48c762eefa8f6ec))
* **python:** bump all required packages as of 2024-03-04 ([#442](https://github.com/tiborsimko/reana-job-controller/issues/442)) ([de119eb](https://github.com/tiborsimko/reana-job-controller/commit/de119eb8f663dcfe1a126747a7c404e39ece47c0))
* **python:** bump shared REANA packages as of 2024-03-04 ([#442](https://github.com/tiborsimko/reana-job-controller/issues/442)) ([fc77628](https://github.com/tiborsimko/reana-job-controller/commit/fc776284abe15030581d5adf4aa575f4f3a1c756))
* **python:** bump shared REANA packages as of 2024-11-28 ([#477](https://github.com/tiborsimko/reana-job-controller/issues/477)) ([9cdd06c](https://github.com/tiborsimko/reana-job-controller/commit/9cdd06c72faa5ded628b2766113ab37ac06f5868))


### Features

* **backends:** add new Compute4PUNCH backend ([#430](https://github.com/tiborsimko/reana-job-controller/issues/430)) ([4243252](https://github.com/tiborsimko/reana-job-controller/commit/42432522c8d9dd5e4ee908a16b1be87046908e08))
* **kubernetes:** add resource settings in Kubernetes jobs ([#484](https://github.com/tiborsimko/reana-job-controller/issues/484)) ([4753ce2](https://github.com/tiborsimko/reana-job-controller/commit/4753ce227efa2bd5b48046d0e650569a0c91abf4))
* **shutdown:** stop all running jobs before stopping workflow ([#423](https://github.com/tiborsimko/reana-job-controller/issues/423)) ([866675b](https://github.com/tiborsimko/reana-job-controller/commit/866675b7288e840130cfee851f4a248a9ae2617d))


### Bug fixes

* **config:** read secret key from env ([#476](https://github.com/tiborsimko/reana-job-controller/issues/476)) ([1b5aa98](https://github.com/tiborsimko/reana-job-controller/commit/1b5aa98b0ed76ea614dac1209ba23b366d417d9f))
* **config:** update reana-auth-vomsproxy to 1.2.1 to fix WLCG IAM ([#457](https://github.com/tiborsimko/reana-job-controller/issues/457)) ([132868f](https://github.com/tiborsimko/reana-job-controller/commit/132868f4824a0f4049febf17c90bea0df838e724))
* **database:** limit the number of open database connections ([#437](https://github.com/tiborsimko/reana-job-controller/issues/437)) ([980f749](https://github.com/tiborsimko/reana-job-controller/commit/980f74982b75176c5958f09bc581e941cdf44310))
* **htcondorcern:** run provided command in unpacked image ([#474](https://github.com/tiborsimko/reana-job-controller/issues/474)) ([9cda591](https://github.com/tiborsimko/reana-job-controller/commit/9cda591affaa1f821409961ec4e379e1bf5fa248)), closes [#471](https://github.com/tiborsimko/reana-job-controller/issues/471)
* **htcondorcern:** support multiline commands ([#474](https://github.com/tiborsimko/reana-job-controller/issues/474)) ([eb07aa9](https://github.com/tiborsimko/reana-job-controller/commit/eb07aa9b7b03d38dd47cd004ff8b48440ad45c2a)), closes [#470](https://github.com/tiborsimko/reana-job-controller/issues/470)
* **kubernetes:** avoid privilege escalation in Kubernetes jobs ([#476](https://github.com/tiborsimko/reana-job-controller/issues/476)) ([389f0ea](https://github.com/tiborsimko/reana-job-controller/commit/389f0ea9606d4ac5fa24458b7cef39e8ab430c64))


### Performance improvements

* **cache:** avoid caching jobs when the cache is disabled ([#435](https://github.com/tiborsimko/reana-job-controller/issues/435)) ([553468f](https://github.com/tiborsimko/reana-job-controller/commit/553468f55f6b63cebba45ccd460593131e5dcfea)), closes [#422](https://github.com/tiborsimko/reana-job-controller/issues/422)


### Code refactoring

* **db:** set job status also in the main database ([#423](https://github.com/tiborsimko/reana-job-controller/issues/423)) ([9d6fc99](https://github.com/tiborsimko/reana-job-controller/commit/9d6fc99063deb468fe9d45d9ad626c745c7bd827))
* **docs:** move from reST to Markdown ([#428](https://github.com/tiborsimko/reana-job-controller/issues/428)) ([4732884](https://github.com/tiborsimko/reana-job-controller/commit/4732884a3da52694fb86d72873eceef3ad2deb27))
* **monitor:** centralise logs and status updates ([#423](https://github.com/tiborsimko/reana-job-controller/issues/423)) ([3685b01](https://github.com/tiborsimko/reana-job-controller/commit/3685b01a57e1d0b1bd363534ff331b988e04719e))
* **monitor:** move fetching of logs to job-manager ([#423](https://github.com/tiborsimko/reana-job-controller/issues/423)) ([1fc117e](https://github.com/tiborsimko/reana-job-controller/commit/1fc117ebb3dd908a01ee3fd539fa24a07cdb4d16))


### Code style

* **black:** format with black v24 ([#426](https://github.com/tiborsimko/reana-job-controller/issues/426)) ([8a2757e](https://github.com/tiborsimko/reana-job-controller/commit/8a2757ee8bf52d1d5189f1dd1d690cb8922599cb))


### Test suite

* adding stop k8s job test ([8ca36bd](https://github.com/tiborsimko/reana-job-controller/commit/8ca36bd5bde461e6f85cf0a78f9588eba259047b))
* adds requirements_dev for Travis ([6c8adc0](https://github.com/tiborsimko/reana-job-controller/commit/6c8adc0d02b2852dbf79e1e82324c67c92d793f0))


### Continuous integration

* add hadolint and flake8 linters ([4ad0ede](https://github.com/tiborsimko/reana-job-controller/commit/4ad0eded2da54fd92f9da7b4ac03fb6861cb1e06))
* added github actions workflow ([67ea0ed](https://github.com/tiborsimko/reana-job-controller/commit/67ea0ed5c533c9a04213d8dc31a9421db69dc804))
* **commitlint:** addition of commit message linter ([#417](https://github.com/tiborsimko/reana-job-controller/issues/417)) ([f547d3b](https://github.com/tiborsimko/reana-job-controller/commit/f547d3bc25f438203252ea149cf6c6e5d2428189))
* **commitlint:** allow release commit style ([#443](https://github.com/tiborsimko/reana-job-controller/issues/443)) ([0fc9794](https://github.com/tiborsimko/reana-job-controller/commit/0fc9794bfbe2799bb9666ec5b2ff1dd15def8c34))
* **commitlint:** check for the presence of concrete PR number ([#425](https://github.com/tiborsimko/reana-job-controller/issues/425)) ([35bc1c5](https://github.com/tiborsimko/reana-job-controller/commit/35bc1c5acb1aa8ff51689142a007da66e49d8d2b))
* pin hadolint version ([8be1f3d](https://github.com/tiborsimko/reana-job-controller/commit/8be1f3d978c258c1cfa615e59192d99e37bed306))
* publish docker image after new release ([6a2abcb](https://github.com/tiborsimko/reana-job-controller/commit/6a2abcbb90920786ab87496a037eab50a17a85a9))
* **pytest:** move to PostgreSQL 14.10 ([#429](https://github.com/tiborsimko/reana-job-controller/issues/429)) ([42622fa](https://github.com/tiborsimko/reana-job-controller/commit/42622fa1597e49fae36c625941188be5a093eda9))
* **release-please:** initial configuration ([#417](https://github.com/tiborsimko/reana-job-controller/issues/417)) ([fca6f74](https://github.com/tiborsimko/reana-job-controller/commit/fca6f74aa0d0e55e41d96b0e79c66a5cb3517189))
* **release-please:** update version in Dockerfile/OpenAPI specs ([#421](https://github.com/tiborsimko/reana-job-controller/issues/421)) ([e6742f2](https://github.com/tiborsimko/reana-job-controller/commit/e6742f2911df46dfbef3b7e9104330d58e2b4211))
* remove older versions from python tests ([5ee2872](https://github.com/tiborsimko/reana-job-controller/commit/5ee287219aca0bae00ad600bbd29dc2ac4bb04dc))
* **runners:** upgrade CI runners to Ubuntu 22.04 ([#486](https://github.com/tiborsimko/reana-job-controller/issues/486)) ([bfbbd7c](https://github.com/tiborsimko/reana-job-controller/commit/bfbbd7c63e12ca3f56cc13fd356c3db389af7bf7))
* **shellcheck:** fix exit code propagation ([#425](https://github.com/tiborsimko/reana-job-controller/issues/425)) ([8e74a85](https://github.com/tiborsimko/reana-job-controller/commit/8e74a85c90df00c8734a6cdd81597f583d11d566))
* update all actions ([2f3ede1](https://github.com/tiborsimko/reana-job-controller/commit/2f3ede1cf130b9b68f71c1c2ec740e8f040dcbf0))


### Documentation

* add .readthedocs.yaml to migrate to RTD v2 ([71fca96](https://github.com/tiborsimko/reana-job-controller/commit/71fca9648faf098a6fdd79d1534e0f973e1fa6a0))
* addition of REST API documentation ([870668f](https://github.com/tiborsimko/reana-job-controller/commit/870668f2def8c574b7d7a5d294d09b58a921969e))
* addition of Travis/Coveralls/RFTD/Waffle/Travis/License badges ([b31c9d8](https://github.com/tiborsimko/reana-job-controller/commit/b31c9d811bc9d532571c7d131ed9ed02d02196ad))
* author ORCID links ([3c1d224](https://github.com/tiborsimko/reana-job-controller/commit/3c1d224fda215ffc7fcacc75fa56af0a26e89276))
* **authors:** complete list of contributors ([#434](https://github.com/tiborsimko/reana-job-controller/issues/434)) ([b9f8364](https://github.com/tiborsimko/reana-job-controller/commit/b9f83647fa8fc337140da5c3f2814ea24a15c5d5))
* autodoc_mock_imports for gssapi ([2fa5221](https://github.com/tiborsimko/reana-job-controller/commit/2fa52212fb744cec197a2c116da96cdb406c6645)), closes [#274](https://github.com/tiborsimko/reana-job-controller/issues/274)
* better navigation and synced descriptions ([18b942f](https://github.com/tiborsimko/reana-job-controller/commit/18b942fc97a9bb3ef94e2c7f2c438fb1699ae10a))
* better structure ([eada161](https://github.com/tiborsimko/reana-job-controller/commit/eada1613742e92cdd4e2e09febbacf9120caef2a))
* change docs to comply with the new secrets cli format ([ac2292c](https://github.com/tiborsimko/reana-job-controller/commit/ac2292c06b3682cd539a4ea212ab5f13082b3ead))
* fix "fork me on GitHub" ribbon ([d9c4532](https://github.com/tiborsimko/reana-job-controller/commit/d9c4532d61067df0447d18b0cce7b33f466ed976))
* fix ReadTheDocs build ([9c0e67a](https://github.com/tiborsimko/reana-job-controller/commit/9c0e67a11d5efe01263c2dab2270a5a5843d3319))
* fix rtfd build badge so it shows the real status ([07e403b](https://github.com/tiborsimko/reana-job-controller/commit/07e403b5b82494f8c9e9772faa132a8a5ba63fd1))
* HTCondorCERN backend usage ([5d5d6cb](https://github.com/tiborsimko/reana-job-controller/commit/5d5d6cbbca838f32b2d81d4da612c332c6deebad))
* improve documentation ([76ea1f3](https://github.com/tiborsimko/reana-job-controller/commit/76ea1f3d268b678d1ad425088a5cb0749f95b8c0))
* improve sphinxcontrib-openapi rendering ([903830d](https://github.com/tiborsimko/reana-job-controller/commit/903830dd67bcf59797f099c38955df277d3c7384))
* initial release ([930b7bd](https://github.com/tiborsimko/reana-job-controller/commit/930b7bd2fbf0feed4ff2f464e01e51143d5fec8c))
* more copyright header messages ([53546a2](https://github.com/tiborsimko/reana-job-controller/commit/53546a24fa0c8430e4bd108b8c4fc67055399259))
* more structured chapters ([f901df9](https://github.com/tiborsimko/reana-job-controller/commit/f901df93d1254dfbb1bf806b4468c6b4b0f2bd73))
* new logo, panel verbiage and links ([347f218](https://github.com/tiborsimko/reana-job-controller/commit/347f218a64a9971b6c121cf41af3bc76a304d3c3))
* pin sphinx to avoid build failure ([9d94384](https://github.com/tiborsimko/reana-job-controller/commit/9d943844ce7d643748594d23a98a5a4f49dafed0))
* ReadTheDocs configuration ([3c073e4](https://github.com/tiborsimko/reana-job-controller/commit/3c073e4c25dcd70a603a8e47bf73df33121801a4))
* remove reference to unused pykube ([2398903](https://github.com/tiborsimko/reana-job-controller/commit/23989030657d0bb6a419be110624d0964c49c3ca))
* set default language to English ([a57cd83](https://github.com/tiborsimko/reana-job-controller/commit/a57cd83a219200fd766f96c07e0ef98dd18df865))
* single-page RTFD outline ([1cb473b](https://github.com/tiborsimko/reana-job-controller/commit/1cb473b5c714fa9b6825299d1a933dbfb22cc6b6))
* update changelog ([5ac0d25](https://github.com/tiborsimko/reana-job-controller/commit/5ac0d25ee128db8bbd51fe74f01ebfa11620a34e))
* updating job manager class diagram ([9326218](https://github.com/tiborsimko/reana-job-controller/commit/932621811e0d16e85040288716826929872354cc))

## [0.9.4](https://github.com/reanahub/reana-job-controller/compare/0.9.3...0.9.4) (2024-11-29)


### Build

* **deps:** update reana-auth-vomsproxy to 1.3.0 ([#466](https://github.com/reanahub/reana-job-controller/issues/466)) ([72e9ea1](https://github.com/reanahub/reana-job-controller/commit/72e9ea1442d2b6cf7d466d0701e269fda1e15b22))
* **docker:** pin setuptools 70 ([#465](https://github.com/reanahub/reana-job-controller/issues/465)) ([c593d9b](https://github.com/reanahub/reana-job-controller/commit/c593d9bc84763f142573396be48c762eefa8f6ec))
* **python:** bump shared REANA packages as of 2024-11-28 ([#477](https://github.com/reanahub/reana-job-controller/issues/477)) ([9cdd06c](https://github.com/reanahub/reana-job-controller/commit/9cdd06c72faa5ded628b2766113ab37ac06f5868))


### Features

* **backends:** add new Compute4PUNCH backend ([#430](https://github.com/reanahub/reana-job-controller/issues/430)) ([4243252](https://github.com/reanahub/reana-job-controller/commit/42432522c8d9dd5e4ee908a16b1be87046908e08))


### Bug fixes

* **config:** read secret key from env ([#476](https://github.com/reanahub/reana-job-controller/issues/476)) ([1b5aa98](https://github.com/reanahub/reana-job-controller/commit/1b5aa98b0ed76ea614dac1209ba23b366d417d9f))
* **config:** update reana-auth-vomsproxy to 1.2.1 to fix WLCG IAM ([#457](https://github.com/reanahub/reana-job-controller/issues/457)) ([132868f](https://github.com/reanahub/reana-job-controller/commit/132868f4824a0f4049febf17c90bea0df838e724))
* **htcondorcern:** run provided command in unpacked image ([#474](https://github.com/reanahub/reana-job-controller/issues/474)) ([9cda591](https://github.com/reanahub/reana-job-controller/commit/9cda591affaa1f821409961ec4e379e1bf5fa248)), closes [#471](https://github.com/reanahub/reana-job-controller/issues/471)
* **htcondorcern:** support multiline commands ([#474](https://github.com/reanahub/reana-job-controller/issues/474)) ([eb07aa9](https://github.com/reanahub/reana-job-controller/commit/eb07aa9b7b03d38dd47cd004ff8b48440ad45c2a)), closes [#470](https://github.com/reanahub/reana-job-controller/issues/470)
* **kubernetes:** avoid privilege escalation in Kubernetes jobs ([#476](https://github.com/reanahub/reana-job-controller/issues/476)) ([389f0ea](https://github.com/reanahub/reana-job-controller/commit/389f0ea9606d4ac5fa24458b7cef39e8ab430c64))

## [0.9.3](https://github.com/reanahub/reana-job-controller/compare/0.9.2...0.9.3) (2024-03-04)


### Build

* **certificates:** update expired CERN Grid CA certificate ([#440](https://github.com/reanahub/reana-job-controller/issues/440)) ([8d6539a](https://github.com/reanahub/reana-job-controller/commit/8d6539a94af035aca1191c9a6a7ff43791a3c930)), closes [#439](https://github.com/reanahub/reana-job-controller/issues/439)
* **docker:** non-editable submodules in "latest" mode ([#416](https://github.com/reanahub/reana-job-controller/issues/416)) ([3bdda63](https://github.com/reanahub/reana-job-controller/commit/3bdda6367d9a4682028a2a7df7268e4c9b42ef6c))
* **python:** bump all required packages as of 2024-03-04 ([#442](https://github.com/reanahub/reana-job-controller/issues/442)) ([de119eb](https://github.com/reanahub/reana-job-controller/commit/de119eb8f663dcfe1a126747a7c404e39ece47c0))
* **python:** bump shared REANA packages as of 2024-03-04 ([#442](https://github.com/reanahub/reana-job-controller/issues/442)) ([fc77628](https://github.com/reanahub/reana-job-controller/commit/fc776284abe15030581d5adf4aa575f4f3a1c756))


### Features

* **shutdown:** stop all running jobs before stopping workflow ([#423](https://github.com/reanahub/reana-job-controller/issues/423)) ([866675b](https://github.com/reanahub/reana-job-controller/commit/866675b7288e840130cfee851f4a248a9ae2617d))


### Bug fixes

* **database:** limit the number of open database connections ([#437](https://github.com/reanahub/reana-job-controller/issues/437)) ([980f749](https://github.com/reanahub/reana-job-controller/commit/980f74982b75176c5958f09bc581e941cdf44310))


### Performance improvements

* **cache:** avoid caching jobs when the cache is disabled ([#435](https://github.com/reanahub/reana-job-controller/issues/435)) ([553468f](https://github.com/reanahub/reana-job-controller/commit/553468f55f6b63cebba45ccd460593131e5dcfea)), closes [#422](https://github.com/reanahub/reana-job-controller/issues/422)


### Code refactoring

* **db:** set job status also in the main database ([#423](https://github.com/reanahub/reana-job-controller/issues/423)) ([9d6fc99](https://github.com/reanahub/reana-job-controller/commit/9d6fc99063deb468fe9d45d9ad626c745c7bd827))
* **docs:** move from reST to Markdown ([#428](https://github.com/reanahub/reana-job-controller/issues/428)) ([4732884](https://github.com/reanahub/reana-job-controller/commit/4732884a3da52694fb86d72873eceef3ad2deb27))
* **monitor:** centralise logs and status updates ([#423](https://github.com/reanahub/reana-job-controller/issues/423)) ([3685b01](https://github.com/reanahub/reana-job-controller/commit/3685b01a57e1d0b1bd363534ff331b988e04719e))
* **monitor:** move fetching of logs to job-manager ([#423](https://github.com/reanahub/reana-job-controller/issues/423)) ([1fc117e](https://github.com/reanahub/reana-job-controller/commit/1fc117ebb3dd908a01ee3fd539fa24a07cdb4d16))


### Code style

* **black:** format with black v24 ([#426](https://github.com/reanahub/reana-job-controller/issues/426)) ([8a2757e](https://github.com/reanahub/reana-job-controller/commit/8a2757ee8bf52d1d5189f1dd1d690cb8922599cb))


### Continuous integration

* **commitlint:** addition of commit message linter ([#417](https://github.com/reanahub/reana-job-controller/issues/417)) ([f547d3b](https://github.com/reanahub/reana-job-controller/commit/f547d3bc25f438203252ea149cf6c6e5d2428189))
* **commitlint:** allow release commit style ([#443](https://github.com/reanahub/reana-job-controller/issues/443)) ([0fc9794](https://github.com/reanahub/reana-job-controller/commit/0fc9794bfbe2799bb9666ec5b2ff1dd15def8c34))
* **commitlint:** check for the presence of concrete PR number ([#425](https://github.com/reanahub/reana-job-controller/issues/425)) ([35bc1c5](https://github.com/reanahub/reana-job-controller/commit/35bc1c5acb1aa8ff51689142a007da66e49d8d2b))
* **pytest:** move to PostgreSQL 14.10 ([#429](https://github.com/reanahub/reana-job-controller/issues/429)) ([42622fa](https://github.com/reanahub/reana-job-controller/commit/42622fa1597e49fae36c625941188be5a093eda9))
* **release-please:** initial configuration ([#417](https://github.com/reanahub/reana-job-controller/issues/417)) ([fca6f74](https://github.com/reanahub/reana-job-controller/commit/fca6f74aa0d0e55e41d96b0e79c66a5cb3517189))
* **release-please:** update version in Dockerfile/OpenAPI specs ([#421](https://github.com/reanahub/reana-job-controller/issues/421)) ([e6742f2](https://github.com/reanahub/reana-job-controller/commit/e6742f2911df46dfbef3b7e9104330d58e2b4211))
* **shellcheck:** fix exit code propagation ([#425](https://github.com/reanahub/reana-job-controller/issues/425)) ([8e74a85](https://github.com/reanahub/reana-job-controller/commit/8e74a85c90df00c8734a6cdd81597f583d11d566))


### Documentation

* **authors:** complete list of contributors ([#434](https://github.com/reanahub/reana-job-controller/issues/434)) ([b9f8364](https://github.com/reanahub/reana-job-controller/commit/b9f83647fa8fc337140da5c3f2814ea24a15c5d5))

## 0.9.2 (2023-12-12)

- Adds metadata labels to Dockerfile.
- Adds automated multi-platform container image building for amd64 and arm64 architectures.
- Changes CVMFS support to allow users to automatically mount any available repository.
- Fixes container image building on the arm64 architecture.
- Fixes the creation of Kubernetes jobs by retrying in case of error and by correctly handling the error after reaching the retry limit.
- Fixes job monitoring in cases when job creation fails, for example when it is not possible to successfully mount volumes.

## 0.9.1 (2023-09-27)

- Adds unique error messages to Kubernetes job monitor to more easily identify source of problems.
- Changes Paramiko to version 3.0.0.
- Changes HTCondor to version 9.0.17 (LTS).
- Changes Rucio authentication helper to version 1.1.1 allowing users to override the Rucio server and authentication hosts independently of VO name.
- Fixes intermittent Slurm connection issues by DNS-resolving the Slurm head node IPv4 address before establishing connections.
- Fixes deletion of failed jobs not being performed when Kerberos is enabled.
- Fixes job monitoring to consider OOM-killed jobs as failed.
- Fixes Slurm command generation issues when using fully-qualified image names.
- Fixes location of HTCondor build dependencies.
- Fixes detection of default Rucio server and authentication host for ATLAS VO.
- Fixes container image names to be Podman-compatible.

## 0.9.0 (2023-01-20)

- Adds support for Rucio authentication for workflow jobs.
- Adds support for specifying `slurm_partition` and `slurm_time` for Slurm compute backend jobs.
- Adds Kerberos sidecar container to renew ticket periodically for long-running jobs.
- Changes `reana-auth-vomsproxy` sidecar to the latest stable version to support client-side proxy file generation technique and ESCAPE VOMS.
- Changes default Slurm partition to `inf-short`.
- Changes to PostgreSQL 12.13.
- Changes the base image of the component to Ubuntu 20.04 LTS and reduces final Docker image size by removing build-time dependencies.

## 0.8.1 (2022-02-07)

- Adds support for specifying `kubernetes_job_timeout` for Kubernetes compute backend jobs.
- Adds a new condition to allow processing jobs in case of receiving multiple failed events when job containers are not in a running state.

## 0.8.0 (2021-11-22)

- Adds database connection closure after each REST API request.
- Adds labels to job and run-batch pods to reduce k8s events to listen to for `job-monitor`.
- Fixes auto-mounting of Kubernetes API token inside user jobs by disabling it.
- Changes job dispatching to use only job-specific node labels.
- Changes to PostgreSQL 12.8.

## 0.7.5 (2021-07-05)

- Changes HTCondor to 8.9.11.
- Changes myschedd package and configuration to latest versions.
- Fixes job command formatting bug for CWL workflows on HTCondor.

## 0.7.4 (2021-04-28)

- Adds configuration environment variable to set job memory limits for the Kubernetes compute backend (`REANA_KUBERNETES_JOBS_MEMORY_LIMIT`).
- Fixes Kubernetes job log capture to include information about failures caused by external factors such as OOMKilled.
- Adds support for specifying `kubernetes_memory_limit` for Kubernetes compute backend jobs.

## 0.7.3 (2021-03-17)

- Adds new configuration to toggle Kubernetes user jobs clean up.
- Fixes HTCondor Docker networking and machine version requirement setup.
- Fixes HTCondor logs and workspace files retrieval on job failure.
- Fixes Slurm job submission providing the correct shell environment to run Singularity.
- Changes HTCondor myschedd to the latest version.
- Changes job status `succeeded` to `finished` to use central REANA nomenclature.
- Changes how to deserialise job commands using central REANA-Commons deserialiser function.

## 0.7.2 (2021-02-03)

- Fixes minor code warnings.
- Changes CI system to include Python flake8 and Dockerfile hadolint checkers.

## 0.7.1 (2020-11-10)

- Adds support for specifying `htcondor_max_runtime` and `htcondor_accounting_group` for HTCondor compute backend jobs.
- Fixes Docker build by properly exiting when there are problems with `myschedd` installation.

## 0.7.0 (2020-10-20)

- Adds support for running unpacked Docker images from CVMFS on HTCondor jobs.
- Adds support for pulling private images using image pull secrets.
- Adds support for VOMS proxy as a new authentication method.
- Adds pinning of all Python dependencies allowing to easily rebuild component images at later times.
- Fixes HTCondor job submission retry technique.
- Changes error reporting on Docker image related failures.
- Changes runtime pods to prefix user workflows with the configured REANA prefix.
- Changes CVMFS to be read-only mount.
- Changes runtime job instantiation into the configured runtime namespace.
- Changes test suite to enable running tests locally also on macOS platform.
- Changes CERN HTCondor compute backend to use the new `myschedd` connection library.
- Changes CERN Slurm compute backend to improve job status detection.
- Changes base image to use Python 3.8.
- Changes code formatting to respect `black` coding style.
- Changes documentation to single-page layout.

## 0.6.1 (2020-05-25)

- Upgrades REANA-Commons package using latest Kubernetes Python client version.

## 0.6.0 (2019-12-20)

- Adds generic job manager class and provides example classes for CERN HTCondor
  and CERN Slurm clusters.
- Moves job controller to the same Kubernetes pod with the
  REANA-Workflow-Engine-\* (sidecar pattern).
- Adds sidecar container to the Kubernetes job pod if Kerberos authentication
  is required.
- Provides user secrets to the job container runtime tasks.
- Refactors job monitoring using singleton pattern.

## 0.5.1 (2019-04-23)

- Pins `urllib3` due to a conflict while installing `Kubernetes` Python
  library.
- Fixes documenation build badge.

## 0.5.0 (2019-04-23)

- Adds a new endpoint to delete jobs (Kubernetes).
- Introduces new common interface for job management which defines what the
  compute backends should offer to be compatible with REANA, currently only
  Kubernetes backend is supported.
- Fixes security vulnerability which allowed users to access other people's
  workspaces.
- Makes CVMFS mounts optional and configurable at repository level.
- Updates the creation of CVMFS volumes specification, it now uses normal
  persistent volume claims.
- Increases stability and improves test coverage.

## 0.4.0 (2018-11-06)

- Improves REST API documentation rendering.
- Changes license to MIT.

## 0.3.2 (2018-09-26)

- Adapts Kubernetes API adaptor to mount shared volumes on jobs as CEPH
  `persistentVolumeClaim`'s (managed by `reana-cluster`) instead of plain
  CEPH volumes.

## 0.3.1 (2018-09-07)

- Pins REANA-Commons and REANA-DB dependencies.

## 0.3.0 (2018-08-10)

- Adds uwsgi for production deployments.
- Switches from pykube to official Kubernetes python client.
- Adds compatibility with latest Kubernetes.

## 0.2.0 (2018-04-19)

- Adds dockerignore file to ease developments.

## 0.1.0 (2018-01-30)

- Initial public release.
