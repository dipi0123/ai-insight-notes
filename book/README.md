# AI Insight Notes

**AI 모델, 입문에서 전문가까지**

이 책은 소프트웨어 개발은 해 봤지만 AI는 처음인 개발자를 위한 책이다. 이 책을 끝까지 공부하면 AI 전체를 이해하고, 경량 language model(언어 모델)이나 computer vision(CV, 컴퓨터 비전) 모델을 직접 설계해서 만들 수 있게 된다. 프로그래밍 기초는 안다고 보고, 수학과 AI 개념은 처음부터 설명한다. 각 장은 앞 장에서 배운 것만 전제로 한다.

## 이 책의 흐름

| 단계 | 배우는 것 | 부 |
|---|---|---|
| 1. 용어와 기술 지도 | AI 기초 용어, 모델 이름의 갈래, 학습 방법의 갈래, 산업 기술의 층위 | 1부 |
| 2. 구조와 동작 | 필요한 수학, machine learning(머신러닝)의 틀과 평가, neural network(신경망) 학습, CNN·Transformer 같은 기본 블록, computer vision 모델과 language model, 그리고 각 모델의 평가 | 2~7부 |
| 3. 학습 방법 | pre-training(사전학습), fine-tuning(파인튜닝)·SFT, reward(보상)와 preference(선호)로 배우는 reinforcement learning(강화 학습)·RLHF·DPO, 그리고 이 방법들로 만든 multimodal(멀티모달)·generative model(생성 모델) — 모델 구조가 어떠하기에 이 방법들이 가능하고 필요한지 | 8~11부 |
| 4. 성능 고도화 | benchmark(벤치마크)·실험·데이터·규모·test-time compute(추론 시점 계산)로 성능을 올리고, 가볍게 만들어 배포하기 | 12~13부 |
| 5. 설계와 구축 | 경량 language model과 CV 모델을 처음부터 끝까지 직접 설계하고 만들기 | 14부 |

15부는 그다음 걸음으로, 논문을 읽고 재현하고 판단하는 법과 학습된 모델의 내부를 들여다보는 법을 다룬다. 3부부터는 단계마다 「직접 만들기」 장이 있어 배운 것을 코드로 돌려 본다. 코드는 [예제 코드](code/README.md)에 있다.

## 읽는 법

각 장 머리에 수준과 선수 장이 있다. 선수 장을 먼저 읽는다.

기술 용어는 영어 원어로 쓰고, 장마다 처음 나올 때 한국어 번역어를 괄호에 단다. 예: precision(정밀도). 논문·공식 문서·코드에서 만나는 이름을 그대로 익히기 위해서다. 뜻이 기억나지 않는 용어는 [용어집](appendix/glossary.md)에서 찾는다.

| 수준 | 이 수준의 장을 읽고 나면 할 수 있는 것 |
|---|---|
| L1 입문 | 용어를 구분하고 큰 그림을 말로 설명한다 |
| L2 기초 | 필요한 수학을 작은 숫자 예시와 짧은 코드로 따라 계산한다 |
| L3 중급 | 모델의 구성 요소와 training loop(학습 루프)를 PyTorch로 직접 구현한다 |
| L4 고급 | 논문의 설계를 읽고 이해해 작은 모델을 직접 설계하고 학습한다 |
| L5 전문가 | 문제에 맞는 모델·학습·평가·배포 전체를 설계하고 그 선택을 판단한다 |

본문의 강조 상자는 네 가지다.

| 상자 | 뜻 |
|---|---|
| **핵심** | 꼭 기억할 한 가지 |
| **주의** | 자주 하는 오해와 실수 |
| **표준과 관례** | 공식 정의, 널리 쓰는 관례값, 특정 논문·도구가 정한 것의 구분 |
| **현업 사례** | 개념을 실제 작업에 대입한 예 |

장 끝의 확인 문제를 풀고 접힌 답을 펼쳐 맞춰 본다. 제목 끝에 「(심화)」가 붙은 절은 처음 읽을 때 건너뛰어도 된다.

## 학습 경로

| 목표 | 읽는 순서 |
|---|---|
| 처음부터 차근차근(권장) | 1부부터 14부까지 차례로, 그다음 15부 |
| 용어와 기술 지도만 | 1부 |
| 학습 방법의 개념을 빠르게 | 1부 → 3부 → 8부 → 9부 → 10부. 막히는 개념은 그 장의 선수 장으로 돌아간다 |
| 경량 language model 만들기 | 1~5부 → 6.3~6.6 → 7부 → 8.1·8.2·8.4·8.6 → 9.1·9.3·9.4·9.8 → 10.1~10.6 → 12.1~12.3·12.5 → 13.1·13.2 → 14.1~14.3 |
| CV 모델 만들기 | 1~5부 → 6부 → 7.1~7.4 → 8.1·8.3 → 9.1·9.6·9.7 → 12.1~12.5 → 13.1·13.2 → 14.1·14.2·14.4 |
| 논문을 읽고 판단하기 | 12.1·12.2 → 15부. 모르는 개념은 선수 장으로 돌아간다 |

## 목차

링크가 없는 장은 아직 실리지 않은 장이다.

<!-- TOC:START -->
### 1부. 큰 그림 — AI 용어와 기술 지도

- [1.1 AI·machine learning·deep learning](part01-big-picture/01-01-ai-ml-dl.md) · L1
- [1.2 모델 이름을 읽는 여섯 개의 축](part01-big-picture/01-02-naming-axes.md) · L1
- 1.3 모델의 한살이: 데이터에서 서비스까지 · L1
- [1.4 학습 방법 지도: pre-training에서 reinforcement learning까지](part01-big-picture/01-04-training-methods-map.md) · L1
- 1.5 대표 모델 지도 · L1
- 1.6 AI 산업의 기술 층위 · L1

### 2부. 수학과 도구의 최소한

- 2.1 vector·matrix·tensor · L2
- 2.2 derivative와 gradient · L2
- 2.3 probability와 statistics · L2
- 2.4 information theory: entropy와 cross-entropy · L2
- 2.5 PyTorch로 계산하기: tensor·autograd·GPU · L2
- 2.6 개발 환경: GPU·클라우드·Hugging Face · L2

### 3부. machine learning의 기본 틀과 평가

- 3.1 학습이란: 모델·loss·optimization · L2
- 3.2 직접 만들기: NumPy로 linear regression과 gradient descent · L2
- 3.3 학습 신호: supervised·unsupervised·self-supervised·reinforcement learning · L2
- 3.4 데이터 나누기: train·dev·test · L2
- 3.5 overfitting과 generalization · L2
- 3.6 평가 설계의 기본 · L2
- 3.7 confusion matrix·precision·recall·F1 · L2
- 3.8 threshold와 곡선: PR·ROC·AUC · L2
- 3.9 고전 machine learning 모델 · L2
- 3.10 그 밖의 학습 방법: semi-supervised·multi-task·continual·federated·active learning · L2

### 4부. neural network 학습의 기초

- 4.1 batch·step·epoch: training loop의 단위 · L2
- 4.2 neuron과 multilayer perceptron · L3
- 4.3 backpropagation · L3
- 4.4 loss function · L3
- 4.5 optimizer와 learning rate · L3
- 4.6 regularization과 normalization · L3
- 4.7 학습 안정성과 문제 진단 · L3
- 4.8 GPU 메모리와 학습 자원 · L3
- 4.9 learning curve 읽기 · L3
- 4.10 checkpoint와 model selection · L3
- 4.11 직접 만들기: training loop와 숫자 classifier · L3

### 5부. neural network 구조의 기본 블록

- 5.1 convolutional neural network(CNN) · L3
- 5.2 대표 CNN: VGG에서 ResNet까지 · L3
- 5.3 recurrent neural network(RNN)과 sequence · L3
- 5.4 embedding과 token · L3
- 5.5 attention · L3
- 5.6 Transformer block · L3
- 5.7 encoder·decoder·encoder-decoder · L3
- 5.8 직접 만들기: Transformer를 처음부터 · L3
- 5.9 그 밖의 구조: graph neural network와 state space model · L4

### 6부. computer vision 모델과 평가

- 6.1 이미지 데이터: preprocessing과 augmentation · L3
- 6.2 직접 만들기: CNN image classifier · L3
- 6.3 Vision Transformer와 Swin Transformer · L3
- 6.4 backbone·neck·head · L3
- 6.5 object detection I: box·IoU·anchor·NMS · L3
- 6.6 detection 평가: 예측-정답 matching과 AP·mAP · L3
- 6.7 image segmentation · L3
- 6.8 segmentation 평가: mask IoU·mIoU·Dice·PQ · L3
- 6.9 label: 형식·품질·생산 · L3
- 6.10 object detection II: DETR 계열 · L4

### 7부. language model과 평가

- 7.1 tokenization · L3
- 7.2 LLM이 글을 만드는 과정 · L3
- 7.3 decoding: 다음 token을 고르는 방법 · L3
- 7.4 language model의 평가 · L3
- 7.5 현대 LLM의 구조 변형: RMSNorm·RoPE·MoE·long context · L4

### 8부. pre-training

- 8.1 pre-training과 representation learning · L3
- 8.2 언어 pre-training objective: next-token prediction과 masked prediction · L3
- 8.3 시각 self-supervised pre-training: contrastive learning·MAE·DINO · L4
- 8.4 pre-training 데이터: 수집·정제·혼합 · L4
- 8.5 continual pre-training과 domain adaptation · L4
- 8.6 직접 만들기: 작은 GPT pre-training · L4

### 9부. fine-tuning과 adaptation

- 9.1 transfer learning과 fine-tuning · L3
- 9.2 prompt와 in-context learning · L3
- 9.3 supervised fine-tuning(SFT)과 instruction tuning · L4
- 9.4 parameter-efficient fine-tuning: LoRA·adapter·prompt tuning · L4
- 9.5 catastrophic forgetting · L4
- 9.6 distillation과 pseudo-label: 큰 모델에게 배우기 · L4
- 9.7 직접 만들기: pre-trained detection model fine-tuning · L4
- 9.8 직접 만들기: 작은 language model SFT와 LoRA · L4

### 10부. reward와 preference로 배우기: reinforcement learning·RLHF·DPO

- 10.1 reinforcement learning의 기초: agent·environment·reward·policy · L3
- 10.2 value-based와 policy-based 방법 · L4
- 10.3 actor-critic과 PPO · L4
- 10.4 RLHF: 사람의 preference로 배우기 · L4
- 10.5 direct preference optimization: DPO와 그 변형 · L4
- 10.6 직접 만들기: 작은 language model DPO · L4
- 10.7 verifiable reward와 reasoning model · L5
- 10.8 reward hacking과 alignment의 한계 · L5

### 11부. multimodal과 generative model

- 11.1 contrastive learning과 CLIP · L4
- 11.2 vision-language model(VLM) · L4
- 11.3 open-vocabulary detection과 grounding · L4
- 11.4 generative model의 큰 그림: autoencoder·VAE·GAN · L4
- 11.5 diffusion model · L4
- 11.6 generative model의 평가 · L4
- 11.7 음성·영상과 그 밖의 modality · L4

### 12부. 성능 고도화

- 12.1 benchmark와 leaderboard 읽기 · L4
- 12.2 실험 설계와 기록 · L4
- 12.3 hyperparameter search · L4
- 12.4 data-centric 개선: label 품질·augmentation·synthetic data · L4
- 12.5 scaling law · L4
- 12.6 test-time compute: 더 생각하게 하기 · L4
- 12.7 distributed·large-scale training · L5

### 13부. 배포와 응용

- 13.1 model compression: quantization·pruning · L4
- 13.2 inference optimization과 serving · L4
- 13.3 retrieval-augmented generation(RAG) · L4
- 13.4 agent와 tool use · L4
- 13.5 라이선스·데이터 권리·safety · L4
- 13.6 운영: 모니터링·data drift·retraining · L5

### 14부. 설계와 구축

- 14.1 크기와 비용 계산하기 · L4
- 14.2 모델 설계의 순서와 선택 · L5
- 14.3 프로젝트: 경량 language model 설계와 구축 · L5
- 14.4 프로젝트: CV 모델 설계와 구축 · L5

### 15부. 연구를 읽고 판단하기

- 15.1 논문 읽는 법 · L4
- 15.2 재현과 검증 · L5
- 15.3 interpretability: 모델 내부 들여다보기 · L5
<!-- TOC:END -->

## 부록

- [용어집](appendix/glossary.md)
- [참고문헌](appendix/references.md)
