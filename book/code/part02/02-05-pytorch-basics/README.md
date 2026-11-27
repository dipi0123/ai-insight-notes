# 2.5 PyTorch로 계산하기: 예제 코드

[2.5장](../../../part02-math-and-tools/02-05-pytorch-basics.md) §5의 시간 재기 스크립트다.

| 파일 | 하는 일 |
|---|---|
| `matmul_timing.py` | n × n matrix multiplication의 시간을 CPU와 accelerator(MPS·CUDA 등)에서 잰다. warm-up 뒤 장치마다 동기화하고, 여러 번 잰 값의 중앙값을 낸다 |

저장소 맨 위에서 실행한다.

```bash
book/code/.venv/bin/python book/code/part02/02-05-pytorch-basics/matmul_timing.py
book/code/.venv/bin/python book/code/part02/02-05-pytorch-basics/matmul_timing.py --cpu-only
```

accelerator가 없으면 CPU 열만 출력한다. `--cpu-only`는 accelerator가 있어도 CPU만 잰다. 시간은 기계와 실행할 때의 부하에 따라 다르다.
