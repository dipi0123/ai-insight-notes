# 용어집

본문에서 쓰는 용어 표기의 정본이다. 이 책은 기술 용어를 영어 원어로 쓰고, 장마다 처음 나올 때 한국어 번역어를 괄호에 단다. 한 줄 정의만 두고 자세한 설명은 「본 장」으로 간다. 링크가 없는 장 번호는 아직 실리지 않은 장이다.

- **표기**는 본문에서 쓰는 형태 그대로다. 하이픈과 띄어쓰기도 같다. 대소문자를 가리지 않고 알파벳순으로 둔다.
- **풀이·다른 이름**은 약어의 풀이, 또는 같은 뜻으로 쓰는 다른 영어 이름이다.
- **한국어**는 본문에서 처음 나올 때 괄호에 다는 번역어다. 자리 잡은 번역어가 없으면 —로 둔다.
- **분류**는 그 용어가 어느 종류의 이름인지 나타낸다: 분야 · 구조 · 과제 · 방식 · 학습신호 · 규모·활용 · 학습과정 · 평가 · 데이터 · 수학 · 시스템. 분야·구조·과제·방식·규모·활용은 [1.2장](../part01-big-picture/01-02-naming-axes.md)에서 모델 이름을 읽는 축과 같다. 1.2장의 학습 축은 [1.4장](../part01-big-picture/01-04-training-methods-map.md)의 다섯 축으로 더 나뉘는데, 신호 축의 이름은 학습신호로, 나머지 네 축(단계·바꾸는 범위·가르치는 쪽·데이터가 들어오는 방식)의 이름은 학습과정으로 분류한다.
- **본 장**은 그 용어를 정의하고 설명하는 장이다. 지나가며 쓰는 장은 올리지 않는다.

## A–Z

| 표기 | 풀이·다른 이름 | 한국어 | 분류 | 한 줄 정의 | 본 장 |
|---|---|---|---|---|---|
| accelerator | — | 가속기 | 시스템 | neural network의 계산처럼 특정 종류의 계산을 범용 CPU보다 빠르게 하도록 쓰는 하드웨어. 예: GPU, TPU | [1.6](../part01-big-picture/01-06-industry-stack.md) |
| accuracy | — | 정확도 | 평가 | 전체 예측 가운데 맞힌 예측의 비율 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md), 3.6 |
| action | — | 행동 | 학습신호 | reinforcement learning에서 모델이 내놓는 행동. language model에서는 생성한 답이 action이다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.1 |
| activation | — | — | 구조 | forward pass 중에 layer가 내놓는 중간 결과값. 학습에서는 backward 계산에 쓰려고 저장해 둔다. activation function과 다른 말이다 | [2.6](../part02-math-and-tools/02-06-dev-environment.md), 4.8 |
| activation function | — | 활성화 함수 | 구조 | layer에서 weight를 곱하고 bias를 더한 결과에 이어서 거치는, 정해진 비선형 함수 | 4.2 |
| active learning | — | 능동 학습 | 학습과정 | 모델이 label이 가장 도움이 될 데이터를 골라 label을 요청하며 배우는 방식 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.10 |
| adaptation | — | 적응 | 학습과정 | foundation model을 바탕으로 특정 task를 하는 모델을 만드는 일. 예: fine-tuning | [1.6](../part01-big-picture/01-06-industry-stack.md), 9.1 |
| anchor box | — | 앵커 박스 | 구조 | object detection에서 box를 예측할 때 바탕으로 삼는, 미리 정해 둔 기준 box. YOLO v2가 쓴다 | [1.5](../part01-big-picture/01-05-landmark-models.md) |
| architecture | — | 구조 | 구조 | 모델 안에서 layer를 어떤 모양으로 짜고 이었는지. 예: CNN, Transformer | [1.2](../part01-big-picture/01-02-naming-axes.md) |
| artificial intelligence | AI | 인공지능 | 분야 | 사람의 지능이 필요하다고 여기는 일을 컴퓨터가 하게 만드는 분야 전체 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| attention | — | — | 구조 | 입력의 각 위치가 다른 위치를 얼마나 참고할지 계산해 정보를 모으는 계산. Transformer의 핵심이다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 5.5 |
| autoencoder | — | 오토인코더 | 구조 | 입력을 작은 숫자 배열로 압축하는 encoder와, 그것에서 입력을 되살리는 decoder를 함께 학습한 모델 | [1.5](../part01-big-picture/01-05-landmark-models.md), 11.4 |
| autograd | — | — | 시스템 | PyTorch의 automatic differentiation. 계산을 실행하는 동안 graph를 기록하고, backward()를 부르면 그 graph를 거꾸로 따라 leaf tensor의 gradient를 계산한다 | [2.5](../part02-math-and-tools/02-05-pytorch-basics.md), 4.3 |
| automatic differentiation | — | 자동 미분 | 수학 | 계산의 중간 단계마다 chain rule을 적용해 gradient를 기호식이나 수치 근사 없이 계산하는 방법. backpropagation은 그 한 경우다 | [2.2](../part02-math-and-tools/02-02-derivatives-gradients.md), [2.5](../part02-math-and-tools/02-05-pytorch-basics.md), 4.3 |
| automatic speech recognition | — | 자동 음성 인식 | 과제 | 말소리를 받아 글로 옮기는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.7 |
| autoregressive model | — | 자기회귀 모델 | 방식 | 앞에서 만든 출력을 보고 다음 조각을 하나씩 이어 붙여 출력을 만드는 모델 | [1.2](../part01-big-picture/01-02-naming-axes.md), 7.2 |
| axis | — | 축 | 수학 | 숫자 배열에서 숫자를 늘어놓는 방향 하나. 배열의 axis 수를 NumPy는 ndim이라 부른다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| backpropagation | — | 역전파 | 수학 | 출력에서 거꾸로 거슬러 가며 weight마다 loss를 줄이려면 어느 쪽으로 고쳐야 하는지 계산하는 방법 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 4.3 |
| base model | — | 베이스 모델 | 규모·활용 | pre-training만 하고 지시를 따르도록 더 학습하지 않은 language model을 흔히 부르는 이름 | [1.2](../part01-big-picture/01-02-naming-axes.md), 9.3 |
| batch | — | 배치 | 학습과정 | 한 번에 함께 계산하려고 묶은 입력들. tensor에서는 맨 앞 axis로 둔다 | 4.1 |
| Bernoulli distribution | — | 베르누이 분포 | 수학 | 0 또는 1을 갖는 random variable의 distribution. 1이 나올 확률 하나로 정해진다. 두 class 분류의 출력이 이것이다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| bfloat16 | Brain floating point | — | 시스템 | 부호·지수·가수 비트가 1-8-7인 16비트 부동소수점 dtype. 같은 16비트인 float16(1-5-10)과 비트 나눔이 다르다 | [2.5](../part02-math-and-tools/02-05-pytorch-basics.md), 4.8 |
| bias | — | 편향 | 구조 | layer에서 입력에 weight를 곱한 결과에 더하는, 학습으로 정해지는 숫자 | 4.2 |
| binary cross-entropy | — | 이진 교차 엔트로피 | 수학 | class가 둘일 때의 cross-entropy −[y log q + (1 − y) log(1 − q)]. y는 0 또는 1인 정답, q는 label이 1일 확률이다 | [2.4](../part02-math-and-tools/02-04-information-theory.md) |
| bit | — | — | 수학 | 밑이 2인 log로 잰 정보량의 단위. 확률 1/2인 사건의 정보량이 1 bit이고, 1 bit는 log 2 ≈ 0.693 nat이다 | [2.4](../part02-math-and-tools/02-04-information-theory.md) |
| bounding box | box | 경계 상자 | 과제 | 사진 속 물체를 둘러싼 사각형. object detection이 물체의 위치로 출력한다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.5 |
| broadcasting | — | 브로드캐스팅 | 수학 | shape가 다른 두 배열을 원소별로 계산할 때, 맨 뒤 axis부터 비교해 크기 1이거나 없는 axis를 상대 크기에 맞춰 늘린 것처럼 계산하는 규칙 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| calibration | — | 보정 | 평가 | 모델이 낸 확률이 실제 정답률과 맞는 정도. 또는 맞도록 고치는 일 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| categorical distribution | multinoulli distribution | 범주형 분포 | 수학 | 유한한 K개 값 중 하나를 갖는 random variable의 distribution. 값마다의 확률을 담은 vector로 정해진다. 분류 출력과 다음 token의 distribution이 이것이다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| chain rule | — | 연쇄 법칙 | 수학 | 이어 붙인 함수의 derivative는 단계마다의 derivative를 곱한 것이라는 규칙. 한 값이 여러 경로로 쓰이면 경로마다의 곱을 더한다 | [2.2](../part02-math-and-tools/02-02-derivatives-gradients.md) |
| chain rule of probability | product rule of probability | 확률의 연쇄 법칙 | 수학 | joint probability를 한 변수씩의 conditional probability의 곱으로 쪼개는 규칙. 문장의 확률을 다음 token 확률의 곱으로 쓰는 근거다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| channel | — | 채널 | 데이터 | 이미지 tensor에서 픽셀마다 따로 담는 값 한 종류, 또는 그 값들을 모은 (H, W) 배열 하나. 컬러 이미지는 red·green·blue 세 channel을 가진다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| checkpoint | — | 체크포인트 | 시스템 | 학습 중간이나 끝에 모델의 parameter 값을 저장한 것 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 4.10 |
| class | — | 클래스 | 과제 | 모델이 구별하는 부류 하나. 예: cat, dog | [1.2](../part01-big-picture/01-02-naming-axes.md) |
| classifier | — | 분류기 | 과제 | classification task를 푸는 모델 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.2 |
| cluster | — | 군집 | 데이터 | 서로 비슷한 데이터끼리 모인 묶음 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.9 |
| CNN | convolutional neural network | 합성곱 신경망 | 구조 | 작은 창을 입력 위로 옮겨 가며 같은 계산을 되풀이하는 layer를 쌓은 neural network. 이미지에 오래 써 온 구조다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 5.1 |
| column vector | — | 열벡터 | 수학 | 원소를 열 하나로 세워 적은 vector. 열이 하나인 matrix로 볼 수 있고, 이 책의 수식은 따로 밝히지 않으면 vector를 column vector로 쓴다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| computational graph | — | 계산 그래프 | 수학 | 계산을 operation 단위로 쪼개, 변수를 node로 두고 operation의 입력에서 출력으로 화살표를 그은 그림 | [2.2](../part02-math-and-tools/02-02-derivatives-gradients.md) |
| computer vision | CV | 컴퓨터 비전 | 분야 | 이미지와 영상을 다루는 AI 분야 | [1.2](../part01-big-picture/01-02-naming-axes.md) |
| concept drift | — | — | 데이터 | 입력과 정답의 관계가 시간이 지나며 바뀌는 것. 모델의 예측이 점점 틀리게 된다 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 13.6 |
| conditional probability | — | 조건부 확률 | 수학 | 어떤 사건이 일어났다는 조건에서 다른 사건이 일어날 확률. joint probability를 조건의 확률로 나눠 구한다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| confidence score | — | 신뢰도 점수 | 과제 | 모델이 자기 예측을 얼마나 확신하는지 나타낸 점수. object detection에서는 box마다 붙는다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.5 |
| continual learning | lifelong learning | 연속 학습 | 학습과정 | task나 데이터가 바뀌어 가는 동안 이어서 배우는 방식. 앞서 배운 것을 잊는 문제가 따라온다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.10, 9.5 |
| continual pre-training | — | 추가 사전학습 | 학습과정 | pre-trained model을 특정 분야 데이터로 pre-training과 같은 방식으로 더 학습하는 것 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 8.5 |
| continuous random variable | — | 연속 확률 변수 | 수학 | 실수값을 갖는 random variable | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| contrastive learning | — | 대조 학습 | 학습신호 | 맞는 짝과 틀린 짝을 가려내도록 배우는 학습. 예: 어느 설명 글이 어느 사진의 것인지 맞히기 | [1.2](../part01-big-picture/01-02-naming-axes.md), 8.3, 11.1 |
| cosine similarity | — | 코사인 유사도 | 수학 | 두 vector의 dot product를 두 norm의 곱으로 나눈 값. 길이와 상관없이 방향이 같은 정도를 −1에서 1 사이로 잰다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| cross-entropy | — | 교차 엔트로피 | 수학 | 실제 distribution p에서 나온 결과를 모델 distribution q의 확률로 잰 정보량의 expectation −Σ p log q. 정답이 one-hot이면 정답 class 확률의 −log, 곧 negative log-likelihood이고 분류 loss로 쓴다 | [2.4](../part02-math-and-tools/02-04-information-theory.md), 4.4 |
| CUDA | — | — | 시스템 | NVIDIA GPU에서 돌 코드를 쓰게 하는 NVIDIA의 기술. PyTorch는 NVIDIA GPU를 device cuda로 부른다 | [1.6](../part01-big-picture/01-06-industry-stack.md), [2.5](../part02-math-and-tools/02-05-pytorch-basics.md) |
| curriculum learning | — | 커리큘럼 학습 | 학습과정 | 쉬운 데이터부터 어려운 데이터 순으로 배우게 짜는 방식 | [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| data cleaning | — | 데이터 정제 | 데이터 | 모은 데이터에서 부정확하거나 지저분한 기록을 걸러 내는 일 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 8.4 |
| data-generating distribution | — | 데이터 생성 분포 | 데이터 | 학습·평가 예제를 모두 만들어 낸다고 가정하는 공통의 probability distribution | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| dataset | — | 데이터셋 | 데이터 | 학습이나 평가에 쓰려고 모아 둔 데이터 묶음 | [1.3](../part01-big-picture/01-03-model-lifecycle.md) |
| dataset card | — | 데이터셋 카드 | 데이터 | Hugging Face Hub의 dataset repository에 있는 README.md. 라이선스·언어·크기 같은 메타데이터와 dataset 설명을 담는다 | [2.6](../part02-math-and-tools/02-06-dev-environment.md) |
| dataset repository | — | 데이터셋 저장소 | 시스템 | Hugging Face Hub에서 dataset 하나의 데이터 파일과 dataset card를 담은 Git 저장소 | [2.6](../part02-math-and-tools/02-06-dev-environment.md) |
| datasets | — | — | 시스템 | Hugging Face의 Python 라이브러리. Hub의 dataset을 내려받아 Apache Arrow 형식으로 캐시하고 split별로 돌려준다 | [2.6](../part02-math-and-tools/02-06-dev-environment.md) |
| decoder | — | 디코더 | 구조 | 모델 안에서 숫자 배열로부터 출력을 만드는 부분. Transformer의 decoder는 출력을 하나씩, 앞서 만든 출력을 다시 받으며 이어 만든다 | [1.5](../part01-big-picture/01-05-landmark-models.md), 5.7 |
| deep learning | — | 딥러닝 | 분야 | 여러 layer를 쌓은 neural network로 feature까지 데이터에서 배우는 machine learning의 한 갈래 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| deep learning framework | — | 딥러닝 프레임워크 | 시스템 | 숫자 배열 계산, 미분의 자동 계산, 여러 종류의 칩에서의 실행을 맡아 모델 코드가 칩에 덜 묶이게 하는 라이브러리. 예: PyTorch, JAX, TensorFlow | [1.6](../part01-big-picture/01-06-industry-stack.md), [2.5](../part02-math-and-tools/02-05-pytorch-basics.md) |
| demonstration | — | 시범 답 | 데이터 | 사람이 직접 써서 보여 주는 바람직한 답. SFT의 학습 데이터가 된다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.3 |
| derivative | — | 도함수 | 수학 | 입력이 하나인 함수에서 입력을 조금 바꿀 때 출력이 변하는 배율. 그래프에서는 그 점의 접선의 기울기다 | [2.2](../part02-math-and-tools/02-02-derivatives-gradients.md) |
| detection model | — | 검출 모델 | 과제 | 사진 속 물체마다 위치와 종류를 출력하는 모델 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 6.5 |
| detector | — | 검출기 | 과제 | object detection task를 푸는 모델 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.5 |
| device | — | 장치 | 시스템 | PyTorch에서 tensor가 놓여 계산되는 장치. 예: cpu, cuda, mps. 함께 계산하는 tensor는 같은 device에 있어야 한다(CPU의 scalar tensor만 예외) | [2.5](../part02-math-and-tools/02-05-pytorch-basics.md) |
| diffusion model | — | 확산 모델 | 방식 | 데이터에 noise를 더해 가는 과정을 거꾸로 되돌리도록 배워, noise에서 시작해 데이터를 만드는 generative model | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.5 |
| directional derivative | — | 방향 도함수 | 수학 | 길이가 1인 vector 방향으로 움직일 때 함수의 기울기. 그 vector와 gradient의 dot product와 같다 | [2.2](../part02-math-and-tools/02-02-derivatives-gradients.md) |
| discrete random variable | — | 이산 확률 변수 | 수학 | 가질 수 있는 값의 수가 유한하거나 셀 수 있는 random variable. 값은 정수가 아니라 이름 붙은 상태여도 된다. 예: 주사위 눈, class | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| distillation | knowledge distillation | 증류 | 학습과정 | 큰 teacher 모델의 출력을 작은 student 모델이 따라 하게 해서 배우는 방법 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.6 |
| distribution | — | 분포 | 수학 | 값들이 어떻게 퍼져 있는지, 또는 각 값이 나올 가능성이 얼마인지 나타낸 것 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| distribution shift | — | 분포 변화 | 데이터 | 학습 데이터와 실제 입력의 distribution이 다른 것. 모델 성능이 떨어지는 흔한 원인이다 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 13.6 |
| dot product | — | 내적 | 수학 | 차원이 같은 두 vector에서 같은 자리의 원소끼리 곱해 모두 더한 값 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| DPO | direct preference optimization | — | 학습과정 | reward model과 reinforcement learning 과정 없이 preference pair에서 바로 모델을 최적화하는 post-training 방법 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.5 |
| dtype | data type | 데이터 타입 | 시스템 | 배열이나 tensor의 원소를 담는 숫자 형식. 예: float32, float64, int64 | [2.5](../part02-math-and-tools/02-05-pytorch-basics.md) |
| element-wise product | Hadamard product | 원소별 곱 | 수학 | shape가 같은 두 배열에서 같은 자리의 원소끼리 곱한 것. matrix multiplication과 다른 계산이다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| embedding | — | 임베딩 | 구조 | 넓게는 모델 안 어느 layer에서든 꺼낸, 입력을 나타내는 숫자 배열. 흔히 embedding layer가 범주마다 학습한 숫자 배열을 가리키고, 비슷한 것은 비슷한 embedding을 갖는다. 예: CLIP은 짝이 맞는 이미지와 글의 embedding이 가까워지도록 배운다 | [1.5](../part01-big-picture/01-05-landmark-models.md), 5.4 |
| empirical distribution | — | 경험 분포 | 데이터 | 학습 데이터가 정하는 distribution. 학습 데이터에서 예제 하나를 무작위로 고를 때의 distribution이다. maximum likelihood는 이것과 모델 distribution 사이의 KL divergence를 줄인다 | [2.4](../part02-math-and-tools/02-04-information-theory.md) |
| encoder | — | 인코더 | 구조 | 모델 안에서 입력을 읽어 숫자 배열로 바꾸는 부분 | [1.5](../part01-big-picture/01-05-landmark-models.md), 5.7 |
| encoder-decoder | — | 인코더-디코더 | 구조 | encoder와 decoder를 모두 둔 구조. 처음 나온 Transformer와 Whisper가 이 구조다 | [1.5](../part01-big-picture/01-05-landmark-models.md), 5.7 |
| entropy | Shannon entropy | 엔트로피 | 수학 | distribution에서 뽑은 사건의 정보량의 expectation −Σ p log p. 고르게 퍼질수록 크고(값이 K개이면 최대 log K), 한 값에 몰리면 0이다 | [2.4](../part02-math-and-tools/02-04-information-theory.md) |
| environment | — | 환경 | 학습신호 | reinforcement learning에서 모델의 action을 받아 그 결과와 reward를 돌려주는 바깥 세계. 예: 게임 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.1 |
| Euclidean distance | — | 유클리드 거리 | 수학 | 두 점의 같은 자리 원소끼리 뺀 차이를 제곱해 더하고 제곱근을 씌운 거리. 원점에서 점까지의 Euclidean distance가 L2 norm이다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| expectation | — | 기댓값 | 수학 | random variable의 값(또는 그 함수의 값)을 확률로 가중해 평균 낸 값 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| expected calibration error | ECE | 기대 보정 오차 | 평가 | confidence 구간마다 accuracy와 평균 confidence의 차이를 구간의 예제 비율로 가중 평균한 값 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| experience | — | 경험 | 데이터 | Mitchell의 학습 정의에서 프로그램이 배우는 재료. 데이터나 연습 시행이 해당한다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| feature | — | 특징 | 데이터 | 모델이 판단에 쓰는, 입력에서 뽑은 정보 조각. 고전 machine learning에서는 사람이 고르고 deep learning에서는 학습이 만든다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| feature engineering | — | 특징 공학 | 학습과정 | 모델에 넣을 feature를 사람이 뽑고 고르는 일. deep learning에서는 학습이 대신한다 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 3.9 |
| federated learning | — | 연합 학습 | 학습과정 | 데이터를 한곳에 모으지 않고 여러 기기에서 학습한 결과만 모으는 방식 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.10 |
| few-shot | — | — | 규모·활용 | task 설명과 함께 예시 몇 개를 입력 글에 넣어, 추가 학습 없이 task를 풀게 하는 것 | [1.5](../part01-big-picture/01-05-landmark-models.md) |
| fine-tuning | — | 파인튜닝 | 학습과정 | pre-trained model을 특정 task나 형식에 맞춰 더 학습하는 것. 이 책은 label 데이터로 하는 supervised 추가 학습이라는 좁은 뜻으로 쓴다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.1 |
| finite difference | — | 유한 차분 | 수학 | 입력을 작은 값만큼 바꿔 본 출력의 차이로 derivative를 어림하는 방법. gradient 계산을 검산하는 데 쓴다 | [2.2](../part02-math-and-tools/02-02-derivatives-gradients.md) |
| float32 | — | — | 시스템 | 원소 하나를 32비트 IEEE 754 부동소수점으로 담는 dtype. PyTorch의 기본 부동소수점 dtype이다 | [2.5](../part02-math-and-tools/02-05-pytorch-basics.md) |
| forward pass | — | 순전파 | 수학 | 입력에서 출력 쪽으로 모델의 계산을 한 번 따라가는 것. inference는 forward pass만 한다 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 4.2 |
| foundation model | — | 파운데이션 모델 | 규모·활용 | 넓은 데이터로 대규모 학습해 여러 task에 맞춰 고쳐 쓸 수 있는 모델 | [1.2](../part01-big-picture/01-02-naming-axes.md), [1.6](../part01-big-picture/01-06-industry-stack.md) |
| freezing | — | 층 고정 | 학습과정 | 일부 layer의 weight를 고정해 학습하지 않는 것. 보통 앞쪽 layer를 고정하고 뒤쪽만 학습한다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.1 |
| full fine-tuning | — | 전체 파인튜닝 | 학습과정 | pre-trained model의 모든 weight를 고치는 fine-tuning | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.1 |
| GAN | generative adversarial network | 생성적 적대 신경망 | 방식 | 데이터를 만드는 neural network와, 데이터가 학습 데이터에서 왔는지 만든 것인지 가려내는 neural network를 경쟁시키며 함께 배우고, 다 배운 뒤에는 만드는 쪽에 무작위 noise를 넣어 데이터를 만드는 generative model | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.4 |
| generative model | — | 생성 모델 | 방식 | 글이나 이미지 같은 데이터를 새로 만들어 내는 모델 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.4 |
| GPU | graphics processing unit | 그래픽 처리 장치 | 시스템 | 원래 그래픽용으로 개발된, 많은 계산을 나란히 하는 칩. deep learning의 학습과 inference에 널리 쓴다 | [1.6](../part01-big-picture/01-06-industry-stack.md), [2.6](../part02-math-and-tools/02-06-dev-environment.md) |
| GPU memory | — | GPU 메모리 | 시스템 | GPU에 달린 메모리. 학습할 때는 weight, gradient, optimizer 상태, activation이 모두 여기에 들어가야 한다 | [2.6](../part02-math-and-tools/02-06-dev-environment.md), 4.8 |
| gradient | — | 기울기 | 수학 | 입력이 여럿이고 출력이 scalar인 함수에서 partial derivative를 모두 모은 vector. 함수가 가장 빨리 커지는 방향을 가리키고, parameter와 shape가 같다 | [2.2](../part02-math-and-tools/02-02-derivatives-gradients.md) |
| gradient descent | steepest descent | 경사 하강법 | 학습과정 | gradient의 반대 방향으로 parameter를 조금씩 옮겨 loss를 줄이는 방법 | 3.1, 3.2 |
| head | — | — | 구조 | 모델 끝에서 최종 출력을 만드는 부분. task에 맞춰 바꿔 단다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 6.4 |
| Hugging Face Hub | — | — | 시스템 | 모델과 dataset을 Git 저장소로 올려 두고 내려받게 하는 곳. 저장소마다 revision을 고정해 받을 수 있다 | [2.6](../part02-math-and-tools/02-06-dev-environment.md) |
| i.i.d. | independent and identically distributed | 독립 동일 분포 | 데이터 | 데이터의 예제들이 서로 independent하고 모두 같은 distribution에서 뽑혔다는 가정 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| identity matrix | — | 단위 행렬 | 수학 | 왼쪽 위에서 오른쪽 아래로 가는 대각선의 원소가 모두 1이고 나머지가 0인 정사각 matrix. 곱한 vector를 바꾸지 않는다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| image classification | — | 이미지 분류 | 과제 | 사진 전체에 class 하나를 매기는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.2 |
| image-text-to-text | — | — | 과제 | 이미지와 글을 받아 글을 내는 task. language model에 이미지를 받는 부분을 이어 붙인 VLM이 이 task를 한다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.2 |
| in-context learning | — | — | 학습과정 | weight를 바꾸지 않고 prompt에 넣은 설명과 예시만으로 원하는 동작을 끌어내는 것 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.2 |
| independence | independent | 독립 | 수학 | 두 random variable의 joint probability가 모든 값에서 각자의 확률의 곱이 되는 성질. 한쪽 값을 알아도 다른 쪽의 확률이 바뀌지 않는다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| inference | — | 추론 | 시스템 | 학습된 모델의 weight를 고정한 채 새 입력의 출력을 계산하는 일 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 7.2, 13.2 |
| inference server | — | 추론 서버 | 시스템 | weight를 칩의 메모리에 올려 두고 들어오는 요청마다 inference를 돌려 결과를 돌려주는 서버 소프트웨어 | [1.6](../part01-big-picture/01-06-industry-stack.md), 13.2 |
| information theory | — | 정보 이론 | 분야 | 정보의 양을 확률로 재는 수학 분야. entropy·cross-entropy·KL divergence가 여기서 나온다 | [2.4](../part02-math-and-tools/02-04-information-theory.md) |
| instance segmentation | — | 인스턴스 분할 | 과제 | 물체마다 그 물체에 속한 픽셀 묶음(mask)과 class를 출력하는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.7 |
| instruction tuning | — | — | 학습과정 | 지시를 따르도록 「지시 → 좋은 답」 데이터로 더 학습하는 것 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.3 |
| Jacobian | Jacobian matrix | 야코비 행렬 | 수학 | vector를 받아 vector를 내는 함수에서 출력 원소마다, 입력 원소마다의 partial derivative를 모은 matrix. 행이 출력, 열이 입력이다 | [2.2](../part02-math-and-tools/02-02-derivatives-gradients.md) |
| joint probability | — | 결합 확률 | 수학 | 두 개 이상의 random variable이 동시에 각자의 값을 가질 확률 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| KL divergence | Kullback-Leibler divergence, relative entropy | KL 발산 | 수학 | 두 distribution p, q의 차이를 재는 양 Σ p log(p/q) = H(p, q) − H(p). 0 이상이고 두 distribution이 같을 때만 0이며, 순서를 바꾸면 값이 달라질 수 있어(대칭이 아니어서) 거리가 아니다 | [2.4](../part02-math-and-tools/02-04-information-theory.md) |
| knowledge base | — | 지식 베이스 | 분야 | 세상에 관한 지식을 형식 언어의 문장으로 적어 두고 논리 규칙으로 추론하게 하는 AI 방식 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| label | — | 라벨 | 데이터 | 입력마다 붙인 정답. 예: 사진에 붙인 「고양이」 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.3](../part01-big-picture/01-03-model-lifecycle.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 6.9 |
| labeling | annotation | 라벨링 | 데이터 | 데이터마다 label을 붙이는 일 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 6.9 |
| language model | LM | 언어 모델 | 과제 | 글 속에서 token이 나올 확률을 계산하는 모델. 글을 만드는 language model은 흔히 앞의 token을 보고 다음 token의 확률을 계산해 글을 이어 쓴다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.2](../part01-big-picture/01-02-naming-axes.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 7.2 |
| latent diffusion | — | 잠재 확산 | 방식 | 이미지의 픽셀이 아니라 autoencoder로 압축한 공간(latent 공간)에서 diffusion을 하는 방식. Stable Diffusion이 쓴다 | [1.5](../part01-big-picture/01-05-landmark-models.md), 11.5 |
| layer | — | 층 | 구조 | neural network를 이루는 계산 단위 하나. 입력을 변환한 결과를 다음 layer로 넘긴다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.2](../part01-big-picture/01-02-naming-axes.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 4.2 |
| learning rate | — | 학습률 | 학습과정 | gradient descent에서 parameter를 한 번에 얼마나 움직일지 정하는 양수 | 3.2, 4.5 |
| learning to rank | — | 순위 학습 | 과제 | 여러 항목의 순서를 맞히도록 배우는 학습. 검색 결과 정렬에 쓴다 | [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| likelihood | — | 가능도 | 수학 | 관측한 데이터를 고정하고, 모델이 그 데이터에 준 확률을 parameter의 함수로 본 것 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| linear combination | — | 선형 결합 | 수학 | vector 여러 개에 각각 scalar를 곱해 더한 것 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| linearly independent | — | 선형 독립 | 수학 | vector 집합에서 어느 vector도 나머지 vector의 linear combination이 아닌 성질 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| LLM | large language model | 대규모 언어 모델 | 규모·활용 | parameter가 아주 많은 language model. 몇 개부터 large인지 정한 공식 기준은 없다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 7.2 |
| log-likelihood | — | 로그 가능도 | 수학 | likelihood의 log. 서로 독립인 예제들의 확률의 곱이 log 확률의 합이 된다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| logistic regression | — | 로지스틱 회귀 | 구조 | feature에 weight를 곱해 더한 값으로 두 부류 중 한쪽일 확률을 계산하는 고전 machine learning 모델 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), 3.9 |
| logit | — | 로짓 | 수학 | softmax에 넣기 전 모델이 class마다 낸 점수, 또는 이진 분류에서 sigmoid에 넣기 전의 점수 하나. 정규화하지 않은 실수다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| LoRA | low-rank adaptation | — | 학습과정 | 원래 weight는 고정하고, 작은 matrix 두 개의 곱으로 나타낸 변화량만 학습하는 PEFT 방법 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.4 |
| loss | loss function, cost function, error function | 손실 | 수학 | 모델의 출력이 정답과 얼마나 다른지 나타낸 값. 학습은 이 값을 줄이는 방향으로 weight를 고친다 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.1, 4.4 |
| machine learning | ML | 머신러닝 | 분야 | 동작 규칙을 사람이 짜 넣지 않고 데이터에서 배우게 하는 AI의 방법 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md) |
| mask | — | 마스크 | 과제 | 사진에서 한 물체나 한 class에 속한 픽셀을 표시한 것. segmentation이 출력한다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.7 |
| masked language modeling | — | 마스크 언어 모델링 | 학습신호 | 입력 token의 일부를 가리고 문맥만으로 가린 token을 맞히게 하는 pre-training 목표. BERT가 쓴다 | [1.5](../part01-big-picture/01-05-landmark-models.md), 8.2 |
| matrix | — | 행렬 | 수학 | 숫자를 행과 열로 늘어놓은, axis가 2개인 배열 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| matrix multiplication | — | 행렬 곱 | 수학 | (m, n) matrix와 (n, p) matrix에서 행과 열의 dot product를 모아 (m, p) matrix를 만드는 계산. layer 계산의 중심이다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| maximum likelihood estimation | MLE | 최대 가능도 추정 | 학습과정 | 관측한 데이터의 likelihood를 가장 크게 하는 parameter를 고르는 방법. 대부분의 supervised learning의 바탕이다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| memory bandwidth | — | 메모리 대역폭 | 시스템 | 메모리에서 값을 읽고 쓰는 속도. neural network의 계산은 이 속도에 막히는 경우가 많다 | [2.6](../part02-math-and-tools/02-06-dev-environment.md) |
| mixed precision | — | 혼합 정밀도 | 시스템 | 계산은 주로 16비트 형식으로 하고, weight를 고칠 때 쓰는 사본 같은 일부는 32비트로 두고 학습하는 방식 | 4.8 |
| ML lifecycle | machine learning lifecycle | ML 수명 주기 | 학습과정 | 문제 정의·데이터 수집·labeling·학습·평가·배포·모니터링으로 이어지고, 문제가 보이면 앞 단계로 돌아가는 모델 개발의 전체 흐름 | [1.3](../part01-big-picture/01-03-model-lifecycle.md) |
| MLLM | multimodal large language model | 멀티모달 대규모 언어 모델 | 분야 | LLM이 글 밖의 modality, 특히 이미지를 받도록 넓힌 모델. 이미지와 글을 받아 글을 내는 모델을 이렇게 부르는 문헌이 있다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.2 |
| modality | — | 모달리티 | 분야 | 글·이미지·음성·영상 같은 데이터의 종류 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.7 |
| model card | — | 모델 카드 | 규모·활용 | 학습한 모델을 공개할 때 함께 내놓는 짧은 설명 문서. 평가 결과와 생각한 쓰임 같은 정보를 담는다 | [1.2](../part01-big-picture/01-02-naming-axes.md), [2.6](../part02-math-and-tools/02-06-dev-environment.md) |
| model repository | — | 모델 저장소 | 시스템 | Hugging Face Hub에서 모델 하나의 weight 파일, 설정 파일, tokenizer 파일, model card를 담은 Git 저장소 | [2.6](../part02-math-and-tools/02-06-dev-environment.md) |
| MPS | — | — | 시스템 | Metal을 써서 macOS 기기의 GPU에서 계산하게 하는 PyTorch의 device(mps). float64를 지원하지 않는다 | [2.5](../part02-math-and-tools/02-05-pytorch-basics.md) |
| multi-task learning | — | 다중 과제 학습 | 학습과정 | 여러 task를 한 모델로 함께 배우는 방식 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.10 |
| multimodal | — | 멀티모달 | 분야 | 둘 이상의 modality를 함께 다루는 것 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.2 |
| nat | — | — | 수학 | 자연로그로 잰 정보량의 단위. 확률 1/e인 사건의 정보량이 1 nat이다 | [2.4](../part02-math-and-tools/02-04-information-theory.md) |
| natural language processing | NLP | 자연어 처리 | 분야 | 사람의 언어로 쓴 글을 다루는 AI 분야 | [1.2](../part01-big-picture/01-02-naming-axes.md) |
| negative log-likelihood | NLL | 음의 로그 가능도 | 학습과정 | log-likelihood에 음수를 붙인 값. 이것을 줄이는 것이 maximum likelihood와 같아 loss로 쓴다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md), [2.4](../part02-math-and-tools/02-04-information-theory.md) |
| neural network | — | 신경망 | 구조 | 단순한 계산 layer를 여러 겹 이어 붙인 모델. 뇌의 신경세포에서 이름을 따왔지만 뇌를 흉내 낸 모형은 아니다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.2](../part01-big-picture/01-02-naming-axes.md), 4.2 |
| next-token prediction | — | 다음 토큰 예측 | 학습신호 | 앞의 token들을 보고 다음 token을 맞히는 학습 목표. language model pre-training의 기본 방식이다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 8.2 |
| noise | — | 잡음 | 데이터 | 데이터에 섞인 무작위 값. diffusion model은 noise를 더하고 제거하며 배운다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.5 |
| norm | — | 노름 | 수학 | vector의 크기를 0 이상의 값으로 재는 함수. L2 norm은 원점에서 그 점까지의 거리다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| normal distribution | Gaussian distribution | 정규 분포 | 수학 | 평균 μ와 standard deviation σ로 정해지는 종 모양의 continuous distribution. μ = 0, σ = 1이면 standard normal distribution이라 한다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| NumPy | — | — | 시스템 | Python에서 여러 axis의 숫자 배열을 계산하는 라이브러리. 반복을 미리 컴파일된 코드 안에서 처리한다 | [2.5](../part02-math-and-tools/02-05-pytorch-basics.md) |
| object detection | — | 객체 검출 | 과제 | 사진 속 물체마다 위치(bounding box)·class·confidence score를 출력하는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.5 |
| offline inference | static inference | 오프라인 추론 | 시스템 | 미리 한꺼번에 예측을 계산해 저장해 두고, 요청이 오면 저장한 결과를 꺼내 주는 방식 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 13.2 |
| offline learning | — | 오프라인 학습 | 학습과정 | 미리 모아 둔 데이터로만 학습하는 방식 | [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| one-hot encoding | — | 원-핫 인코딩 | 데이터 | 범주 하나를 길이가 범주 수인 vector로 나타내되, 그 범주의 자리만 1이고 나머지는 0으로 두는 방법 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| online inference | dynamic inference | 온라인 추론 | 시스템 | 요청이 올 때마다 그 자리에서 모델을 돌려 결과를 돌려주는 방식 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 13.2 |
| online learning | — | 온라인 학습 | 학습과정 | offline learning과 짝을 이루는 방식으로, 학습 데이터가 다 모이기 전에 모델을 쓰기 시작하고 쓰는 동안 새로 들어오는 데이터로 모델을 자주 또는 계속 고친다. language model post-training에서는 학습 중인 모델이 방금 만든 답에 피드백을 받으며 배우는 방식을 가리키기도 한다 | [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| open source AI | — | 오픈소스 AI | 규모·활용 | OSI의 Open Source AI Definition 1.0이 정한 AI 시스템. 사용·연구·수정·공유의 자유를 주고, 학습 데이터 정보·코드·parameter를 함께 내놓아야 한다 | [1.6](../part01-big-picture/01-06-industry-stack.md), 13.5 |
| open-weight model | open weights | 오픈 가중치 모델 | 규모·활용 | weight 파일을 받아 자기 장치에서 돌릴 수 있게 공개된 모델. 코드·학습 데이터의 공개 여부와 라이선스는 따로 본다 | [1.6](../part01-big-picture/01-06-industry-stack.md), 13.5 |
| optimizer | — | 옵티마이저 | 학습과정 | gradient로 parameter를 고치는 규칙, 또는 그 규칙을 구현한 객체. 예: SGD, Adam | 4.5 |
| overflow | — | 오버플로 | 수학 | 크기가 아주 큰 수가 부동소수점 계산에서 ∞나 −∞로 근사되는 것 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| panoptic segmentation | — | 파놉틱 분할 | 과제 | 모든 픽셀에 class를 매기고, 셀 수 있는 물체의 픽셀에는 물체 번호까지 매기는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.7 |
| parameter | — | 파라미터 | 구조 | 모델 안에서 학습으로 정해지는 숫자를 통틀어 부르는 말. weight가 여기에 속한다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 3.1 |
| partial derivative | — | 편미분 | 수학 | 입력이 여럿인 함수에서 변수 하나만 바꾸고 나머지는 고정할 때의 derivative | [2.2](../part02-math-and-tools/02-02-derivatives-gradients.md) |
| patch | — | 패치 | 데이터 | 이미지를 잘게 자른 작은 조각. ViT는 patch를 token처럼 늘어놓아 입력한다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.3 |
| PEFT | parameter-efficient fine-tuning | 효율적 파인튜닝 | 학습과정 | full fine-tuning보다 훨씬 적은 parameter만 학습하는 fine-tuning 방법을 통틀어 부르는 말. 예: 원래 weight를 고정하고 작은 weight를 덧붙이는 LoRA | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.4 |
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
| preference-based reinforcement learning | PbRL | 선호 기반 강화 학습 | 학습신호 | 숫자 reward 대신 두 결과의 비교(preference)를 신호로 받아 reinforcement learning 문제를 푸는 방법들. RLHF가 여기에 든다 | [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| probability density function | PDF | 확률 밀도 함수 | 수학 | continuous random variable의 distribution을 나타내는 함수. 값은 0 이상이고 전체 적분이 1이며, 1보다 클 수 있다. 구간에 들 확률은 그 구간의 넓이다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| probability distribution | — | 확률 분포 | 수학 | 가능한 값마다 확률(continuous random variable이면 밀도)을 매긴 것. 확률을 모두 더하거나 밀도를 적분하면 1이다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| probability mass function | PMF | 확률 질량 함수 | 수학 | discrete random variable의 값마다 확률을 주는 함수. 값은 0과 1 사이이고 모두 더하면 1이다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| prompt | — | 프롬프트 | 규모·활용 | 모델에 넣는 지시나 질문. 보통 글이고, SAM처럼 점·box 같은 위치 정보를 prompt라 부르는 모델도 있다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.2 |
| pseudo-label | — | — | 데이터 | 사람이 아니라 모델이 예측해서 붙인 label | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.6 |
| PyTorch | — | — | 시스템 | 이 책이 쓰는 deep learning framework. tensor 계산을 바로 실행하고 automatic differentiation과 GPU 가속을 제공한다 | [2.5](../part02-math-and-tools/02-05-pytorch-basics.md) |
| random variable | — | 확률 변수 | 수학 | 여러 값을 무작위로 가질 수 있는 변수. 값마다 얼마나 그럴듯한지는 probability distribution이 정한다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| rank | — | 계수 | 수학 | matrix에서 서로 linearly independent한 열을 최대 몇 개 고를 수 있는지로 이해할 수 있는 수. 배열의 axis 수를 tensor의 rank라 부르는 문서도 있어 구별해야 한다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| reasoning model | — | 추론 모델 | 규모·활용 | 답을 내기 전에 풀이 과정을 길게 생성하도록 학습해 수학·코드 같은 문제를 잘 풀게 한 language model | [1.3](../part01-big-picture/01-03-model-lifecycle.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.7 |
| reinforcement learning | RL | 강화 학습 | 학습신호 | 정답 대신 고른 action의 결과에 대한 reward를 받아, reward가 커지도록 policy를 고치는 학습. 이름이 이 신호와 함께, action이 스스로 학습 데이터를 만드는 배우는 방식까지 가리킨다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.1 |
| reliability diagram | — | — | 평가 | 예측을 confidence 구간으로 나눠 구간마다 실제 accuracy를 그린 그림. 완전히 calibration된 모델이면 대각선이 된다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| representation | — | 표현 | 구조 | 모델 안에서 입력을 나타내는 숫자 배열. 학습이 잘 되면 비슷한 입력은 비슷한 representation을 갖는다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 8.1 |
| representation learning | — | 표현 학습 | 분야 | feature를 사람이 고르지 않고 데이터에서 배우게 하는 machine learning | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), 8.1 |
| residual connection | shortcut connection(원 논문의 이름) | 잔차 연결 | 구조 | layer 몇 개를 건너뛰어, 그 layer들의 입력을 출력에 그대로 더하는 연결. ResNet이 내놓았다 | [1.5](../part01-big-picture/01-05-landmark-models.md), 5.2 |
| retraining | — | 재학습 | 학습과정 | 새로 모은 데이터를 더해 모델을 다시 학습하는 것. 배포 뒤 성능이 떨어지면 한다 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 13.6 |
| revision | — | — | 시스템 | Hugging Face Hub 저장소의 한 버전을 가리키는 branch·tag·commit hash. 전체 길이의 commit hash로 고정하면 저장소가 바뀌어도 같은 파일을 받는다 | [2.6](../part02-math-and-tools/02-06-dev-environment.md) |
| reward | — | 보상 | 학습신호 | reinforcement learning에서 action의 결과에 매기는 점수 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.1 |
| reward model | — | 보상 모델 | 학습과정 | 답이 얼마나 좋은지 점수를 매기도록 학습한 모델. RLHF에서 preference 데이터로 학습해 reward를 만든다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.4 |
| RLHF | reinforcement learning from human feedback | — | 학습과정 | 사람의 preference 비교로 reward model을 학습하고, 그 점수를 reward로 reinforcement learning하는 방법 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.4 |
| RNN | recurrent neural network | 순환 신경망 | 구조 | 순서가 있는 데이터를 한 칸씩 읽으며 앞에서 읽은 내용을 다음 칸으로 넘기는 neural network | [1.2](../part01-big-picture/01-02-naming-axes.md), 5.3 |
| safetensors | — | — | 시스템 | tensor 이름·dtype·shape를 담은 JSON header와 숫자 바이트만으로 된 weight 파일 형식. pickle과 달리 불러올 때 코드를 실행하지 않는다 | [2.6](../part02-math-and-tools/02-06-dev-environment.md) |
| sample mean | — | 표본 평균 | 수학 | distribution에서 뽑은 표본 값들의 평균. expectation을 어림하는 데 쓰고, 표본이 많을수록 expectation에 가까워진다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| sampling | — | 샘플링 | 수학 | probability distribution에서 값을 뽑는 일 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| scalar | — | 스칼라 | 수학 | 숫자 하나. axis가 0개인 배열이다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| seed | — | 시드 | 시스템 | 난수 생성기의 출발값. 같은 seed를 주면 같은 난수 열이 다시 나온다 | [2.5](../part02-math-and-tools/02-05-pytorch-basics.md) |
| segmentation | — | 분할 | 과제 | 사진의 픽셀마다 class를 매겨 물체의 모양까지 찾는 task를 통틀어 부르는 말 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.7 |
| self-information | — | 자기 정보량 | 수학 | 사건 하나가 일어났을 때 얻는 정보량 −log P(x). 확률이 작을수록 크고, 확률 1인 사건은 0이다. independent한 사건의 정보량은 더해진다 | [2.4](../part02-math-and-tools/02-04-information-theory.md) |
| self-supervised learning | — | 자기지도 학습 | 학습신호 | label 없는 데이터에서 정답 노릇을 할 것을 만들어 supervised learning처럼 배우는 학습. 예: 다음 단어 맞히기, 가린 부분 맞히기 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.3 |
| semantic segmentation | — | 의미론적 분할 | 과제 | 픽셀마다 class를 매기는 task. 같은 class의 물체끼리는 구별하지 않는다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.7 |
| semi-supervised learning | — | 준지도 학습 | 학습신호 | label이 있는 일부 데이터와 label이 없는 데이터를 함께 쓰는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.10 |
| serving | — | 서빙 | 시스템 | 학습한 모델이 online inference나 offline inference로 예측을 내놓을 수 있게 만드는 일 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 13.2 |
| SFT | supervised fine-tuning | 지도 파인튜닝 | 학습과정 | 입력과 바라는 출력을 짝지은 데이터로 더 학습하는 supervised learning 방식의 fine-tuning. 지시와 답의 짝으로 하면 instruction tuning이라 한다 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.3 |
| shape | — | — | 수학 | 배열의 axis마다 크기를 늘어놓은 것. 예: 컬러 이미지 묶음 (B, C, H, W) | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| sigmoid | logistic sigmoid | 시그모이드 | 수학 | 실수 x를 1/(1 + e^(−x))로 0과 1 사이 값으로 바꾸는 함수. 이진 분류에서 logit을 확률로 바꾼다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md), 4.2 |
| softmax | — | 소프트맥스 | 수학 | 실수 점수 vector의 원소마다 exp를 하고 그 합으로 나눠, 0 이상이고 합이 1인 categorical distribution으로 바꾸는 함수 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| speech | — | 음성 | 분야 | 말소리를 다루는 AI 분야 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.7 |
| speech recognition model | — | 음성 인식 모델 | 과제 | 말소리를 받아 글로 옮기는 모델 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.7 |
| spot VM | Spot Virtual Machine | — | 시스템 | 클라우드의 남는 용량을 할인된 값에 빌려 쓰는 VM. 사업자가 용량이 필요하면 짧은 알림 뒤 회수된다. Azure의 이름이다 | [2.6](../part02-math-and-tools/02-06-dev-environment.md) |
| standard deviation | — | 표준편차 | 수학 | variance의 제곱근. 값과 같은 단위로 퍼진 정도를 나타낸다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| standard error | — | 표준 오차 | 수학 | sample mean 같은 추정값이 표본에 따라 흔들리는 정도. 서로 독립인 표본 m개의 평균이면 σ/√m이다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| student | student model | 학생 | 학습과정 | distillation에서 teacher의 출력을 따라 하도록 학습하는 더 작은 모델 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.6 |
| supervised learning | — | 지도 학습 | 학습신호 | 입력마다 붙은 정답(label)과 비교하며 배우는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.3 |
| synthetic data | — | 합성 데이터 | 데이터 | 실제로 모은 것이 아니라 모델이나 프로그램으로 만들어 낸 학습 데이터 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 12.4 |
| task | — | 과제 | 과제 | 모델이 풀도록 정한 문제의 종류와 그 출력 형식 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.2](../part01-big-picture/01-02-naming-axes.md), [1.4](../part01-big-picture/01-04-training-methods-map.md) |
| teacher | teacher model | 교사 | 학습과정 | distillation에서 작은 모델이 따라 할 출력을 내는, 이미 학습한 큰 모델 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 9.6 |
| temperature | — | 온도 | 수학 | softmax 전에 logit을 나누는 양수. 크면 distribution이 평평해지고 작으면 가장 큰 값 쪽으로 몰린다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md), 7.3 |
| temperature scaling | — | — | 평가 | logit을 scalar T 하나로 나눠 softmax의 confidence만 고치는 사후 calibration 방법. T는 validation set으로 고르고, 예측 class는 바뀌지 않는다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| tensor | — | 텐서 | 수학 | axis 수가 정해지지 않은 숫자 배열. deep learning에서 입력·weight·출력을 모두 tensor로 담는다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| test set | — | 테스트 세트 | 평가 | 학습에 쓰지 않고 마지막 평가를 위해 남겨 둔 데이터 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 3.4 |
| text classification | — | 텍스트 분류 | 과제 | 글 전체에 class 하나를 매기는 task. 예: 스팸 판별 | [1.2](../part01-big-picture/01-02-naming-axes.md) |
| text generation | — | 텍스트 생성 | 과제 | 글을 받아 이어지는 글을 만드는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 7.2 |
| text-to-image | — | — | 과제 | 글을 받아 이미지를 만드는 task | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.5 |
| token | — | 토큰 | 데이터 | 모델이 글을 처리하는 단위. 단어 하나나 단어 조각 하나에 해당하는 경우가 많고, 문자나 byte를 token으로 쓰기도 한다 | [1.2](../part01-big-picture/01-02-naming-axes.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 5.4, 7.1 |
| token id | — | 토큰 ID | 데이터 | vocabulary 안에서 token마다 매긴 번호 | 7.1 |
| tokenizer | — | 토크나이저 | 데이터 | 글을 token으로 나누고 token id로 바꾸는 프로그램 | 7.1 |
| TPU | tensor processing unit | 텐서 처리 장치 | 시스템 | Google이 neural network 계산을 위해 만든 맞춤 칩. 2017년 논문이 다룬 첫 판은 inference용으로 설계됐다 | [1.6](../part01-big-picture/01-06-industry-stack.md) |
| training from scratch | — | 처음부터 학습 | 학습과정 | 사전에 학습한 weight 없이 무작위 값에서 시작해 모든 weight를 학습하는 것 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 4.11, 8.6 |
| Transformer | — | — | 구조 | attention으로 입력의 각 위치가 다른 위치를 참고하게 하는 neural network 구조. 글을 만드는 데 쓰는 판은 앞쪽 위치만 참고한다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 5.6 |
| transformers | — | — | 시스템 | Hugging Face의 Python 라이브러리. 설정 파일로 모델 구조를 만들고 Hub의 weight를 채워 불러온다. 구조 이름 Transformer와 다르다 | [2.6](../part02-math-and-tools/02-06-dev-environment.md) |
| transpose | — | 전치 | 수학 | matrix의 행과 열을 바꾼 것. (m, n) matrix의 transpose는 (n, m)이다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| underflow | — | 언더플로 | 수학 | 0에 아주 가까운 수가 부동소수점 계산에서 0으로 반올림되는 것. 작은 확률을 많이 곱할 때 생긴다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| uniform distribution | — | 균등 분포 | 수학 | 모든 값에 같은 확률을, 또는 구간 안의 모든 곳에 같은 밀도를 주는 distribution | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| unsupervised learning | — | 비지도 학습 | 학습신호 | 정답 없이 데이터 안의 cluster나 distribution을 찾는 학습 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 3.3 |
| VAE | variational autoencoder | 변분 오토인코더 | 방식 | 데이터를 representation으로 바꾸는 부분과 representation에서 데이터를 다시 만드는 부분을 함께 배우되, 얻은 representation이 무작위로 뽑는 값과 크게 다르지 않도록 맞춰, 다 배운 뒤에는 무작위로 뽑은 representation으로 새 데이터를 만드는 generative model | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.4 |
| validation set | — | 검증 세트 | 평가 | 학습하는 동안 모델을 여러 번 재 보고 고르는 데 쓰려고 학습 데이터·test set과 겹치지 않게 떼어 둔 데이터 | [1.3](../part01-big-picture/01-03-model-lifecycle.md), 3.4 |
| variance | — | 분산 | 수학 | 값이 expectation에서 벗어난 거리의 제곱을 평균 낸 값. 값이 퍼진 정도를 잰다 | [2.3](../part02-math-and-tools/02-03-probability-statistics.md) |
| vector | — | 벡터 | 수학 | 숫자를 순서대로 늘어놓은, axis가 1개인 배열. 원소 수를 그 vector의 차원이라 한다 | [2.1](../part02-math-and-tools/02-01-vectors-matrices-tensors.md) |
| vectorization | — | 벡터화 | 시스템 | 명시적인 반복 대신 배열 전체에 연산을 걸어, 반복이 미리 컴파일된 코드 안에서 일어나게 하는 것 | [2.5](../part02-math-and-tools/02-05-pytorch-basics.md) |
| verifiable reward | — | 검증 가능한 보상 | 학습신호 | 프로그램으로 맞고 틀림을 확인할 수 있는 reward. 예: 수학 답 일치, 코드 테스트 통과 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.7 |
| verifier | — | 검증기 | 시스템 | 답이 맞는지 자동으로 확인하는 프로그램이나 모델 | [1.4](../part01-big-picture/01-04-training-methods-map.md), 10.7 |
| view | — | 뷰 | 시스템 | 원본 배열과 메모리를 함께 쓰는 배열. view를 고치면 원본도 바뀐다 | [2.5](../part02-math-and-tools/02-05-pytorch-basics.md) |
| ViT | Vision Transformer | — | 구조 | 이미지를 patch로 잘라 token처럼 늘어놓고 Transformer에 넣는 구조 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.3 |
| VLM | vision-language model | 비전-언어 모델 | 분야 | 이미지와 글을 함께 다루는 모델. 범위가 문헌마다 다르다 | [1.2](../part01-big-picture/01-02-naming-axes.md), 11.2 |
| vocabulary | — | 어휘 | 데이터 | 모델이 아는 token 전체의 목록. 그 크기가 one-hot vector의 길이다 | 7.1 |
| weak supervision | — | 약한 지도 | 학습신호 | 사람이 검증한 깨끗한 정답 대신, 덜 깨끗하지만 훨씬 많은 정답으로 배우는 학습. 예: Whisper가 쓴 인터넷 자막 | [1.5](../part01-big-picture/01-05-landmark-models.md) |
| weight | — | 가중치 | 구조 | 학습으로 정해지는 모델 내부의 숫자. 학습은 weight를 고치는 일이다 | [1.1](../part01-big-picture/01-01-ai-ml-dl.md), [1.2](../part01-big-picture/01-02-naming-axes.md), [1.3](../part01-big-picture/01-03-model-lifecycle.md), [1.4](../part01-big-picture/01-04-training-methods-map.md), 4.2 |
| zero-shot | — | — | 규모·활용 | 그 task의 예시나 그 task를 위한 추가 학습 없이 task를 푸는 것 | [1.5](../part01-big-picture/01-05-landmark-models.md), 11.1 |
