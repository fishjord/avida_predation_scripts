#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

struct Alignment {
  char* aln_i;
  char* aln_j;
  int score;
};

#define DIAG 0
#define UP 1
#define LEFT 2

typedef unsigned char byte;

void global_alignment(const char* seqi, const char* seqj, int match, int mismatch, int gap, Alignment* out) {
  int m = strlen(seqi);
  int n = strlen(seqj);
  short al, ii, ij;

  short** dp = new short*[m+1];
  byte** trace = new byte*[m+1];

  for(int index = 0;index < m + 1;index++) {
    dp[index] = new short[n + 1];
    trace[index] = new byte[n + 1];

    dp[index][0] = index * gap;
    trace[index][0] = UP;
  }

  for(int index = 0;index < n + 1;index++) {    
    dp[0][index] = (short)index * gap;
    trace[0][index] = LEFT;
  }

  dp[0][0] = 0;
  trace[0][0] = DIAG;

  for(int i = 1;i < m + 1;i++) {
    for(int j = 1;j < n + 1;j++) {
      if(seqi[i - 1] == seqj[j - 1]) {
	al = dp[i - 1][j - 1] + match;
      } else {
	al = dp[i - 1][j - 1] + mismatch;
      }

      ii = dp[i][j - 1] + gap;
      ij = dp[i - 1][j] + gap;

      if(al >= ii && al >= ij) {
	dp[i][j] = al;
	trace[i][j] = DIAG;
      } else if(ii >= al && ii >= ij) {
	dp[i][j] = ii;
	trace[i][j] = LEFT;
      } else {
	dp[i][j] = ij;
	trace[i][j] = UP;
      }
    }
  }

  char* aln_i = (char*)malloc(m + n + 1);
  char* aln_j = (char*)malloc(m + n + 1);

  memset(aln_i, '\0', m + n + 1);
  memset(aln_j, '\0', m + n + 1);
  int length = 0;

  int i = m, j = n, t;
  while(i > 0 || j > 0) {
    t = trace[i][j];
    if(t == DIAG) {
      aln_i[length] = seqi[i - 1];
      aln_j[length] = seqj[j - 1];
      i--;
      j--;
    } else if(t == LEFT) {
      aln_i[length] = '-';
      aln_j[length] = seqj[j - 1];
      j--;
    } else if(t == UP) {
      aln_i[length] = seqi[i - 1];
      aln_j[length] = '-';
      i--;
    } else {
      assert(false);
    }

    length++;
  }

  char swap;
  for(int index = 0;index < length / 2;index++) {
    swap = aln_i[index];
    aln_i[index] = aln_i[length - index - 1];
    aln_i[length - index - 1] = swap;

    swap = aln_j[index];
    aln_j[index] = aln_j[length - index - 1];
    aln_j[length - index - 1] = swap;
  }

  out->aln_i = aln_i;
  out->aln_j = aln_j;
  out->score = dp[m][n];

  for(int index = 0;index < m + 1;index++) {
    delete dp[index];
    delete trace[index];
  }

  delete dp;
  delete trace;
}

static PyObject* py_alignment(PyObject *self, PyObject *args) {
  const char* seqi;
  const char* seqj;
  int match, mismatch, gap;

  if(!PyArg_ParseTuple(args, "ssiii", &seqi, &seqj, &match, &mismatch, &gap)) {
    return NULL;
  }

  Alignment aln;
  global_alignment(seqi, seqj, match, mismatch, gap, &aln);
  return Py_BuildValue("ssi", aln.aln_i, aln.aln_j, aln.score);
}

static PyMethodDef alignmentMethods[] = {
  {"global_alignment", py_alignment, METH_VARARGS, "Align two strings"},
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initalignment(void)
{
  (void) Py_InitModule("alignment", alignmentMethods);
}

int main(void) {
  const char* seqi = "ABC";
  const char* seqj = "AABBCC";
  Alignment align;

  global_alignment(seqi, seqj, 0, -1, -1, &align);

  printf("Alni: %s\nAlnj: %s\nscore: %d\n", align.aln_i, align.aln_j, align.score);
}
