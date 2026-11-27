"""CPU와 accelerator(MPS·CUDA 등)에서 matrix multiplication 시간을 잰다.

실행: book/code/.venv/bin/python book/code/part02/02-05-pytorch-basics/matmul_timing.py
accelerator가 있어도 CPU만 재려면 --cpu-only를 붙인다.
"""
import argparse
import platform
import statistics
import subprocess
import time

import torch

SIZES = [64, 256, 1024, 4096]   # n × n matrix 두 개를 곱한다
REPS = {64: 50, 256: 50, 1024: 20, 4096: 10}
WARMUP = 20


def pick_accelerator(cpu_only):
    """쓸 수 있는 accelerator의 device. 없거나 --cpu-only면 None."""
    if cpu_only or not torch.accelerator.is_available():
        return None
    return torch.accelerator.current_accelerator()


def sync(device):
    """CPU가 아니면 그 장치에 넣은 계산이 다 끝날 때까지 기다린다."""
    if device.type != "cpu":
        torch.accelerator.synchronize()


def median_ms(A, B, device, reps):
    for _ in range(WARMUP):            # 먼저 몇 번 돌린 뒤에 잰다
        A @ B
    sync(device)
    times = []
    for _ in range(reps):
        t0 = time.perf_counter()
        A @ B
        sync(device)                   # 계산이 끝난 뒤에 시계를 멈춘다
        times.append(time.perf_counter() - t0)
    return statistics.median(times) * 1000


def measure(n, device):
    g = torch.Generator().manual_seed(0)
    A = torch.randn(n, n, generator=g).to(device)
    B = torch.randn(n, n, generator=g).to(device)
    return median_ms(A, B, device, REPS[n])


def hardware_name():
    if platform.system() == "Darwin":
        r = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                           capture_output=True, text=True)
        if r.returncode == 0:
            return r.stdout.strip()
    return platform.processor() or platform.machine()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpu-only", action="store_true")
    args = parser.parse_args()
    acc = pick_accelerator(args.cpu_only)
    cpu = torch.device("cpu")
    print(f"하드웨어 {hardware_name()}, Python {platform.python_version()}, "
          f"torch {torch.__version__}, CPU thread {torch.get_num_threads()}")
    print(f"dtype float32, warm-up {WARMUP}번, 반복 {REPS}, 값은 반복의 중앙값(ms)")
    if acc is None:
        print("accelerator를 쓰지 않는다(없거나 --cpu-only): CPU만 잰다")
        for n in SIZES:
            print(f"n={n:5d}  cpu {measure(n, cpu):9.3f}")
        return
    for n in SIZES:
        c, a = measure(n, cpu), measure(n, acc)
        print(f"n={n:5d}  cpu {c:9.3f}  {acc.type} {a:9.3f}  cpu/{acc.type} {c / a:6.2f}")


if __name__ == "__main__":
    main()
