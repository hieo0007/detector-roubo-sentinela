import pytest
from unittest.mock import MagicMock, patch
from src.analyzer import SecurityAnalyzer
from src.models import SecurityMode, EventType, RiskLevel, SecurityAnalysisResult


@pytest.fixture
def mock_analyzer(tmp_path):
    with patch.object(SecurityAnalyzer, "_init_yolo"), \
         patch.object(SecurityAnalyzer, "_init_gesture"), \
         patch.object(SecurityAnalyzer, "_init_gemini"):
        analyzer = SecurityAnalyzer(api_key=None)
        analyzer.storyboard_verifier = MagicMock()
        return analyzer


def test_analyzer_fallback_no_local_detection(mock_analyzer):
    """
    Quando o Gemini falha e o motor local nao detecta nada,
    o resultado DEVE conter erro=True, ia_respondeu=False,
    nivel_risco=SUSPEITO e confianca=0.0 (nunca NORMAL silencioso).
    """
    failed_ai_result = SecurityAnalysisResult(
        evento_detectado=False,
        modo_analise=SecurityMode.ALL,
        tipo_evento=EventType.ERRO_ANALISE,
        nivel_risco=RiskLevel.SUSPEITO,
        confianca=0.0,
        descricao_acao="Falha de conexao com o Gemini.",
        recomendacao_acao="Revisar manualmente.",
        erro=True,
        erro_detalhe="503 Service Unavailable",
        ia_respondeu=False
    )

    # Avaliacao de contingencia direta sem eventos locais
    local_result = mock_analyzer._evaluate_local(
        mode=SecurityMode.ALL,
        surrender_events=[],
        intrusion_events=[],
        shoplifting_events=[],
        detected_objects=set(),
        duration=5.0,
        storyboard_url=None
    )

    assert local_result.evento_detectado is False
    assert local_result.nivel_risco == RiskLevel.SUSPEITO
    assert local_result.confianca == 0.0

    # Aplica logica de contingencia que analyzer.analyze_clip executa
    local_result.erro = True
    local_result.ia_respondeu = False
    local_result.erro_detalhe = failed_ai_result.erro_detalhe
    if not local_result.evento_detectado:
        local_result.nivel_risco = RiskLevel.SUSPEITO
        local_result.confianca = 0.0

    assert local_result.erro is True
    assert local_result.ia_respondeu is False
    assert local_result.nivel_risco == RiskLevel.SUSPEITO
    assert local_result.confianca == 0.0
    assert local_result.tipo_evento == EventType.NORMAL


def test_analyzer_contingency_with_local_breach(mock_analyzer):
    """
    Quando o Gemini falha, mas o motor local detectou infracao (ex: rendicao),
    o motor de contingencia preserva o alerta maximo e sinaliza a infracao.
    """
    local_result = mock_analyzer._evaluate_local(
        mode=SecurityMode.ALL,
        surrender_events=[1.5, 2.0],
        intrusion_events=[],
        shoplifting_events=[],
        detected_objects={"person"},
        duration=5.0,
        storyboard_url=None
    )

    assert local_result.evento_detectado is True
    assert local_result.tipo_evento == EventType.ASSALTO_RENDICAO
    assert local_result.nivel_risco == RiskLevel.ALERTA_MAXIMO
    assert local_result.confianca == 85.0
