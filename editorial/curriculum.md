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

- 부·장의 신설·삭제·순서·제목 변경은 사용자가 정한다(ED-12).
- `tools/book.py`가 이 표를 읽는다. 부 제목은 `## N부. 제목`, 표는 위 일곱 칸 순서를 지킨다. 칸 안에 `|`를 쓰지 않는다.

## 1부. 큰 그림 — AI 지도
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 1.1 | 인공지능·머신러닝·딥러닝 | L1 | — | 셋은 어떤 포함 관계인가? 규칙을 짜 넣은 프로그램과 데이터로 배우는 모델은 무엇이 다른가? | `book/part01-big-picture/01-01-ai-ml-dl.md` | 계획 |
| 1.2 | 모델 이름을 읽는 여섯 개의 축 | L1 | 1.1 | CNN·ViT·LLM·VLM·디퓨전 같은 이름은 어떤 기준으로 붙나? 왜 서로 겹쳐 보이나? 공식 분류 체계가 있나? | `book/part01-big-picture/01-02-naming-axes.md` | 계획 |
| 1.3 | 모델의 한살이: 데이터에서 서비스까지 | L1 | 1.1 | 데이터 수집·라벨링·학습·평가·배포는 어떻게 이어지나? 학습과 추론은 무엇이 다른가? | `book/part01-big-picture/01-03-model-lifecycle.md` | 계획 |
| 1.4 | 대표 모델 지도 | L1 | 1.2 | ResNet·YOLO·SAM·CLIP·BERT·GPT·Stable Diffusion·Whisper는 각 축에서 어디에 놓이나? | `book/part01-big-picture/01-04-landmark-models.md` | 계획 |

## 2부. 수학과 도구의 최소한
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 2.1 | 벡터·행렬·텐서 | L2 | 1.1 | 사진과 문장은 어떻게 숫자 배열이 되나? 텐서의 shape는 어떻게 읽나? | `book/part02-math-and-tools/02-01-vectors-matrices-tensors.md` | 계획 |
| 2.2 | 미분과 기울기 | L2 | 2.1 | 기울기는 무엇을 알려 주나? 연쇄 법칙은 왜 학습의 핵심인가? | `book/part02-math-and-tools/02-02-derivatives-gradients.md` | 계획 |
| 2.3 | 확률과 통계 | L2 | 2.1 | 확률분포·기댓값·분산은 무엇인가? softmax 출력은 확률인가? | `book/part02-math-and-tools/02-03-probability-statistics.md` | 계획 |
| 2.4 | 정보 이론: 엔트로피와 교차 엔트로피 | L2 | 2.3 | 엔트로피·교차 엔트로피·KL 발산은 무엇을 재나? 분류 손실에 왜 쓰나? | `book/part02-math-and-tools/02-04-information-theory.md` | 계획 |
| 2.5 | Python·NumPy·PyTorch 첫걸음 | L2 | 2.1, 2.2 | 텐서 연산과 자동 미분(autograd)은 코드로 어떻게 쓰나? 계산을 GPU로 어떻게 옮기나? | `book/part02-math-and-tools/02-05-python-pytorch.md` | 계획 |

## 3부. 머신러닝의 기본 틀
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 3.1 | 학습이란: 모델·손실·최적화 | L2 | 1.3, 2.2 | 모델이 "배운다"는 것은 무엇을 바꾸는 것인가? 파라미터와 하이퍼파라미터는 어떻게 다른가? | `book/part03-ml-basics/03-01-model-loss-optimization.md` | 계획 |
| 3.2 | 학습 신호: 지도·비지도·자기지도·강화 학습 | L2 | 3.1 | 정답은 어디서 오나? 라벨이 없어도 학습할 수 있나? | `book/part03-ml-basics/03-02-learning-signals.md` | 계획 |
| 3.3 | 데이터 나누기: train·dev·test | L2 | 3.1 | 데이터를 왜 셋으로 나누나? validation과 dev는 같은 말인가? 데이터 누수란 무엇인가? | `book/part03-ml-basics/03-03-data-splits.md` | 계획 |
| 3.4 | 과적합과 일반화 | L2 | 3.3 | 학습 점수는 오르는데 평가 점수가 떨어지는 까닭은? 편향과 분산은 무엇인가? | `book/part03-ml-basics/03-04-overfitting-generalization.md` | 계획 |
| 3.5 | 고전 머신러닝 모델 | L2 | 3.1 | 선형·로지스틱 회귀, 결정 트리, 앙상블은 어떻게 동작하나? 딥러닝이 필요한 경우와 아닌 경우는? | `book/part03-ml-basics/03-05-classical-ml.md` | 계획 |

## 4부. 신경망과 딥러닝 학습
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

## 7부. 컴퓨터 비전
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 7.1 | 이미지 데이터: 전처리와 증강 | L3 | 2.1, 4.6 | 해상도·채널·정규화·리사이즈는 모델 입력을 어떻게 바꾸나? 어떤 증강이 언제 해로운가? | `book/part07-computer-vision/07-01-image-data.md` | 계획 |
| 7.2 | Vision Transformer와 Swin Transformer | L3 | 6.6 | 이미지를 패치로 잘라 Transformer에 넣으면 무엇이 좋고 무엇이 어렵나? Swin의 윈도 attention은 무엇을 바꾸나? | `book/part07-computer-vision/07-02-vit-swin.md` | 계획 |
| 7.3 | backbone·neck·head | L3 | 6.2, 7.2 | 검출·분할 모델은 어떤 부품으로 조립되나? FPN은 크기가 다른 물체를 어떻게 다루나? | `book/part07-computer-vision/07-03-backbone-neck-head.md` | 계획 |
| 7.4 | 객체 검출 I: 2단계·1단계 검출기 | L3 | 5.4, 7.3 | R-CNN 계열과 YOLO는 어떻게 다른가? anchor와 NMS는 무엇인가? | `book/part07-computer-vision/07-04-detection-classic.md` | 계획 |
| 7.5 | 객체 검출 II: DETR 계열 | L4 | 6.6, 7.4 | 검출을 집합 예측으로 보면 무엇이 달라지나? query와 Hungarian 매칭은 무엇인가? | `book/part07-computer-vision/07-05-detection-detr.md` | 계획 |
| 7.6 | 영상 분할 | L3 | 7.4 | semantic·instance·panoptic 분할은 어떻게 다른가? Mask R-CNN·Mask2Former·SAM은 mask를 어떻게 내나? | `book/part07-computer-vision/07-06-segmentation.md` | 계획 |
| 7.7 | 시각 자기지도 학습과 비전 파운데이션 모델 | L4 | 3.2, 7.2 | 라벨 없이 이미지 특징을 어떻게 배우나? MAE·DINO·DINOv2는 무엇을 학습하나? | `book/part07-computer-vision/07-07-visual-self-supervised.md` | 계획 |
| 7.8 | 라벨: 형식·품질·생산 | L3 | 5.1, 7.6 | box·polygon·mask 라벨은 어떻게 다르고 COCO 형식은 무엇인가? 라벨 오류는 학습과 평가에 어떤 영향을 주나? | `book/part07-computer-vision/07-08-labels.md` | 계획 |

## 8부. 언어 모델
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 8.1 | 토큰화 | L3 | 6.4 | 글은 어떻게 토큰으로 쪼개지나? BPE·WordPiece는 무엇인가? 언어마다 토큰 수가 왜 다른가? | `book/part08-language-models/08-01-tokenization.md` | 계획 |
| 8.2 | 언어 모델링과 사전학습 목표 | L3 | 6.7, 8.1 | 다음 토큰 예측과 마스크 예측은 모델에게 무엇을 배우게 하나? 사전학습이란 무엇인가? | `book/part08-language-models/08-02-pretraining-objectives.md` | 계획 |
| 8.3 | 대규모 언어 모델(LLM)과 스케일링 | L4 | 8.2 | 모델·데이터·계산량을 키우면 성능은 어떻게 변하나? 스케일링 법칙은 무엇을 말하나? | `book/part08-language-models/08-03-llm-scaling.md` | 계획 |
| 8.4 | 디코딩: 글을 만들어 내는 방법 | L3 | 8.2 | greedy·beam search·temperature·top-p는 출력을 어떻게 바꾸나? | `book/part08-language-models/08-04-decoding.md` | 계획 |
| 8.5 | 지시 학습과 정렬 | L4 | 8.3 | SFT·RLHF·DPO는 사전학습 모델을 어떻게 대화형 모델로 바꾸나? | `book/part08-language-models/08-05-instruction-alignment.md` | 계획 |

## 9부. 멀티모달과 생성 모델
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 9.1 | 대조 학습과 CLIP | L4 | 7.2, 8.2 | 이미지와 글을 같은 임베딩 공간에 어떻게 놓나? zero-shot 분류는 어떻게 가능한가? | `book/part09-multimodal-generative/09-01-contrastive-clip.md` | 계획 |
| 9.2 | open-vocabulary 검출과 grounding | L4 | 7.5, 9.1 | 텍스트 프롬프트로 찾을 대상을 정하는 검출기는 어떻게 동작하나? GLIP·Grounding DINO는 VLM과 무엇이 다른가? | `book/part09-multimodal-generative/09-02-open-vocabulary-detection.md` | 계획 |
| 9.3 | 비전-언어 모델(VLM) | L4 | 8.5, 9.1 | 이미지 인코더와 LLM은 어떻게 이어 붙이나? VLM이 좌표나 polygon을 글로 낼 때 무엇이 어렵나? | `book/part09-multimodal-generative/09-03-vlm.md` | 계획 |
| 9.4 | 생성 모델의 큰 그림: 오토인코더·VAE·GAN | L4 | 2.3, 4.3 | 판별 모델과 생성 모델은 무엇이 다른가? VAE와 GAN은 어떻게 샘플을 만드나? | `book/part09-multimodal-generative/09-04-autoencoder-vae-gan.md` | 계획 |
| 9.5 | 디퓨전 모델 | L4 | 9.4 | 노이즈에서 이미지를 어떻게 만드나? latent diffusion과 DiT는 무엇인가? 디퓨전은 구조인가 생성 방식인가? | `book/part09-multimodal-generative/09-05-diffusion.md` | 계획 |
| 9.6 | 음성·영상과 그 밖의 모달리티 | L4 | 6.6 | 음성 인식 모델(Whisper 등)과 영상 모델은 Transformer를 어떻게 쓰나? | `book/part09-multimodal-generative/09-06-audio-video.md` | 계획 |

## 10부. 사전학습 모델의 활용과 적응
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 10.1 | 전이 학습과 파인튜닝 | L3 | 3.2, 4.4 | 사전학습 가중치에서 시작하면 무엇이 좋은가? 어느 층을 고정(freeze)하고 어느 층을 학습하나? | `book/part10-adaptation/10-01-transfer-finetuning.md` | 계획 |
| 10.2 | 효율적 파인튜닝: LoRA·adapter | L4 | 10.1 | 모델 전체를 학습하지 않고 일부만 바꾸는 방법은? LoRA는 무엇을 학습하나? | `book/part10-adaptation/10-02-peft-lora.md` | 계획 |
| 10.3 | 프롬프트와 in-context learning | L3 | 8.4 | 가중치를 바꾸지 않고 예시만으로 과제를 수행하는 원리는? 좋은 프롬프트의 조건은? | `book/part10-adaptation/10-03-prompting.md` | 계획 |
| 10.4 | 검색 결합 생성(RAG) | L4 | 6.4, 10.3 | 외부 문서를 찾아 넣어 답하게 하는 구조는 어떻게 동작하나? | `book/part10-adaptation/10-04-rag.md` | 계획 |
| 10.5 | 에이전트와 도구 사용 | L4 | 10.3 | LLM이 도구를 부르고 여러 단계를 수행하는 구조는 어떻게 생겼나? | `book/part10-adaptation/10-05-agents.md` | 계획 |
| 10.6 | 큰 모델로 라벨 만들기: pseudo-label과 교사-학생 학습 | L4 | 5.1, 7.8, 10.1 | 큰 모델(VLM 등)이 만든 라벨로 작은 모델을 학습하면 무엇을 배우나? 그 라벨과의 일치도는 무엇을 뜻하나? | `book/part10-adaptation/10-06-pseudo-labels.md` | 계획 |
| 10.7 | 경량화: 증류·양자화·가지치기 | L4 | 10.1 | 큰 모델을 작고 빠르게 만드는 방법은? 그 대가로 무엇을 잃나? | `book/part10-adaptation/10-07-compression.md` | 계획 |

## 11부. 학습 엔지니어링 실전
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 11.1 | 실험 설계와 기록 | L4 | 3.3, 4.4 | 기준선과 ablation은 무엇인가? 실험을 재현할 수 있게 무엇을 기록하나? | `book/part11-training-engineering/11-01-experiments.md` | 계획 |
| 11.2 | 체크포인트와 모델 선택 | L3 | 4.5, 5.2 | best checkpoint는 어떤 지표로 고르나? early stopping은 언제 쓰나? 여러 지표를 평균해 선택 지표로 쓸 때 주의할 점은? | `book/part11-training-engineering/11-02-checkpoints-selection.md` | 계획 |
| 11.3 | 학습 곡선 읽기 | L4 | 4.7, 11.2 | dev 지표가 epoch마다 오르내리는 것은 문제인가? 곡선의 모양은 각각 무엇을 뜻하나? | `book/part11-training-engineering/11-03-learning-curves.md` | 계획 |
| 11.4 | 하이퍼파라미터 탐색 | L4 | 11.1 | 학습률·batch 크기 같은 값은 어떤 순서와 방법으로 찾나? | `book/part11-training-engineering/11-04-hyperparameter-search.md` | 계획 |
| 11.5 | 분산·대규모 학습 | L5 | 4.8 | 데이터 병렬·모델 병렬·파이프라인 병렬은 무엇인가? DDP·FSDP·ZeRO는 무엇을 나누나? | `book/part11-training-engineering/11-05-distributed-training.md` | 계획 |
| 11.6 | 추론 최적화와 서빙 | L4 | 10.7 | 지연 시간과 처리량은 어떻게 다른가? ONNX·TensorRT·vLLM은 무엇을 빠르게 하나? | `book/part11-training-engineering/11-06-inference-serving.md` | 계획 |
| 11.7 | 운영: 모니터링·데이터 드리프트·재학습 | L5 | 11.6 | 배포한 모델의 성능이 떨어지는 것을 어떻게 알아채나? 언제 다시 학습하나? | `book/part11-training-engineering/11-07-operations.md` | 계획 |

## 12부. 연구를 읽고 판단하기
| 장 | 제목 | 수준 | 선수 | 이 장의 질문 | 파일 | 상태 |
|---|---|---|---|---|---|---|
| 12.1 | 논문 읽는 법 | L4 | 5.8 | 논문의 주장과 근거는 어떻게 가려 읽나? 결과표와 ablation은 어떻게 읽나? | `book/part12-research/12-01-reading-papers.md` | 계획 |
| 12.2 | 재현과 검증 | L5 | 11.1, 12.1 | 논문 결과를 내 환경에서 확인하려면 무엇을 맞춰야 하나? 재현이 안 될 때 무엇을 의심하나? | `book/part12-research/12-02-reproduction.md` | 계획 |
| 12.3 | 모델 선택의 의사결정 | L5 | 5.8, 11.6 | 정확도·비용·지연 시간·라이선스를 어떻게 저울질하나? | `book/part12-research/12-03-model-selection.md` | 계획 |
| 12.4 | 라이선스·데이터 권리·안전 | L4 | 1.3 | 모델 가중치와 데이터셋의 라이선스는 무엇을 허용하나? 모델을 쓸 때의 안전과 책임은 무엇인가? | `book/part12-research/12-04-license-safety.md` | 계획 |
