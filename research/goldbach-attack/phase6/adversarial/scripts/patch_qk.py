p='qk.py'; s=open(p).read()
old="""            evals,evecs=np.linalg.eigh(C)
            jj=np.argmax(np.abs(evals)); h=evecs[:,jj]
            # boundary test function v = sum h_j phi_j ; chi-content a_chi = <f_chi,v>
            # with F_chi = A*G[:,chi] (nodes), P_comp=(2/phi) sum F_chi F_chi^H => a=F^H h
            F=A[:,None]*G
            a=F.conj().T@h
            ab2=np.abs(a)**2
            tot=ab2.sum()
            w=ab2/tot if tot>0 else ab2
            neff=float(1.0/np.sum(w**2)) if tot>0 else 0.0
            # participation ratio alternative
            npart=float((w.sum()**2)/np.sum(w**2)) if tot>0 else 0.0
            order=np.argsort(-ab2)
            top10=ab2[order[:10]]
            fn=np.abs(G)**2  # per-char norms squared at nodes
            nrm=fn.sum(axis=0)
            # correlation between |a| and ||f||
            corr=float(np.corrcoef(ab2, nrm)[0,1]) if tot>0 else 0.0
            out.update(chi=dict(tot_ab2=float(tot), n_eff=neff, top10_share=float(top10.sum()/tot) if tot>0 else 0.0,
                                top10_abs=[float(x) for x in np.sqrt(top10)],
                                max_abs=float(np.abs(a).max()), med_abs=float(np.median(np.abs(a))),
                                mean_abs=float(np.mean(np.abs(a))),
                                corr_absa2_fn2=corr,
                                q90_abs=float(np.quantile(np.abs(a),0.9)),
                                q99_abs=float(np.quantile(np.abs(a),0.99)),
                                q999_abs=float(np.quantile(np.abs(a),0.999))))"""
new="""            evals,evecs=np.linalg.eigh(C)
            jj=np.argmax(np.abs(evals)); h=evecs[:,jj]
            evq,evecq=np.linalg.eigh(CQ); jq=np.argmax(np.abs(evq)); qhat=evecq[:,jq]
            overlap=float(abs(np.vdot(qhat,h)))
            F=A[:,None]*G
            a=F.conj().T@h
            b=F.conj().T@qhat
            ab2=np.abs(a)**2
            tot=ab2.sum()
            w=ab2/tot if tot>0 else ab2
            neff=float(1.0/np.sum(w**2)) if tot>0 else 0.0
            order=np.argsort(-ab2)
            top10=ab2[order[:10]]
            fn=np.abs(G)**2
            nrm=fn.sum(axis=0)
            corr=float(np.corrcoef(ab2, nrm)[0,1]) if tot>0 else 0.0
            bb=np.abs(b); sig_std=float(np.std(bb)); sig_mean=float(np.mean(bb)); sig_rms=float(np.sqrt(np.mean(bb**2)))
            n_odd=int(cg.nodd)
            lam_pred=float(sig_std/np.sqrt(n_odd))
            Ph=float(np.real(np.vdot(h,(2.0/cg.phi)*(F@a))))
            Qh=float(np.real(np.vdot(h,CQ@h)))
            out.update(chi=dict(tot_ab2=float(tot), n_eff=neff, top10_share=float(top10.sum()/tot) if tot>0 else 0.0,
                                top10_abs=[float(x) for x in np.sqrt(top10)],
                                max_abs=float(np.abs(a).max()), med_abs=float(np.median(np.abs(a))),
                                mean_abs=float(np.mean(np.abs(a))), corr_absa2_fn2=corr,
                                q90_abs=float(np.quantile(np.abs(a),0.9)),
                                q99_abs=float(np.quantile(np.abs(a),0.99)),
                                q999_abs=float(np.quantile(np.abs(a),0.999))),
                       align=dict(overlap=overlap, lam_q=float(np.abs(evq).max()),
                                  b_std=sig_std, b_mean=sig_mean, b_rms=sig_rms,
                                  lam_pred_std_over_sqrtn=lam_pred,
                                  z_equiv=float(np.abs(lam)/lam_pred) if lam_pred>0 else None,
                                  Pn_rayleigh=Ph, Qn_rayleigh=Qh))"""
assert old in s, 'old block not found'
s=s.replace(old,new)
open(p,'w').write(s)
print('patched alignment OK')
