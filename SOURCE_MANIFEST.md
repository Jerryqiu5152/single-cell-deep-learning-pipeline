# Source Manifest

This folder combines selected source-branch materials, uploaded project documents, recovered local H5AD matrices, and saved output artifacts. The manuscript is the authority for reported paper results. Synced source documents were treated as read-only.

## Selected materials

| Project file | Source | Notes |
|---|---|---|
| `scripts/process_pcluster_jerry.ipynb` | `run_data_JQ` workflow, project-adapted | Canonical cleaned notebook. Step 5.2.3 contains the custom PyTorch scVI-style VAE; Step 5.3 uses that embedding for the manuscript comparison. Paths use `scripts/project_paths.py`; execution outputs are cleared. |
| `scripts/process_pcluster_jerry (1).ipynb` | `run_data_JQ` branch, exact executed source copy | Preserved WSL notebook with saved Step 5.3 output. It retains older/general scVI wording in earlier sections; the evaluated Step 5.3 third embedding is loaded from `5.2.3_scVI/scvi_custom/merged_scvi_custom.h5ad`. |
| `results/embedding/embedding_evaluation.csv` | Transcribed from executed WSL Step 5.3 output | Manuscript-aligned summary; not recomputed from included latent embeddings. Component metrics are retained at printed precision; overall scores at full printed precision. |
| `scripts/step5_2_3_scvi.py` | `run_data_JQ` branch, adapted | Optional scvi-tools implementation; it is not the source of the manuscript-reported values. |
| `scripts/cell_annotation_DL_v2_3.ipynb` | `dev_yg` branch | Selected annotation workflow, with outputs cleared and paths adapted. |
| `scripts/deepsharp_genemarker.ipynb` and `scripts/deepsharp_genemarker.py` | `dev_yg` branch | Selected marker workflow, with machine-specific paths adapted. |
| `test_data/atlas/Immune_All_Low.pkl` | `dev_yg` branch | CellTypist atlas used by the selected PBMC workflow. Other atlas models present in the branch archive were not required by this workflow. |
| Six per-run H5AD matrices under `test_data/analysis_tree/` | Recovered local materials | Raw and EmptyDrops-filtered matrices for the three GEO/SRA runs. |
| `test_data/output/combined_predictions.xlsx` | `dev_yg` branch | Legacy workbook; its annotation counts and approach order do not match the final manuscript output. No replacement workbook was found in the uploaded folders or branch archives. |

## Reproducibility status

- The executed WSL notebook `scripts/process_pcluster_jerry (1).ipynb` preserves the Step 5.3 output matching the manuscript: NB-VAE 0.697345, PCA + Harmony 0.674383, and custom PyTorch scVI-style VAE 0.697902.
- The custom PyTorch scVI-style embedding/model and the NB-VAE and Harmony evaluation embeddings are absent. The CSV is a documented transcription of the saved notebook output, not an independently recomputed result.
- The latest annotation workbook was not found. The included `combined_predictions.xlsx` remains as a legacy artifact and is labeled accordingly in `test_data/output/README.md`.
- Marker result artifacts are included, but the trained marker checkpoints and required annotation H5AD outputs were not found. The saved marker artifacts cannot be exactly regenerated from this package alone.
- Supplemental alternate notebooks were supplied later. Their reported analysis outputs differ from the paper and are marked as unverified alternatives.
- No original lockfile or complete environment export was found.

## Excluded alternatives and missing materials

- Older NB-VAE and Harmony outputs plus `merged_nbvae_model.pt` were found in a prior local output folder. Their relationship to the manuscript scores is unverified, and that checkpoint has not been confirmed compatible with the marker workflows.
- The `dev_yg` branch archive also contained `Immune_All_High.pkl` and `Healthy_COVID19_PBMC.pkl`; the selected workflow uses `Immune_All_Low.pkl`, so these unused atlas models were not added. Review their redistribution terms before publishing them.
- Neither branch archive contained the merged-HVG intermediate, the custom PyTorch scVI-style embedding/model, the corresponding NB-VAE/Harmony embeddings, the marker checkpoints, or `adata_umap.h5ad`.
- Raw sequencing FASTQ and an original environment lockfile were not present. See `DATA_AND_REPRODUCIBILITY.md` for details.

