import os
import json
import urllib.request
import urllib.parse
from typing import Optional, Tuple

class TelegramNotifier:
    """
    Despachante de Alertas de Segurança em Tempo Real via Telegram Bot API:
    - Envia avisos imediatos com nível de risco, horário e descrição forense.
    - Anexa a imagem do Storyboard/Quadro-chave diretamente no chat do celular.
    - Utiliza requisições nativas sem necessidade de bibliotecas externas pesadas.
    """
    def __init__(self, config_path: str):
        self.config_path = config_path

    def _get_credentials(self) -> Tuple[Optional[str], Optional[str]]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("telegram_bot_token"), data.get("telegram_chat_id")
            except Exception:
                pass
        return None, None

    def test_connection(self, token: str, chat_id: str) -> Tuple[bool, str]:
        """Testa se o Bot Token e o Chat ID estão válidos."""
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": "SENTINELA CCTV: Conexao estabelecida com sucesso. Alertas de seguranca ativos.",
            "parse_mode": "Markdown"
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=6) as response:
                if response.status == 200:
                    return True, "Mensagem de teste enviada com sucesso ao Telegram!"
                return False, f"Resposta HTTP: {response.status}"
        except Exception as e:
            return False, f"Falha na conexão: {str(e)}"

    def send_alert(
        self,
        event_type: str,
        risk_level: str,
        description: str,
        timestamp_sec: float,
        image_path: Optional[str] = None
    ) -> bool:
        """Envia o alerta e o registro fotográfico ao Telegram se configurado."""
        token, chat_id = self._get_credentials()
        if not token or not chat_id:
            return False

        caption = (
            f"*SENTINELA — ALERTA PATRIMONIAL*\n"
            f"• Evento: `{event_type}`\n"
            f"• Gravidade: `{risk_level}`\n"
            f"• Timestamp: `{timestamp_sec:.1f}s`\n"
            f"• Resumo: {description}"
        )

        # Se houver imagem do Storyboard, envia via sendPhoto com multipart
        if image_path and os.path.exists(image_path):
            try:
                url = f"https://api.telegram.org/bot{token}/sendPhoto"
                boundary = "----SentinelSecurityBoundary123456"

                with open(image_path, "rb") as f:
                    img_data = f.read()

                body = bytearray()
                # Campo chat_id
                body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n".encode())
                # Campo caption
                body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode())
                # Campo parse_mode
                body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"parse_mode\"\r\n\r\nMarkdown\r\n".encode())
                # Campo photo
                filename = os.path.basename(image_path)
                body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{filename}\"\r\nContent-Type: image/jpeg\r\n\r\n".encode())
                body.extend(img_data)
                body.extend(f"\r\n--{boundary}--\r\n".encode())

                req = urllib.request.Request(
                    url,
                    data=bytes(body),
                    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    return resp.status == 200
            except Exception as e:
                print(f"[NOTIFICADOR] Falha ao enviar foto ao Telegram: {e}")

        # Fallback de texto se envio de foto falhar ou não houver imagem
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {"chat_id": chat_id, "text": caption, "parse_mode": "Markdown"}
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                return resp.status == 200
        except Exception as e:
            print(f"[NOTIFICADOR] Falha ao enviar mensagem ao Telegram: {e}")
            return False
