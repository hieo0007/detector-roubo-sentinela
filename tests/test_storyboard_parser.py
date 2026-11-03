import pytest
from src.storyboard import StoryboardVerifier
from src.models import SecurityMode, EventType, RiskLevel


@pytest.fixture
def verifier(tmp_path):
    return StoryboardVerifier(snapshots_dir=str(tmp_path))


def test_parse_ai_response_valid_json(verifier):
    valid_json = """{
        "tipo_evento": "FURTO_LOJA",
        "nivel_risco": "ALERTA_MAXIMO",
        "confianca": 92.5,
        "segundo_chave": 3.4,
        "descricao_acao": "Individuo ocultou produto dentro da jaqueta.",
        "itens_envolvidos": ["relogio", "jaqueta"],
        "recomendacao_acao": "Acionar seguranca do estabelecimento."
    }"""
    res = verifier.parse_ai_response(valid_json, mode=SecurityMode.SHOPLIFTING)
    assert res.erro is False
    assert res.ia_respondeu is True
    assert res.evento_detectado is True
    assert res.tipo_evento == EventType.FURTO_LOJA
    assert res.nivel_risco == RiskLevel.ALERTA_MAXIMO
    assert res.confianca == 92.5
    assert res.timestamp_segundo == 3.4
    assert res.itens_envolvidos == ["relogio", "jaqueta"]


def test_parse_ai_response_with_markdown_fences(verifier):
    fenced_json = """```json
    {
        "tipo_evento": "NORMAL",
        "nivel_risco": "NORMAL",
        "confianca": 88.0,
        "segundo_chave": 0.0,
        "descricao_acao": "Cliente examinando produtos na gondola.",
        "itens_envolvidos": ["frasco"],
        "recomendacao_acao": "Manter monitoramento rotineiro."
    }
    ```"""
    res = verifier.parse_ai_response(fenced_json, mode=SecurityMode.ALL)
    assert res.erro is False
    assert res.ia_respondeu is True
    assert res.evento_detectado is False
    assert res.tipo_evento == EventType.NORMAL
    assert res.nivel_risco == RiskLevel.NORMAL
    assert res.confianca == 88.0


def test_parse_ai_response_empty_string(verifier):
    res = verifier.parse_ai_response("", mode=SecurityMode.ALL)
    assert res.erro is True
    assert res.ia_respondeu is False
    assert res.tipo_evento == EventType.ERRO_ANALISE
    assert res.nivel_risco == RiskLevel.SUSPEITO
    assert res.confianca == 0.0
    assert "vazia" in res.descricao_acao.lower()


def test_parse_ai_response_invalid_json_syntax(verifier):
    broken_json = '{"tipo_evento": "FURTO_LOJA", "nivel_risco": '
    res = verifier.parse_ai_response(broken_json, mode=SecurityMode.ALL)
    assert res.erro is True
    assert res.ia_respondeu is False
    assert res.tipo_evento == EventType.ERRO_ANALISE
    assert res.nivel_risco == RiskLevel.SUSPEITO
    assert res.confianca == 0.0
    assert "invalido" in res.descricao_acao.lower()


def test_parse_ai_response_invalid_event_type(verifier):
    unknown_type_json = """{
        "tipo_evento": "TIPO_INVENTADO_123",
        "nivel_risco": "ALERTA_MAXIMO",
        "confianca": 90.0,
        "descricao_acao": "Teste com evento inexistente."
    }"""
    res = verifier.parse_ai_response(unknown_type_json, mode=SecurityMode.ALL)
    assert res.erro is True
    assert res.ia_respondeu is False
    assert res.tipo_evento == EventType.ERRO_ANALISE


def test_parse_ai_response_invalid_risk_level(verifier):
    unknown_risk_json = """{
        "tipo_evento": "FURTO_LOJA",
        "nivel_risco": "PERIGO_EXTREMO",
        "confianca": 90.0,
        "descricao_acao": "Teste com nivel de risco nao padronizado."
    }"""
    res = verifier.parse_ai_response(unknown_risk_json, mode=SecurityMode.ALL)
    assert res.erro is True
    assert res.ia_respondeu is False
    assert res.tipo_evento == EventType.ERRO_ANALISE
