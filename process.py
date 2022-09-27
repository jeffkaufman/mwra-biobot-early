import statsmodels.api as sm
import math

n_endog = []
n_exog = []

s_endog = []
s_exog = []

ns_endog = []
ns_exog = []

with open("biobot.tsv") as inf:
    for i, line in enumerate(inf):
        date, n, s = line.split('\t')
        if n.strip():
            n_exog.append([i])
            n_endog.append(int(n))
            ns_exog.append([i])
            ns_endog.append(int(n))
        if s.strip():
            s_exog.append([i])
            s_endog.append(int(s))
            ns_exog.append([i])
            ns_endog.append(int(s))

def to_pct(log_space):
    return math.exp(log_space) - 1
            
for name, endog, exog in [["north", n_endog, n_exog],
                          ["south", s_endog, s_exog],
                          ["both", ns_endog, ns_exog]]:
    model = sm.GLM(endog, sm.add_constant(exog),
                   family=sm.families.Tweedie())
    result = model.fit()
    pvalue = result.pvalues[1]
    y_intercept = result.params[0]
    coef = result.params[1]
    ci_025, ci_975 = result.conf_int()[1]

    print("%s: %.1f%% [%.1f%%, %.1f%%] p=%.2e, y_intercept=%.2f" % (
        name,
        100 * to_pct(coef),
        100 * to_pct(ci_025),
        100 * to_pct(ci_975),
        pvalue,
        y_intercept))
