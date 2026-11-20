# Single-Cell Deep Learning Pipeline

This repository organizes the manuscript workflow, available data inputs, result artifacts, figures, and supporting documents. The paper is the authority for reported results.

## Canonical workflow

1. `scripts/process_pcluster_jerry.ipynb` — project-adapted preprocessing, custom PyTorch scVI-style embedding, embedding comparison, and downstream graph analysis. The third embedding in Step 5.3 is the custom PyTorch model, not scvi-tools SCVI.
2. `scripts/cell_annotation_DL_v2_3.ipynb` — selected annotation workflow from `dev_yg`.
3. `scripts/deepsharp_genemarker.ipynb` and `scripts/deepsharp_genemarker.py` — selected marker workflow from `dev_yg`.
4. `scripts/step5_2_3_scvi.py` — optional scvi-tools implementation; it did not produce the manuscript-reported comparison values.

The canonical project-adapted notebook is `scripts/process_pcluster_jerry.ipynb`. The exact executed WSL notebook from `run_data_JQ` is preserved at `scripts/process_pcluster_jerry (1).ipynb`; its saved Step 5.3 output is the source for the manuscript-aligned values and summary CSV. The canonical notebook uses `scripts/project_paths.py`; it has not been rerun because required intermediate embeddings are not included.

The notebooks route project data through `scripts/project_paths.py`. Set `SCDLP_DATA_ROOT` to `test_data/analysis_tree` to use the recovered per-run input matrices; see `DATA_AND_REPRODUCIBILITY.md`.

Supplemental notebooks supplied later are stored in `docs/supplemental_workflows/alternate_local_notebooks/`. They are marked as alternate, unverified workflows and are not the paper's canonical analysis.

## Included material

- `test_data/atlas/Immune_All_Low.pkl` — CellTypist atlas used by the selected workflow.
- `test_data/metadata/sample sheet.csv` — sample metadata.
- `test_data/analysis_tree/cellranger/mtx_conversions/` — six per-run converted H5AD matrices: raw and EmptyDrops-filtered for all three SRR runs.
- `test_data/output/` — processed archive parts and saved result artifacts. `combined_predictions.xlsx` is a legacy annotation workbook and does not represent the manuscript's final annotation counts; see `test_data/output/README.md`.
- `results/embedding/embedding_evaluation.csv` — manuscript-aligned summary transcribed from the executed WSL notebook output; it is not recomputed from included embeddings.
- `docs/` and `paper_assets/` — manuscript, reference documents, presentation, and figures. The executed source-run notebook is in `scripts/`.

## Remaining reproducibility limits

- Raw FASTQ files are not included; GEO/SRA identifiers and retrieval notes are in `DATA_AND_REPRODUCIBILITY.md`.
- The merged-HVG input, custom PyTorch scVI-style embedding and saved model, and the NB-VAE and Harmony embeddings are not included. The archived WSL notebook records the executed comparison, but the table cannot be independently regenerated from this repository alone.
- The current final `combined_predictions.xlsx` could not be recovered from the uploaded project folders. The included workbook is an older result and should not be used as the manuscript's final prediction table.
- Marker checkpoints and the required `adata_umap.h5ad` are missing. The marker table is included, but cannot be exactly regenerated from the package.
- `requirements.in` is unpinned and untested. No original lockfile was found.

See `SOURCE_MANIFEST.md` for provenance, recovered files, and excluded alternatives.

