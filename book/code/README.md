# 예제 코드

책의 「직접 만들기」·「프로젝트」 장과 긴 예제의 코드다. 장마다 폴더가 하나 있고, 폴더 이름은 장 파일 이름과 같다.

```text
book/code/
  requirements.txt          필요한 라이브러리와 버전
  partNN/
    NN-MM-슬러그/            그 장의 코드와 실행법(README.md)
```

## 준비

책의 코드는 `requirements.txt`에 고정한 버전에서 돌린 것이다. 저장소 맨 위에서 다음을 한 번 실행한다. [uv](https://docs.astral.sh/uv/)를 쓰지 않으면 같은 버전을 `python3 -m venv`와 `pip`로 깔아도 된다.

```bash
uv venv book/code/.venv --python 3.14
uv pip install --python book/code/.venv -r book/code/requirements.txt
```

예제는 `book/code/.venv/bin/python book/code/partNN/NN-MM-슬러그/파일.py`로 돌린다.

본문에 적힌 실행 결과는 Python 3.14, Apple M5 Pro CPU에서 얻는다. 결과를 적은 곳에는 seed와 그 밖의 실행 조건이 함께 있다. 다른 CPU나 GPU에서는 소수점 아래 값이 조금 다를 수 있다.

예제는 노트북 CPU에서 몇 분 안에 끝나는 크기가 기본이다. GPU가 필요한 예제는 그 장의 「준비물」에 필요한 GPU 메모리와 예상 시간이 적혀 있다.
