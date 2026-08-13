"""Parámetros, constantes y patrones del MVP.

Centraliza límites, mensajes de aviso y categorías para que la UI y los
servicios externos compartan los mismos valores. Las claves de API se
leen desde variables de entorno y nunca se incluyen en el repositorio.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from dotenv import load_dotenv

# Carga .env si existe; no falla si está ausente.
load_dotenv()

# ---------------------------------------------------------------------------
# Identidad de la aplicación
# ---------------------------------------------------------------------------
APP_NAME = "Asistente de Revisión Científica"

# User-Agent compartido por todas las peticiones a servicios públicos.
USER_AGENT = "Doma-ScientificReview/0.1 (mailto:contact@doma.example)"

# Tiempo máximo de espera para peticiones HTTP externas (segundos).
REQUEST_TIMEOUT = 20

# Tamaño máximo de PDF aceptado, tanto en carga como en descarga (MB).
MAX_UPLOAD_MB = 25

# ---------------------------------------------------------------------------
# Expresiones regulares
# ---------------------------------------------------------------------------
# DOI con prefijo opcional (doi:, https://doi.org/, etc.). Acepta el formato
# 10.NNNN/<cualquier cosa hasta espacio/comilla/fin>. La captura puede
# incluir puntuación final; las funciones de canonización la recortan
# con ``rstrip`` para no contaminar el identificador.
DOI_PATTERN = re.compile(
    r"(?:doi[:\s]*|https?://(?:dx\.)?doi\.org/)?(10\.\d{4,9}/[^\s\"'<>]+)",
    re.IGNORECASE,
)

# Patrones para identificar PMID dentro de texto libre o URL.
PMID_PATTERN = re.compile(r"(?:pubmed\.ncbi\.nlm\.nih\.gov/|PMID\s*:?\s*)(\d{5,9})", re.I)

# ---------------------------------------------------------------------------
# Estado editorial y aviso humano
# ---------------------------------------------------------------------------
HUMAN_DECISION_VALUES = ("Pendiente", "Aprobar", "Rechazar")

HUMAN_REVIEW_NOTICE = (
    "El sistema no aprueba ni rechaza documentos: solo presenta evidencias. "
    "Toda decisión debe ser registrada por una persona revisora con su "
    "justificación correspondiente."
)

# Categorías temáticas sugeridas para el panel humano. La lista es editable
# y se centra en ejemplos coherentes con la línea de investigación de Doma
# (sueño, ansiedad y otros dominios relacionados).
TOPIC_PRESETS = (
    "Sueño",
    "Ansiedad",
    "Estrés",
    "Depresión",
    "Bienestar general",
    "Otro",
)

# ---------------------------------------------------------------------------
# API opcional de síntesis
# ---------------------------------------------------------------------------
LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip()
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").strip()
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini").strip()

# Si no hay clave configurada, la app opera en modo "citas literales".
LLM_ENABLED = bool(LLM_API_KEY)

# Temperatura baja para que la síntesis no invente contenido.
LLM_TEMPERATURE = 0.1

# ---------------------------------------------------------------------------
# Almacenamiento local
# ---------------------------------------------------------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "revision_cientifica.db"

# ---------------------------------------------------------------------------
# Endpoints de servicios públicos
# ---------------------------------------------------------------------------
CROSSREF_API = "https://api.crossref.org/works/{doi}"
PUBMED_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PUBMED_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
OPENALEX_API = "https://api.openalex.org/works/doi:{doi}"
