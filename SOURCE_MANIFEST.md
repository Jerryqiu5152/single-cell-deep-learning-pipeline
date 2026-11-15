# Source Manifest

This folder combines the selected source-branch materials, uploaded project documents, recovered local H5AD matrices, and saved output artifacts. The manuscript is the authority for reported paper results. Synced source documents were treated as read-only.

## Selected materials

| Project file | Source | Notes |
|---|---|---|
| `scripts/process_pcluster_jerry.ipynb` | `run_data_JQ` branch, adapted for this project | Step 5.2.3 now contains the custom PyTorch scVI-style VAE workflow identified by the author as the source of the manuscript-reported comparison. Step 5.3 points to its `merged_scvi_custom.h5ad` output. Paths use `scripts/project_paths.py`; notebook execution outputs were cleared. |
| `scripts/step5_2_3_scvi.py` | `run_data_JQ` branch, adapted for this project | Retained as an optional scvi-tools implementation; it is not the source of the manuscript-reported values. |
| `scripts/cell_annotation_DL_v2_3.ipynb` | `dev_yg` branch | Selected annotation workflow, with outputs cleared and paths adapted. |
| `scripts/deepsharp_genemarker.ipynb` and `scripts/deepsharp_genemarker.py` | `dev_yg` branch | Selected marker workflow, with machine-specific paths adapted. |
| `test_data/atlas/Immune_All_Low.pkl` | `dev_yg` branch | CellTypist atlas model. |
| Six per-run H5AD matrices under `test_data/analysis_tree/` | Recovered local materials | Raw and EmptyDrops-filtered matrices for the three GEO/SRA runs. |

## Reproducibility status

- The custom PyTorch scVI-style embedding and the NB-VAE and Harmony embeddings used by Step 5.3 are not included. The manuscript-reported evaluation table is transcribed in the notebook; its original CSV was not recovered.
- The archived `run_data_JQ` notebook includes saved output from a different execution whose evaluation values differ from the manuscript table. It is not treated as the source record for the manuscript values.
- Marker result artifacts are included, but the trained marker checkpoints and required annotation H5AD outputs were not found. The saved marker artifacts cannot be exactly regenerated from this package alone.
- Supplemental alternate notebooks were supplied later. Their reported analysis outputs differ from the paper and are marked as unverified alternatives.
- No original lockfile or complete environment export was found.

## Excluded alternatives and missing materials

- Older NB-VAE and Harmony outputs plus `merged_nbvae_model.pt` were found in a prior local output folder. Their relationship to the manuscript scores is unverified, and that checkpoint has not been confirmed compatible with the marker workflows.
- Branch archives did not contain the custom PyTorch scVI-style embedding/model, the corresponding NB-VAE/Harmony evaluation embeddings, the marker checkpoints, or `adata_umap.h5ad`.
- Raw sequencing FASTQ, an original environment lockfile, and the files named above were not present. See `DATA_AND_REPRODUCIBILITY.md` for details.
