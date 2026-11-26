# 편찬 계획

책의 부·장 구성과 장별 상태의 정본이다. 책의 목차(`book/README.md`)는 이 파일에서 `python3 tools/book.py toc`로 만든다.

| 칸 | 뜻 |
|---|---|
| 장 | 부 번호.장 번호 |
| 수준 | L1 입문 ~ L5 전문가. 정의는 [책의 「읽는 법」](../book/README.md#읽는-법) |
| 선수 | 먼저 읽어야 하는 장. 없으면 — |
| 이 장의 질문 | 이 장을 읽고 나면 답할 수 있어야 하는 질문. 사용자 질문을 어느 장에 반영할지 고를 때 본다 |
| 파일 | 장 파일 경로(저장소 기준) |
| 상태 | `계획` · `초고 · 집필AI` · `검토완료 · 집필AI / 검토AI` · `확정 · 집필AI / 검토AI` ([작업 절차 §0](workflow.md#0-장-상태)) |

- 부는 [AGENTS.md](../AGENTS.md#이-프로젝트)의 다섯 단계를 따른다: 용어와 기술 지도(1부) → 구조와 동작(2~7부) → 학습 방법과 그것으로 만든 모델(8~11부) → 성능 고도화와 배포(12~13부) → 설계와 구축(14부). 15부는 그 뒤의 연구 판단이다.
- 차례대로 읽으면 수준이 오르도록 짠다. 부 안에서는 수준이 내려가지 않고, 어떤 장도 뒤에 나오는 장을 선수로 두지 않는다. 평가 지표는 그 지표가 재는 모델을 배운 뒤에 둔다.
- 제목이 「직접 만들기:」인 장은 코드를 짜서 돌려 보는 장이고, 「프로젝트:」인 장은 설계부터 배포까지 혼자 해 보는 장이다. 코드는 `book/code/`에 둔다(ED-14).
- 부·장의 신설·삭제·순서·제목 변경은 사용자가 정한다(ED-12).
- `tools/book.py`가 이 표를 읽는다. 부 제목은 `## N부. 제목`, 표는 위 일곱 칸 순서를 지킨다. 칸 안에 `|`를 쓰지 않는다.

## 1부. 큰 그림 — AI 용어와 기술 지도
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 1.1 | AI·machine learning·deep learning | L1 | — | 셋은 어떤 포함 관계인가? 규칙을 짜 넣은 프로그램과 데이터로 배우는 모델은 무엇이 다른가? | `book/part01-big-picture/01-01-ai-ml-dl.md` | 초고 · Claude |
| 1.2 | 모델 이름을 읽는 여섯 개의 축 | L1 | 1.1 | CNN·ViT·LLM·VLM·diffusion 같은 이름은 어떤 기준으로 붙나? 왜 서로 겹쳐 보이나? 공식 분류 체계가 있나? classification·detection·segmentation 같은 task는 각각 무엇을 출력하나? | `book/part01-big-picture/01-02-naming-axes.md` | 초고 · Claude |
| 1.3 | ML lifecycle: 데이터에서 서비스까지 | L1 | 1.1, 1.2 | 데이터 수집·labeling·학습·평가·배포는 어떻게 이어지나? 학습과 inference는 무엇이 다른가? | `book/part01-big-picture/01-03-model-lifecycle.md` | 초고 · Claude |
| 1.4 | 학습 방법 지도: pre-training에서 reinforcement learning까지 | L1 | 1.3 | 학습 방법의 이름은 어떤 기준으로 나뉘나? pre-training·fine-tuning·SFT·RLHF·distillation은 각각 학습의 어느 단계에서 무엇을 정답으로 삼나? reinforcement learning과 preference learning은 어떤 관계인가? 대화형 AI는 어떤 학습 단계를 거쳐 만들어지나? | `book/part01-big-picture/01-04-training-methods-map.md` | 초고 · Claude |
| 1.5 | 대표 모델 지도 | L1 | 1.2 | ResNet·YOLO·SAM·CLIP·BERT·GPT·Stable Diffusion·Whisper는 각 축에서 어디에 놓이나? | `book/part01-big-picture/01-05-landmark-models.md` | 초고 · Claude |
| 1.6 | AI 산업의 기술 층위 | L1 | 1.3 | 반도체·프레임워크·foundation model·serving·응용은 어떻게 층을 이루나? open-weight model과 API 모델은 무엇이 다른가? | `book/part01-big-picture/01-06-industry-stack.md` | 초고 · Claude |

## 2부. 수학과 도구의 최소한
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 2.1 | vector·matrix·tensor | L2 | 1.1 | 사진과 문장은 어떻게 숫자 배열이 되나? 텐서의 shape는 어떻게 읽나? | `book/part02-math-and-tools/02-01-vectors-matrices-tensors.md` | 계획 |
| 2.2 | derivative와 gradient | L2 | 2.1 | 기울기는 무엇을 알려 주나? 연쇄 법칙은 왜 학습의 핵심인가? | `book/part02-math-and-tools/02-02-derivatives-gradients.md` | 계획 |
| 2.3 | probability와 statistics | L2 | 2.1 | 확률분포·기댓값·분산은 무엇인가? softmax 출력은 확률인가? | `book/part02-math-and-tools/02-03-probability-statistics.md` | 계획 |
| 2.4 | information theory: entropy와 cross-entropy | L2 | 2.3 | 엔트로피·교차 엔트로피·KL 발산은 무엇을 재나? 분류 손실에 왜 쓰나? | `book/part02-math-and-tools/02-04-information-theory.md` | 계획 |
| 2.5 | PyTorch로 계산하기: tensor·autograd·GPU | L2 | 2.1, 2.2 | 다른 언어를 쓰던 개발자가 알아야 할 Python·NumPy 관례는? 텐서 연산과 자동 미분(autograd)은 코드로 어떻게 쓰나? 계산을 GPU로 어떻게 옮기나? | `book/part02-math-and-tools/02-05-pytorch-basics.md` | 계획 |
| 2.6 | 개발 환경: GPU·클라우드·Hugging Face | L2 | 2.5 | 학습에 필요한 GPU는 어떻게 고르고 빌리나? Hugging Face의 모델·데이터셋·라이브러리는 무엇을 대신해 주나? | `book/part02-math-and-tools/02-06-dev-environment.md` | 계획 |

## 3부. machine learning의 기본 틀과 평가
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 3.1 | 학습이란: 모델·loss·optimization | L2 | 1.3, 2.2 | 모델이 "배운다"는 것은 무엇을 바꾸는 것인가? 파라미터와 하이퍼파라미터는 어떻게 다른가? | `book/part03-ml-basics/03-01-model-loss-optimization.md` | 계획 |
| 3.2 | 직접 만들기: NumPy로 linear regression과 gradient descent | L2 | 2.5, 3.1 | 손실을 정의하고 기울기를 구해 가중치를 고치는 과정을 NumPy로 처음부터 짜면 어떤 모양인가? 학습률과 반복 횟수를 바꾸면 무엇이 달라지나? | `book/part03-ml-basics/03-02-build-linear-regression.md` | 계획 |
| 3.3 | 학습 신호: supervised·unsupervised·self-supervised·reinforcement learning | L2 | 3.1 | 정답은 어디서 오나? 라벨이 없어도 학습할 수 있나? | `book/part03-ml-basics/03-03-learning-signals.md` | 계획 |
| 3.4 | 데이터 나누기: train·dev·test | L2 | 3.1 | 데이터를 왜 셋으로 나누나? validation과 dev는 같은 말인가? 데이터 누수란 무엇인가? | `book/part03-ml-basics/03-04-data-splits.md` | 계획 |
| 3.5 | overfitting과 generalization | L2 | 3.4 | 학습 점수는 오르는데 평가 점수가 떨어지는 까닭은? 편향과 분산은 무엇인가? | `book/part03-ml-basics/03-05-overfitting-generalization.md` | 계획 |
| 3.6 | 평가 설계의 기본 | L2 | 3.4 | 무엇을 기준(정답)으로 점수를 내나? 기준 라벨을 사람이 아니라 다른 모델이 만들었다면 점수의 뜻은 어떻게 달라지나? 회귀 문제는 무엇으로 평가하나(MSE·MAE)? | `book/part03-ml-basics/03-06-evaluation-design.md` | 계획 |
| 3.7 | confusion matrix·precision·recall·F1 | L2 | 3.6 | 정밀도와 재현율은 왜 서로 당기나? F1은 공식 용어인가? 클래스별 F1을 평균하는 방법(macro·micro)은? | `book/part03-ml-basics/03-07-precision-recall-f1.md` | 계획 |
| 3.8 | threshold와 곡선: PR·ROC·AUC | L2 | 3.7 | 점수 문턱을 바꾸면 지표는 어떻게 변하나? PR 곡선과 ROC 곡선은 언제 쓰나? | `book/part03-ml-basics/03-08-thresholds-curves.md` | 계획 |
| 3.9 | 고전 machine learning 모델 | L2 | 3.5, 3.7 | 선형·로지스틱 회귀, 결정 트리, 앙상블은 어떻게 동작하나? 딥러닝이 필요한 경우와 아닌 경우는? | `book/part03-ml-basics/03-09-classical-ml.md` | 계획 |
| 3.10 | 그 밖의 학습 방법: semi-supervised·multi-task·continual·federated·active learning | L2 | 3.3 | 라벨이 일부만 있을 때, 여러 과제를 한 모델로 배울 때, 데이터가 계속 들어오거나 여러 곳에 흩어져 있을 때, 라벨 붙일 데이터를 골라야 할 때는 각각 어떻게 배우나? 각 방법은 어떤 문제를 풀려고 나왔나? | `book/part03-ml-basics/03-10-other-learning-paradigms.md` | 계획 |

## 4부. neural network 학습의 기초
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 4.1 | batch·step·epoch: training loop의 단위 | L2 | 3.2 | batch·step·iteration·epoch는 어떻게 다른가? 학습 진행률과 로그는 어떻게 읽나? | `book/part04-deep-learning/04-01-batch-step-epoch.md` | 계획 |
| 4.2 | neuron과 multilayer perceptron | L3 | 2.1, 3.2 | 층·가중치·편향·활성화 함수는 무엇인가? 층을 쌓으면 무엇이 좋아지나? | `book/part04-deep-learning/04-02-neurons-mlp.md` | 계획 |
| 4.3 | backpropagation | L3 | 2.2, 4.2 | 오차는 어떻게 각 가중치까지 전달되나? 자동 미분은 이 계산을 어떻게 대신하나? | `book/part04-deep-learning/04-03-backpropagation.md` | 계획 |
| 4.4 | loss function | L3 | 2.4, 4.2 | 회귀와 분류에서는 각각 무엇을 최소화하나? 손실 값의 크기는 무엇을 뜻하나? 여러 손실을 더해 쓰는 이유는? | `book/part04-deep-learning/04-04-loss-functions.md` | 계획 |
| 4.5 | optimizer와 learning rate | L3 | 4.1, 4.3 | SGD·모멘텀·Adam·AdamW는 무엇이 다른가? warmup과 학습률 스케줄은 왜 쓰나? | `book/part04-deep-learning/04-05-optimizers-learning-rate.md` | 계획 |
| 4.6 | regularization과 normalization | L3 | 3.5, 4.5 | dropout·weight decay·데이터 증강은 과적합을 어떻게 줄이나? BatchNorm과 LayerNorm은 무엇이 다른가? 규제(regularization)와 정규화(normalization)는 어떻게 다른가? | `book/part04-deep-learning/04-06-regularization-normalization.md` | 계획 |
| 4.7 | 학습 안정성과 문제 진단 | L3 | 4.5 | loss가 발산하거나 멈추는 원인은? 기울기 소실·폭주, 초기화, 기울기 클리핑은 무엇인가? | `book/part04-deep-learning/04-07-training-stability.md` | 계획 |
| 4.8 | GPU 메모리와 학습 자원 | L3 | 2.5, 4.1 | 메모리 부족(OOM)은 왜 생기나? 혼합 정밀도·gradient accumulation·activation checkpointing은 무엇을 아끼나? | `book/part04-deep-learning/04-08-gpu-memory.md` | 계획 |
| 4.9 | learning curve 읽기 | L3 | 3.5, 4.7 | train loss와 dev 지표의 곡선은 어떻게 읽나? dev 지표가 epoch마다 오르내리는 것은 문제인가? 곡선의 모양은 각각 무엇을 뜻하나? | `book/part04-deep-learning/04-09-learning-curves.md` | 계획 |
| 4.10 | checkpoint와 model selection | L3 | 3.7, 4.9 | best checkpoint는 어떤 지표로 고르나? early stopping은 언제 쓰나? 여러 지표를 평균해 선택 지표로 쓸 때 주의할 점은? | `book/part04-deep-learning/04-10-checkpoints-selection.md` | 계획 |
| 4.11 | 직접 만들기: training loop와 숫자 classifier | L3 | 2.5, 4.5, 4.10 | 데이터 로딩·모델·손실·옵티마이저·평가·체크포인트로 이어지는 학습 루프를 PyTorch로 처음부터 짜면 어떤 모양인가? 손글씨 숫자 분류기는 어떻게 만드나? | `book/part04-deep-learning/04-11-build-training-loop.md` | 계획 |

## 5부. neural network 구조의 기본 블록
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 5.1 | convolutional neural network(CNN) | L3 | 4.2 | 합성곱 필터는 이미지에서 무엇을 찾나? 특징 맵·수용 영역·풀링은 무엇인가? | `book/part05-architectures/05-01-cnn.md` | 계획 |
| 5.2 | 대표 CNN: VGG에서 ResNet까지 | L3 | 4.7, 5.1 | 층을 깊게 쌓을수록 생기는 문제는? 잔차 연결(residual connection)은 그것을 어떻게 푸나? | `book/part05-architectures/05-02-vgg-resnet.md` | 계획 |
| 5.3 | recurrent neural network(RNN)과 sequence | L3 | 4.3 | 순서가 있는 데이터는 어떻게 다루나? RNN·LSTM의 한계는 무엇이었나? | `book/part05-architectures/05-03-rnn.md` | 계획 |
| 5.4 | embedding과 token | L3 | 2.1, 4.2 | 단어나 이미지 조각은 어떻게 벡터가 되나? 임베딩 공간의 거리는 무엇을 뜻하나? | `book/part05-architectures/05-04-embeddings-tokens.md` | 계획 |
| 5.5 | attention | L3 | 5.4 | query·key·value는 무엇인가? self-attention과 cross-attention은 어떻게 다른가? 계산량은 입력 길이에 따라 어떻게 늘어나나? | `book/part05-architectures/05-05-attention.md` | 계획 |
| 5.6 | Transformer block | L3 | 4.6, 5.5 | Transformer 한 층은 무엇으로 이뤄지나? 위치 정보는 어떻게 넣나? | `book/part05-architectures/05-06-transformer.md` | 계획 |
| 5.7 | encoder·decoder·encoder-decoder | L3 | 5.6 | BERT형·GPT형·T5형은 구조와 쓰임이 어떻게 다른가? | `book/part05-architectures/05-07-encoder-decoder.md` | 계획 |
| 5.8 | 직접 만들기: Transformer를 처음부터 | L3 | 5.7 | attention과 Transformer 블록을 고수준 라이브러리 없이 PyTorch로 구현하면 어떤 모양인가? 각 단계에서 텐서의 shape는 어떻게 바뀌나? | `book/part05-architectures/05-08-build-transformer.md` | 계획 |
| 5.9 | 그 밖의 구조: graph neural network와 state space model | L4 | 5.3, 5.6 | 그래프처럼 연결된 데이터는 어떻게 다루나? 상태 공간 모델은 RNN·Transformer와 무엇이 같고 무엇이 다른가? | `book/part05-architectures/05-09-other-architectures.md` | 계획 |

## 6부. computer vision 모델과 평가
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 6.1 | 이미지 데이터: preprocessing과 augmentation | L3 | 2.1, 4.6 | 해상도·채널·정규화·리사이즈는 모델 입력을 어떻게 바꾸나? 어떤 증강이 언제 해로운가? | `book/part06-computer-vision/06-01-image-data.md` | 계획 |
| 6.2 | 직접 만들기: CNN image classifier | L3 | 4.11, 5.2, 6.1 | 작은 CNN 분류기를 처음부터 학습하면 어떤 정확도가 나오고, 증강과 구조를 바꾸면 무엇이 달라지나? | `book/part06-computer-vision/06-02-build-cnn-classifier.md` | 계획 |
| 6.3 | Vision Transformer와 Swin Transformer | L3 | 5.6 | 이미지를 패치로 잘라 Transformer에 넣으면 무엇이 좋고 무엇이 어렵나? Swin의 윈도 attention은 무엇을 바꾸나? | `book/part06-computer-vision/06-03-vit-swin.md` | 계획 |
| 6.4 | backbone·neck·head | L3 | 5.2, 6.3 | 비전 모델은 어떤 부품으로 조립되나? 같은 backbone에 head만 바꿔 다른 과제를 푸는 것은 어떻게 가능한가? FPN은 크기가 다른 물체를 어떻게 다루나? | `book/part06-computer-vision/06-04-backbone-neck-head.md` | 계획 |
| 6.5 | object detection I: box·IoU·anchor·NMS | L3 | 6.4 | 검출 모델은 무엇을 출력하나? 두 box가 얼마나 겹치는지는 IoU로 어떻게 재나? R-CNN 계열과 YOLO는 어떻게 다르고, anchor와 NMS는 무엇인가? | `book/part06-computer-vision/06-05-detection-classic.md` | 계획 |
| 6.6 | detection 평가: 예측-정답 matching과 AP·mAP | L3 | 3.8, 6.5 | 검출 결과가 "맞았다"는 기준은 무엇인가? IoU 0.5는 어디서 왔나? AP·mAP·AP50은 어떻게 계산되며, 문턱을 정해 낸 F1과 왜 직접 비교하면 안 되나? | `book/part06-computer-vision/06-06-detection-evaluation.md` | 계획 |
| 6.7 | image segmentation | L3 | 6.5 | semantic·instance·panoptic 분할은 어떻게 다른가? Mask R-CNN과 SAM은 mask를 어떻게 내나? | `book/part06-computer-vision/06-07-segmentation.md` | 계획 |
| 6.8 | segmentation 평가: mask IoU·mIoU·Dice·PQ | L3 | 6.6, 6.7 | mask IoU·mIoU·Dice·PQ는 각각 무엇을 재나? 검출 평가와 무엇이 같고 무엇이 다른가? | `book/part06-computer-vision/06-08-segmentation-evaluation.md` | 계획 |
| 6.9 | label: 형식·품질·생산 | L3 | 3.6, 6.7 | box·polygon·mask 라벨은 어떻게 다르고 COCO 형식은 무엇인가? 라벨 오류는 학습과 평가에 어떤 영향을 주나? | `book/part06-computer-vision/06-09-labels.md` | 계획 |
| 6.10 | object detection II: DETR 계열 | L4 | 5.6, 6.6 | 검출을 집합 예측으로 보면 무엇이 달라지나? object query와 Hungarian 매칭은 무엇인가? 같은 방식이 분할(Mask2Former)로 어떻게 이어지나? | `book/part06-computer-vision/06-10-detection-detr.md` | 계획 |

## 7부. language model과 평가
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 7.1 | tokenization | L3 | 5.4 | 글은 어떻게 토큰으로 쪼개지나? BPE·WordPiece는 무엇인가? 언어마다 토큰 수가 왜 다른가? | `book/part07-language-models/07-01-tokenization.md` | 계획 |
| 7.2 | LLM이 글을 만드는 과정 | L3 | 5.7, 7.1 | decoder-only 언어 모델은 입력을 받아 어떻게 다음 토큰을 고르나? KV cache는 무엇을 아끼나? | `book/part07-language-models/07-02-llm-generation.md` | 계획 |
| 7.3 | decoding: 다음 token을 고르는 방법 | L3 | 7.2 | greedy·beam search·temperature·top-p는 출력을 어떻게 바꾸나? | `book/part07-language-models/07-03-decoding.md` | 계획 |
| 7.4 | language model의 평가 | L3 | 2.4, 3.6, 7.3 | perplexity는 무엇을 재나? BLEU·ROUGE, 벤치마크 정답률, 사람 평가, LLM 평가는 각각 언제 쓰나? | `book/part07-language-models/07-04-language-model-evaluation.md` | 계획 |
| 7.5 | 현대 LLM의 구조 변형: RMSNorm·RoPE·MoE·long context | L4 | 7.2 | 현대 LLM 블록은 원래 Transformer와 무엇이 다른가(RMSNorm·SwiGLU·RoPE 등)? MoE는 왜 토큰당 계산량을 크게 늘리지 않고 파라미터를 늘릴 수 있나? 긴 문맥은 어떤 구조 변경으로 다루나? | `book/part07-language-models/07-05-modern-llm-architecture.md` | 계획 |

## 8부. pre-training
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 8.1 | pre-training과 representation learning | L3 | 3.3, 5.6 | 왜 먼저 큰 데이터로 넓게 배우나? 층마다 어떤 표현이 쌓이기에 사전학습한 모델을 다른 과제로 옮겨 쓸 수 있나? | `book/part08-pretraining/08-01-pretraining-representation.md` | 계획 |
| 8.2 | 언어 pre-training objective: next-token prediction과 masked prediction | L3 | 7.2, 8.1 | 다음 토큰 예측과 마스크 예측은 모델에게 무엇을 배우게 하나? BERT형과 GPT형은 왜 다른 목표로 학습하나? | `book/part08-pretraining/08-02-language-pretraining.md` | 계획 |
| 8.3 | 시각 self-supervised pre-training: contrastive learning·MAE·DINO | L4 | 6.3, 8.1 | 라벨 없이 이미지 특징을 어떻게 배우나? 대조 학습·MAE·DINO·DINOv2는 무엇을 맞히도록 학습하나? | `book/part08-pretraining/08-03-visual-self-supervised.md` | 계획 |
| 8.4 | pre-training 데이터: 수집·정제·혼합 | L4 | 8.2 | 사전학습 데이터는 어떻게 모으고 거르나? 중복 제거와 데이터 혼합 비율은 성능에 어떤 영향을 주나? | `book/part08-pretraining/08-04-pretraining-data.md` | 계획 |
| 8.5 | continual pre-training과 domain adaptation | L4 | 8.4 | 사전학습한 모델을 특정 분야 데이터로 더 사전학습(continual pre-training)하면 무엇이 달라지나? 언제 필요하고 무엇을 조심하나? | `book/part08-pretraining/08-05-continual-pretraining.md` | 계획 |
| 8.6 | 직접 만들기: 작은 GPT pre-training | L4 | 5.8, 7.1, 8.2 | 토크나이저부터 학습 루프·생성까지 작은 언어 모델을 직접 사전학습하면 어떤 모양인가? 모델 크기와 학습량에 따라 생성 결과는 어떻게 달라지나? | `book/part08-pretraining/08-06-build-small-gpt.md` | 계획 |

## 9부. fine-tuning과 adaptation
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 9.1 | transfer learning과 fine-tuning | L3 | 4.5, 8.1 | 사전학습 가중치에서 시작하면 무엇이 좋은가? 어느 층을 고정(freeze)하고 어느 층을 학습하나? 추가 사전학습과는 무엇이 다른가? | `book/part09-finetuning/09-01-transfer-finetuning.md` | 계획 |
| 9.2 | prompt와 in-context learning | L3 | 7.3, 9.1 | 가중치를 바꾸지 않고 예시만으로 과제를 수행하는 원리는? 파인튜닝과 언제 무엇을 고르나? | `book/part09-finetuning/09-02-prompting-icl.md` | 계획 |
| 9.3 | supervised fine-tuning(SFT)과 instruction tuning | L4 | 8.2, 9.1 | SFT는 사전학습과 무엇이 같고 무엇이 다른가? 지시 데이터는 어떻게 만들고, 손실은 어느 토큰에만 거나? | `book/part09-finetuning/09-03-sft-instruction-tuning.md` | 계획 |
| 9.4 | parameter-efficient fine-tuning: LoRA·adapter·prompt tuning | L4 | 9.1 | 모델 전체를 학습하지 않고 일부만 바꿔도 되는 것은 가중치 행렬의 어떤 성질 때문인가? LoRA는 무엇을 학습하나? | `book/part09-finetuning/09-04-peft-lora.md` | 계획 |
| 9.5 | catastrophic forgetting | L4 | 9.1 | 새 과제를 배우면 이전 능력을 잃는 까닭은? 이를 줄이는 방법은? | `book/part09-finetuning/09-05-catastrophic-forgetting.md` | 계획 |
| 9.6 | distillation과 pseudo-label: 큰 모델에게 배우기 | L4 | 3.6, 6.9, 9.1 | 큰 모델의 출력이나 라벨로 작은 모델을 학습하면 무엇을 배우나? 그 라벨과의 일치도는 무엇을 뜻하나? | `book/part09-finetuning/09-06-distillation-pseudo-labels.md` | 계획 |
| 9.7 | 직접 만들기: pre-trained detection model fine-tuning | L4 | 6.6, 6.9, 9.1 | 공개된 사전학습 검출 모델을 내 데이터에 맞춰 학습하려면 데이터·설정·평가를 어떻게 준비하나? | `book/part09-finetuning/09-07-build-detector-finetune.md` | 계획 |
| 9.8 | 직접 만들기: 작은 language model SFT와 LoRA | L4 | 8.6, 9.3, 9.4 | 사전학습한 작은 언어 모델을 지시 데이터로 SFT하고 LoRA로 학습하면 출력이 어떻게 달라지나? 전체 파인튜닝과 비교하면? | `book/part09-finetuning/09-08-build-sft-lora.md` | 계획 |

## 10부. reward와 preference로 배우기: reinforcement learning·RLHF·DPO
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 10.1 | reinforcement learning의 기초: agent·environment·reward·policy | L3 | 3.3 | 정답 대신 보상으로 배운다는 것은 무슨 뜻인가? 상태·행동·정책·가치는 무엇인가? | `book/part10-reward-and-preference/10-01-rl-basics.md` | 계획 |
| 10.2 | value-based와 policy-based 방법 | L4 | 2.3, 10.1 | Q-learning과 정책 경사(policy gradient)는 각각 무엇을 학습하나? | `book/part10-reward-and-preference/10-02-value-policy-methods.md` | 계획 |
| 10.3 | actor-critic과 PPO | L4 | 10.2 | 정책을 한 번에 크게 바꾸면 왜 위험한가? PPO는 갱신을 어떻게 제한하나? | `book/part10-reward-and-preference/10-03-actor-critic-ppo.md` | 계획 |
| 10.4 | RLHF: 사람의 preference로 배우기 | L4 | 9.3, 10.3 | 다음 토큰 예측과 SFT만으로는 왜 원하는 답이 충분히 나오지 않나? 보상 모델은 어떻게 만들고 PPO로 언어 모델을 어떻게 고치나? | `book/part10-reward-and-preference/10-04-rlhf.md` | 계획 |
| 10.5 | direct preference optimization: DPO와 그 변형 | L4 | 10.4 | 보상 모델 없이 선호 데이터로 바로 학습하는 방법은? RLHF와 무엇을 주고받나? | `book/part10-reward-and-preference/10-05-dpo.md` | 계획 |
| 10.6 | 직접 만들기: 작은 language model DPO | L4 | 9.8, 10.5 | 선호 데이터로 작은 언어 모델을 DPO 학습하면 출력이 어떻게 달라지나? 무엇을 보고 학습이 잘됐다고 판단하나? | `book/part10-reward-and-preference/10-06-build-dpo.md` | 계획 |
| 10.7 | verifiable reward와 reasoning model | L5 | 10.5 | 정답을 확인할 수 있는 과제(수학·코드)로 강화 학습하면 무엇이 달라지나? GRPO 같은 방법은 무엇을 바꾸나? 추론(reasoning) 모델은 어떻게 학습되나? | `book/part10-reward-and-preference/10-07-rlvr-reasoning.md` | 계획 |
| 10.8 | reward hacking과 alignment의 한계 | L5 | 10.4 | 모델이 보상을 속이는 것은 어떤 경우인가? KL 제약은 무엇을 막나? | `book/part10-reward-and-preference/10-08-reward-hacking.md` | 계획 |

## 11부. multimodal과 generative model
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 11.1 | contrastive learning과 CLIP | L4 | 6.3, 7.2, 8.3 | 이미지와 글을 같은 임베딩 공간에 어떻게 놓나? zero-shot 분류는 어떻게 가능한가? | `book/part11-multimodal-generative/11-01-contrastive-clip.md` | 계획 |
| 11.2 | vision-language model(VLM) | L4 | 9.3, 11.1 | 이미지 인코더와 LLM은 어떻게 이어 붙이고 어떤 순서로 학습하나? VLM은 위치(좌표)를 어떻게 출력하나? | `book/part11-multimodal-generative/11-02-vlm.md` | 계획 |
| 11.3 | open-vocabulary detection과 grounding | L4 | 6.10, 11.2 | 텍스트 프롬프트로 찾을 대상을 정하는 검출기는 어떻게 동작하나? GLIP·Grounding DINO는 VLM과 무엇이 다른가? | `book/part11-multimodal-generative/11-03-open-vocabulary-detection.md` | 계획 |
| 11.4 | generative model의 큰 그림: autoencoder·VAE·GAN | L4 | 2.3, 4.4 | 판별 모델과 생성 모델은 무엇이 다른가? VAE와 GAN은 어떻게 샘플을 만드나? | `book/part11-multimodal-generative/11-04-autoencoder-vae-gan.md` | 계획 |
| 11.5 | diffusion model | L4 | 11.4 | 노이즈에서 이미지를 어떻게 만드나? latent diffusion과 DiT는 무엇인가? 디퓨전은 구조인가 생성 방식인가? | `book/part11-multimodal-generative/11-05-diffusion.md` | 계획 |
| 11.6 | generative model의 평가 | L4 | 3.6, 11.5 | 생성한 이미지의 품질과 다양성은 어떻게 재나(FID 등)? 자동 지표와 사람 평가는 어떻게 함께 쓰나? | `book/part11-multimodal-generative/11-06-generative-evaluation.md` | 계획 |
| 11.7 | 음성·영상과 그 밖의 modality | L4 | 5.6, 8.1 | 음성 인식 모델(Whisper 등)과 영상 모델은 Transformer를 어떻게 쓰나? | `book/part11-multimodal-generative/11-07-audio-video.md` | 계획 |

## 12부. 성능 고도화
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 12.1 | benchmark와 leaderboard 읽기 | L4 | 6.6, 7.4 | 논문·리더보드 수치를 내 문제의 목표치로 쓰면 안 되는 이유는? 표준 지표·관례값·자체 정의를 어떻게 가려내나? 데이터 오염이란? | `book/part12-performance/12-01-benchmarks.md` | 계획 |
| 12.2 | 실험 설계와 기록 | L4 | 3.4, 4.10 | 기준선과 ablation은 무엇인가? 실험을 재현할 수 있게 무엇을 기록하나? | `book/part12-performance/12-02-experiments.md` | 계획 |
| 12.3 | hyperparameter search | L4 | 12.2 | 학습률·batch 크기 같은 값은 어떤 순서와 방법으로 찾나? | `book/part12-performance/12-03-hyperparameter-search.md` | 계획 |
| 12.4 | data-centric 개선: label 품질·augmentation·synthetic data | L4 | 6.9, 9.6 | 모델을 바꾸지 않고 데이터로 성능을 올리는 방법은? 합성 데이터는 언제 돕고 언제 해치나? | `book/part12-performance/12-04-data-centric.md` | 계획 |
| 12.5 | scaling law | L4 | 8.1 | 모델·데이터·계산량을 키우면 성능은 어떻게 변하나? 정해진 계산 예산은 모델 크기와 데이터 양에 어떻게 나누나? | `book/part12-performance/12-05-scaling-laws.md` | 계획 |
| 12.6 | test-time compute: 더 생각하게 하기 | L4 | 7.3, 9.2 | chain-of-thought·self-consistency·검증기 같은 방법은 가중치를 바꾸지 않고 성능을 어떻게 올리나? 추론에 계산을 더 쓰면 무엇이 좋아지나? | `book/part12-performance/12-06-test-time-compute.md` | 계획 |
| 12.7 | distributed·large-scale training | L5 | 4.8 | 데이터 병렬·모델 병렬·파이프라인 병렬은 무엇인가? DDP·FSDP·ZeRO는 무엇을 나누나? | `book/part12-performance/12-07-distributed-training.md` | 계획 |

## 13부. 배포와 응용
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 13.1 | model compression: quantization·pruning | L4 | 9.1 | 큰 모델을 작고 빠르게 만드는 방법은? 그 대가로 무엇을 잃나? | `book/part13-deployment/13-01-quantization-pruning.md` | 계획 |
| 13.2 | inference optimization과 serving | L4 | 13.1 | 지연 시간과 처리량은 어떻게 다른가? ONNX·TensorRT·vLLM은 무엇을 빠르게 하나? 기기 안(온디바이스)에서 돌리려면 무엇이 필요한가? | `book/part13-deployment/13-02-inference-serving.md` | 계획 |
| 13.3 | retrieval-augmented generation(RAG) | L4 | 5.4, 9.2 | 외부 문서를 찾아 넣어 답하게 하는 구조는 어떻게 동작하나? | `book/part13-deployment/13-03-rag.md` | 계획 |
| 13.4 | agent와 tool use | L4 | 9.2 | LLM이 도구를 부르고 여러 단계를 수행하는 구조는 어떻게 생겼나? | `book/part13-deployment/13-04-agents.md` | 계획 |
| 13.5 | 라이선스·데이터 권리·safety | L4 | 1.6 | 모델 가중치와 데이터셋의 라이선스는 무엇을 허용하나? 모델을 쓸 때의 안전과 책임은 무엇인가? | `book/part13-deployment/13-05-license-safety.md` | 계획 |
| 13.6 | 운영: 모니터링·data drift·retraining | L5 | 13.2 | 배포한 모델의 성능이 떨어지는 것을 어떻게 알아채나? 언제 다시 학습하나? | `book/part13-deployment/13-06-operations.md` | 계획 |

## 14부. 설계와 구축
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 14.1 | 크기와 비용 계산하기 | L4 | 4.8, 12.5 | 파라미터 수·연산량(FLOPs)·메모리·학습 시간은 어떻게 추정하나? 가진 GPU로 어느 크기의 모델을 학습할 수 있나? | `book/part14-design-build/14-01-size-and-cost.md` | 계획 |
| 14.2 | 모델 설계의 순서와 선택 | L5 | 12.1, 12.2, 14.1 | 문제 정의에서 출발해 구조·크기·데이터·학습 방법·평가·배포 조건을 어떤 순서로 정하나? 처음부터 만들지 공개 모델을 가져다 쓸지, 후보 모델의 정확도·비용·지연 시간·라이선스를 어떻게 저울질하나? | `book/part14-design-build/14-02-design-process.md` | 계획 |
| 14.3 | 프로젝트: 경량 language model 설계와 구축 | L5 | 8.6, 10.6, 13.2, 14.2 | 목적에 맞는 작은 언어 모델을 토크나이저·사전학습·SFT·선호 학습·평가·배포까지 직접 설계하고 만들려면 무엇을 어떤 순서로 결정하나? | `book/part14-design-build/14-03-project-small-lm.md` | 계획 |
| 14.4 | 프로젝트: CV 모델 설계와 구축 | L5 | 9.7, 13.1, 14.2 | 내 문제에 맞는 검출·분할 모델을 데이터·라벨·backbone 선택·학습·평가·경량화·배포까지 직접 설계하고 만들려면 무엇을 어떤 순서로 결정하나? | `book/part14-design-build/14-04-project-cv-model.md` | 계획 |

## 15부. 연구를 읽고 판단하기
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 15.1 | 논문 읽는 법 | L4 | 12.1 | 논문의 주장과 근거는 어떻게 가려 읽나? 결과표와 ablation은 어떻게 읽나? | `book/part15-research/15-01-reading-papers.md` | 계획 |
| 15.2 | 재현과 검증 | L5 | 12.2, 15.1 | 논문 결과를 내 환경에서 확인하려면 무엇을 맞춰야 하나? 재현이 안 될 때 무엇을 의심하나? | `book/part15-research/15-02-reproduction.md` | 계획 |
| 15.3 | interpretability: 모델 내부 들여다보기 | L5 | 5.6, 8.1 | 학습된 모델 안에서 층과 뉴런은 무엇을 표현하나? attention 시각화·probing·기계적 해석 가능성은 무엇을 알려 주고 무엇을 알려 주지 못하나? | `book/part15-research/15-03-interpretability.md` | 계획 |
