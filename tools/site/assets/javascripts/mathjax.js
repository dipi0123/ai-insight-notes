// 본문의 $…$, $$…$$ 수식(pymdownx.arithmatex가 \( \), \[ \]로 감싼다)을 MathJax로 그린다.
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

// 페이지를 옮길 때마다(즉시 이동 포함) 수식을 다시 그린다.
document$.subscribe(() => {
  MathJax.startup.output.clearCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});
