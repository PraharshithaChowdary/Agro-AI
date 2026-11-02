# AGRO AI — Update and Model Audit (2026-10-24)

## Changes made

### Accounts and persistence
- Login no longer silently creates an account. New users must use `/api/auth/signup`; login only authenticates existing credentials.
- Plant identification and named-plant/crop/soil analysis history is stored against the authenticated user when signed in. A new `plant_analysis_history` table stores result JSON, organ/type, image filename, timestamp, and user ownership. Production history additionally stores the request fields as JSON in `input_json`; uploaded image bytes are not retained. Guest previews remain possible but explicitly report that they were not saved to an account.
- Production and plant-analysis history endpoints require authentication and filter by the current account; anonymous visitors cannot query another user's history. Plant image uploads are validated for size, decode integrity, and minimum dimensions before inference.
- Weekly plans and profile inputs persist to the signed-in account; guest plan generation remains a non-persisted preview; the service no longer reports local-only state as a successful account save. Updating a saved plan checks that the signed-in user owns the record.
- Assistant conversations persist per user when signed in; guest use is a non-persisted preview; global LLM configuration changes are restricted to authenticated administrators. Failed history persistence now returns an error rather than silently pretending to save.
- Frontend auth no longer keeps a stale cached user after a server-reported authentication error.

### Assistant and module reliability
- Removed the client-side assistant fallback that gave pesticide rates and source claims without contacting the backend. Backend errors are now surfaced to the UI rather than disguised as an AI answer.
- Assistant responses add role-oriented follow-up guidance based on the role attached to the authenticated user (`farmer`, `buyer`, or `general`).
- Updated landing-page copy to remove unsupported blanket claims of 100% privacy/offline operation. Updated training docs to distinguish synthetic-feature experiments from real-photo accuracy.
- Crop/soil model inference no longer raises low/unknown model scores to fabricated high confidence values. Colour-based rules return no numerical confidence, and output includes limitations. Unverified crop disease results do not provide model-derived chemical recommendations; they advise confirmation first.
- Metadata and `EVALUATION_REPORT.md` no longer present the contradictory 15.15% plant identification result as passed. Legacy score figures are preserved only as unverified historical fields.

### Plant image classifier
- Plant identification selects the shipped ONNX image classifier for supported leaf/whole-plant images instead of using the 98-label engineered-feature joblib model as if it recognised images. The backend can also select a separately trained `plant_identifier.keras` model when the training script registers it, with class-label count checks and MobileNetV2-matching preprocessing.
- The ONNX model metadata lists 14 supported labels: capsicum-annuum, citrus-sinensis, cucurbita-pepo, fragaria-ananassa, glycine-max, malus-domestica, prunus-avium, prunus-persica, rubus-idaeus, solanum-lycopersicum, solanum-tuberosum, vaccinium-corymbosum, vitis-vinifera, and zea-mays. Unsupported organs/classes should be inconclusive rather than forcibly assigned a species.
- Added `onnxruntime` to backend requirements. Corrected the image training script to use MobileNetV2's expected `[-1, 1]` preprocessing and store Keras metadata separately without overwriting the currently deployed ONNX class map.

## Important limits — not concealed

- **A genuine model retraining run has not been completed.** The archive has pretrained binary model files and CSVs containing engineered 48-feature rows, but not the labelled original photographs needed for a credible, supervised image retrain/holdout test. The retraining script is now wired so a trained Keras model can be used by the backend, but it still needs a real labelled photo dataset and must be run with TensorFlow installed.
- The local execution environment could not install missing dependencies because network/package access was unavailable. In particular, `bcrypt` is unavailable, and `frontend/node_modules` is absent. The full pytest suite stops at collection with `ModuleNotFoundError: bcrypt`; the frontend production build was not verified. The existing `frontend/dist` was retained but was not regenerated, so run a fresh build before deployment.
- The supplied evaluation report records 15.15% in-distribution identification accuracy against an >85% target; that target is failed. Its synthetic specimen evaluation is not a real-world benchmark. The actual real-photo accuracy of the shipped ONNX model remains unverified.
- Crop-disease/soil classification from engineered colour/shape features is inherently limited. The UI still provides a category candidate, but the response now clearly states that it is a screening result; soil fertility/pH and disease diagnosis need independent tests/field verification.

## Required local verification

From `backend/`, install `requirements.txt`, confirm the database backup exists, then run `pytest -q`. Confirm the `onnxruntime` install and test a balanced set of real photographs. From `frontend/`, run `npm ci` and `npm run build`. Do not advertise an accuracy percentage until a separately held-out, labelled, real-photo evaluation has been completed.

## Protecting data

A database backup was created outside this delivery folder as `/mnt/data/AGRO_AI_original_db_backup.db`. The shipped database was not intentionally wiped or recreated. Before deployment, back up your live database independently and verify access controls with two test accounts.
