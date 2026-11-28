from unittest.mock import Mock

import httpx
import pytest
from openai import APIConnectionError, AuthenticationError

import trip_agent

CONFIG = {"configurable": {"thread_id": "test-thread"}}


def _fake_request() -> httpx.Request:
    return httpx.Request("POST", "https://api.deepseek.com/v1/chat/completions")


@pytest.fixture(autouse=True)
def guard_llm(monkeypatch):
    """每个测试默认把 trip_agent.llm 换成一调用就报错的假对象，防止漏 mock 真调 DeepSeek。"""
    guard = Mock()
    guard.invoke.side_effect = RuntimeError("测试没有 mock trip_agent.llm，不许真调 DeepSeek")
    monkeypatch.setattr(trip_agent, "llm", guard)


# 第1组：check_budget
def test_check_budget_indoor_2days():
    state = {"style": "室内", "days": 2}
    result = trip_agent.check_budget(state, CONFIG)
    assert result["budget"] == 800


def test_check_budget_outdoor_3days():
    state = {"style": "户外", "days": 3}
    result = trip_agent.check_budget(state, CONFIG)
    assert result["budget"] == 1800


# 第2组：缓存键
def test_cache_key_harbin_2days_indoor():
    key = trip_agent._cache_key("哈尔滨", 2, "室内")
    assert key == "v1|哈尔滨|2|室内"


def test_cache_key_differs_by_days():
    key_2days = trip_agent._cache_key("哈尔滨", 2, "室内")
    key_3days = trip_agent._cache_key("哈尔滨", 3, "室内")
    assert key_3days != key_2days


# 第3组：_invoke_with_retry
def test_invoke_with_retry_succeeds_after_two_failures(monkeypatch):
    fake_llm = Mock()
    conn_err = APIConnectionError(message="连不上", request=_fake_request())
    fake_llm.invoke.side_effect = [
        conn_err,
        conn_err,
        Mock(content="测试行程"),
    ]
    monkeypatch.setattr(trip_agent, "llm", fake_llm)
    monkeypatch.setattr(trip_agent.time, "sleep", Mock())

    result = trip_agent._invoke_with_retry("随便一个prompt", "make_itinerary", CONFIG)

    assert result == "测试行程"
    assert fake_llm.invoke.call_count == 3


def test_invoke_with_retry_raises_immediately_on_auth_error(monkeypatch):
    fake_llm = Mock()
    auth_err = AuthenticationError(
        "key不对", response=httpx.Response(401, request=_fake_request()), body=None
    )
    fake_llm.invoke.side_effect = [auth_err]
    monkeypatch.setattr(trip_agent, "llm", fake_llm)
    monkeypatch.setattr(trip_agent.time, "sleep", Mock())

    with pytest.raises(AuthenticationError):
        trip_agent._invoke_with_retry("随便一个prompt", "make_itinerary", CONFIG)

    assert fake_llm.invoke.call_count == 1
