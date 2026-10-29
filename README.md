# A quantifier refinement for singular hyperplanes in directed-cycle compartmental models

Version 1.0.0, local release candidate. The unchanged manuscript retains its revision identifier draft-2026-10-30-r1; 1.0.0 identifies this public package. Read [the paper](paper.pdf), [TeX source](paper.tex), [claims](claims.json) and [verification record](VERIFICATION-RECORD.md).

This note refines the quantifiers of Conjecture 4.6 in Ahmed et al., arXiv:2412.05283v3, and proves the resulting inclusion. For a directed cycle with input 1 and output p, the proposed hyperplane is contained in the coefficient-Jacobian rank-defect set when the leak index ell is strictly before p. The proof works for all cycle sizes n>=3 and the entire real hyperplane, including zero and negative rates. It differentiates with respect to all independent edge and leak rates before restricting to the hyperplane.

A positive three-compartment endpoint example ell=p has full column rank. Failure of that proposed inclusion does not challenge other theorems in the source article or classify the whole singular locus. Rank loss is not here equated with pointwise global nonidentifiability. There is no finite/noisy-data guarantee.

## Reproduce

Python 3 with SymPy 1.14.0 is required. A matching environment must already be installed for an offline run. The runner does not install dependencies or access the network.

```sh
python3 -B reproduce.py
python3 -B check_packet.py
python3 -B publication_privacy.py
```

Three unchanged programs run serially in disposable build/ directories, each with 60-second CPU and wall limits. Mathematical outputs are compared exactly with frozen baselines; timing, RSS and Python-version measurements are excluded. Output is results/reproduction.json. Assertions must remain enabled. The interpreter and SymPy are not bundled. CI installs requirements.txt before running the checks. Tests were run locally with the existing SymPy 1.14.0 environment.

The supplied PDF is unchanged. With Tectonic and its resources already cached:

```sh
mkdir -p build/pdf
tectonic --only-cached --untrusted --outdir build/pdf paper.tex
```

## Attribution and limits

Ahmed et al. formulated the question and give the coefficient map in Lemma 3.10 of [arXiv:2412.05283v3](https://arxiv.org/abs/2412.05283v3), with attribution to Gerberding, Obatake, and Shiu. This note relies on that known formula and credits their framework.

The comparison is to the specified arXiv version. The final SIAM full text and the Dai–Shao primary full text remain unread; relevance of the latter to this inclusion has not been established. Prior refinements or corrections have not been excluded. This is a quantifier refinement and proof, not a claim of priority or absence of prior publication. The manuscript received an AI review with two MINOR comments applied; the revision was not independently rereviewed. No human peer review or formal certification is claimed.

## 日本語

有向円環の線形区画モデルに関する原著予想4.6の「量化の精密化と証明」です。漏出位置を出力位置pより手前のell<pに限ると、提案された超平面が係数Jacobianの階数欠損集合に含まれることを、全nと零・負の率も含む実超平面全体で示します。ell=pには正の反例があります。

問いと既知の係数公式はAhmedほか、および同論文が帰属するGerberding–Obatake–Shiuに基づきます。刊行版全文・Dai–Shao本文は未読で、同じ精密化や訂正が未発表とは断定しません。特異集合全体の分類、点ごとの大域的非識別性、有限・雑音データの推定は扱いません。一般証明と有限検算を区別します。

## License

Code and CI: Apache-2.0. Original article, text and generated data: CC BY 4.0. See LICENSE and full texts. Cited third-party articles are not redistributed.
