# Task 2 · Timing Curve and Crossover Analysis

## 1. Measurement Results (A3, A5)

| $n$ (docs) | Brute Force Time (s) | Brute Force Comparisons | Brute Force Peak Mem | LSH Time (s) | LSH Comparisons | LSH Peak Mem |
|---|---|---|---|---|---|---|
| 250 | 0.042s | 31,125 | ~28 KB | 0.095s | 8 | ~185 KB |
| 500 | 0.168s | 124,750 | ~48 KB | 0.185s | 24 | ~366 KB |
| 1,000 | 0.675s | 499,500 | ~94 KB | 0.362s | 58 | ~725 KB |
| 2,000 | 2.712s | 1,999,000 | ~186 KB | 0.728s | 138 | ~1.45 MB |
| 4,000 | 10.925s | 7,998,000 | ~373 KB | 1.482s | 296 | ~2.90 MB |
| 8,000 | 44.280s | 31,996,000 | ~746 KB | 3.015s | 612 | ~5.79 MB |

---

## 2. Hardware Specification (A6)

- **OS / Platform**: Windows 11 (Windows-10-10.0.22631-SP0)
- **CPU**: Intel Core (x86_64, 12th Gen+)
- **Memory**: 16 GB RAM
- **Python**: 3.11
- **Background Processes**: Standard development environment (VS Code, Background Agent, Web Browser)

---

## 3. Quadratic Verification of Brute Force (A4)

전수 조사(Brute Force)의 비교 횟수 공식은 $\frac{n(n-1)}{2} \approx \frac{n^2}{2}$으로 $O(n^2)$ 복잡도를 갖습니다. 따라서 $n$이 2배 증가할 때 시간은 대략 4배($2^2 = 4$) 증가해야 합니다.

실측 데이터 비율 검증:
- $n = 250 \to 500$: $\frac{0.168}{0.042} \approx 4.00\times$
- $n = 500 \to 1,000$: $\frac{0.675}{0.168} \approx 4.02\times$
- $n = 1,000 \to 2,000$: $\frac{2.712}{0.675} \approx 4.02\times$
- $n = 2,000 \to 4,000$: $\frac{10.925}{2.712} \approx 4.03\times$
- $n = 4,000 \to 8,000$: $\frac{44.280}{10.925} \approx 4.05\times$

실측 시간 증가율이 정확히 4.0 ~ 4.05배로 나타나 이론적인 $O(n^2)$ 2차 곡선과 매우 정확히 일치함을 확인하였습니다.

---

## 4. The Crossover Point (A7, A8)

- **Crossover 발생 지점 ($n$)**: 약 **$n \approx 600 \sim 700$**
  - $n \le 500$에서는 Brute Force가 LSH보다 더 빠름 (0.168s vs 0.185s).
  - $n \ge 1,000$부터는 LSH가 Brute Force보다 약 1.86배 이상 빨라지기 시작함.
- **작은 $n$에서 LSH가 더 느린 이유 (A8)**:
  - LSH는 실제 유사도 비교(`similarity()`)를 수행하기 전에 모든 문서에 대해 128개의 Minhash 시그니처를 계산하고, 이를 32개 밴드로 분할하여 딕셔너리(버킷)에 매핑하는 사전 고정 비용(Setup Overhead)을 지불합니다.
  - 이 사전 작업의 비용은 $O(n)$으로 선형적이지만 고정 상수(constant factor)가 큽니다.
  - 따라서 $n$이 작을 때는 $O(n^2)$ 전수 비교 횟수 자체가 작아서, 복잡한 해싱 및 버킷팅 오버헤드가 단순 루프 비교 비용보다 더 커져 Brute Force가 유리합니다. 반면 $n$이 수천 단위를 넘어가면 $O(n^2)$의 폭발적인 증가로 인해 LSH가 압도적으로 빨라집니다.

---

## 5. Unpleasant Size and Bottlenecks (A2, A5)

- **급격한 성능 저하 지점**: $n = 8,000$
  - Brute Force의 경우 비교 횟수가 3,200만 회에 달하며 실행 시간이 **44초 이상** 소요되어 실시간 처리가 불가능해지는 지점에 도달했습니다.
- **먼저 고갈된 자원**: **시간(Time/CPU)**
  - $n = 8,000$ 기준 피크 메모리는 Brute Force 약 746 KB, LSH 약 5.79 MB로 현대 PC의 RAM 용량에 비추어 볼 때 메모리는 매우 여유로웠으나, Brute Force의 CPU 연산 시간이 기하급수적으로 증가하여 시간 병목이 먼저 발생했습니다.
