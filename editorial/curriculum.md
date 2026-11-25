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

- 부는 [AGENTS.md](../AGENTS.md#이-프로젝트)의 다섯 단계를 따른다: 용어와 기술 지도(1부) → 구조와 동작(2~9부) → 학습 방법(10~12부) → 성능 고도화(13~14부) → 설계와 구축(15부). 16부는 그 뒤의 연구 판단이다.
- 제목이 「직접 만들기:」인 장은 코드를 짜서 돌려 보는 장이고, 「프로젝트:」인 장은 설계부터 배포까지 혼자 해 보는 장이다. 코드는 `book/code/`에 둔다(ED-14).
- 부·장의 신설·삭제·순서·제목 변경은 사용자가 정한다(ED-12).
- `tools/book.py`가 이 표를 읽는다. 부 제목은 `## N부. 제목`, 표는 위 일곱 칸 순서를 지킨다. 칸 안에 `|`를 쓰지 않는다.

## 1부. 큰 그림 — AI 용어와 기술 지도
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 1.1 | 인공지능·머신러닝·딥러닝 | L1 | — | 셋은 어떤 포함 관계인가? 규칙을 짜 넣은 프로그램과 데이터로 배우는 모델은 무엇이 다른가? | `book/part01-big-picture/01-01-ai-ml-dl.md` | 계획 |
| 1.2 | 모델 이름을 읽는 여섯 개의 축 | L1 | 1.1 | CNN·ViT·LLM·VLM·디퓨전 같은 이름은 어떤 기준으로 붙나? 왜 서로 겹쳐 보이나? 공식 분류 체계가 있나? | `book/part01-big-picture/01-02-naming-axes.md` | 계획 |
| 1.3 | 모델의 한살이: 데이터에서 서비스까지 | L1 | 1.1 | 데이터 수집·라벨링·학습·평가·배포는 어떻게 이어지나? 학습과 추론은 무엇이 다른가? | `book/part01-big-picture/01-03-model-lifecycle.md` | 계획 |
| 1.4 | 학습 방법 지도: 사전학습에서 강화 학습까지 | L1 | 1.3 | 학습 방법의 이름은 어떤 기준으로 나뉘나? 사전학습·파인튜닝·SFT·RLHF·증류는 각각 학습의 어느 단계에서 무엇을 정답으로 삼나? 강화 학습과 선호 학습은 어떤 관계인가? 대화형 AI는 어떤 학습 단계를 거쳐 만들어지나? | `book/part01-big-picture/01-04-training-methods-map.md` | 초고 · Claude |
| 1.5 | 대표 모델 지도 | L1 | 1.2 | ResNet·YOLO·SAM·CLIP·BERT·GPT·Stable Diffusion·Whisper는 각 축에서 어디에 놓이나? | `book/part01-big-picture/01-05-landmark-models.md` | 계획 |
| 1.6 | AI 산업의 기술 층위 | L1 | 1.3 | 반도체·프레임워크·파운데이션 모델·서빙·응용은 어떻게 층을 이루나? 오픈 가중치 모델과 API 모델은 무엇이 다른가? | `book/part01-big-picture/01-06-industry-stack.md` | 계획 |

## 2부. 수학과 도구의 최소한
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 2.1 | 벡터·행렬·텐서 | L2 | 1.1 | 사진과 문장은 어떻게 숫자 배열이 되나? 텐서의 shape는 어떻게 읽나? | `book/part02-math-and-tools/02-01-vectors-matrices-tensors.md` | 계획 |
| 2.2 | 미분과 기울기 | L2 | 2.1 | 기울기는 무엇을 알려 주나? 연쇄 법칙은 왜 학습의 핵심인가? | `book/part02-math-and-tools/02-02-derivatives-gradients.md` | 계획 |
| 2.3 | 확률과 통계 | L2 | 2.1 | 확률분포·기댓값·분산은 무엇인가? softmax 출력은 확률인가? | `book/part02-math-and-tools/02-03-probability-statistics.md` | 계획 |
| 2.4 | 정보 이론: 엔트로피와 교차 엔트로피 | L2 | 2.3 | 엔트로피·교차 엔트로피·KL 발산은 무엇을 재나? 분류 손실에 왜 쓰나? | `book/part02-math-and-tools/02-04-information-theory.md` | 계획 |
| 2.5 | PyTorch로 계산하기: 텐서·자동 미분·GPU | L2 | 2.1, 2.2 | 다른 언어를 쓰던 개발자가 알아야 할 Python·NumPy 관례는? 텐서 연산과 자동 미분(autograd)은 코드로 어떻게 쓰나? 계산을 GPU로 어떻게 옮기나? | `book/part02-math-and-tools/02-05-pytorch-basics.md` | 계획 |
| 2.6 | 개발 환경: GPU·클라우드·Hugging Face | L2 | 2.5 | 학습에 필요한 GPU는 어떻게 고르고 빌리나? Hugging Face의 모델·데이터셋·라이브러리는 무엇을 대신해 주나? | `book/part02-math-and-tools/02-06-dev-environment.md` | 계획 |

## 3부. 머신러닝의 기본 틀
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 3.1 | 학습이란: 모델·손실·최적화 | L2 | 1.3, 2.2 | 모델이 "배운다"는 것은 무엇을 바꾸는 것인가? 파라미터와 하이퍼파라미터는 어떻게 다른가? | `book/part03-ml-basics/03-01-model-loss-optimization.md` | 계획 |
| 3.2 | 학습 신호: 지도·비지도·자기지도·강화 학습 | L2 | 3.1 | 정답은 어디서 오나? 라벨이 없어도 학습할 수 있나? | `book/part03-ml-basics/03-02-learning-signals.md` | 계획 |
| 3.3 | 데이터 나누기: train·dev·test | L2 | 3.1 | 데이터를 왜 셋으로 나누나? validation과 dev는 같은 말인가? 데이터 누수란 무엇인가? | `book/part03-ml-basics/03-03-data-splits.md` | 계획 |
| 3.4 | 과적합과 일반화 | L2 | 3.3 | 학습 점수는 오르는데 평가 점수가 떨어지는 까닭은? 편향과 분산은 무엇인가? | `book/part03-ml-basics/03-04-overfitting-generalization.md` | 계획 |
| 3.5 | 고전 머신러닝 모델 | L2 | 3.1 | 선형·로지스틱 회귀, 결정 트리, 앙상블은 어떻게 동작하나? 딥러닝이 필요한 경우와 아닌 경우는? | `book/part03-ml-basics/03-05-classical-ml.md` | 계획 |
| 3.6 | 그 밖의 학습 방법: 준지도·다중 과제·연속·연합·능동 학습 | L2 | 3.2 | 라벨이 일부만 있을 때, 여러 과제를 한 모델로 배울 때, 데이터가 계속 들어오거나 여러 곳에 흩어져 있을 때, 라벨 붙일 데이터를 골라야 할 때는 각각 어떻게 배우나? 각 방법은 어떤 문제를 풀려고 나왔나? | `book/part03-ml-basics/03-06-other-learning-paradigms.md` | 계획 |

## 4부. 신경망 학습의 기초
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 4.1 | 뉴런과 다층 퍼셉트론 | L3 | 2.1, 3.1 | 층·가중치·편향·활성화 함수는 무엇인가? 층을 쌓으면 무엇이 좋아지나? | `book/part04-deep-learning/04-01-neurons-mlp.md` | 계획 |
| 4.2 | 역전파 | L3 | 2.2, 4.1 | 오차는 어떻게 각 가중치까지 전달되나? 자동 미분은 이 계산을 어떻게 대신하나? | `book/part04-deep-learning/04-02-backpropagation.md` | 계획 |
| 4.3 | 손실 함수 | L3 | 2.4, 4.1 | 회귀·분류·검출에서는 각각 무엇을 최소화하나? 여러 손실을 더해 쓰는 이유는? | `book/part04-deep-learning/04-03-loss-functions.md` | 계획 |
| 4.4 | 옵티마이저와 학습률 | L3 | 4.2 | SGD·모멘텀·Adam·AdamW는 무엇이 다른가? warmup과 학습률 스케줄은 왜 쓰나? | `book/part04-deep-learning/04-04-optimizers-learning-rate.md` | 계획 |
| 4.5 | batch·step·epoch: 학습 루프의 단위 | L2 | 3.1 | batch·step·iteration·epoch는 어떻게 다른가? 학습 진행률과 로그는 어떻게 읽나? | `book/part04-deep-learning/04-05-batch-step-epoch.md` | 계획 |
| 4.6 | 규제와 정규화 | L3 | 3.4, 4.4 | dropout·weight decay·데이터 증강은 과적합을 어떻게 줄이나? BatchNorm과 LayerNorm은 무엇이 다른가? 규제(regularization)와 정규화(normalization)는 어떻게 다른가? | `book/part04-deep-learning/04-06-regularization-normalization.md` | 계획 |
| 4.7 | 학습 안정성과 문제 진단 | L3 | 4.4 | loss가 발산하거나 멈추는 원인은? 기울기 소실·폭주, 초기화, 기울기 클리핑은 무엇인가? | `book/part04-deep-learning/04-07-training-stability.md` | 계획 |
| 4.8 | GPU 메모리와 학습 자원 | L3 | 2.5, 4.5 | 메모리 부족(OOM)은 왜 생기나? 혼합 정밀도·gradient accumulation·activation checkpointing은 무엇을 아끼나? | `book/part04-deep-learning/04-08-gpu-memory.md` | 계획 |
| 4.9 | 직접 만들기: 학습 루프와 숫자 분류기 | L3 | 2.5, 4.4, 4.5 | 데이터 로딩·모델·손실·옵티마이저·평가로 이어지는 학습 루프를 PyTorch로 처음부터 짜면 어떤 모양인가? 손글씨 숫자 분류기는 어떻게 만드나? | `book/part04-deep-learning/04-09-build-training-loop.md` | 계획 |

## 5부. 평가와 지표
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 5.1 | 평가 설계의 기본 | L2 | 3.3 | 무엇을 기준(정답)으로 점수를 내나? 기준 라벨을 사람이 아니라 다른 모델이 만들었다면 점수의 뜻은 어떻게 달라지나? | `book/part05-evaluation/05-01-evaluation-design.md` | 계획 |
| 5.2 | 혼동행렬·정밀도·재현율·F1 | L2 | 5.1 | 정밀도와 재현율은 왜 서로 당기나? F1은 공식 용어인가? 클래스별 F1을 평균하는 방법(macro·micro)은? | `book/part05-evaluation/05-02-precision-recall-f1.md` | 계획 |
| 5.3 | 점수 문턱과 곡선: PR·ROC·AUC | L2 | 5.2 | 점수 문턱을 바꾸면 지표는 어떻게 변하나? PR 곡선과 ROC 곡선은 언제 쓰나? | `book/part05-evaluation/05-03-thresholds-curves.md` | 계획 |
| 5.4 | IoU와 예측-정답 짝짓기 | L2 | 5.2 | 검출 결과가 "맞았다"는 기준은 무엇인가? IoU 0.5는 어디서 왔나? 짝짓기 규칙은 점수를 어떻게 바꾸나? | `book/part05-evaluation/05-04-iou-matching.md` | 계획 |
| 5.5 | AP와 mAP | L3 | 5.3, 5.4 | 논문의 검출 수치(AP·mAP·AP50)는 어떻게 계산되나? 문턱을 정해 낸 F1과 왜 직접 비교하면 안 되나? | `book/part05-evaluation/05-05-ap-map.md` | 계획 |
| 5.6 | 분할 지표 | L3 | 5.4 | mask IoU·mIoU·Dice·PQ는 각각 무엇을 재나? | `book/part05-evaluation/05-06-segmentation-metrics.md` | 계획 |
| 5.7 | 언어·생성 모델의 평가 | L3 | 2.4, 5.1 | perplexity·BLEU·ROUGE·FID는 무엇을 재나? 사람 평가와 LLM 평가는 언제 쓰나? | `book/part05-evaluation/05-07-generative-evaluation.md` | 계획 |
| 5.8 | 벤치마크와 리더보드 읽기 | L4 | 5.5 | 논문 수치를 내 문제의 목표치로 쓰면 안 되는 이유는? 표준 지표·관례값·자체 정의를 어떻게 가려내나? 데이터 오염이란? | `book/part05-evaluation/05-08-benchmarks.md` | 계획 |

## 6부. 신경망 구조의 기본 블록
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 6.1 | 합성곱 신경망(CNN) | L3 | 4.1 | 합성곱 필터는 이미지에서 무엇을 찾나? 특징 맵·수용 영역·풀링은 무엇인가? | `book/part06-architectures/06-01-cnn.md` | 계획 |
| 6.2 | 대표 CNN: VGG에서 ResNet까지 | L3 | 4.7, 6.1 | 층을 깊게 쌓을수록 생기는 문제는? 잔차 연결(residual connection)은 그것을 어떻게 푸나? | `book/part06-architectures/06-02-vgg-resnet.md` | 계획 |
| 6.3 | 순환 신경망(RNN)과 시퀀스 | L3 | 4.2 | 순서가 있는 데이터는 어떻게 다루나? RNN·LSTM의 한계는 무엇이었나? | `book/part06-architectures/06-03-rnn.md` | 계획 |
| 6.4 | 임베딩과 토큰 | L3 | 2.1, 4.1 | 단어나 이미지 조각은 어떻게 벡터가 되나? 임베딩 공간의 거리는 무엇을 뜻하나? | `book/part06-architectures/06-04-embeddings-tokens.md` | 계획 |
| 6.5 | attention | L3 | 6.4 | query·key·value는 무엇인가? self-attention과 cross-attention은 어떻게 다른가? 계산량은 입력 길이에 따라 어떻게 늘어나나? | `book/part06-architectures/06-05-attention.md` | 계획 |
| 6.6 | Transformer 블록 | L3 | 4.6, 6.5 | Transformer 한 층은 무엇으로 이뤄지나? 위치 정보는 어떻게 넣나? | `book/part06-architectures/06-06-transformer.md` | 계획 |
| 6.7 | 인코더·디코더·인코더-디코더 | L3 | 6.6 | BERT형·GPT형·T5형은 구조와 쓰임이 어떻게 다른가? | `book/part06-architectures/06-07-encoder-decoder.md` | 계획 |
| 6.8 | 직접 만들기: Transformer를 처음부터 | L3 | 6.7 | attention과 Transformer 블록을 고수준 라이브러리 없이 PyTorch로 구현하면 어떤 모양인가? 각 단계에서 텐서의 shape는 어떻게 바뀌나? | `book/part06-architectures/06-08-build-transformer.md` | 계획 |

## 7부. 컴퓨터 비전 모델
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 7.1 | 이미지 데이터: 전처리와 증강 | L3 | 2.1, 4.6 | 해상도·채널·정규화·리사이즈는 모델 입력을 어떻게 바꾸나? 어떤 증강이 언제 해로운가? | `book/part07-computer-vision/07-01-image-data.md` | 계획 |
| 7.2 | Vision Transformer와 Swin Transformer | L3 | 6.6 | 이미지를 패치로 잘라 Transformer에 넣으면 무엇이 좋고 무엇이 어렵나? Swin의 윈도 attention은 무엇을 바꾸나? | `book/part07-computer-vision/07-02-vit-swin.md` | 계획 |
| 7.3 | backbone·neck·head | L3 | 6.2, 7.2 | 검출·분할 모델은 어떤 부품으로 조립되나? FPN은 크기가 다른 물체를 어떻게 다루나? | `book/part07-computer-vision/07-03-backbone-neck-head.md` | 계획 |
| 7.4 | 객체 검출 I: 2단계·1단계 검출기 | L3 | 5.4, 7.3 | R-CNN 계열과 YOLO는 어떻게 다른가? anchor와 NMS는 무엇인가? | `book/part07-computer-vision/07-04-detection-classic.md` | 계획 |
| 7.5 | 객체 검출 II: DETR 계열 | L4 | 6.6, 7.4 | 검출을 집합 예측으로 보면 무엇이 달라지나? query와 Hungarian 매칭은 무엇인가? | `book/part07-computer-vision/07-05-detection-detr.md` | 계획 |
| 7.6 | 영상 분할 | L3 | 7.4 | semantic·instance·panoptic 분할은 어떻게 다른가? Mask R-CNN·Mask2Former·SAM은 mask를 어떻게 내나? | `book/part07-computer-vision/07-06-segmentation.md` | 계획 |
| 7.7 | 라벨: 형식·품질·생산 | L3 | 5.1, 7.6 | box·polygon·mask 라벨은 어떻게 다르고 COCO 형식은 무엇인가? 라벨 오류는 학습과 평가에 어떤 영향을 주나? | `book/part07-computer-vision/07-07-labels.md` | 계획 |
| 7.8 | 직접 만들기: CNN 이미지 분류기 | L3 | 4.9, 6.2, 7.1 | 작은 CNN 분류기를 처음부터 학습하면 어떤 정확도가 나오고, 증강과 구조를 바꾸면 무엇이 달라지나? | `book/part07-computer-vision/07-08-build-cnn-classifier.md` | 계획 |

## 8부. 언어 모델
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 8.1 | 토큰화 | L3 | 6.4 | 글은 어떻게 토큰으로 쪼개지나? BPE·WordPiece는 무엇인가? 언어마다 토큰 수가 왜 다른가? | `book/part08-language-models/08-01-tokenization.md` | 계획 |
| 8.2 | LLM이 글을 만드는 과정 | L3 | 6.7, 8.1 | decoder-only 언어 모델은 입력을 받아 어떻게 다음 토큰을 고르나? KV cache는 무엇을 아끼나? | `book/part08-language-models/08-02-llm-generation.md` | 계획 |
| 8.3 | 디코딩: 다음 토큰을 고르는 방법 | L3 | 8.2 | greedy·beam search·temperature·top-p는 출력을 어떻게 바꾸나? | `book/part08-language-models/08-03-decoding.md` | 계획 |
| 8.4 | LLM 구조의 변형: MoE·긴 문맥 | L4 | 8.2 | Mixture of Experts는 왜 토큰당 계산량을 크게 늘리지 않고 파라미터를 늘릴 수 있나? 긴 문맥은 어떤 구조 변경으로 다루나? | `book/part08-language-models/08-04-llm-architecture-variants.md` | 계획 |

## 9부. 멀티모달과 생성 모델
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 9.1 | 대조 학습과 CLIP | L4 | 7.2, 8.2 | 이미지와 글을 같은 임베딩 공간에 어떻게 놓나? zero-shot 분류는 어떻게 가능한가? | `book/part09-multimodal-generative/09-01-contrastive-clip.md` | 계획 |
| 9.2 | open-vocabulary 검출과 grounding | L4 | 7.5, 9.1 | 텍스트 프롬프트로 찾을 대상을 정하는 검출기는 어떻게 동작하나? GLIP·Grounding DINO는 VLM과 무엇이 다른가? | `book/part09-multimodal-generative/09-02-open-vocabulary-detection.md` | 계획 |
| 9.3 | 비전-언어 모델(VLM) | L4 | 8.2, 9.1 | 이미지 인코더와 LLM은 어떻게 이어 붙이나? VLM은 위치(좌표)를 어떻게 출력하나? | `book/part09-multimodal-generative/09-03-vlm.md` | 계획 |
| 9.4 | 생성 모델의 큰 그림: 오토인코더·VAE·GAN | L4 | 2.3, 4.3 | 판별 모델과 생성 모델은 무엇이 다른가? VAE와 GAN은 어떻게 샘플을 만드나? | `book/part09-multimodal-generative/09-04-autoencoder-vae-gan.md` | 계획 |
| 9.5 | 디퓨전 모델 | L4 | 9.4 | 노이즈에서 이미지를 어떻게 만드나? latent diffusion과 DiT는 무엇인가? 디퓨전은 구조인가 생성 방식인가? | `book/part09-multimodal-generative/09-05-diffusion.md` | 계획 |
| 9.6 | 음성·영상과 그 밖의 모달리티 | L4 | 6.6 | 음성 인식 모델(Whisper 등)과 영상 모델은 Transformer를 어떻게 쓰나? | `book/part09-multimodal-generative/09-06-audio-video.md` | 계획 |

## 10부. 사전학습
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 10.1 | 사전학습과 표현 학습 | L3 | 3.2, 6.6 | 왜 먼저 큰 데이터로 넓게 배우나? 층마다 어떤 표현이 쌓이기에 사전학습한 모델을 다른 과제로 옮겨 쓸 수 있나? | `book/part10-pretraining/10-01-pretraining-representation.md` | 계획 |
| 10.2 | 언어 사전학습 목표: 다음 토큰 예측과 마스크 예측 | L3 | 8.2, 10.1 | 다음 토큰 예측과 마스크 예측은 모델에게 무엇을 배우게 하나? BERT형과 GPT형은 왜 다른 목표로 학습하나? | `book/part10-pretraining/10-02-language-pretraining.md` | 계획 |
| 10.3 | 시각 자기지도 사전학습: 대조 학습·MAE·DINO | L4 | 7.2, 10.1 | 라벨 없이 이미지 특징을 어떻게 배우나? MAE·DINO·DINOv2는 무엇을 맞히도록 학습하나? | `book/part10-pretraining/10-03-visual-self-supervised.md` | 계획 |
| 10.4 | 사전학습 데이터: 수집·정제·혼합 | L4 | 10.2 | 사전학습 데이터는 어떻게 모으고 거르나? 중복 제거와 데이터 혼합 비율은 성능에 어떤 영향을 주나? | `book/part10-pretraining/10-04-pretraining-data.md` | 계획 |
| 10.5 | 추가 사전학습과 도메인 적응 | L4 | 10.4 | 이미 사전학습한 모델을 특정 분야 데이터로 더 사전학습(continual pre-training)하는 것은 파인튜닝과 무엇이 다른가? | `book/part10-pretraining/10-05-continual-pretraining.md` | 계획 |
| 10.6 | 직접 만들기: 작은 GPT 사전학습 | L4 | 6.8, 8.1, 10.2 | 토크나이저부터 학습 루프·생성까지 작은 언어 모델을 직접 사전학습하면 어떤 모양인가? 모델 크기와 학습량에 따라 생성 결과는 어떻게 달라지나? | `book/part10-pretraining/10-06-build-small-gpt.md` | 계획 |

## 11부. 파인튜닝과 적응
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 11.1 | 전이 학습과 파인튜닝 | L3 | 4.4, 10.1 | 사전학습 가중치에서 시작하면 무엇이 좋은가? 어느 층을 고정(freeze)하고 어느 층을 학습하나? | `book/part11-finetuning/11-01-transfer-finetuning.md` | 계획 |
| 11.2 | 파괴적 망각 | L4 | 11.1 | 새 과제를 배우면 이전 능력을 잃는 까닭은? 이를 줄이는 방법은? | `book/part11-finetuning/11-02-catastrophic-forgetting.md` | 계획 |
| 11.3 | 효율적 파인튜닝: LoRA·adapter·prompt tuning | L4 | 11.1 | 모델 전체를 학습하지 않고 일부만 바꿔도 되는 것은 가중치 행렬의 어떤 성질 때문인가? LoRA는 무엇을 학습하나? | `book/part11-finetuning/11-03-peft-lora.md` | 계획 |
| 11.4 | 지도 파인튜닝(SFT)과 지시 학습 | L4 | 10.2, 11.1 | SFT는 사전학습과 무엇이 같고 무엇이 다른가? 지시 데이터는 어떻게 만들고, 손실은 어느 토큰에만 거나? | `book/part11-finetuning/11-04-sft-instruction-tuning.md` | 계획 |
| 11.5 | 증류와 pseudo-label: 큰 모델에게 배우기 | L4 | 5.1, 7.7, 11.1 | 큰 모델의 출력이나 라벨로 작은 모델을 학습하면 무엇을 배우나? 그 라벨과의 일치도는 무엇을 뜻하나? | `book/part11-finetuning/11-05-distillation-pseudo-labels.md` | 계획 |
| 11.6 | 프롬프트와 in-context learning | L3 | 8.3 | 가중치를 바꾸지 않고 예시만으로 과제를 수행하는 원리는? 파인튜닝과 언제 무엇을 고르나? | `book/part11-finetuning/11-06-prompting-icl.md` | 계획 |
| 11.7 | 직접 만들기: 사전학습 검출 모델 파인튜닝 | L4 | 7.4, 7.8, 11.1 | 공개된 사전학습 검출 모델을 내 데이터에 맞춰 학습하려면 데이터·설정·평가를 어떻게 준비하나? | `book/part11-finetuning/11-07-build-detector-finetune.md` | 계획 |
| 11.8 | 직접 만들기: 작은 언어 모델 SFT와 LoRA | L4 | 10.6, 11.3, 11.4 | 사전학습한 작은 언어 모델을 지시 데이터로 SFT하고 LoRA로 학습하면 출력이 어떻게 달라지나? 전체 파인튜닝과 비교하면? | `book/part11-finetuning/11-08-build-sft-lora.md` | 계획 |

## 12부. 보상과 선호로 배우기: 강화 학습·RLHF·DPO
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 12.1 | 강화 학습의 기초: 에이전트·환경·보상·정책 | L3 | 3.2 | 정답 대신 보상으로 배운다는 것은 무슨 뜻인가? 상태·행동·정책·가치는 무엇인가? | `book/part12-reinforcement-learning/12-01-rl-basics.md` | 계획 |
| 12.2 | 가치 기반과 정책 기반 방법 | L4 | 2.3, 12.1 | Q-learning과 정책 경사(policy gradient)는 각각 무엇을 학습하나? | `book/part12-reinforcement-learning/12-02-value-policy-methods.md` | 계획 |
| 12.3 | actor-critic과 PPO | L4 | 12.2 | 정책을 한 번에 크게 바꾸면 왜 위험한가? PPO는 갱신을 어떻게 제한하나? | `book/part12-reinforcement-learning/12-03-actor-critic-ppo.md` | 계획 |
| 12.4 | RLHF: 사람의 선호로 배우기 | L4 | 11.4, 12.3 | 다음 토큰 예측과 SFT만으로는 왜 원하는 답이 충분히 나오지 않나? 보상 모델은 어떻게 만들고 PPO로 언어 모델을 어떻게 고치나? | `book/part12-reinforcement-learning/12-04-rlhf.md` | 계획 |
| 12.5 | 직접 선호 최적화: DPO와 그 변형 | L4 | 12.4 | 보상 모델 없이 선호 데이터로 바로 학습하는 방법은? RLHF와 무엇을 주고받나? | `book/part12-reinforcement-learning/12-05-dpo.md` | 계획 |
| 12.6 | 검증 가능한 보상과 추론 모델 | L5 | 12.5 | 정답을 확인할 수 있는 과제(수학·코드)로 강화 학습하면 무엇이 달라지나? GRPO 같은 방법은 무엇을 바꾸나? 추론(reasoning) 모델은 어떻게 학습되나? | `book/part12-reinforcement-learning/12-06-rlvr-reasoning.md` | 계획 |
| 12.7 | 보상 해킹과 정렬의 한계 | L5 | 12.4 | 모델이 보상을 속이는 것은 어떤 경우인가? KL 제약은 무엇을 막나? | `book/part12-reinforcement-learning/12-07-reward-hacking.md` | 계획 |
| 12.8 | 직접 만들기: 작은 언어 모델 DPO | L4 | 11.8, 12.5 | 선호 데이터로 작은 언어 모델을 DPO 학습하면 출력이 어떻게 달라지나? 무엇을 보고 학습이 잘됐다고 판단하나? | `book/part12-reinforcement-learning/12-08-build-dpo.md` | 계획 |

## 13부. 성능 고도화
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 13.1 | 실험 설계와 기록 | L4 | 3.3, 4.4 | 기준선과 ablation은 무엇인가? 실험을 재현할 수 있게 무엇을 기록하나? | `book/part13-performance/13-01-experiments.md` | 계획 |
| 13.2 | 체크포인트와 모델 선택 | L3 | 4.5, 5.2 | best checkpoint는 어떤 지표로 고르나? early stopping은 언제 쓰나? 여러 지표를 평균해 선택 지표로 쓸 때 주의할 점은? | `book/part13-performance/13-02-checkpoints-selection.md` | 계획 |
| 13.3 | 학습 곡선 읽기 | L4 | 4.7, 13.2 | dev 지표가 epoch마다 오르내리는 것은 문제인가? 곡선의 모양은 각각 무엇을 뜻하나? | `book/part13-performance/13-03-learning-curves.md` | 계획 |
| 13.4 | 하이퍼파라미터 탐색 | L4 | 13.1 | 학습률·batch 크기 같은 값은 어떤 순서와 방법으로 찾나? | `book/part13-performance/13-04-hyperparameter-search.md` | 계획 |
| 13.5 | 데이터 중심 개선: 라벨 품질·증강·합성 데이터 | L4 | 7.7, 11.5 | 모델을 바꾸지 않고 데이터로 성능을 올리는 방법은? 합성 데이터는 언제 돕고 언제 해치나? | `book/part13-performance/13-05-data-centric.md` | 계획 |
| 13.6 | 스케일링 법칙 | L4 | 10.1 | 모델·데이터·계산량을 키우면 성능은 어떻게 변하나? 정해진 계산 예산은 모델 크기와 데이터 양에 어떻게 나누나? | `book/part13-performance/13-06-scaling-laws.md` | 계획 |
| 13.7 | 추론 시점 계산: 더 생각하게 하기 | L4 | 8.3, 12.6 | chain-of-thought·self-consistency·검증기 같은 방법은 가중치를 바꾸지 않고 성능을 어떻게 올리나? 추론에 계산을 더 쓰면 무엇이 좋아지나? | `book/part13-performance/13-07-test-time-compute.md` | 계획 |
| 13.8 | 분산·대규모 학습 | L5 | 4.8 | 데이터 병렬·모델 병렬·파이프라인 병렬은 무엇인가? DDP·FSDP·ZeRO는 무엇을 나누나? | `book/part13-performance/13-08-distributed-training.md` | 계획 |

## 14부. 배포와 응용
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 14.1 | 경량화: 양자화·가지치기 | L4 | 11.1 | 큰 모델을 작고 빠르게 만드는 방법은? 그 대가로 무엇을 잃나? | `book/part14-deployment/14-01-quantization-pruning.md` | 계획 |
| 14.2 | 추론 최적화와 서빙 | L4 | 14.1 | 지연 시간과 처리량은 어떻게 다른가? ONNX·TensorRT·vLLM은 무엇을 빠르게 하나? | `book/part14-deployment/14-02-inference-serving.md` | 계획 |
| 14.3 | 검색 결합 생성(RAG) | L4 | 6.4, 11.6 | 외부 문서를 찾아 넣어 답하게 하는 구조는 어떻게 동작하나? | `book/part14-deployment/14-03-rag.md` | 계획 |
| 14.4 | 에이전트와 도구 사용 | L4 | 11.6 | LLM이 도구를 부르고 여러 단계를 수행하는 구조는 어떻게 생겼나? | `book/part14-deployment/14-04-agents.md` | 계획 |
| 14.5 | 운영: 모니터링·데이터 드리프트·재학습 | L5 | 14.2 | 배포한 모델의 성능이 떨어지는 것을 어떻게 알아채나? 언제 다시 학습하나? | `book/part14-deployment/14-05-operations.md` | 계획 |

## 15부. 설계와 구축
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 15.1 | 모델 설계의 순서 | L5 | 5.8, 13.1 | 문제 정의에서 출발해 구조·크기·데이터·학습 방법·평가·배포 조건을 어떤 순서로 정하나? 처음부터 만들지, 사전학습 모델을 가져다 쓸지 어떻게 고르나? | `book/part15-design-build/15-01-design-process.md` | 계획 |
| 15.2 | 크기와 비용 계산하기 | L4 | 4.8, 13.6 | 파라미터 수·연산량(FLOPs)·메모리·학습 시간은 어떻게 추정하나? 가진 GPU로 어느 크기의 모델을 학습할 수 있나? | `book/part15-design-build/15-02-size-and-cost.md` | 계획 |
| 15.3 | 프로젝트: 경량 언어 모델 설계와 구축 | L5 | 10.6, 12.8, 14.2, 15.2 | 목적에 맞는 작은 언어 모델을 토크나이저·사전학습·SFT·선호 학습·평가·배포까지 직접 설계하고 만들려면 무엇을 어떤 순서로 결정하나? | `book/part15-design-build/15-03-project-small-lm.md` | 계획 |
| 15.4 | 프로젝트: CV 모델 설계와 구축 | L5 | 11.7, 14.1, 15.2 | 내 문제에 맞는 검출·분할 모델을 데이터·라벨·backbone 선택·학습·평가·경량화·배포까지 직접 설계하고 만들려면 무엇을 어떤 순서로 결정하나? | `book/part15-design-build/15-04-project-cv-model.md` | 계획 |

## 16부. 연구를 읽고 판단하기
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 16.1 | 논문 읽는 법 | L4 | 5.8 | 논문의 주장과 근거는 어떻게 가려 읽나? 결과표와 ablation은 어떻게 읽나? | `book/part16-research/16-01-reading-papers.md` | 계획 |
| 16.2 | 재현과 검증 | L5 | 13.1, 16.1 | 논문 결과를 내 환경에서 확인하려면 무엇을 맞춰야 하나? 재현이 안 될 때 무엇을 의심하나? | `book/part16-research/16-02-reproduction.md` | 계획 |
| 16.3 | 공개 모델 비교와 선택 | L5 | 5.8, 14.2 | 후보 모델들의 정확도·비용·지연 시간·라이선스를 어떻게 저울질하나? | `book/part16-research/16-03-model-comparison.md` | 계획 |
| 16.4 | 라이선스·데이터 권리·안전 | L4 | 1.6 | 모델 가중치와 데이터셋의 라이선스는 무엇을 허용하나? 모델을 쓸 때의 안전과 책임은 무엇인가? | `book/part16-research/16-04-license-safety.md` | 계획 |
