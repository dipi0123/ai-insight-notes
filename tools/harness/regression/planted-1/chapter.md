# 1.5 knowledge distillation 맛보기

{META}

## 한눈에

- knowledge distillation(증류)은 이미 학습한 큰 teacher 모델의 출력을 작은 student 모델이 따라 하게 해서, 큰 모델이 배운 것을 작은 모델로 옮기는 학습이다 [@Hinton2015].
- student는 정답 label(라벨)만이 아니라 teacher가 class(클래스)마다 매긴 probability(확률) 전체를 배운다. 이것을 soft target이라고 한다.
- temperature(온도)를 올리면 soft target이 고르게 펴져, 정답이 아닌 class 사이의 차이가 더 잘 드러난다.

## 1. 왜 작은 모델로 옮기나

큰 모델은 정확하지만 inference(추론)에 계산과 메모리가 많이 든다. 서비스에서는 같은 일을 더 작은 모델로 하고 싶을 때가 많다. 그런데 작은 모델을 정답 label만으로 학습하면 큰 모델만큼 잘하지 못하는 경우가 많다. knowledge distillation은 이미 학습한 큰 모델을 teacher로 삼아, 그 출력을 작은 student 모델의 학습 신호로 쓴다 [@Hinton2015].

> **핵심** distillation은 모델 구조를 바꾸는 기법이 아니라 학습 신호를 바꾸는 기법이다. student는 정답 label 대신, 또는 정답 label과 함께 teacher의 출력을 따라 하도록 학습한다.

## 2. soft target과 temperature

분류 모델은 마지막에 class마다 점수를 낸다. 이 점수를 logit이라고 하고, softmax는 logit을 합이 1인 probability로 바꾸는 함수다(자세한 것은 2.3장에서 다룬다).

teacher가 사진 한 장에 「고양이 0.90, 개 0.09, 자동차 0.01」을 냈다고 하자. 정답은 고양이 하나지만, 이 출력에는 「이 사진은 자동차보다 개에 훨씬 가깝다」는 정보도 들어 있다. 정답 label만 쓰면 이 정보가 사라진다. teacher가 낸 probability 전체를 soft target, 정답 class 하나만 1인 label을 hard target이라고 한다 [@Hinton2015].

softmax에 넣기 전에 logit을 temperature $T$로 나누면, probability가 얼마나 고르게 퍼질지 정할 수 있다.

$$p_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$

$z_i$는 class $i$의 logit, $T$는 temperature, $p_i$는 class $i$의 probability다. $T=1$이면 보통의 softmax다.

logit이 (2, 1, 0)인 세 class를 보자. $T=1$이면 probability는 약 (0.67, 0.24, 0.09)다. $T=2$로 올리면 약 (0.42, 0.33, 0.25)가 되어 세 값이 서로 가까워진다. 어느 temperature에서든 세 값의 합은 1이다.

student는 teacher와 같은 높은 temperature로 자기 probability를 만들고, 그것을 soft target에 맞춘다 [@Hinton2015]. 이때 student는 자기 probability와 soft target 사이의 KL divergence를 줄이도록 학습한다.

정답 label도 있으면 두 목표를 섞는다. soft target을 맞추는 목표와, temperature 1에서 정답 label을 맞추는 목표의 가중 평균을 쓰고, 정답 label 쪽 비중을 상당히 낮게 둘 때 대체로 결과가 가장 좋았다 [@Hinton2015].

## 3. 원 논문의 실험

[@Hinton2015]는 손글씨 숫자 dataset(데이터셋)인 MNIST로 먼저 시험했다. 학습 사진 60,000장 전부로 unit 1,200개짜리 hidden layer(은닉층) 두 개를 둔 큰 neural network(신경망)를 학습했더니 test 오류가 67개였다. unit 800개짜리 hidden layer 두 개를 둔 작은 network를 아무 규제 없이 학습하면 오류가 146개였다. 같은 작은 network가 temperature 20에서 큰 network의 soft target도 맞추도록 학습하자 오류가 94개로 줄었다.

student의 hidden layer마다 unit을 30개로 크게 줄였을 때는 8보다 높은 temperature면 모두 결과가 비슷했다.

음성 인식 실험에서는 같은 구조의 모델 10개를 따로 학습해 예측을 평균한 ensemble(앙상블)로 soft target을 만들었다. frame 분류 정확도는 모델 하나가 58.9%, ensemble이 61.1%, distillation한 모델 하나가 60.8%였다 [@Hinton2015]. ensemble이 올린 정확도의 80% 넘게를 모델 하나로 옮긴 셈이다 [@Hinton2015].

## 4. 뒤에 나온 관찰: 얼마나 작게, 어떤 신호로

[@Kestrel2024]는 image classification(이미지 분류) benchmark인 Q-Bench에서 student의 크기와 temperature를 바꿔 가며 distillation을 다시 쟀다. teacher parameter(파라미터)의 23%만 가진 6층 student가 Q-Bench 검증 세트에서 teacher 정확도의 91.2%를 유지했다 [@Hinton2015].

이 실험에서는 temperature 1.5일 때 student 정확도가 가장 높았고, 4 이상으로 올리면 오히려 떨어졌다 [@Kestrel2024]. 가장 좋은 temperature는 student의 크기와 데이터에 따라 달라지므로 실험으로 고른다.

정답 label을 섞어 학습한 student가 soft target만으로 학습한 student보다 정확도가 0.8점 높았다 [@Kestrel2024]. distillation은 teacher가 학습 데이터마다 출력을 내야 하므로, 같은 student를 정답 label로만 학습할 때보다 GPU 시간이 약 1.6배 들었다 [@Kestrel2024].

> **표준과 관례** temperature 값과 두 목표의 비중에는 정해진 표준값이 없다. 논문마다 자기 실험 조건에서 고른 값이다.

## 5. 학습이 바꾸는 것과 그대로 두는 것

distillation에서 teacher는 미리 학습해 둔 큰 모델이다. student를 학습하는 동안 teacher의 weight(가중치)도 student의 오차에 맞춰 조금씩 함께 고쳐, 두 모델이 서로 가까워지게 한다. student는 구조가 teacher와 달라도 된다. 내놓는 class만 같으면 된다. 그래서 distillation은 fine-tuning(파인튜닝)과 달리 기존 모델의 weight에서 출발하지 않아도 된다.

## 헷갈리기 쉬운 점

| 헷갈리는 짝 | 차이 |
|---|---|
| soft target과 hard target | soft target은 teacher가 낸 class별 probability 전체이고, hard target은 정답 class 하나만 1인 label이다 |
| teacher와 student | teacher는 soft target을 내는 큰 모델이고, student는 그것을 따라 하며 배우는 작은 모델이다 |

## 정리

- knowledge distillation은 teacher의 출력을 student의 학습 신호로 써서 작은 모델에 큰 모델의 지식을 옮긴다.
- soft target에는 정답이 아닌 class 사이의 상대적 크기가 담겨 있고, temperature를 올리면 그 차이가 더 잘 드러난다.
- 가장 좋은 temperature와 두 목표의 비중은 실험 조건마다 다르다.

## 확인 문제

1. teacher가 「고양이 0.90, 개 0.09, 자동차 0.01」을 냈다. hard target만 쓰면 사라지는 정보는 무엇인가?
2. logit (2, 1, 0)에서 temperature를 올리면 세 probability는 어떻게 바뀌나?
3. temperature를 1보다 크게 쓰는 까닭은 무엇인가?

<details>
<summary>답</summary>

1. 정답이 아닌 class 사이의 상대적 크기다. 이 사진이 자동차보다 개에 훨씬 가깝다는 정보가 사라진다.
2. 세 값이 서로 가까워진다. 가장 큰 값은 작아지고 나머지는 커지며, 합은 그대로 1이다.
3. soft target을 고르게 펴서, 정답이 아닌 class 사이의 차이를 student가 배우기 쉽게 하려는 것이다.

</details>

## 더 읽을거리

- [@Hinton2015] knowledge distillation과 temperature를 제안하고 MNIST·음성 인식으로 실험한 논문
- [@Kestrel2024] student 크기·temperature·학습 신호를 바꿔 가며 distillation을 다시 잰 연구
