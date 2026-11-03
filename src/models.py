from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SecurityMode(str, Enum):
    ALL = "TODOS"                # Monitora Furto, Invasão e Assalto simultaneamente
    SHOPLIFTING = "LOJA"         # Foco em furto discreto e ocultação de produtos
    PERIMETER = "PERIMETRO"     # Foco em invasão de perímetro, cerca virtual e pular muros
    ROBBERY = "ASSALTO"          # Foco em assalto, rendição (mãos ao alto) e área de caixa

class EventType(str, Enum):
    NORMAL = "NORMAL"
    FURTO_LOJA = "FURTO_LOJA"
    INVASAO_PERIMETRO = "INVASAO_PERIMETRO"
    ASSALTO_RENDICAO = "ASSALTO_RENDICAO"
    SUSPEITO = "SUSPEITO"
    ERRO_ANALISE = "ERRO_ANALISE"

class RiskLevel(str, Enum):
    NORMAL = "NORMAL"
    SUSPEITO = "SUSPEITO"
    ALERTA_MAXIMO = "ALERTA_MAXIMO"

class TimelineStep(BaseModel):
    sec: float
    title: str
    status: str
    icon: str
    desc: str
    snapshot_url: Optional[str] = None

class SecurityAnalysisResult(BaseModel):
    """
    Schema tipado para diagnóstico inteligente de segurança e detecção de roubo/invasão.
    """
    evento_detectado: bool = Field(
        description="True se qualquer furto, invasão de perímetro ou assalto for identificado."
    )
    modo_analise: SecurityMode = Field(
        default=SecurityMode.ALL,
        description="Modo de segurança empregado na análise."
    )
    tipo_evento: EventType = Field(
        default=EventType.NORMAL,
        description="Classificação da ocorrência: NORMAL, FURTO_LOJA, INVASAO_PERIMETRO, ASSALTO_RENDICAO ou SUSPEITO."
    )
    nivel_risco: RiskLevel = Field(
        default=RiskLevel.NORMAL,
        description="Grau de criticidade: NORMAL, SUSPEITO ou ALERTA_MAXIMO."
    )
    confianca: float = Field(
        default=0.0,
        ge=0.0, le=100.0,
        description="Nível de certeza do sistema (0.0 a 100.0%)."
    )
    descricao_acao: str = Field(
        description="Explicação contextual detalhada do comportamento identificado."
    )
    timestamp_segundo: float = Field(
        default=0.0,
        description="Segundo exato do vídeo em que a ação de roubo/invasão ocorreu."
    )
    itens_envolvidos: List[str] = Field(
        default_factory=list,
        description="Itens, bolsas, armas ou vestimentas envolvidos na conduta."
    )
    recomendacao_acao: str = Field(
        description="Ação prática recomendada para o proprietário ou equipe de segurança."
    )
    storyboard_url: Optional[str] = Field(
        default=None,
        description="Caminho relativo da imagem do storyboard temporal avaliada pela IA."
    )
    clip_url: Optional[str] = Field(
        default=None,
        description="Caminho relativo do clipe de evidência forense (7s) gerado."
    )
    timeline: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Passos cronológicos detalhados com snapshots anotados."
    )
    erro: bool = Field(
        default=False,
        description="True se ocorreu falha de comunicação ou resposta inválida na análise."
    )
    erro_detalhe: Optional[str] = Field(
        default=None,
        description="Mensagem técnica ou detalhe da falha caso erro=True."
    )
    ia_respondeu: bool = Field(
        default=True,
        description="False se a IA não respondeu e foi utilizado laudo de contingência do motor local."
    )

# Alias para compatibilidade com código legado se necessário
TheftAnalysisResult = SecurityAnalysisResult
