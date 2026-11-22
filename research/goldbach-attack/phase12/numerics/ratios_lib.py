"""Libraries for phase-12 ratios-truth numerics.

Reuses the validated phase-11 fast DFT pipeline for R_q (exact full primitive-character sum)
and the phase-11b corrected M_q (proper A_q mask: keep p with q%p != 0), NOT the buggy
phase-10 mask code.
"""
import sys, os
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
PH11=os.path.abspath(os.path.join(HERE,'..','..','phase11','numerics'))
PH10=os.path.abspath(os.path.join(HERE,'..','..','phase10','numerics'))
sys.path.insert(0,PH11); sys.path.insert(0,PH10)
from fastpipe import Group, make_logtab, factorize       # noqa: E402
from core import compute_E                                # noqa: E402
from corrected import M_correct, Aq_correct, Zq_correct    # noqa: E402
from mainterm import zeta_q, Xqe                          # noqa: E402  (zeta_q/Xqe are correct; Aprod is NOT used)

def eval_shift(G, logtab, a, b, s, t):
    """R_q (exact primitive sum) and corrected M_q."""
    R = compute_E(G, a, b, s, t, logtab=logtab)
    M, _ = M_correct(G, a, b, s, t)
    return R, M

def gen_shifts(n, T=2.0, seed=0, min_ab=0.5, config='hyp11', eta=0.1):
    """config='hyp11': Re a=Re b=1/2, Re s=Re t=1/2+eta (Hyp 1.1).
       config='shifted': all four Re=1/2+eta (RAT(c) configuration).
       |Im a + Im b| > min_ab (avoid a+b near the pole at 1)."""
    rng = np.random.default_rng(seed)
    out = []
    while len(out) < n:
        A, B, S, U = rng.uniform(-T, T, 4)
        if abs(A + B) < min_ab:
            continue
        if config == 'hyp11':
            out.append((A, B, S, U))
        else:
            out.append((A, B, S, U))
    return out

def make_ab(sh, config, eta):
    A, B, S, U = sh
    if config == 'hyp11':
        a = complex(0.5, A); b = complex(0.5, B)
    else:
        a = complex(0.5 + eta, A); b = complex(0.5 + eta, B)
    s = complex(0.5 + eta, S); t = complex(0.5 + eta, U)
    return a, b, s, t

def run_q(q, shifts, config, eta, Kmax=None):
    """Return arrays: complex residuals R-M, |R|, |M| for each shift."""
    G = Group(q)
    if G.empty:
        return None
    if Kmax is None:
        ims = [max(abs(sh[0]), abs(sh[1]), abs(sh[2]), abs(sh[3])) for sh in shifts]
        Kmax = max(8, int(max(ims) + 3))
    logtab = make_logtab(G.x, Kmax)
    ds = []
    Es = []
    Ms = []
    for sh in shifts:
        a, b, s, t = make_ab(sh, config, eta)
        R, M = eval_shift(G, logtab, a, b, s, t)
        ds.append(R - M); Es.append(R); Ms.append(M)
    return dict(q=q, phi=G.phi, phist=G.phist, n=len(shifts), d=np.array(ds), E=np.array(Es), M=np.array(Ms))

def stats(res):
    d = np.abs(res['d']); E = np.abs(res['E']); M = np.abs(res['M'])
    return dict(q=res['q'], phist=res['phist'], n=res['n'],
                rms=float(np.sqrt(np.mean(d**2))), med=float(np.median(d)), mx=float(d.max()),
                E_rms=float(np.sqrt(np.mean(E**2))), M_rms=float(np.sqrt(np.mean(M**2))),
                rel_rms=float(np.sqrt(np.mean((d/np.maximum(M,1e-300))**2))),
                mean_abs=float(abs(np.mean(res['d']))),
                rms_over_sqrtq=float(np.sqrt(np.mean(d**2))/res['q']**0.5))
