#!/usr/bin/env python3
"""
Optional scvi-tools SCVI workflow (not used for manuscript-reported comparison values). Run as a standalone script so it survives SSH disconnection.
Usage:
    nohup python3 step5_2_3_scvi.py > step5_2_3_scvi.log 2>&1 &
    tail -f step5_2_3_scvi.log   # monitor progress
"""
import os
from project_paths import data_path
import warnings
import logging
import torch
import pandas as pd
import scanpy as sc
import scvi
import matplotlib
matplotlib.use("Agg")   # no display needed
import matplotlib.pyplot as plt
from scvi.model import SCVI
from threadpoolctl import threadpool_limits

warnings.filterwarnings("ignore", message=".*NVML.*")
warnings.filterwarnings("ignore", message=".*CUDA initialization.*")
warnings.filterwarnings("ignore", message=".*srun.*")
logging.getLogger("lightning.fabric.plugins.environments.slurm").setLevel(logging.ERROR)
logging.getLogger("lightning").setLevel(logging.ERROR)

# ── Parameters ─────────────────────────────────────────────────────────────────
n_hidden               = 128
n_layers               = 2
n_latent               = 30
dispersion             = "gene"
gene_likelihood        = "zinb"
batch_key              = "batch"
categorical_covariates = None
continuous_covariates  = None
n_threads              = 4

# ── Paths ──────────────────────────────────────────────────────────────────────
input_h5ad = str(data_path("output/5.1_merged_hvgs/merged_hvgs.h5ad"))
out_dir    = str(data_path("output/5.2.3_scVI"))
os.makedirs(out_dir, exist_ok=True)
prefix = "merged_scvi"

# ── Setup ──────────────────────────────────────────────────────────────────────
torch.set_float32_matmul_precision("medium")
threadpool_limits(n_threads)
scvi.settings.num_threads = n_threads
scvi.settings.seed = 0

print(f"Loading {input_h5ad} ...")
adata = sc.read_h5ad(input_h5ad)
print(f"  Loaded : {adata.n_obs} cells x {adata.n_vars} genes")

# ── Train ──────────────────────────────────────────────────────────────────────
SCVI.setup_anndata(
    adata,
    batch_key=batch_key,
    categorical_covariate_keys=categorical_covariates,
    continuous_covariate_keys=continuous_covariates,
)
model = SCVI(
    adata,
    n_hidden=n_hidden,
    n_layers=n_layers,
    n_latent=n_latent,
    dispersion=dispersion,
    gene_likelihood=gene_likelihood,
)
print("Training scVI ...")
# Manuscript configuration: maximum 400 epochs with early stopping enabled.
model.train(early_stopping=True, max_epochs=400)
print("Training complete.")

# ── Train vs Validation loss curve ────────────────────────────────────────────
available_keys = list(model.history.keys())
print(f"  History keys: {available_keys}")

train_key = next((k for k in ["elbo_train", "train_loss_epoch"] if k in available_keys), None)
val_key   = next((k for k in ["elbo_validation", "validation_loss"] if k in available_keys), None)

if train_key and val_key:
    train_hist = model.history[train_key].values.squeeze()
    val_hist   = model.history[val_key].values.squeeze()

    plt.figure(figsize=(6, 3))
    plt.plot(train_hist, label="train ELBO")
    plt.plot(val_hist,   label="validation ELBO", linestyle="--")
    plt.xlabel("Epoch"); plt.ylabel("ELBO loss")
    plt.title("Step 5.2.3 scVI — Train vs Validation ELBO")
    plt.legend(); plt.tight_layout()
    plt.savefig(os.path.join(out_dir, f"{prefix}_loss.png"), dpi=150)
    plt.close()
    print(f"  Saved : {prefix}_loss.png")
    print(f"  Best val ELBO : {val_hist.min():.4f}  (epoch {val_hist.argmin() + 1})")
else:
    print(f"  Loss plot skipped — unexpected history keys: {available_keys}")

# ── Extract latent embedding ───────────────────────────────────────────────────
adata.obsm["X_emb"] = model.get_latent_representation()

for k in ["_scvi_manager_uuid", "_scvi_uuid"]:
    adata.uns.pop(k, None)

# ── Save ───────────────────────────────────────────────────────────────────────
adata.write_h5ad(os.path.join(out_dir, f"{prefix}.h5ad"))
model.save(os.path.join(out_dir, f"{prefix}_model"), overwrite=True)
pd.DataFrame(adata.obsm["X_emb"], index=adata.obs_names).to_pickle(
    os.path.join(out_dir, f"X_{prefix}.pkl")
)

print(f"  Latent shape : {adata.obsm['X_emb'].shape}")
print(f"  Output       : {out_dir}")
print("Step 5.2.3 scVI — done.")

