import numpy as np

UL = 0
U = 1
L = 2

match_score = 1
mismatch_score = -1
gap_penalty = -1

def s(a, b):
    if(a == b):
        return match_score
    else:
        return mismatch_score

seq1 = "TGCTACAACTTCCGAGTCC"
seq2 = "CTTTGGTACAATACATACGTGATCCAG"

n = len(seq1)
m = len(seq2)

M = np.zeros(shape=(n+1, m+1, 2), dtype=np.int8)
arg_max = (0,0)
max_val = 0

for i in range(1, n+1):
    for j in range(1, m+1):
        ul = M[i-1][j-1][0] + s(seq1[i-1], seq2[j-1])
        l = M[i-1][j][0] + gap_penalty
        u = M[i][j-1][0] + gap_penalty
        
        M[i][j][0] = max(ul, u, l)
        M[i][j][1] = np.argmax([ul, u, l])
        if(M[i][j][0] > max_val):
            max_val = M[i][j][0]
            arg_max = (i,j)

#backtracking:
i, j = arg_max
end_i, end_j = arg_max

match_seq1 = ""
match_seq2 = ""

while(M[i][j][0] > 0):
    back_tracker = M[i][j][1]
    if(back_tracker == UL):
        i -= 1
        j -= 1
        match_seq1 = seq1[i] + match_seq1
        match_seq2 = seq2[j] + match_seq2
    elif(back_tracker == U):
        j -= 1
        match_seq1 = "-" + match_seq1
        match_seq2 = seq2[j] + match_seq2
    elif(back_tracker == L):
        i -= 1
        match_seq1 = seq1[j] + match_seq1
        match_seq2 = "-" + match_seq2

print(match_seq1)
print(match_seq2)
    