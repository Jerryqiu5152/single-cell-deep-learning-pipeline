"""
================================================================================
 scVI decoder  +  Chapter-4 custom NN  +  DeepSHAP  ->  cell-type x gene markers
================================================================================
 Implements Book 3:  Chapter 4 (Approach 3 classifier)  ->  5.4 (DeepSHAP)
                     ->  5.6 (aggregate -> decode -> C x genes marker table).

 IMPORTANT — this script does NOT retrain anything:
   * scVI is NOT re-run.  You already produced the 30-dim latent codes Z;
     this script LOADS Z from disk.  It opens the scVI model object only to
     read the frozen DECODER weights for the 5.6 loading matrix (a load, not
     a fit).  If you saved the 30 x n_HVG loading matrix L already, skip
     opening scVI entirely (see 4C).
   * Approach 3 is NOT re-run.  You already trained the custom NN and have its
     predicted labels; this script LOADS the labels and the frozen NN weights.
     DeepSHAP needs the NN object because it back-propagates through the NN's
     layers -- but loading frozen weights is not training.

 So the only NEW computation here is DeepSHAP + the decoder-loading read +
 one matrix multiply.  Nothing is optimized or updated.

 Packages (Lilly): install torch, shap, scvi-tools, scanpy from the internal
 JFrog Artifactory (Developer Platform Front Door), not public PyPI.
================================================================================
"""

import numpy as np
import torch
import torch.nn as nn
import scanpy as sc
import scvi
import shap
import json


# ------------------------------------------------------------------ #
# The Chapter-4 architecture. Must MATCH what you trained (only so the
# saved weights load into the right shapes). Loading != retraining.
# ------------------------------------------------------------------ #
class CellTypeNet(nn.Module):
    def __init__(self, n_latent=30, n_classes=20, h1=128, h2=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_latent, h1), nn.ReLU(),
            nn.Linear(h1, h2),       nn.ReLU(),
            nn.Linear(h2, n_classes),
        )
    def forward(self, z):
        return torch.softmax(self.net(z), dim=1)     # P(type); matches 5.4


def main():
    # ============================================================== #
    # 1.  LOAD WHAT YOU ALREADY HAVE  (no scVI re-run, no NN re-train)
    # ============================================================== #
    # 1a. latent codes you already computed with scVI  (n_cells x 30)
    Z = np.load("latent_Z.npy").astype("float32")          # <-- your saved Z
    n_cells, n_latent = Z.shape
    Zt = torch.tensor(Z)

    # 1b. predicted cell-type labels you already got from Approach 3
    pred = np.load("pred_labels.npy").astype(int)          # <-- your saved labels
    C = int(pred.max()) + 1

    # 1c. the frozen custom NN (loaded, NOT trained) -- needed by DeepSHAP,
    #     which must back-propagate through its layers.
    net = CellTypeNet(n_latent=n_latent, n_classes=C)
    net.load_state_dict(torch.load("celltype_net.pt"))
    net.eval()
    for p in net.parameters():
        p.requires_grad_(False)                            # frozen

    # ============================================================== #
    # 2.  DeepSHAP on the frozen NN  (section 5.4)
    #     Uses Z (from scVI) + the NN's weights (from Ch 4).
    #     Uses NO scVI weights.  Output: phi (n_cells x 30).
    # ============================================================== #
    rng = np.random.default_rng(0)
    bg_idx = rng.choice(n_cells, size=min(200, n_cells), replace=False)
    background = Zt[bg_idx]                                 # baseline set

    explainer = shap.DeepExplainer(net, background)
    shap_all = explainer.shap_values(Zt)                   # list of C arrays (n_cells x 30)
    shap_all = np.stack(shap_all, axis=0)                  # (C, n_cells, 30)
    phi = shap_all[pred, np.arange(n_cells), :]            # each cell's predicted-class row

    # efficiency check (5.4): sum of 30 phi  ~=  P(pred) - P(baseline)
    with torch.no_grad():
        p_cells = net(Zt).numpy()
        p_base = net(background).numpy().mean(0)
    gap = p_cells[np.arange(n_cells), pred] - p_base[pred]
    print("mean |sum(phi) - gap| =", round(float(np.abs(phi.sum(1) - gap).mean()), 5),
          " (~0 confirms efficiency)")

    # ============================================================== #
    # 3.  AGGREGATE BY TYPE -> Imp (C x 30)   (5.6 step 2)
    # ============================================================== #
    Imp = np.zeros((C, n_latent))
    for k in range(C):
        rows = phi[pred == k]
        if len(rows):
            Imp[k] = np.abs(rows).mean(0)

    # ============================================================== #
    # 4.  DECODER LOADINGS  L  (30 x n_HVG)   (5.6 step 3)
    #     THIS is the only step that uses scVI's own weights (decoder).
    #     Pick ONE of 4A / 4B / 4C.
    # ============================================================== #

    # ---- 4A. LDVAE (linear decoder): EXACT, one line, recommended ----
    #     If you trained LinearSCVI, L = decoder weight matrix, exactly.
    # adata = sc.read_h5ad("hemibrain_hvg.h5ad")
    # ld = scvi.model.LinearSCVI.load("ldvae_model/", adata=adata)   # load, not train
    # L = ld.get_loadings().values.T                                 # (30 x n_HVG)
    # genes = ld.adata.var_names.to_numpy()

    # ---- 4B. Standard nonlinear scVI: Jacobian of the frozen decoder ----
    #     L = (W_dec . G2 . W2 . G1 . W1)^T at the baseline z0, via autograd
    #     (works for any n_layers). Local approximation.
    adata = sc.read_h5ad("hemibrain_hvg.h5ad")
    scvi_model = scvi.model.SCVI.load("scvi_model/", adata=adata)   # load, not train
    genes = adata.var_names.to_numpy()
    z0 = torch.tensor(Z[bg_idx].mean(0, keepdims=True), dtype=torch.float32)

    def decode_logmu(z):
        # frozen-decoder mean path -> per-gene log-mean (n_HVG,).
        # The exact accessor is version-dependent; adjust to your scvi-tools
        # version if needed (e.g. scvi_model.module.decoder(...) signature).
        dec = scvi_model.module.decoder
        out = dec("gene", z, torch.zeros(z.shape[0], 1))
        px_scale = out[0] if isinstance(out, (tuple, list)) else out
        return torch.log(px_scale.squeeze(0) + 1e-8)

    J = torch.autograd.functional.jacobian(decode_logmu, z0.requires_grad_(True))
    L = J.squeeze().T.detach().numpy()                     # (30 x n_HVG)

    # ---- 4C. Pre-saved loadings: if you already extracted L, just load it ----
    #     (then you don't need to open scVI at all)
    # L = np.load("decoder_loadings_L.npy")                # (30 x n_HVG)
    # genes = np.load("hvg_names.npy", allow_pickle=True)

    print("loading matrix L:", L.shape, " (30 x n_HVG)")

    # ============================================================== #
    # 5.  MARKER TABLE  M = Imp . |L|  (C x n_HVG)   (5.6 steps 4-5)
    # ============================================================== #
    M = Imp @ np.abs(L)                                     # (C x n_HVG)

    type_names = [f"type{k}" for k in range(C)]            # rename to your labels
    top_n = 15
    table = {}
    for k in range(C):
        order = np.argsort(-M[k])[:top_n]
        table[type_names[k]] = [(str(genes[j]), float(round(M[k][j], 4))) for j in order]

    for t, mk in table.items():
        print(f"{t}:  " + ", ".join(g for g, _ in mk[:8]))
    with open("marker_table.json", "w") as f:
        json.dump(table, f, indent=2)
    print("Saved marker_table.json.  Capped at the ~n_HVG decoder genes.")


if __name__ == "__main__":
    main()