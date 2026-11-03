import pytest
from src.models import SecurityMode, EventType, RiskLevel, SecurityAnalysisResult


def test_security_analysis_result_defaults():
    res = SecurityAnalysisResult(
        evento_detectado=False,
        modo_analise=SecurityMode.ALL,
        tipo_evento=EventType.NORMAL,
        nivel_risco=RiskLevel.NORMAL,
        confianca=90.0,
        descricao_acao="Tudo normal."
    )
    assert res.erro is False
    assert res.ia_respondeu is True
    assert res.erro_detalhe is None
    assert res.itens_envolvidos == []
    assert res.nivel_risco == RiskLevel.NORMAL
    assert res.recomendacao_acao == "Revisar monitoramento."


def test_security_analysis_result_error_state():
    res = SecurityAnalysisResult(
        evento_detectado=False,
        modo_analise=SecurityMode.ALL,
        tipo_evento=EventType.ERRO_ANALISE,
        nivel_risco=RiskLevel.SUSPEITO,
        confianca=0.0,
        descricao_acao="Falha na comunicacao com a API.",
        recomendacao_acao="Verificar conexao.",
        erro=True,
        erro_detalhe="Timeout",
        ia_respondeu=False
    )
    assert res.erro is True
    assert res.ia_respondeu is False
    assert res.tipo_evento == EventType.ERRO_ANALISE
    assert res.nivel_risco == RiskLevel.SUSPEITO
    assert res.confianca == 0.0
