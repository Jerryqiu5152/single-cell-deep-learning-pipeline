# Data and Reproducibility

## Data sources

The manuscript uses GEO series [GSE174609](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE174609) and SRA runs **SRR14575500**, **SRR14575504**, and **SRR14575508**. Raw sequencing FASTQ files are not included.

Six converted H5AD matrices are included under `test_data/analysis_tree/cellranger/mtx_conversions/<SRR>/`: one `*_raw_matrix.h5ad` and one `*_emptydrops_filter_matrix.h5ad` for each SRR. The preprocessing notebook confirms these names and directory structure. These are count matrices converted by the upstream pipeline; they are not raw sequencing reads.

Other included data and saved artifacts:

- `test_data/atlas/Immune_All_Low.pkl` — CellTypist atlas model.
- `test_data/metadata/sample sheet.csv` — sample metadata with relative FASTQ paths to be populated if running the upstream sequence-processing workflow.
- `test_data/output/merged_integrate_part*.h5ad.zip` — processed archive parts from the source repository.
- `test_data/output/combined_predictions.xlsx`, `approach3_deepshap_marker_table.json`, and the UMAP image — saved result artifacts.

The archive parts and converted matrices do not include every intermediate needed by all later notebooks. For example, downstream steps expect `output/5.1_merged_hvgs/merged_hvgs.h5ad`.

## Path configuration

Set `SCDLP_DATA_ROOT` to `test_data/analysis_tree` to use the included per-run matrices. Later stages write into this analysis tree. Launch Jupyter from the project folder. The bundled CellTypist atlas is used by default; set `SCDLP_ATLAS_PATH` only to override it.

Example PowerShell setup from the project folder:

```powershell
$env:SCDLP_DATA_ROOT = (Resolve-Path '.\test_data\analysis_tree').Path
jupyter lab
```

Raw FASTQ and any other required upstream files must be obtained from GEO/SRA and placed where the sample sheet and pipeline expect them. Review source-data and third-party model terms before redistribution.

## Missing items for exact regeneration

- The scvi-tools result `output/5.2.3_scVI/merged_scvi.h5ad` and saved scvi-tools model are not included. The notebook/helper can create them from the HVG input, but this run has not been repeated in this package.
- The canonical marker notebook expects `hemibrain_nn_model.pt`, `hemibrain_scanvi_nbvae_model.pt`, and annotation H5AD outputs. These were not found.
- The supplemental alternate workflow expects `customnn_model.pt`, `scanvi_nbvae_model.pt`, and `adata_umap.h5ad`. Those were not found either.
- An older `merged_nbvae_model.pt` exists in a prior local output folder, but its compatibility with either marker workflow has not been established; it is not included as a substitute.
- No original lockfile or complete environment export was found. `requirements.in` lists imported dependencies but has no pinned versions and has not been tested as an environment.

The embedding comparison displayed in the canonical notebook is transcribed from the manuscript, not freshly computed. See `SOURCE_MANIFEST.md` for branch provenance and the status of supplemental files.
