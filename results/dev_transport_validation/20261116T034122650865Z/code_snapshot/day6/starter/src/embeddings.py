"""Choose a real embedding provider (API or local) and implement this contract."""
from typing import Protocol


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class MyEmbedder:
    """Pinned local CPU E5, no automatic network downloads or silent truncation."""

    def __init__(self, model_name: str, batch_size: int = 8) -> None:
        from pathlib import Path
        import os
        root = Path(__file__).resolve().parents[2]
        self.revision = '614241f622f53c4eeff9890bdc4f31cfecc418b3'
        if model_name != 'intfloat/multilingual-e5-small':
            raise ValueError('Model differs from approved setup')
        os.environ['HF_HOME'] = str(root/'.cache/huggingface')
        os.environ['HF_HUB_OFFLINE'] = '1'
        os.environ['TOKENIZERS_PARALLELISM'] = 'false'
        from huggingface_hub import snapshot_download
        from sentence_transformers import SentenceTransformer
        import torch
        torch.set_num_threads(4)
        torch.manual_seed(0)
        snapshot = snapshot_download(model_name, revision=self.revision, local_files_only=True, token=False,
            allow_patterns=['*.json','model.safetensors','sentencepiece.bpe.model','README.md','LICENSE'])
        self.model = SentenceTransformer(snapshot, device='cpu', local_files_only=True, trust_remote_code=False)
        self.model.max_seq_length = 512
        self.model_name = model_name
        self.dimensions = self.model.get_sentence_embedding_dimension()
        if self.dimensions != 384:
            raise ValueError('Unexpected embedding dimensions')
        self.batch_size = batch_size
        self.last_token_lengths = []

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._encode(['passage: ' + text for text in texts])

    def embed_query(self, question: str) -> list[float]:
        return self.embed_queries([question])[0]

    def embed_queries(self, questions: list[str]) -> list[list[float]]:
        return self._encode(['query: ' + text for text in questions])

    def _encode(self, texts):
        if not texts:
            return []
        self.last_token_lengths = [len(ids) for ids in self.model.tokenizer(texts, truncation=False, padding=False)['input_ids']]
        if max(self.last_token_lengths) > 512:
            raise ValueError('Input exceeds approved model limit; do not silently truncate')
        return self.model.encode(texts, batch_size=self.batch_size, normalize_embeddings=True,
                                 show_progress_bar=False).tolist()
