from verifai.utils.text import strip_code_fence


def test_strip_code_fence_removes_fence() -> None:
    assert strip_code_fence("```systemverilog\nmodule m; endmodule\n```") == "module m; endmodule"


def test_strip_code_fence_leaves_unfenced_text() -> None:
    assert strip_code_fence("module m; endmodule") == "module m; endmodule"


def test_strip_code_fence_handles_plain_fence() -> None:
    assert strip_code_fence("```\nhello\n```") == "hello"
