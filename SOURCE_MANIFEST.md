# Source Manifest

This folder combines the selected source-branch materials, uploaded project documents, recovered local H5AD matrices, and saved output artifacts. The manuscript is the authority for reported paper results. Synced source documents were treated as read-only.

## Canonical files

| Destination | Origin | Notes |
|---|---|---|
| `scripts/process_pcluster_jerry.ipynb` | `run_data_JQ` branch | Selected preprocessing and embedding notebook. Project-copy edits align the evaluation with the manuscript's separate scvi-tools result and route data paths through `scripts/project_paths.py`. Stale execution outputs were cleared. |
| `scripts/step5_2_3_scvi.py` | `run_data_JQ` branch | Project-copy input path and maximum epoch count aligned to the manuscript (400). |
| `scripts/cell_annotation_DL_v2_3.ipynb` | `dev_yg` branch | Updated annotation notebook cited by the manuscript; paths made configurable in the project copy. |
| `scripts/deepsharp_genemarker.ipynb`, `scripts/deepsharp_genemarker.py` | `dev_yg` branch | Marker workflow and companion helper. Paths made configurable in the notebook copy. |
| `test_data/atlas/Immune_All_Low.pkl` | `dev_yg` branch | CellTypist atlas model. |
| `test_data/metadata/sample sheet.csv` | `run_data_JQ` branch | Cluster-specific FASTQ paths replaced with relative `fastqs/` paths for portability. |
| `test_data/analysis_tree/cellranger/mtx_conversions/<SRR>/` | Prior local project folder | Six converted H5AD matrices, raw and EmptyDrops-filtered for all three manuscript runs. Filenames and directory layout match the supplied preprocessing notebook. |
| `test_data/output/merged_integrate_part*.h5ad.zip` | `run_data_JQ` branch | Eleven processed archive parts. |
| Saved workbook, marker JSON, and UMAP output in `test_data/output/` | `dev_yg` branch | Later-stage saved artifacts. |
| `docs/`, `paper_assets/` | User-provided materials and existing project workspace | Manuscript, references, presentation, and figure assets. |

## Supplemental notebooks

The user supplied `scRNAseq_1_Preprocess.ipynb`, two byte-identical copies of `scRNAseq_2.1_CellReTypeSupervised.ipynb`, and `scRNAseq_3_GeneMarker.ipynb`. Copies are in `docs/supplemental_workflows/alternate_local_notebooks/`. They are explicitly marked as an alternate, unverified workflow; notebook execution outputs were cleared in the project copies. They are not part of the canonical manuscript workflow because the Approach 1/2 assignments differ.

The original saved output from the supplemental gene-marker notebook reported 9,192 explained cells across 80 strata and a mean SHAP efficiency gap of 13.95278. The manuscript reports 9,182 cells across 79 strata and a near-zero gap. Treat those supplemental outputs as a different run, not as support for the paper.

## Additional local candidates not included

- A `merged_hvgs.h5ad` file was found in two local locations; the copies have the same SHA-256. Its shape, metadata, and derivation could not be checked against the manuscript, so it was not installed as the canonical 5.1 output.
- Older NB-VAE and Harmony outputs plus `merged_nbvae_model.pt` were found. Their relationship to the reported scores is unverified, and that checkpoint has not been confirmed compatible with the marker workflows.
- Branch archives did not contain the scvi-tools H5AD/model or the marker checkpoint files listed in `DATA_AND_REPRODUCIBILITY.md`.

## Known omissions

Raw sequencing FASTQ, the scvi-tools result/model, the named marker checkpoints and required annotation H5AD outputs, an original environment lockfile, and a project license were not present. See `DATA_AND_REPRODUCIBILITY.md` for details.
