# Concrete production delta

Before a service can use this design, supply real authenticated identity, protected key distribution/rotation, historical policy versions, access-controlled storage and independently protected freshness checkpoints. Separate identity from user-provided record fields. Bind exact retry IDs to content/result and define how to reconcile an append whose acknowledgement was lost.

Replace exclusive in-process ownership with transactional concurrency control, model crash points between append/sync/checkpoint/response, test backup restoration against trusted tips, and review log/metric disclosure. Confidentiality requires an established AEAD design and nonce/key lifecycle, absent here. Do not convert the HMAC into an encryption scheme. Load limits must include connection count and queues as well as frame/record bounds. None of these tasks is counted complete by passing the local mutation tests.
