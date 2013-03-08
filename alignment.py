def global_alignment(x_seq, y_seq, match, mismatch, gap):
    m = len(x_seq)
    n = len(y_seq)

    dp = [None] * (m + 1)
    trace = [None] * (m + 1)
    dp[0] = [x * gap for x in range(0, n + 1)]
    trace[0] = ["left"] * (n + 1)

    for i in range(1, m + 1):
        dp[i] = [None] * (n + 1)
        trace[i] = [None] * (n + 1)

        dp[i][0] = i * gap
        trace[i][0] = "up"

    dp[0][0] = 0
    trace[0][0] = "diag"

    for i in range(1, (m + 1)):
        for j in range(1, (n + 1)):
            if x_seq[i - 1] == y_seq[j - 1]:
                match_score = match
            else:
                match_score = mismatch

            al = dp[i - 1][j - 1] + match_score
            ix = dp[i][j - 1] + gap
            iy = dp[i - 1][j] + gap

            dp[i][j] = max(al, max(ix, iy))

            if al >= ix and al >= iy:
                dp[i][j] = al
                trace[i][j] = "diag"
            elif ix >= al and ix >= iy:
                dp[i][j] = ix
                trace[i][j] = "left"
            else:
                dp[i][j] = iy
                trace[i][j] = "up"

    i = m
    j = n

    aln_x = ""
    aln_y = ""

    while i > 0 or j > 0:
        t = trace[i][j]

        if t == "diag":
            aln_x += x_seq[i - 1]
            aln_y += y_seq[j - 1]

            j -= 1
            i -= 1
        elif t == "left":
            aln_x += "-"
            aln_y += y_seq[j - 1]

            j -= 1
        elif t == "up":
            aln_x += x_seq[i - 1]
            aln_y += "-"

            i -= 1

    return (aln_x[::-1], aln_y[::-1], dp[m][n])
