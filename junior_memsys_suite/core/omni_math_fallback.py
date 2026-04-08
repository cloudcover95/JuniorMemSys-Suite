import numpy as np

class SovereignOmniKernel:
    def __init__(self, variance_retention=0.95, h_bar_mkt=0.01):
        self.variance_retention = variance_retention
        self.h_bar_mkt = h_bar_mkt
        self.rank = 1

    def compute_svd_mesh(self, X: np.ndarray):
        self.mu = np.mean(X, axis=1, keepdims=True)
        X_centered = X - self.mu
        U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
        explained_variance = (S ** 2) / (np.shape(X)[1] - 1)
        cumulative_variance = np.cumsum(explained_variance) / np.sum(explained_variance)
        self.rank = int(np.searchsorted(cumulative_variance, self.variance_retention) + 1)
        self.S_reduced = S[:self.rank]
        self.Vt_reduced = Vt[:self.rank, :]
        return self.S_reduced, self.Vt_reduced

    def map_freedman_ladder(self, standard_candle_idx=0):
        V_standard = self.Vt_reduced[:, standard_candle_idx]
        diff = self.Vt_reduced - V_standard[:, np.newaxis]
        weighted_diff_sq = (diff ** 2) * (self.S_reduced[:, np.newaxis] ** 2)
        distances = np.sqrt(np.sum(weighted_diff_sq, axis=0))
        return np.round(distances, 4)

    def calculate_quantum_matrix(self, z_scores, deltas, base_vols):
        safe_bases = np.where(base_vols > 0, base_vols, self.h_bar_mkt)
        action_hats = deltas / safe_bases
        q_marks = 1.0 - np.exp(-(np.abs(z_scores) * action_hats))
        return np.round(q_marks, 4)
