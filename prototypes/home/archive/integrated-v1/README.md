# Home + Today Integrated v1 archive

Approved Phase 4 working baseline selected on 2026-08-13.

Source during review: `preview_10_margin_labels_left.html`.

Restored HTML SHA-256:

`66f1f8af4795aa579394ec07bc872798141907c6c216f5af0daed4f96e5c32b4`

The artifact is stored as gzip + base64 chunks named:

`home-today-integrated-v1.html.gz.b64.part*`

Restore from the repository root with:

```bash
python prototypes/home/archive/integrated-v1/restore_integrated_v1.py
```

The script writes `home-today-integrated-v1.html` inside this directory and verifies the expected SHA-256.

Important: this baseline explicitly has **no Home wing expansion**. Timeline gap/margin labels are on the **left**.
