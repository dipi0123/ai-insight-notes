# 용어집

본문에서 쓰는 용어 표기의 정본이다. 한 줄 정의만 두고 자세한 설명은 「본 장」으로 간다. 링크가 없는 장 번호는 아직 실리지 않은 장이다.

- **표기**는 본문에서 쓰는 형태 그대로다. 영문으로 시작하는 표기는 「A–Z」 절에 알파벳순으로, 한글로 시작하는 표기는 「ㄱ–ㅎ」 절에 가나다순으로 둔다.
- **분류**는 그 용어가 어느 갈래의 이름인지 나타낸다: 분야 · 구조 · 과제 · 방식 · 학습신호 · 규모·활용 · 학습과정 · 평가 · 데이터 · 수학 · 시스템.

## A–Z

| 표기 | 원어·풀이 | 분류 | 한 줄 정의 | 본 장 |
|---|---|---|---|---|
| DPO | direct preference optimization | 학습과정 | 보상 모델과 강화 학습 과정 없이 선호 쌍에서 바로 모델을 최적화하는 사후학습 방법 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.5 |
| PEFT | parameter-efficient fine-tuning, 효율적 파인튜닝 | 학습과정 | 원래 가중치는 그대로 두고 작게 덧붙인 가중치만 학습하는 파인튜닝. LoRA가 대표적이다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.4 |
| RLHF | reinforcement learning from human feedback | 학습과정 | 사람의 선호 비교로 보상 모델을 학습하고, 그 점수를 보상으로 강화 학습하는 방법 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.4 |
| SFT | supervised fine-tuning, 지도 파인튜닝 | 학습과정 | 「지시 → 좋은 답」 쌍을 따라 하게 하는 지도 학습 방식의 파인튜닝 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.3 |

## ㄱ–ㅎ

| 표기 | 원어·풀이 | 분류 | 한 줄 정의 | 본 장 |
|---|---|---|---|---|
| 강화 학습 | reinforcement learning, RL | 학습신호 | 정답 대신 행동의 결과에 대한 보상을 받아, 보상이 커지도록 행동 방식을 고치는 학습 틀 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.1 |
| 비지도 학습 | unsupervised learning | 학습신호 | 정답 없이 데이터 안의 묶음이나 분포를 찾는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.3 |
| 사전학습 | pre-training | 학습과정 | 큰 데이터로 넓고 일반적인 표현을 먼저 배우는 단계 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 8.1 |
| 사후학습 | post-training | 학습과정 | 사전학습 뒤 모델을 다듬는 학습을 통틀어 부르는 업계 관례 용어. SFT·선호 최적화·강화 학습을 포함한다 | [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| 선호 학습 | preference learning | 학습신호 | 두 결과 중 어느 쪽이 나은지 비교한 데이터로 배우는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.4 |
| 자기지도 학습 | self-supervised learning | 학습신호 | 데이터의 일부를 가리고 맞히게 해서 데이터 스스로 정답을 만드는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.3 |
| 준지도 학습 | semi-supervised learning | 학습신호 | 라벨이 있는 일부 데이터와 라벨이 없는 데이터를 함께 쓰는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.10 |
| 증류 | knowledge distillation, 지식 증류 | 학습과정 | 큰 모델(교사)의 출력을 작은 모델(학생)이 따라 하게 해서 배우는 방법 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.6 |
| 지도 학습 | supervised learning | 학습신호 | 입력마다 붙은 정답(라벨)과 비교하며 배우는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.3 |
| 추가 사전학습 | continual pre-training | 학습과정 | 사전학습한 모델을 특정 분야 데이터로 사전학습과 같은 방식으로 더 학습하는 것 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 8.5 |
| 파인튜닝 | fine-tuning | 학습과정 | 사전학습한 모델을 특정 과제나 형식에 맞춰 더 학습하는 것. 이 책은 라벨 데이터로 하는 지도 추가 학습이라는 좁은 뜻으로 쓴다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.1 |
