"""Encurta pausas da narração para caber em 15 s. uso: python3 -I tighten.py entrada.wav saida.wav 0.5"""
import sys, numpy as np, subprocess
src, dst, maxgap = sys.argv[1], sys.argv[2], float(sys.argv[3])
raw = subprocess.run(['ffmpeg','-v','error','-i',src,'-f','s16le','-ac','1','-ar','24000','-'],capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32)
sr = 24000; win = int(0.02*sr)
e = np.sqrt(np.convolve(x**2, np.ones(win)/win, 'same'))
quiet = e < 10**(-38/20)*32768
out=[]; i=0; n=len(x)
# corta silêncio inicial/final e limita pausas
while i<n:
    j=i
    if quiet[i]:
        while j<n and quiet[j]: j+=1
        g=j-i
        keep = 0 if (i==0 or j==n) else min(g, int(maxgap*sr))
        out.append(x[i:i+keep//2]); out.append(x[j-(keep-keep//2):j])
    else:
        while j<n and not quiet[j]: j+=1
        out.append(x[i:j])
    i=j
y=np.concatenate(out).astype(np.int16)
subprocess.run(['ffmpeg','-v','error','-y','-f','s16le','-ar','24000','-ac','1','-i','-',dst],input=y.tobytes(),check=True)
