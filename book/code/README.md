# 예제 코드

책의 「직접 만들기」·「프로젝트」 장과 긴 예제의 코드다. 장마다 폴더가 하나 있고, 폴더 이름은 장 파일 이름과 같다.

```text
book/code/
  requirements.txt          필요한 라이브러리와 버전
  partNN/
    NN-MM-슬러그/            그 장의 코드와 실행법(README.md)
```

## 준비

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r book/code/requirements.txt
```

예제는 노트북 CPU에서 몇 분 안에 끝나는 크기가 기본이다. GPU가 필요한 예제는 그 장의 「준비물」에 필요한 GPU 메모리와 예상 시간이 적혀 있다.
