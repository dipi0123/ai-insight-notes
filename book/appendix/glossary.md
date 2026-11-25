# 용어집

본문에서 쓰는 용어 표기의 정본이다. 이 책은 기술 용어를 영어 원어로 쓰고, 장마다 처음 나올 때 한국어 번역어를 괄호에 단다. 한 줄 정의만 두고 자세한 설명은 「본 장」으로 간다. 링크가 없는 장 번호는 아직 실리지 않은 장이다.

- **표기**는 본문에서 쓰는 형태 그대로다. 하이픈과 띄어쓰기도 같다. 대소문자를 가리지 않고 알파벳순으로 둔다.
- **풀이·다른 이름**은 약어의 풀이, 또는 같은 뜻으로 쓰는 다른 영어 이름이다.
- **한국어**는 본문에서 처음 나올 때 괄호에 다는 번역어다. 자리 잡은 번역어가 없으면 —로 둔다.
- **분류**는 그 용어가 어느 갈래의 이름인지 나타낸다: 분야 · 구조 · 과제 · 방식 · 학습신호 · 규모·활용 · 학습과정 · 평가 · 데이터 · 수학 · 시스템. 분야·구조·과제·방식·규모·활용은 [1.2장](../part01-big-picture/01-02-naming-axes.md)에서 모델 이름을 읽는 축과 같다. 1.2장의 학습 축은 [1.4장](../part01-big-picture/01-04-training-methods-map.md)의 다섯 축으로 더 나뉘는데, 신호 축의 이름은 학습신호로, 나머지 네 축(단계·바꾸는 범위·가르치는 쪽·데이터가 들어오는 방식)의 이름은 학습과정으로 분류한다.

## A–Z

| 표기 | 풀이·다른 이름 | 한국어 | 분류 | 한 줄 정의 | 본 장 |
|---|---|---|---|---|---|
| action | — | 행동 | 학습신호 | reinforcement learning에서 모델이 내놓는 행동. language model에서는 생성한 답이 action이다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.1 |
| active learning | — | 능동 학습 | 학습과정 | 모델이 label이 가장 도움이 될 데이터를 골라 label을 요청하며 배우는 방식 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.10 |
| architecture | — | 구조 | 구조 | 모델 안에서 layer를 어떤 모양으로 짜고 이었는지. 예: CNN, Transformer | [1.2](../part01-big-picture/01-02-naming-axes.md) |
| artificial intelligence | AI | 인공지능 | 분야 | 사람의 지능이 필요하다고 여기는 일을 컴퓨터가 하게 만드는 분야 전체 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| attention | — | — | 구조 | 입력의 각 위치가 다른 위치를 얼마나 참고할지 계산해 정보를 모으는 계산. Transformer의 핵심이다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 5.5 |
| autoregressive model | — | 자기회귀 모델 | 방식 | 앞에서 만든 출력을 보고 다음 조각을 하나씩 이어 붙여 출력을 만드는 모델 | [1.2](../part01-big-picture/01-02-naming-axes.md), 7.2 |
| backpropagation | — | 역전파 | 수학 | 출력에서 거꾸로 거슬러 가며 weight마다 loss를 줄이려면 어느 쪽으로 고쳐야 하는지 계산하는 방법 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 4.3 |
| base model | — | 베이스 모델 | 규모·활용 | pre-training만 하고 지시를 따르도록 더 학습하지 않은 language model을 흔히 부르는 이름 | [1.2](../part01-big-picture/01-02-naming-axes.md), 9.3 |
| bounding box | box | 경계 상자 | 과제 | 사진 속 물체를 둘러싼 사각형. object detection이 물체의 위치로 출력한다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.5 |
| checkpoint | — | 체크포인트 | 시스템 | 학습 중간이나 끝에 모델의 parameter 값을 저장한 것 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 4.10 |
| class | — | 클래스 | 과제 | 모델이 구별하는 부류 하나. 예: cat, dog | [1.2](../part01-big-picture/01-02-naming-axes.md) |
| classifier | — | 분류기 | 과제 | classification task를 푸는 모델 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.2 |
| cluster | — | 군집 | 데이터 | 서로 비슷한 데이터끼리 모인 묶음 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.9 |
| CNN | convolutional neural network | 합성곱 신경망 | 구조 | 작은 창을 입력 위로 옮겨 가며 같은 계산을 되풀이하는 layer를 쌓은 neural network. 이미지에 오래 써 온 구조다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 5.1 |
| computer vision | CV | 컴퓨터 비전 | 분야 | 이미지와 영상을 다루는 AI 분야 | [1.2](../part01-big-picture/01-02-naming-axes.md) |
| concept drift | — | — | 데이터 | 입력과 정답의 관계가 시간이 지나며 바뀌는 것. 모델의 예측이 점점 틀리게 된다 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 13.6 |
| confidence score | — | 신뢰도 점수 | 과제 | 모델이 자기 예측을 얼마나 확신하는지 나타낸 점수. object detection에서는 box마다 붙는다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.5 |
| continual learning | lifelong learning | 연속 학습 | 학습과정 | task나 데이터가 바뀌어 가는 동안 이어서 배우는 방식. 앞서 배운 것을 잊는 문제가 따라온다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.10, 9.5 |
| continual pre-training | — | 추가 사전학습 | 학습과정 | pre-trained model을 특정 분야 데이터로 pre-training과 같은 방식으로 더 학습하는 것 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 8.5 |
| contrastive learning | — | 대조 학습 | 학습신호 | 맞는 짝과 틀린 짝을 가려내도록 배우는 학습. 예: 어느 설명 글이 어느 사진의 것인지 맞히기 | [1.2](../part01-big-picture/01-02-naming-axes.md), 8.3, 11.1 |
| curriculum learning | — | 커리큘럼 학습 | 학습과정 | 쉬운 데이터부터 어려운 데이터 순으로 배우게 짜는 방식 | [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| data cleaning | — | 데이터 정제 | 데이터 | 모은 데이터에서 부정확하거나 지저분한 기록을 걸러 내는 일 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 8.4 |
| dataset | — | 데이터셋 | 데이터 | 학습이나 평가에 쓰려고 모아 둔 데이터 묶음 | [1.3](../part01-big-picture/01-03-model-lifecycle.md) |
| deep learning | — | 딥러닝 | 분야 | 여러 layer를 쌓은 neural network로 feature까지 데이터에서 배우는 machine learning의 한 갈래 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| demonstration | — | 시범 답 | 데이터 | 사람이 직접 써서 보여 주는 바람직한 답. SFT의 학습 데이터가 된다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.3 |
| detection model | — | 검출 모델 | 과제 | 사진 속 물체마다 위치와 종류를 출력하는 모델 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 6.5 |
| detector | — | 검출기 | 과제 | object detection task를 푸는 모델 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.5 |
| diffusion model | — | 확산 모델 | 방식 | 데이터에 noise를 더해 가는 과정을 거꾸로 되돌리도록 배워, noise에서 시작해 데이터를 만드는 generative model | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.5 |
| distillation | knowledge distillation | 증류 | 학습과정 | 큰 teacher 모델의 출력을 작은 student 모델이 따라 하게 해서 배우는 방법 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.6 |
| distribution | — | 분포 | 수학 | 값들이 어떻게 퍼져 있는지, 또는 각 값이 나올 가능성이 얼마인지 나타낸 것 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 2.3 |
| distribution shift | — | 분포 변화 | 데이터 | 학습 데이터와 실제 입력의 distribution이 다른 것. 모델 성능이 떨어지는 흔한 원인이다 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 13.6 |
| DPO | direct preference optimization | — | 학습과정 | reward model과 reinforcement learning 과정 없이 preference pair에서 바로 모델을 최적화하는 post-training 방법 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.5 |
| environment | — | 환경 | 학습신호 | reinforcement learning에서 모델의 action을 받아 그 결과와 reward를 돌려주는 바깥 세계. 예: 게임 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.1 |
| experience | — | 경험 | 데이터 | Mitchell의 학습 정의에서 프로그램이 배우는 재료. 데이터나 연습 시행이 해당한다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| expert system | — | 전문가 시스템 | 시스템 | 전문가의 지식을 「만약 ~이면 ~이다」 규칙으로 적어 넣어 판단하게 하는 프로그램 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| feature | — | 특징 | 데이터 | 모델이 판단에 쓰는, 입력에서 뽑은 정보 조각. 고전 machine learning에서는 사람이 고르고 deep learning에서는 학습이 만든다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| feature engineering | — | 특징 공학 | 학습과정 | 모델에 넣을 feature를 사람이 뽑고 고르는 일. deep learning에서는 학습이 대신한다 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 3.9 |
| federated learning | — | 연합 학습 | 학습과정 | 데이터를 한곳에 모으지 않고 여러 기기에서 학습한 결과만 모으는 방식 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.10 |
| fine-tuning | — | 파인튜닝 | 학습과정 | pre-trained model을 특정 task나 형식에 맞춰 더 학습하는 것. 이 책은 label 데이터로 하는 supervised 추가 학습이라는 좁은 뜻으로 쓴다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.1 |
| forward pass | — | 순전파 | 수학 | 입력에서 출력 쪽으로 모델의 계산을 한 번 따라가는 것. inference는 forward pass만 한다 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 4.2 |
| foundation model | — | 파운데이션 모델 | 규모·활용 | 넓은 데이터로 대규모 학습해 여러 task에 맞춰 고쳐 쓸 수 있는 모델 | [1.2](../part01-big-picture/01-02-naming-axes.md), 1.6 |
| freezing | — | 층 고정 | 학습과정 | 일부 layer의 weight를 고정해 학습하지 않는 것. 보통 앞쪽 layer를 고정하고 뒤쪽만 학습한다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.1 |
| full fine-tuning | — | 전체 파인튜닝 | 학습과정 | pre-trained model의 모든 weight를 고치는 fine-tuning | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.1 |
| GAN | generative adversarial network | 생성적 적대 신경망 | 방식 | 데이터를 만드는 neural network와 진짜인지 가려내는 neural network를 경쟁시키며 배우는 generative model | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.4 |
| generative model | — | 생성 모델 | 방식 | 글이나 이미지 같은 데이터를 새로 만들어 내는 모델 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.4 |
| head | — | — | 구조 | 모델 끝에서 최종 출력을 만드는 부분. task에 맞춰 바꿔 단다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 6.4 |
| image classification | — | 이미지 분류 | 과제 | 사진 전체에 class 하나를 매기는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.2 |
| image-text-to-text | — | — | 과제 | 이미지와 글을 받아 글을 내는 task. VLM이 하는 task다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.2 |
| in-context learning | — | — | 학습과정 | weight를 바꾸지 않고 prompt에 넣은 설명과 예시만으로 원하는 동작을 끌어내는 것 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.2 |
| inference | — | 추론 | 시스템 | 학습된 모델의 weight를 고정한 채 새 입력의 출력을 계산하는 일 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 7.2, 13.2 |
| instance segmentation | — | 인스턴스 분할 | 과제 | 물체마다 그 물체에 속한 픽셀 묶음(mask)과 class를 출력하는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.7 |
| instruction tuning | — | — | 학습과정 | 지시를 따르도록 「지시 → 좋은 답」 데이터로 더 학습하는 것 | [1.2](../part01-big-picture/01-02-naming-axes.md), 9.3 |
| knowledge base | — | 지식 베이스 | 분야 | 세상에 관한 지식을 형식 언어의 문장으로 적어 두고 논리 규칙으로 추론하게 하는 AI 방식 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| label | — | 라벨 | 데이터 | 입력마다 붙인 정답. 예: 사진에 붙인 「고양이」 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.3](../part01-big-picture/01-03-model-lifecycle.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 6.9 |
| labeling | annotation | 라벨링 | 데이터 | 데이터마다 label을 붙이는 일 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 6.9 |
| language model | LM | 언어 모델 | 과제 | 글에서 다음 token이 나올 확률을 계산하는 모델. 이 확률로 글을 이어 쓴다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.2](../part01-big-picture/01-02-naming-axes.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 7.2 |
| layer | — | 층 | 구조 | neural network를 이루는 계산 단위 하나. 입력을 변환한 결과를 다음 layer로 넘긴다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.2](../part01-big-picture/01-02-naming-axes.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 4.2 |
| learning to rank | — | 순위 학습 | 과제 | 여러 항목의 순서를 맞히도록 배우는 학습. 검색 결과 정렬에 쓴다 | [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| LLM | large language model | 대규모 언어 모델 | 규모·활용 | parameter가 아주 많은 language model. 몇 개부터 large인지 정한 공식 기준은 없다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 7.2 |
| logistic regression | — | 로지스틱 회귀 | 구조 | feature에 weight를 곱해 더한 값으로 두 부류 중 한쪽일 확률을 계산하는 고전 machine learning 모델 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), 3.9 |
| LoRA | low-rank adaptation | — | 학습과정 | 원래 weight는 고정하고, 작은 matrix 두 개의 곱으로 나타낸 변화량만 학습하는 PEFT 방법 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.4 |
| loss | — | 손실 | 수학 | 모델의 출력이 정답과 얼마나 다른지 나타낸 값. 학습은 이 값을 줄이는 방향으로 weight를 고친다 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.1, 4.4 |
| machine learning | ML | 머신러닝 | 분야 | 동작 규칙을 사람이 짜 넣지 않고 데이터에서 배우게 하는 AI의 방법 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| mask | — | 마스크 | 과제 | 사진에서 한 물체나 한 class에 속한 픽셀을 표시한 것. segmentation이 출력한다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.7 |
| modality | — | 모달리티 | 분야 | 글·이미지·음성·영상 같은 데이터의 종류 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.7 |
| multi-task learning | — | 다중 과제 학습 | 학습과정 | 여러 task를 한 모델로 함께 배우는 방식 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.10 |
| multimodal | — | 멀티모달 | 분야 | 둘 이상의 modality를 함께 다루는 것 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.2 |
| natural language processing | NLP | 자연어 처리 | 분야 | 사람의 언어로 쓴 글을 다루는 AI 분야 | [1.2](../part01-big-picture/01-02-naming-axes.md) |
| neural network | — | 신경망 | 구조 | 단순한 계산 layer를 여러 겹 이어 붙인 모델. 뇌의 신경세포에서 이름을 따왔지만 뇌를 흉내 낸 모형은 아니다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.2](../part01-big-picture/01-02-naming-axes.md), 4.2 |
| next-token prediction | — | 다음 토큰 예측 | 학습신호 | 앞의 token들을 보고 다음 token을 맞히는 학습 목표. language model pre-training의 기본 방식이다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 8.2 |
| noise | — | 잡음 | 데이터 | 데이터에 섞인 무작위 값. diffusion model은 noise를 더하고 걷어 내며 배운다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.5 |
| object detection | — | 객체 검출 | 과제 | 사진 속 물체마다 위치(bounding box)·class·confidence score를 출력하는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.5 |
| offline inference | static inference | 오프라인 추론 | 시스템 | 미리 한꺼번에 예측을 계산해 저장해 두고, 요청이 오면 저장한 결과를 꺼내 주는 방식 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 13.2 |
| offline learning | — | 오프라인 학습 | 학습과정 | 미리 모아 둔 데이터로만 학습하는 방식 | [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| online inference | dynamic inference | 온라인 추론 | 시스템 | 요청이 올 때마다 그 자리에서 모델을 돌려 결과를 돌려주는 방식 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 13.2 |
| online learning | — | 온라인 학습 | 학습과정 | 학습하는 동안 새 데이터를 받거나 스스로 만들며 배우는 방식 | [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| panoptic segmentation | — | 파놉틱 분할 | 과제 | 모든 픽셀에 class를 매기고, 셀 수 있는 물체의 픽셀에는 물체 번호까지 매기는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.7 |
| parameter | — | 파라미터 | 구조 | 모델 안에서 학습으로 정해지는 숫자를 통틀어 부르는 말. weight가 대부분을 차지한다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 3.1 |
| patch | — | 패치 | 데이터 | 이미지를 잘게 자른 작은 조각. ViT는 patch를 token처럼 늘어놓아 입력한다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.3 |
| PEFT | parameter-efficient fine-tuning | 효율적 파인튜닝 | 학습과정 | 원래 weight는 그대로 두고 작게 덧붙인 weight만 학습하는 fine-tuning. LoRA가 대표적이다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.4 |
| performance measure | — | 성능 척도 | 평가 | Mitchell의 학습 정의에서 성능을 재는 기준. 예: 맞힌 비율, 이긴 비율 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| policy | — | 정책 | 학습신호 | reinforcement learning에서 상황마다 어떤 action을 고를지 정하는 행동 방식. language model에서는 모델 자체가 policy다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.1 |
| post-training | — | 사후학습 | 학습과정 | pre-training 뒤 모델을 다듬는 학습을 통틀어 부르는 업계 관례 용어. SFT·preference optimization·reinforcement learning을 포함한다 | [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| PPO | proximal policy optimization | — | 학습과정 | policy를 한 번에 너무 크게 바꾸지 않도록 제한하며 학습하는 reinforcement learning 알고리즘. RLHF에서 널리 쓴다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.3 |
| pre-trained model | — | 사전학습 모델 | 규모·활용 | pre-training을 마친 모델. fine-tuning의 출발점이 된다 | [1.2](../part01-big-picture/01-02-naming-axes.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 8.1 |
| pre-training | — | 사전학습 | 학습과정 | 큰 데이터로 넓고 일반적인 representation을 먼저 배우는 단계 | [1.2](../part01-big-picture/01-02-naming-axes.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 8.1 |
| preference | — | 선호 | 데이터 | 두 결과 중 어느 쪽이 나은지 고른 판단 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.4 |
| preference learning | — | 선호 학습 | 학습신호 | 두 결과 중 어느 쪽이 나은지 비교한 데이터로 배우는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.4 |
| preference optimization | — | 선호 최적화 | 학습과정 | preference pair로 모델을 바로 최적화하는 post-training 방법을 통틀어 부르는 말. DPO가 대표적이다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.5 |
| preference pair | — | 선호 쌍 | 데이터 | 같은 입력에 대한 두 답과, 그중 어느 쪽이 나은지의 판단을 묶은 데이터 한 건 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.4 |
| probability distribution | — | 확률 분포 | 수학 | 가능한 결과마다 확률을 매긴 것. 모든 확률의 합은 1이다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 2.3 |
| prompt | — | 프롬프트 | 규모·활용 | 모델에 넣는 지시나 질문 글 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.2 |
| pseudo-label | — | — | 데이터 | 사람이 아니라 모델이 예측해서 붙인 label | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.6 |
| reasoning model | — | 추론 모델 | 규모·활용 | 답을 내기 전에 풀이 과정을 길게 생성하도록 학습해 수학·코드 같은 문제를 잘 풀게 한 language model | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.7 |
| reinforcement learning | RL | 강화 학습 | 학습신호 | 정답 대신 action의 결과에 대한 reward를 받아, reward가 커지도록 policy를 고치는 학습 틀 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.1 |
| representation | — | 표현 | 구조 | 모델 안에서 입력을 나타내는 숫자 배열. 학습이 잘 되면 비슷한 입력은 비슷한 representation을 갖는다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 8.1 |
| representation learning | — | 표현 학습 | 분야 | feature를 사람이 고르지 않고 데이터에서 배우게 하는 machine learning | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), 8.1 |
| retraining | — | 재학습 | 학습과정 | 새로 모은 데이터를 더해 모델을 다시 학습하는 것. 배포 뒤 성능이 떨어지면 한다 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 13.6 |
| reward | — | 보상 | 학습신호 | reinforcement learning에서 action의 결과에 매기는 점수 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.1 |
| reward model | — | 보상 모델 | 학습과정 | 답이 얼마나 좋은지 점수를 매기도록 학습한 모델. RLHF에서 preference 데이터로 학습해 reward를 만든다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.4 |
| RLHF | reinforcement learning from human feedback | — | 학습과정 | 사람의 preference 비교로 reward model을 학습하고, 그 점수를 reward로 reinforcement learning하는 방법 | [1.2](../part01-big-picture/01-02-naming-axes.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.4 |
| RNN | recurrent neural network | 순환 신경망 | 구조 | 순서가 있는 데이터를 한 칸씩 읽으며 앞에서 읽은 내용을 다음 칸으로 넘기는 neural network | [1.2](../part01-big-picture/01-02-naming-axes.md), 5.3 |
| segmentation | — | 분할 | 과제 | 사진의 픽셀마다 class를 매겨 물체의 모양까지 찾는 task를 통틀어 부르는 말 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.7 |
| self-supervised learning | — | 자기지도 학습 | 학습신호 | 데이터의 일부를 가리고 맞히게 해서 데이터 스스로 정답을 만드는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.3 |
| semantic segmentation | — | 의미론적 분할 | 과제 | 픽셀마다 class를 매기는 task. 같은 class의 물체끼리는 구별하지 않는다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.7 |
| semi-supervised learning | — | 준지도 학습 | 학습신호 | label이 있는 일부 데이터와 label이 없는 데이터를 함께 쓰는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.10 |
| serving | — | 서빙 | 시스템 | 학습한 모델이 online inference나 offline inference로 예측을 내놓을 수 있게 만드는 일 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 13.2 |
| SFT | supervised fine-tuning | 지도 파인튜닝 | 학습과정 | 「지시 → 좋은 답」 쌍을 따라 하게 하는 supervised learning 방식의 fine-tuning | [1.2](../part01-big-picture/01-02-naming-axes.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.3 |
| speech | — | 음성 | 분야 | 말소리를 다루는 AI 분야 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.7 |
| speech recognition model | — | 음성 인식 모델 | 과제 | 말소리를 받아 글로 옮기는 모델 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.7 |
| supervised learning | — | 지도 학습 | 학습신호 | 입력마다 붙은 정답(label)과 비교하며 배우는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.3 |
| synthetic data | — | 합성 데이터 | 데이터 | 실제로 모은 것이 아니라 모델이나 프로그램으로 만들어 낸 학습 데이터 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 12.4 |
| task | — | 과제 | 과제 | 모델이 풀도록 정한 문제의 종류와 그 출력 형식 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.2](../part01-big-picture/01-02-naming-axes.md), [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| test set | — | 테스트 세트 | 평가 | 학습에 쓰지 않고 마지막 평가를 위해 남겨 둔 데이터 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 3.4 |
| text classification | — | 텍스트 분류 | 과제 | 글 전체에 class 하나를 매기는 task. 예: 스팸 판별 | [1.2](../part01-big-picture/01-02-naming-axes.md) |
| text generation | — | 텍스트 생성 | 과제 | 글을 받아 이어지는 글을 만드는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 7.2 |
| text-to-image | — | — | 과제 | 글을 받아 이미지를 만드는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.5 |
| token | — | 토큰 | 데이터 | 모델이 글을 처리하는 단위. 단어 하나나 단어 조각 하나에 해당한다 | [1.2](../part01-big-picture/01-02-naming-axes.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 5.4, 7.1 |
| training from scratch | — | 처음부터 학습 | 학습과정 | 사전에 학습한 weight 없이 무작위 값에서 시작해 모든 weight를 학습하는 것 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 4.11, 8.6 |
| Transformer | — | — | 구조 | attention으로 입력의 모든 위치가 서로를 참고하게 하는 neural network 구조 | [1.2](../part01-big-picture/01-02-naming-axes.md), 5.6 |
| unsupervised learning | — | 비지도 학습 | 학습신호 | 정답 없이 데이터 안의 cluster나 distribution을 찾는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.3 |
| VAE | variational autoencoder | 변분 오토인코더 | 방식 | 데이터를 작은 표현으로 줄였다가 다시 만들어 내도록 배우는 generative model | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.4 |
| verifiable reward | — | 검증 가능한 보상 | 학습신호 | 프로그램으로 맞고 틀림을 확인할 수 있는 reward. 예: 수학 답 일치, 코드 테스트 통과 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.7 |
| verifier | — | 검증기 | 시스템 | 답이 맞는지 자동으로 확인하는 프로그램이나 모델 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.7 |
| ViT | Vision Transformer | — | 구조 | 이미지를 patch로 잘라 token처럼 늘어놓고 Transformer에 넣는 구조 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.3 |
| VLM | vision-language model | 비전-언어 모델 | 분야 | 이미지와 글을 함께 다루는 모델. 범위가 문헌마다 다르다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.2 |
| weight | — | 가중치 | 구조 | 학습으로 정해지는 모델 내부의 숫자. 학습은 weight를 고치는 일이다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.2](../part01-big-picture/01-02-naming-axes.md), [1.3](../part01-big-picture/01-03-model-lifecycle.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 4.2 |
