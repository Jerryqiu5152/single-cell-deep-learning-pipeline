# Single-Cell Deep Learning Pipeline

This repository organizes the manuscript workflow, available data inputs, result artifacts, figures, and supporting documents. The paper is the source of truth for reported results.

## Canonical workflow

1. `scripts/process_pcluster_jerry.ipynb` — preprocessing, embeddings, evaluation, and downstream graph. Its evaluation points to the separately trained scvi-tools SCVI output described in the paper.
2. `scripts/cell_annotation_DL_v2_3.ipynb` — the annotation workflow selected from `dev_yg`.
3. `scripts/deepsharp_genemarker.ipynb` and `scripts/deepsharp_genemarker.py` — marker workflow selected from `dev_yg`.
4. `scripts/step5_2_3_scvi.py` — standalone scvi-tools helper, set to the paper's 400-epoch maximum and model dimensions.

The notebooks route former cluster paths through `scripts/project_paths.py`. Set `SCDLP_DATA_ROOT` to `test_data/analysis_tree` to use the recovered per-run input matrices; see `DATA_AND_REPRODUCIBILITY.md`. The notebooks have not been rerun after path configuration, so the package does not claim a fresh reproduction.

Supplemental notebooks supplied later are stored in `docs/supplemental_workflows/alternate_local_notebooks/`. They are clearly marked as an alternate, unverified workflow and are not the paper's canonical analysis.

## Included material

- `test_data/atlas/Immune_All_Low.pkl` — CellTypist atlas.
- `test_data/metadata/sample sheet.csv` — sample metadata.
- `test_data/analysis_tree/cellranger/mtx_conversions/` — six per-run converted H5AD matrices: raw and EmptyDrops-filtered for all three SRR runs.
- `test_data/output/` — processed archive parts, saved tables, and figures.
- `docs/` and `paper_assets/` — manuscript, reference documents, presentation, and figures.

## Remaining reproducibility limits

- Raw FASTQ files are not included; the GEO/SRA identifiers and retrieval notes are in `DATA_AND_REPRODUCIBILITY.md`.
- The scvi-tools `merged_scvi.h5ad` and saved model are not included, so the manuscript's embedding metrics cannot be regenerated from this folder alone. The notebook labels its comparison values as transcribed from the paper.
- Marker checkpoints and the required `adata_umap.h5ad` are missing. The marker table is included, but cannot be exactly regenerated from the package.
- `requirements.in` is unpinned and untested. No original lockfile was found.
- No project license is included yet. Add one on GitHub only after choosing terms you are authorized to grant; third-party materials may have separate terms.

See `SOURCE_MANIFEST.md` for provenance, recovered files, and excluded alternatives.
