# Data and Reproducibility

## Data sources

The manuscript uses GEO series [GSE174609](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE174609) and SRA runs **SRR14575500**, **SRR14575504**, and **SRR14575508**. Raw sequencing FASTQ files are not included.

Six converted H5AD matrices are included under `test_data/analysis_tree/cellranger/mtx_conversions/<SRR>/`: one `*_raw_matrix.h5ad` and one `*_emptydrops_filter_matrix.h5ad` for each SRR. These are count matrices converted by the upstream pipeline; they are not raw sequencing reads.

Other included data and saved artifacts:

- `test_data/atlas/Immune_All_Low.pkl` — CellTypist atlas model used by the selected workflow.
- `test_data/metadata/sample sheet.csv` — sample metadata with relative FASTQ paths to populate if running the upstream sequence-processing workflow.
- `test_data/output/merged_integrate_part*.h5ad.zip` — processed archive parts from the source repository.
- `test_data/output/approach3_deepshap_marker_table.json` and the UMAP image — saved marker and annotation artifacts.
- `results/embedding/embedding_evaluation.csv` — summary of the WSL Step 5.3 output; the executed source notebook is preserved at `scripts/process_pcluster_jerry (1).ipynb`.
- `test_data/output/combined_predictions.xlsx` — a legacy annotation workbook, not the manuscript's final prediction workbook. No current final workbook was found in the uploaded project folders or branch archives.

The archive parts and converted matrices do not include every intermediate needed by later notebooks. For example, downstream steps expect `output/5.1_merged_hvgs/merged_hvgs.h5ad`.

## Path configuration

Set `SCDLP_DATA_ROOT` to `test_data/analysis_tree` to use the included per-run matrices. Later stages write into this analysis tree. Launch Jupyter from the project folder. The bundled CellTypist atlas is used by default; set `SCDLP_ATLAS_PATH` only to override it.

Example PowerShell setup from the project folder:

```powershell
$env:SCDLP_DATA_ROOT = (Resolve-Path '.\test_data\analysis_tree').Path
jupyter lab
```

Raw FASTQ and any other required upstream files must be obtained from GEO/SRA and placed where the sample sheet and pipeline expect them. Review source-data and third-party model terms before redistribution.

## Missing items for exact regeneration

- The merged-HVG input at `output/5.1_merged_hvgs/merged_hvgs.h5ad`, the custom PyTorch scVI-style embedding at `output/5.2.3_scVI/scvi_custom/merged_scvi_custom.h5ad`, its `scvi_custom_model.pt`, and the NB-VAE and Harmony embeddings are not included. These files were not present in the uploaded project folder or the `run_data_JQ` / `dev_yg` branch archives.
- The executed WSL notebook does preserve the Step 5.3 outputs: NB-VAE overall score 0.697345, PCA + Harmony 0.674383, and custom PyTorch scVI-style VAE 0.697902. The CSV is a transcription of those saved outputs, not a fresh calculation from latent files. The scores are point estimates from one fixed 5,000-cell subsample (random state 0).
- The separate `scripts/step5_2_3_scvi.py` runs scvi-tools SCVI as an optional alternative. That representation did not produce the manuscript-reported comparison values; its H5AD and model are not included.
- The selected marker notebook expects `hemibrain_nn_model.pt`, `hemibrain_scanvi_nbvae_model.pt`, and annotation H5AD outputs. These were not found in the uploaded folders or branch archives. The supplemental alternate workflow expects `customnn_model.pt`, `scanvi_nbvae_model.pt`, and `adata_umap.h5ad`; those were not found either.
- An older `merged_nbvae_model.pt` exists in a prior local output folder, but its compatibility with either marker workflow has not been established; it is not a substitute.
- The legacy `combined_predictions.xlsx` is the same file from the `dev_yg` archive; it predates the final annotation output. The newer final workbook was not among the files located.
- No original lockfile or complete environment export was found. `requirements.in` lists imported dependencies but has no pinned versions and has not been tested as an environment.

The canonical project notebook contains the selected code and the manuscript-aligned summary. The archived WSL notebook supplies the executed-output provenance. Exact regeneration still requires the missing intermediate data, model checkpoints, and a versioned environment. See `SOURCE_MANIFEST.md` for branch provenance and excluded alternatives.

