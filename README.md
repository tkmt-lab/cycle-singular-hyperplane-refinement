# A quantifier refinement for singular hyperplanes in directed-cycle compartmental models

Version 1.0.0 — 2026-11-17. DOI: —. [Code repository](https://github.com/tkmt-lab/cycle-singular-hyperplane-refinement).

For generically locally identifiable directed-cycle compartmental models, this note proves the hyperplane inclusion in Conjecture 4.6 of Ahmed et al. (arXiv:2412.05283v3) when the leak index is strictly before the output, for all n>=3 and the entire real hyperplane.
A positive three-compartment example at the output endpoint has full column rank and gives a counterexample to the universal endpoint inclusion.
Together, these results specify the leak-position condition for using this inclusion in identifiability analysis.

## Quick start

With Python 3, run:

```sh
python3 -B checks/endpoint.py
```

For n=3, p=2, L={2} and rates (2,1,3,1), expect `"rank_over_Q": 4`, `"passed": true` and maximal minors including -12. See [Reproduce](#reproduce) for all checks and dependencies.

## The inclusion

The cycle has input at vertex 1 and output at vertex p. Under the source article's generic local identifiability assumptions, take a non-leak index a in [p-1] minus L and a leak index ell in L intersect [p-1]. The hyperplane r_a=r_ell+lambda_ell is contained in the coefficient-Jacobian rank-defect set. The proof covers zero and negative rates as well as positive rates. It differentiates with respect to all independent edge and leak rates before restricting to the hyperplane, and uses a separate equal-column argument where the displayed kernel vector vanishes.

Read [the paper](paper.pdf), [TeX source](paper.tex), [claims](claims.json) and [verification record](VERIFICATION-RECORD.md) for the proof, exact finite checks and their scope.

## Reproduce

Use Python 3 with SymPy 1.14.0 already installed. The runner uses this environment offline.

```sh
python3 -B reproduce.py
python3 -B check_packet.py
python3 -B publication_privacy.py
```

Three check programs run serially in disposable build/ directories, each with 60-second CPU and wall limits. Mathematical outputs are compared exactly with frozen baselines, after omitting timing, RSS and Python-version measurements. Output is results/reproduction.json. Keep Python assertions enabled. CI installs requirements.txt before running the checks.

Rebuild the supplied PDF with pdfLaTeX (TeX Live with lmodern and AMS packages):

```sh
mkdir -p build/pdf
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build/pdf paper.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build/pdf paper.tex
```

## 日本語：円環の区画模型における特異超平面の量化の精密化

版 1.0.0 — 公開日 2026-11-17。DOI: —。[コードの repo](https://github.com/tkmt-lab/cycle-singular-hyperplane-refinement)。

一般的局所識別可能性など原著の仮定を満たす有向円環の区画模型で、Ahmed らの予想4.6の超平面包含を、漏出位置が出力位置より前の ell<p の場合に全 n>=3 で証明します。
零・負の率を含む実超平面全体が対象で、出力と同じ位置 ell=p には正の反例があります。
識別可能性を調べる際に、この包含が成り立つ漏出位置の条件を明確にします。

最初の実行例（Python 3）：

```sh
python3 -B checks/endpoint.py
```

n=3, p=2, L={2}、率 (2,1,3,1) に対して、階数4、`"passed": true`、最大小行列式の一つが -12 と出ます。

入力は頂点1、出力は頂点pです。a は [p-1] の非漏出位置、ell は同じ区間の漏出位置とし、超平面 r_a=r_ell+lambda_ell が係数 Jacobian の階数欠損集合に含まれることを示します。全独立率で微分した Jacobian を使い、核ベクトルが零になる点は別の二列一致で扱います。一般の包含は散文の証明、付属プログラムは有限例の厳密な検算です。全検査と PDF の生成手順は [Reproduce](#reproduce)、本文は [paper.pdf](paper.pdf) を参照してください。

## Scope / 範囲

The result concerns this hyperplane inclusion. It does not challenge other theorems in the source article, classify the whole singular locus, equate rank loss with pointwise global nonidentifiability, or give finite/noisy-data guarantees. The endpoint counterexample does not assert regularity at every endpoint point.

The comparison is to arXiv:2412.05283v3. The final SIAM full text and the Dai–Shao primary full text remain unread; relevance of the latter to this inclusion has not been established. Prior refinements or corrections have not been excluded, and no claim of priority is made. The claims are supported by ordinary mathematical proofs and exact finite checks. No human peer review or formal certification is claimed. The [verification record](VERIFICATION-RECORD.md) describes the checks and review history.

対象はこの超平面包含です。原著の他の定理への反論、特異集合全体の分類、階数欠損からの点ごとの大域的非識別性、有限・雑音データの推定保証は含みません。端点の反例は、端点の全点で正則だという主張ではありません。

照合対象は arXiv:2412.05283v3 です。刊行版全文と Dai–Shao 本文は未読で、後者の関連性も未評価です。同じ精密化や訂正が未発表とは断定せず、優先権は主張しません。主張は散文の証明と厳密な有限検算に基づきます。人間の査読・形式認証は受けていません。検証の経緯は [verification record](VERIFICATION-RECORD.md) にまとめています。

## Attribution and thanks / 先行研究への謝意

Ahmed et al. formulated the question and give the coefficient map in Lemma 3.10 of [arXiv:2412.05283v3](https://arxiv.org/abs/2412.05283v3), with attribution to Gerberding, Obatake, and Shiu. I am grateful to these authors for the question and coefficient formula on which this work builds.

問いと既知の係数公式は Ahmed ら、および同論文が帰属する Gerberding–Obatake–Shiu の仕事に基づきます。この問いと係数公式を築いた著者の方々に感謝します。

## Author and contact / 著者・連絡先

Tatsuhiko Takimoto（滝本竜彦）, Independent researcher. Research contact / 研究用メール: [research@tatsuhikotakimoto.com](mailto:research@tatsuhikotakimoto.com).

## License

Code and CI: Apache-2.0. Original article, text and generated data: CC BY 4.0. See [LICENSE](LICENSE) and the full license texts. Third-party articles are cited through bibliographic references and links.
