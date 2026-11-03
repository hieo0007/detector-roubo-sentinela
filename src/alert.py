import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import shutil
import time
import json
import winsound
from .models import SecurityAnalysisResult, RiskLevel

class AlertManager:
    """
    Gerenciador de alertas sonoros/visuais e arquivamento de evidências criminais.
    """
    def __init__(self, evidencias_dir: str = "evidencias", play_sound: bool = True):
        self.evidencias_dir = evidencias_dir
        self.play_sound = play_sound
        os.makedirs(self.evidencias_dir, exist_ok=True)

    def trigger(self, clip_path: str, report: SecurityAnalysisResult):
        """Dispara alarmes e arquiva relatório/vídeo se evento for suspeito ou crime"""
        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        is_alert = report.evento_detectado or report.nivel_risco in [RiskLevel.SUSPEITO, RiskLevel.ALERTA_MAXIMO]

        print("\n" + "="*60)
        if report.nivel_risco == RiskLevel.ALERTA_MAXIMO:
            print(f"[ALERTA CRITICO: {report.tipo_evento.value}] Confiança: {report.confianca:.1f}%")
        elif report.nivel_risco == RiskLevel.SUSPEITO:
            print(f"[AVISO SUSPEITO: {report.tipo_evento.value}] Confiança: {report.confianca:.1f}%")
        else:
            print(f"[REGULAR / NORMAL] Confiança: {report.confianca:.1f}%")

        print(f"Modo: {report.modo_analise.value}")
        print(f"Descrição: {report.descricao_acao}")
        print(f"Momento da ação: {report.timestamp_segundo:.1f}s")
        if report.itens_envolvidos:
            print(f"Itens Envolvidos: {', '.join(report.itens_envolvidos)}")
        print(f"Recomendação: {report.recomendacao_acao}")
        print("="*60 + "\n")

        # O som é gerenciado exclusivamente pelo painel web via Web Audio sintético,
        # eliminando completamente os sons padrão e beeps do Windows.
        pass

        # Salva o pacote forense de evidência (vídeo + JSON)
        if is_alert:
            dest_video = os.path.join(self.evidencias_dir, f"evidencia_{timestamp_str}.mp4")
            dest_json = os.path.join(self.evidencias_dir, f"evidencia_{timestamp_str}.json")

            if os.path.exists(clip_path):
                try:
                    shutil.copy(clip_path, dest_video)
                except Exception:
                    pass

            with open(dest_json, "w", encoding="utf-8") as f:
                json.dump(report.model_dump(), f, ensure_ascii=False, indent=2)

            print(f"[EVIDÊNCIA SALVA] Registrado em: {dest_video} e {dest_json}")
