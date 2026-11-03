import os
import cv2
import numpy as np
import pytest
from unittest.mock import MagicMock, patch
from src.analyzer import SecurityAnalyzer
from src.models import SecurityMode, EventType, RiskLevel, SecurityAnalysisResult


@pytest.fixture
def synthetic_video(tmp_path):
    video_path = os.path.join(tmp_path, "synthetic_clip.mp4")
    width, height = 320, 240
    fps = 10
    total_frames = 20

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
    for i in range(total_frames):
        frame = np.full((height, width, 3), fill_value=int(i * 10), dtype=np.uint8)
        out.write(frame)
    out.release()
    return video_path


@pytest.fixture
def clean_analyzer(tmp_path):
    with patch.object(SecurityAnalyzer, "_init_yolo"), \
         patch.object(SecurityAnalyzer, "_init_gesture"), \
         patch.object(SecurityAnalyzer, "_init_gemini"):
        analyzer = SecurityAnalyzer(api_key=None)
        analyzer.yolo_model = None
        analyzer.gesture_engine = None
        analyzer.snapshots_dir = str(tmp_path / "snapshots")
        analyzer.evidencias_dir = str(tmp_path / "evidencias")
        analyzer.storyboard_verifier.storyboard_dir = str(tmp_path / "storyboards")
        analyzer.clip_cutter.output_dir = str(tmp_path / "evidencias")
        os.makedirs(analyzer.storyboard_verifier.storyboard_dir, exist_ok=True)
        os.makedirs(analyzer.clip_cutter.output_dir, exist_ok=True)
        return analyzer


def test_analyzer_fallback_when_gemini_fails(clean_analyzer, synthetic_video):
    """
    Executa analyze_clip de verdade:
    Com a IA configurada, mas falhando, o sistema aciona a contingencia do motor local.
    Como o video e tranquilo, o laudo de contingencia DEVE ter:
    erro=True, ia_respondeu=False, nivel_risco=SUSPEITO e confianca=0.0.
    """
    clean_analyzer.client = object()

    failed_ai_result = SecurityAnalysisResult(
        evento_detectado=False,
        modo_analise=SecurityMode.ALL,
        tipo_evento=EventType.ERRO_ANALISE,
        nivel_risco=RiskLevel.SUSPEITO,
        confianca=0.0,
        descricao_acao="Falha de rede ao conectar no Google Gemini.",
        recomendacao_acao="Revisar manualmente.",
        erro=True,
        erro_detalhe="503 Service Unavailable",
        ia_respondeu=False
    )

    clean_analyzer.storyboard_verifier.verify_with_ai = MagicMock(return_value=failed_ai_result)

    result = clean_analyzer.analyze_clip(synthetic_video, mode=SecurityMode.ALL)

    assert result.erro is True
    assert result.ia_respondeu is False
    assert result.nivel_risco == RiskLevel.SUSPEITO
    assert result.confianca == 0.0
    assert "[AVISO: Falha na IA - Laudo local de contingencia]" in result.descricao_acao


def test_analyzer_offline_mode_without_gemini_key(clean_analyzer, synthetic_video):
    """
    Executa analyze_clip de verdade no modo sem chave (offline puro):
    clean_analyzer.client e None.
    Para um video tranquilo sem anomalias, o motor local DEVE retornar:
    NORMAL com 85% de confianca, erro=False e ia_respondeu=False.
    """
    clean_analyzer.client = None

    result = clean_analyzer.analyze_clip(synthetic_video, mode=SecurityMode.ALL)

    assert result.erro is False
    assert result.ia_respondeu is False
    assert result.evento_detectado is False
    assert result.tipo_evento == EventType.NORMAL
    assert result.nivel_risco == RiskLevel.NORMAL
    assert result.confianca == 85.0
    assert "Ambiente monitorado sem anomalias" in result.descricao_acao


def test_analyzer_fallback_with_local_surrender(clean_analyzer, synthetic_video):
    """
    Quando o Gemini falha mas o motor local detectou rendicao,
    o laudo de contingencia preserva ALERTA_MAXIMO e ASSALTO_RENDICAO.
    """
    clean_analyzer.client = object()
    clean_analyzer.gesture_engine = MagicMock()
    clean_analyzer.gesture_engine.analyze_frame.return_value = (None, {"is_surrender": True})

    failed_ai_result = SecurityAnalysisResult(
        evento_detectado=False,
        modo_analise=SecurityMode.ALL,
        tipo_evento=EventType.ERRO_ANALISE,
        nivel_risco=RiskLevel.SUSPEITO,
        confianca=0.0,
        descricao_acao="Falha de rede ao conectar no Google Gemini.",
        recomendacao_acao="Revisar manualmente.",
        erro=True,
        erro_detalhe="503 Service Unavailable",
        ia_respondeu=False
    )
    clean_analyzer.storyboard_verifier.verify_with_ai = MagicMock(return_value=failed_ai_result)

    result = clean_analyzer.analyze_clip(synthetic_video, mode=SecurityMode.ALL)

    assert result.erro is True
    assert result.ia_respondeu is False
    assert result.evento_detectado is True
    assert result.tipo_evento == EventType.ASSALTO_RENDICAO
    assert result.nivel_risco == RiskLevel.ALERTA_MAXIMO
    assert result.confianca == 85.0
